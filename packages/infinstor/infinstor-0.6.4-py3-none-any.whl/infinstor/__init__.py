import sys
import os
import io
import boto3
from io import StringIO
from multiprocessing.connection import wait
from multiprocessing import Process, Pipe, Queue
from queue import Empty
import pandas as pd
from pandas import DataFrame
from tqdm import tqdm
import ast
import subprocess
import tempfile
import pickle
from . import infin_ast
from datetime import datetime, timedelta
import time
from mlflow import start_run, end_run, log_metric, log_param, log_artifacts, set_experiment, log_artifact
from os.path import sep
import mlflow.projects
from contextlib import contextmanager,redirect_stderr,redirect_stdout
import pprint
import types
import shutil
from . import servicedefs
import builtins
from infinstor_mlflow_plugin.tokenfile import read_token_file
from os.path import expanduser
from requests.exceptions import HTTPError
import requests
import inspect
import glob

# import astpretty

TRANSFORM_RAW_PD = "infin_transform_raw_to_pd"
TRANSFORM_RAW_DS = "infin_transform_raw_to_ds"
TRANSFORM_CSV_PD = "infin_transform_csv_to_pd"
TRANSFORM_CSV_DS = "infin_transform_csv_to_ds"
TRANSFORM_ONE_OBJ = "infin_transform_one_object"
TRANSFORM_DIR_BY_DIR = "infin_transform_dir_by_dir"

verbose = False

def num_threads():
    return 8

class FuncLister(ast.NodeVisitor):
    def __init__(self, glbs):
        self.glbs = glbs;

    def visit_FunctionDef(self, node):
        self.glbs[node.name] = "'" + node.name + "'";
        # print('>> Funclister: ' + node.name)
        self.generic_visit(node)

def get_label_info(label):
    tokfile = expanduser('~') + sep + '.infinstor' + sep + '/token'
    token, refresh_token, token_time, client_id, service = read_token_file(tokfile)

    payload = ("label=" + label)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': token
        }
    url = 'https://api.' + builtins.service + '.com/listlabels'
    try:
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        raise
    except Exception as err:
        print(f'Other error occurred: {err}')
        raise
    labels = response.json()['labels']
    for one_label in labels:
        labelname = one_label['label']
        if (labelname == label):
            return one_label['timespec'], one_label['bucketname'], one_label['prefix']
        else:
            return None, None, None


def download_one_dir(label):
    timespec, bucketname, prefix = get_label_info(label)
    endpoint = "https://lbl" + label + ".s3proxy." + builtins.service + ".com:443/";

    session = boto3.session.Session(profile_name='infinstor')
    client = session.client('s3', endpoint_url=endpoint)
    dict_of_arrays_of_files = dict()
    list_dir_by_dir(client, bucketname, prefix, True, dict_of_arrays_of_files)
    tmpdir_root = tempfile.mkdtemp()
    try:
        start_run()
        for parentdir in dict_of_arrays_of_files:
            array_of_files = dict_of_arrays_of_files[parentdir]
            if (verbose == True):
                info('Number Of Objects in parentdir ' + parentdir + ': ' +str(len(array_of_files)))
            local_tmpdir = tmpdir_root + sep + parentdir
            if (verbose == True):
                info('Local temp dir is ' + local_tmpdir)
            os.makedirs(local_tmpdir, mode=0o755, exist_ok=True)
            objects = download_objects_inner(endpoint, bucketname, parentdir, array_of_files,\
                    False, None, local_tmpdir)
    finally:
        end_run()
    return tmpdir_root

# fills out array_of_files with all the files in this prefix
def list_one_dir(client, bucket, prefix_in, recurse, array_of_files):
    paginator = client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket, Prefix=prefix_in, Delimiter="/")
    for page in page_iterator:

        # print('Files:')
        contents = page.get('Contents')
        if (contents != None):
            # print('   ' + str(contents))
            count = 0;
            for one_content in contents:
                object_name = one_content['Key']
                full_object_name = object_name
                # print(full_object_name)
                array_of_files.append(full_object_name)
                count += 1
            if (count > 0):
                print(str(count) + " files in " + prefix_in)

        # print('Directories:')
        common_prefixes = page.get('CommonPrefixes')
        if (common_prefixes != None):
            for prefix in common_prefixes:
                this_prefix = str(prefix['Prefix'])
                # print('   ' + this_prefix)
                if (bool(recurse) and this_prefix != None ):
                    list_one_dir(client, bucket, this_prefix, recurse, array_of_files)

