import sys
import argparse
from . import run_transform_inline

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--timespec', help='InfinSnap/InfinSlice time specification')
    parser.add_argument('--service', help='infinstor|isstage?|isdemo?')
    parser.add_argument('--bucket', help='bucket name')
    parser.add_argument('--prefix', help='path in bucket')
    parser.add_argument('--xformname', help='name of transformation')
    args, unknown_args = parser.parse_known_args()
    print(str(unknown_args))
    kwa = dict()
    for ou in unknown_args:
        if (ou.startswith('--')):
            oup = ou[2:].split('=')
            if (len(oup) == 2):
                kwa[oup[0]] = oup[1]
    print(str(kwa))
    if (len(kwa.items()) > 0):
        return run_transform_inline(args.timespec, args.service, args.bucket, args.prefix, args.xformname, **kwa)
    else:
        return run_transform_inline(args.timespec, args.service, args.bucket, args.prefix, args.xformname)

if __name__ == "__main__":
    main()
