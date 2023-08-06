import sys
import argparse
from . import run_transform_inline
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--service', help='infinstor|isstage?|isdemo?')
    parser.add_argument('--input_data_spec', help='input data spec')
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
    input_data_spec = json.loads(args.input_data_spec)
    if (len(kwa.items()) > 0):
        return run_transform_inline(args.service, input_data_spec, args.xformname, **kwa)
    else:
        return run_transform_inline(args.service, input_data_spec, args.xformname)

if __name__ == "__main__":
    main()