# returns parentdir (with no leading or trailing /) and filename
def get_parent_dir_and_fn(full_object_key):
    components = full_object_key.split(sep)
    parentdir = ''
    for comp in components[0:len(components) -1]:
        if (parentdir == ''):
            parentdir = comp
        else:
            parentdir = parentdir + sep + comp
    return parentdir, components[len(components) - 1]

# fills out dict_of_arrays_of_files with a dict of parentdir -> array_of_files_in_parent_dir
def list_dir_by_dir(client, bucket, prefix_in, recurse, dict_of_arrays_of_files):
    paginator = client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket, Prefix=prefix_in, Delimiter="/")
    for page in page_iterator:

        # print('Files:')
        contents = page.get('Contents')
        if (contents != None):
            # print('   ' + str(contents))
            count = 0;
            for one_content in contents:
                object_name = one_content['Key']
                full_object_name = object_name
                # print(full_object_name)
                parent_dir, filename = get_parent_dir_and_fn(object_name)
                if (parent_dir in dict_of_arrays_of_files):
                    files_in_this_dir = dict_of_arrays_of_files[parent_dir]
                else:
                    files_in_this_dir = []
                    dict_of_arrays_of_files[parent_dir] = files_in_this_dir
                files_in_this_dir.append(filename)
                count += 1
            if (count > 0):
                print(str(count) + " files in " + prefix_in)

        # print('Directories:')
        common_prefixes = page.get('CommonPrefixes')
        if (common_prefixes != None):
            for prefix in common_prefixes:
                this_prefix = str(prefix['Prefix'])
                # print('   ' + this_prefix)
                if (bool(recurse) and this_prefix != None ):
                    list_dir_by_dir(client, bucket, this_prefix, recurse, dict_of_arrays_of_files)

def info(msg):
    now = datetime.now()
    print(__name__ + '[' + str(os.getpid()) + '][' + now.strftime('%Y-%m-%d %H:%M:%S') + ']' + msg)

def log_artifacts_recursively(temp_output_dir):
    for filename in glob.iglob(temp_output_dir + '**/**', recursive=True):
        if (os.path.isfile(filename)):
            bn = os.path.basename(filename)
            bn_minus_tmp = filename[len(temp_output_dir):].lstrip()
            key = 'infinstor/' + os.path.dirname(bn_minus_tmp).lstrip('/')
            info("Logging artifact " + str(filename) + " to " + key)
            log_artifact(filename, key)

class download_task:
    def __init__(self, command, bucketname, parentdir, filename):
        self.command = command
        self.bucketname = bucketname
        self.parentdir = parentdir
        self.filename = filename

def s3downloader(**kwargs):
    download_task_q = kwargs.pop('command_q')
    write_pipe = kwargs.pop('write_pipe')
    endpoint = kwargs.pop('endpoint')
    glb = kwargs.pop('globals')
    tmpfile_dir = kwargs.pop('tmpfile_dir')

    # 1. tmpfile_dir=None, glb=None: Read object into memory and return bytes to pipe
    # 2. tmpfile_dir is present and glb=None: Read object into tmpfile_dir and return status
    # 3. tmpfile_dir is present and glb is present: Read object into tmpfile_dir and call
    #    the function infin_transform_one_object using glb as globals. Send status back
    # Note: If glb is present, tmpfile_dir must be present. We always call
    # infin_transform_one_object by passing in a temporary file

    if (glb != None):
        namespaced_infin_transform_one_object =\
                namespaced_function(glb['infin_transform_one_object'], glb, None, True)

    session = boto3.session.Session(profile_name='infinstor')
    client = session.client('s3', endpoint_url=endpoint)
    while (True):
        try:
            if (verbose == True):
                start = datetime.now()
            download_task = download_task_q.get()
            if (verbose == True):
                end = datetime.now()
                td = end - start
                ms = (td.days * 86400000) + (td.seconds * 1000) + (td.microseconds / 1000)
                if (ms > 10):
                    info('s3downloader: q.get took ' + str(ms) + ' ms')
        except Empty as e:
            if (verbose == True):
                info('s3downloader: No more entries in download_task_q. Exiting..')
            write_pipe.close()
            break
        op = download_task.command
        if (op == 'download'):
            if (verbose == True):
                info('s3downloader: Received download command')
            bucketname = download_task.bucketname
            parentdir = download_task.parentdir
            filename = download_task.filename
            if (parentdir == ''):
                full_object_key = filename
            else:
                full_object_key = parentdir + sep + filename
            if (verbose == True):
                info('s3downloader: starting download of ' + full_object_key\
                        + ' from ' + bucketname)
                start = datetime.now()

            if (tmpfile_dir == None):
                obj = client.get_object(Bucket=bucketname, Key=full_object_key)
                content_length = obj['ContentLength']
                strbody = obj['Body']
                bts = strbody.read()
                dtm = obj['LastModified']
                key = dtm.strftime('%Y-%m-%d %H:%M:%S') + ' ' + bucketname + '/' + full_object_key
            else:
                tmpf_name = tmpfile_dir + sep + filename
                client.download_file(bucketname, full_object_key, tmpf_name)
                content_length = os.stat(tmpf_name).st_size
                key = bucketname + '/' + full_object_key

            if (glb == None):
                while (not write_pipe.writable):
                    info('s3downloader: WARNING write pipe not writable')
                    time.sleep(2)
                try:
                    write_pipe.send(key)
                    write_pipe.send(filename)
                    if (tmpfile_dir == None):
                        write_pipe.send(bts)
                    else:
                        write_pipe.send('Success')
                except Exception as e:
                    status_str = str(e)
                    info("Error sending bytes back: " + status_str)
            else:
                try:
                    temp_output_dir = tempfile.mkdtemp()
                    #namespaced_infin_transform_one_object(bucketname, parentdir,\
                    #        filename, tmpf_name, **kwargs)
                    namespaced_infin_transform_one_object(tmpf_name, temp_output_dir, **kwargs)
                except Exception as e1:
                    status_str = str(e1)
                    info("Error executing infin_transform_one_object_tmpfile: " + status_str)
                else:
                    log_artifacts_recursively(temp_output_dir)
                    status_str = 'Success'
                finally:
                    shutil.rmtree(temp_output_dir)
                os.remove(tmpf_name)
                write_pipe.send(key)
                write_pipe.send(filename)
                write_pipe.send(status_str)
        elif (op == 'quit'):
            if (verbose == True):
                info('s3downloader: Received quit command')
            write_pipe.close()
            break
        else:
            info('s3downloader: Unknown command ' + op)
            write_pipe.close()
            break

def namespaced_function(function, global_dict, defaults=None, preserve_context=False):
    '''
    Redefine (clone) a function under a different globals() namespace scope
        preserve_context:
            Allow keeping the context taken from orignal namespace,
            and extend it with globals() taken from
            new targetted namespace.
    '''
    if defaults is None:
        defaults = function.__defaults__

    if preserve_context:
        _global_dict = function.__globals__.copy()
        _global_dict.update(global_dict)
        global_dict = _global_dict
    new_namespaced_function = types.FunctionType(
        function.__code__,
        global_dict,
        name=function.__name__,
        argdefs=defaults,
        closure=function.__closure__
    )
    new_namespaced_function.__dict__.update(function.__dict__)
    return new_namespaced_function

def load_one_csv_from_bytearray(bts):
    s = str(bts, 'utf-8')
    sio = StringIO(s)
    return pd.read_csv(sio)

def download_objects(endpoint, bucketname, parentdir, array_of_files, is_csv, glb):
    try:
        start_run()
        return download_objects_inner(endpoint, bucketname, parentdir, array_of_files, is_csv, None, None)
    finally:
        end_run()

# returns a pandas DataFrame with index 'YY-MM-dd HH:MM:SS bucketname/filename'
# and one column named RawBytes that contains the raw bytes from the object
# This inner method is called after the outer method wraps in mlflow start_run
def download_objects_inner(endpoint, bucketname, parentdir, array_of_files, is_csv,\
        glb, tmpfile_dir, **kwargs):
    log_param("object_count", len(array_of_files))

    command_q = Queue(len(array_of_files) + num_threads())
    for onefile in array_of_files:
        command_q.put(download_task('download', bucketname, parentdir, onefile))
    for i in range(num_threads()):
        command_q.put(download_task('quit', '', '', ''))

    pipe_from_child = []
    processes = []
    for i in range(num_threads()):
        r1, w1 = Pipe(False)
        pipe_from_child.append(r1)
        newkwargs = dict(kwargs)
        newkwargs['command_q'] = command_q
        newkwargs['write_pipe'] = w1
        newkwargs['endpoint'] = endpoint
        newkwargs['globals'] = glb
        newkwargs['tmpfile_dir'] = tmpfile_dir
        p = Process(target=s3downloader, args=(), kwargs=newkwargs)
        p.start()
        processes.append(p)
        w1.close()

    filebytes = []
    filenames = []
    filekeys = []
    step = 0
    with tqdm(total=len(array_of_files)) as pbar:
        files_read = 0
        while pipe_from_child:
            ready = wait(pipe_from_child, timeout=10)
            for read_pipe in pipe_from_child:
                try:
                    while (read_pipe.poll()):
                        key = read_pipe.recv()
                        fn = read_pipe.recv()
                        bts = read_pipe.recv()
                        filekeys.append(key)
                        filenames.append(fn)
                        filebytes.append(bts)
                        pbar.update(1)
                        files_read += 1
                        if ((files_read % 10) == 0):
                            log_metric("downloaded", files_read, step=step)
                            step += 1
                except EOFError:
                    pipe_from_child.remove(read_pipe)

    for i in range(num_threads()):
        processes[i].join()
    if (is_csv == True):
        rv = pd.concat(map(load_one_csv_from_bytearray, filebytes))
    else:
        data = {'FileName': filenames, 'RawBytes': filebytes}
        rv = DataFrame(data, index=filekeys)
    log_metric("downloaded", files_read, step=step)
    return rv

def actually_run_transformation(client, endpoint, cache_path, is_pandas_df, bucketname,\
        prefix_in, is_csv, xformname, transformation_string, one_object_only, **kwargs):
    array_of_files = []
    list_one_dir(client, bucketname, prefix_in, True, array_of_files)
    if (one_object_only):
        first = array_of_files[0]
        array_of_files = []
        array_of_files.append(first)
    print('actually_run_transformation: total number Of objects: ' + str(len(array_of_files)))
    try:
        start_run()
        objects = download_objects_inner(endpoint, bucketname, '', array_of_files, is_csv, None, None, **kwargs)
    finally:
        end_run()

    transformAst = infin_ast.extract_transform(TRANSFORM_RAW_PD, src_str=transformation_string)
    # XXX we should use the following statement to figure out what
    # kind of an object the infin_transform function returns
    # infin_ast.add_type_statements(transformAst)
    transformSrc = infin_ast.get_source(transformAst)

    if (verbose == True):
        print('transformSrc=' + transformSrc);

    if (is_csv):
        if (is_pandas_df):
            xn = TRANSFORM_CSV_PD
        else:
            xn = TRANSFORM_CSV_DS
    else:
        if (is_pandas_df):
            xn = TRANSFORM_RAW_PD
        else:
            xn = TRANSFORM_RAW_DS

    tree = ast.parse(transformSrc)

    compiledcode2 = compile(tree, "<string>", "exec")

    # Add all functions in xformcode to the globals dictionary
    glb = {}
    fl = FuncLister(glb)
    fl.visit(tree)
    try:
        exec(compiledcode2, glb)
    except Exception as e:
        status_str = str(e)
    else:
        status_str = 'Success'
    # print('Globals=')
    # pprint.pprint(glb)
    info("Execution of global statics complete. status_str=" + status_str)

    namespaced_infin_transform_fnx = namespaced_function(glb[xn], glb, None, True)
    try:
        namespaced_infin_transform_fnx(objects, **kwargs)
    except Exception as e:
        status_str = str(e)
        info("Error executing " + xn + ", status=" + status_str)
    else:
        status_str = 'Success'

    if (is_pandas_df == True):
        if (cache_path != None):
            fd, tmpf_name = tempfile.mkstemp(suffix='.pkl')
            os.close(fd)
            objects.to_pickle(tmpf_name)
            client.put_object(Body=open(tmpf_name, 'rb'), Bucket='infinstor-pseudo-bucket',\
                Key=cache_path)
            os.remove(tmpf_name)
        else:
            print('cache_path not specified. not caching')
    else:
        print('saving tf.data.Dataset unimplemented')
    return objects

def read_and_xform_to_pd(time_spec, service_name, bucketname, prefix_in, is_csv,\
        xformname, transform_string, one_object_only, **kwargs):
    endpoint = "https://" + time_spec + ".s3proxy." + service_name + ".com:443/";
    session = boto3.session.Session(profile_name='infinstor')
    client = session.client('s3', endpoint_url=endpoint)

    cache_path = None
    if (xformname == None):
        print('xformname not specified. Not checking cache')
        return actually_run_transformation(client, endpoint, cache_path, True,\
                bucketname, prefix_in, is_csv, xformname, transform_string,\
                one_object_only, **kwargs)

    # check if we can download a cached version
    cache_path = 'cache/' + xformname + '/' + time_spec + '/'\
            + bucketname + '/' + prefix_in + 'pd.DataFrame'
    print('Looking up cache entry ' + cache_path)
    try:
        s3obj = client.get_object(Bucket='infinstor-pseudo-bucket', Key=cache_path)
        print('cache hit for ' + cache_path)
        body_bytes = s3obj['Body'].read()
        cached_obj = pickle.loads(body_bytes)
    except client.exceptions.NoSuchKey:
        print('cache miss for ' + cache_path)
        cached_obj = actually_run_transformation(client, endpoint, cache_path, True,\
                bucketname, prefix_in, is_csv, xformname, transform_string, False, **kwargs)
    finally:
        return cached_obj

def read_and_xform_to_ds(time_spec, service_name, bucketname, prefix_in, is_csv,\
        xformname, transform_string, one_object_only, **kwargs):
    endpoint = "https://" + time_spec + ".s3proxy." + service_name + ".com:443/";
    session = boto3.session.Session(profile_name='infinstor')
    client = session.client('s3', endpoint_url=endpoint)

    if (xformname == None):
        print('xformname not specified. Not checking cache')
        return actually_run_transformation(client, endpoint, cache_path,\
                False, bucketname, prefix_in, is_csv,\
                xformname, transform_string, one_object_only, **kwargs)

    # check if we can download a cached version
    cache_path = 'cache/' + xformname + '/' + time_spec + '/'\
            + bucketname + '/' + prefix_in + 'tf.data.Dataset'
    print('Looking up cache entry ' + cache_path)
    try:
        cached_obj = client.get_object(Bucket='infinstor-pseudo-bucket', Key=cache_path)
        print('cache hit for ' + cache_path)
        # XXX read and deserialize here
    except client.exceptions.NoSuchKey:
        print('cache miss for ' + cache_path)
        cached_obj = actually_run_transformation(client, endpoint, cache_path, False,\
                bucketname, prefix_in, is_csv, xformname, transform_string, False, **kwargs)
    finally:
        return cached_obj

def run_xform_periodically(seconds, service_name, bucketname, prefix_in, xformname, **kwargs):
    endpoint = "https://s3proxy." + service_name + ".com:443/";
    print('infinstor proxy endpoint=' + endpoint)
    session = boto3.session.Session(profile_name='infinstor')
    client = session.client('s3', endpoint_url=endpoint)

    xform_obj = client.get_object(Bucket='infinstor-pseudo-bucket', Key='transforms/' + xformname)
    strbody = xform_obj['Body']
    bts = strbody.read()
    transform_string = str(bts, 'utf-8')
    return run_xform_string_periodically(seconds, service_name, bucketname, prefix_in, xformname, transform_string, **kwargs)

def run_xform_string_periodically(seconds, service_name, bucketname, prefix_in, xformname, transform_string, **kwargs):
    while (True):
        start_time = datetime.utcnow()
        time.sleep(seconds)
        end_time = datetime.utcnow()
        time_spec = 'tm' + start_time.strftime("%Y%m%d%H%M%S")\
                + '-tm' + end_time.strftime("%Y%m%d%H%M%S")
        read_and_xform_to_pd(time_spec, service_name, bucketname, prefix_in, False,\
                xformname, transform_string, False, **kwargs)

def new_dict_with_just_one(dict_in):
    one_dir = list(dict_in.keys())[0]
    newdict = dict()
    newdict[one_dir] = dict_in[one_dir]
    return newdict

def read_and_xform_one_object(time_spec, service_name, bucketname,\
        prefix_in, xformname, transform_string, one_object_only, **kwargs):
    endpoint = "https://" + time_spec + ".s3proxy." + service_name + ".com:443/";
    session = boto3.session.Session(profile_name='infinstor')
    client = session.client('s3', endpoint_url=endpoint)

    transformAst = infin_ast.extract_transform(TRANSFORM_ONE_OBJ, src_str=transform_string)
    transformSrc = infin_ast.get_source(transformAst)
    tree = ast.parse(transformSrc)
    # astpretty.pprint(tree)
    compiledcode1 = compile(tree, "<string>", "exec")

    dict_of_arrays_of_files = dict()
    list_dir_by_dir(client, bucketname, prefix_in, True, dict_of_arrays_of_files)
    if (one_object_only): # truncate to first directory
        dict_of_arrays_of_files = new_dict_with_just_one(dict_of_arrays_of_files)
    try:
        start_run()
        for parentdir in dict_of_arrays_of_files:
            array_of_files = dict_of_arrays_of_files[parentdir]
            info('Number Of Objects in parentdir ' + parentdir + ' = ' + str(len(array_of_files)))
            # Add all functions in xformcode to the globals dictionary
            glb = {}
            fl = FuncLister(glb)
            fl.visit(tree)
            try:
                exec(compiledcode1, glb)
            except Exception as e:
                status_str = str(e)
            else:
                status_str = 'Success'
            # print('Globals=')
            # pprint.pprint(glb)
            info("Execution of global statics for parentdir " + parentdir\
                    + " complete. status_str=" + status_str)
            tdir = tempfile.mkdtemp()
            objects = download_objects_inner(endpoint, bucketname, parentdir, array_of_files,\
                        False, glb, tdir, **kwargs)
            shutil.rmtree(tdir)
    finally:
        end_run()
    return objects

def read_and_xform_dir_by_dir(time_spec, service_name, bucketname,\
        prefix_in, xformname, transform_string, one_object_only, **kwargs):
    endpoint = "https://" + time_spec + ".s3proxy." + service_name + ".com:443/";
    session = boto3.session.Session(profile_name='infinstor')
    client = session.client('s3', endpoint_url=endpoint)

    transformAst = infin_ast.extract_transform(TRANSFORM_DIR_BY_DIR, src_str=transform_string)
    transformSrc = infin_ast.get_source(transformAst)
    tree = ast.parse(transformSrc)
    # astpretty.pprint(tree)
    compiledcode1 = compile(tree, "<string>", "exec")

    dict_of_arrays_of_files = dict()
    list_dir_by_dir(client, bucketname, prefix_in, True, dict_of_arrays_of_files)
    if (one_object_only): # truncate to first directory
        dict_of_arrays_of_files = new_dict_with_just_one(dict_of_arrays_of_files)
    try:
        start_run()
        for parentdir in dict_of_arrays_of_files:
            array_of_files = dict_of_arrays_of_files[parentdir]
            temp_input_dir = tempfile.mkdtemp()
            temp_output_dir = tempfile.mkdtemp()
            info('Processing parentdir ' + parentdir + ' with ' + str(len(array_of_files))\
                    + ' objects, temp_input_dir=' + str(temp_input_dir)\
                    + ', temp_output_dir=' + str(temp_output_dir))
            objects = download_objects_inner(endpoint, bucketname, parentdir, array_of_files,\
                    False, None, temp_input_dir, **kwargs)

            transformAst = infin_ast.extract_transform(TRANSFORM_DIR_BY_DIR,\
                    src_str=transform_string)
            transformSrc = infin_ast.get_source(transformAst)
            xn = TRANSFORM_DIR_BY_DIR
            tree = ast.parse(transformSrc)
            compiledcode3 = compile(tree, "<string>", "exec")

            # Add all functions in xformcode to the globals dictionary
            glb = {}
            fl = FuncLister(glb)
            fl.visit(tree)
            try:
                exec(compiledcode3, glb)
            except Exception as e:
                status_str = str(e)
                shutil.rmtree(temp_input_dir)
                continue # process next directory
            else:
                status_str = 'Success'
            # print('Globals=')
            # pprint.pprint(glb)
            info("Execution of global statics complete. status_str=" + status_str)

            namespaced_infin_transform_fnx = namespaced_function(glb[xn], glb, None, True)
            try:
                namespaced_infin_transform_fnx(temp_input_dir, temp_output_dir, **kwargs)
            except Exception as e:
                status_str = str(e)
                info("Error executing " + xn + ", status=" + status_str)
            else:
                info("Successfully executed transform " + xn + " for parentdir " + parentdir)
            finally:
                shutil.rmtree(temp_input_dir)

            try:
                dest_path = 'infinstor/' + parentdir
                for one_output_file in os.listdir(temp_output_dir):
                    fq_local = os.path.join(temp_output_dir, one_output_file)
                    info("Logging artifact " + str(fq_local) + " to " + dest_path)
                    log_artifact(fq_local, dest_path)
            except Exception as e:
                status_str = str(e)
                info("Error logging artifacts for parentdir " + str(parentdir)\
                        + ": " + status_str)
            else:
                info("Successfully logged artifacts for parentdir " + str(parentdir))
            finally:
                shutil.rmtree(temp_output_dir)
    finally:
        end_run()

def look_for_transform(transform_string, transform_symbol):
    transformAst = infin_ast.extract_transform(transform_symbol, src_str=transform_string)
    transformSrc = infin_ast.get_source(transformAst)
    if (verbose == True):
        print('transformSrc=' + transformSrc);
    tree = ast.parse(transformSrc)
    glb = {}
    fl = FuncLister(glb)
    fl.visit(tree)
    for key, value in glb.items():
        if (key == transform_symbol):
            return True
    return False

def run_transform_inline(time_spec, service_name, bucketname, prefix_in, xformname, **kwargs):
    endpoint = "https://" + time_spec + ".s3proxy." + service_name + ".com:443/";
    print('infinstor proxy endpoint=' + endpoint)
    session = boto3.session.Session(profile_name='infinstor')
    client = session.client('s3', endpoint_url=endpoint)

    xform_obj = client.get_object(Bucket='infinstor-pseudo-bucket', Key='transforms/' + xformname)
    strbody = xform_obj['Body']
    bts = strbody.read()
    transform_string = str(bts, 'utf-8')
    return run_transform_string_inline(time_spec, service_name, bucketname, prefix_in,\
            xformname, transform_string, False, **kwargs)

def run_transform_string_inline(time_spec, service_name, bucketname, prefix_in,\
        xformname, transform_string, one_object_only, **kwargs):
    if (look_for_transform(transform_string, TRANSFORM_RAW_PD)):
        print("Running transform " + str(TRANSFORM_RAW_PD))
        return read_and_xform_to_pd(time_spec, service_name, bucketname, prefix_in, False,\
                xformname, transform_string, one_object_only, **kwargs)
    elif (look_for_transform(transform_string, TRANSFORM_RAW_DS)):
        print("Running transform " + str(TRANSFORM_RAW_DS))
        return read_and_xform_to_ds(time_spec, service_name, bucketname, prefix_in, False,\
                xformname, transform_string, one_object_only, **kwargs)
    elif (look_for_transform(transform_string, TRANSFORM_CSV_PD)):
        print("Running transform " + str(TRANSFORM_CSV_PD))
        return read_and_xform_to_pd(time_spec, service_name, bucketname, prefix_in, True,\
                xformname, transform_string, one_object_only, **kwargs)
    elif (look_for_transform(transform_string, TRANSFORM_CSV_DS)):
        print("Running transform " + str(TRANSFORM_CSV_DS))
        return read_and_xform_to_ds(time_spec, service_name, bucketname, prefix_in, True,\
                xformname, transform_string, one_object_only, **kwargs)
    elif (look_for_transform(transform_string, TRANSFORM_ONE_OBJ)):
        print("Running transform " + str(TRANSFORM_ONE_OBJ))
        return read_and_xform_one_object(time_spec, service_name, bucketname, prefix_in,\
                xformname, transform_string, one_object_only, **kwargs)
    elif (look_for_transform(transform_string, TRANSFORM_DIR_BY_DIR)):
        print("Running transform " + str(TRANSFORM_DIR_BY_DIR))
        return read_and_xform_dir_by_dir(time_spec, service_name, bucketname, prefix_in,\
                xformname, transform_string, one_object_only, **kwargs)
    else:
        raise Exception("Cannot find a known transform function");

def run_transform_singlevm(time_spec, service_name, bucketname, prefix_in, xformname,\
        instance_type, **kwargs):
    # save the conda environment
    projdir = tempfile.mkdtemp()
    print('Project dir: ' + projdir)
    condayaml = os.open(projdir + sep + 'conda.yaml', os.O_CREAT|os.O_WRONLY, mode=0o644)
    cmd = ['conda', 'env', 'export', '--no-builds']
    print('Running cmd:')
    print(*cmd)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,\
                stdin=subprocess.DEVNULL, close_fds=True)
    for line in process.stdout:
        os.write(condayaml, line)
    process.wait()

    with open(projdir + sep + 'MLproject', "w") as projfile:
        kwp = ''
        for key, value in kwargs.items():
            kwp = kwp + (' --' + key + '={' + key + '}')
        projfile.write('Name: run-' + xformname + '\n')
        projfile.write('conda_env: conda.yaml\n')
        projfile.write('\n')
        projfile.write('entry_points:' + '\n')
        projfile.write('  main:' + '\n')
        projfile.write('    parameters:\n')
        projfile.write('      timespec: string\n')
        projfile.write('      service: string\n')
        projfile.write('      bucket: string\n')
        projfile.write('      prefix: string\n')
        projfile.write('      xformname: string\n')
        for key, value in kwargs.items():
            projfile.write('      ' + key + ': string\n')
        projfile.write('    command: "python -c \'from infinstor import mlflow_run; mlflow_run.main()\'\
                    --timespec={timespec} --service={service}\
                    --bucket={bucket} --prefix={prefix} --xformname={xformname}' + kwp + '"\n')

    child_env = os.environ.copy()
    child_env['MLFLOW_TRACKING_URI'] = 'infinstor://' + service_name + '/'
    cmd = ['mlflow', 'run',\
            '-b', 'infinstor-backend', '--backend-config',\
            '{"instance_type": "' + instance_type + '"}',\
            projdir,\
            '-P', 'timespec=' + time_spec,\
            '-P', 'service=' + service_name,\
            '-P', 'bucket=' + bucketname,\
            '-P', 'prefix=' + prefix_in,\
            '-P', 'xformname=' + xformname ]
    for key, value in kwargs.items():
        cmd.append('-P')
        cmd.append(key + '=' + value)
    print('Running cmd:')
    print(*cmd)
    process = subprocess.Popen(cmd, env=child_env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,\
            stdin=subprocess.DEVNULL, close_fds=True)
    for line in process.stdout:
        print(line.decode('utf-8'))
    process.wait()

    return None

def run_transform_emr(time_spec, service_name, bucketname, prefix_in, xformname, **kwargs):
    print('Error: Unimplemented')
    return None

def run_transform_old(time_spec, service_name, bucketname, prefix_in, xformname, run_location,**kwargs):
    run_options = dict()
    if (run_location == "inline"):
        run_options['run_location'] = 'inline'
        run_options['time_spec'] = time_spec
        run_options['service_name'] = service_name
        run_options['bucketname'] = bucketname
        run_options['prefix'] = prefix_in
        run_options['xformname'] = xformname
        return run_transform_new(**dict(kwargs, run_options=run_options))
    elif (run_location == "singlevm"):
        run_options['run_location'] = 'singlevm'
        run_options['time_spec'] = time_spec
        run_options['service_name'] = service_name
        run_options['bucketname'] = bucketname
        run_options['prefix'] = prefix_in
        run_options['xformname'] = xformname
        run_options['instance_type'] = kwargs.pop('instance_type')
        return run_transform_singlevm(time_spec, service_name, bucketname, prefix_in, xformname,\
                instance_type, **kwargs)
    elif (run_location == "emr"):
        run_options['run_location'] = 'singlevm'
        run_options['time_spec'] = time_spec
        run_options['service_name'] = service_name
        run_options['bucketname'] = bucketname
        run_options['prefix'] = prefix_in
        run_options['xformname'] = xformname
        run_options['instance_type'] = kwargs.pop('instance_type')
    return run_transform_new(**dict(kwargs, run_options=run_options))

def run_transform(run_options, **kwargs):
    run_location = run_options.pop('run_location')
    if (run_location == "inline"):
        time_spec = run_options.pop('time_spec')
        service_name = run_options.pop('service_name')
        bucketname = run_options.pop('bucketname')
        prefix_in = run_options.pop('prefix')
        xformname = run_options.pop('xformname')
        return run_transform_inline(time_spec, service_name, bucketname, prefix_in, xformname,\
                **kwargs)
    elif (run_location == "singlevm"):
        time_spec = run_options.pop('time_spec')
        service_name = run_options.pop('service_name')
        bucketname = run_options.pop('bucketname')
        prefix_in = run_options.pop('prefix')
        xformname = run_options.pop('xformname')
        instance_type = run_options.pop('instance_type')
        return run_transform_singlevm(time_spec, service_name, bucketname, prefix_in, xformname,\
                instance_type, **kwargs)
    elif (run_location == "emr"):
        time_spec = run_options.pop('time_spec')
        service_name = run_options.pop('service_name')
        bucketname = run_options.pop('bucketname')
        prefix_in = run_options.pop('prefix')
        xformname = run_options.pop('xformname')
        return run_transform_emr(time_spec, service_name, bucketname, prefix_in, xformname,\
                **kwargs)

def test_once(servicename, bucketname, path_in_bucket,  time_spec, **kwargs):
    caller_globals = dict(inspect.getmembers(inspect.stack()[1][0]))["f_globals"]
    code_str = ''
    for one_line in caller_globals['In']:
        code_str = one_line # pick last cell's code
    # print(code_str)

    clean_code = ''
    code_str_lines = code_str.splitlines()
    for one_line in code_str_lines:
        if (one_line == '%reset -f'):
            continue
        if (one_line == 'from infinstor import test_once # infinstor'):
            continue
        if (one_line.startswith('rv = test_once')):
            continue
        clean_code += (one_line + '\n')
    # print(clean_code)
    return run_transform_string_inline(time_spec, servicename, bucketname, path_in_bucket,\
            None, clean_code, True, **kwargs)
