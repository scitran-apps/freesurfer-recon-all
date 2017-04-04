#! /usr/bin/env python2.7
#
# Parse config.json and return strings that can be passed back to the calling
# function.
#

# Parse config file
def parse_config(args):
    import json
    import os

    # If the config file does not exist then exit
    if not os.path.isfile(args.json_file):
        raise SystemExit('File does not exist: %s!' % args.json_file)

    if args.json_file.endswith('manifest.json'):
        manifest=True
    else:
        manifest=False

    # Read the config json file
    with open(args.json_file, 'r') as jsonfile:
        config = json.load(jsonfile)

    # Load defaults from manifest
    if manifest:
        default_config = config['config']
        config = {}
        config['config'] = {}
        for k in default_config.iterkeys():
            config['config'][k] = default_config[k]['default']

    if args.i:
        print config['config']['subject_id']

    # Print options for recon-all
    if args.o:
        print config['config']['reconall_options']

    # Print options for recon-all
    if args.r:
        print config['config']['register_surfaces']

    # Convert surfaces to obj
    if args.s:
        print config['config']['convert_surfaces']

    # Convert mgz to nifti
    if args.n:
        print config['config']['convert_volumes']

    # Convert aseg stats to csv
    if args.a:
        print config['config']['convert_stats']

    # Process hippocampal subfields
    if args.c:
        print config['config']['hippocampal_subfields']

    # Process brainstem substructures
    if args.b:
        print config['config']['brainstem_structures']

    # Parse config for license elements
    if args.l:
        if config['config']['license_key'] and config['config']['license_key'][0] == "*":
            license_key = config['config']['license_key']
        else:
            license_key = "*" + config['config']['license_key']
        print config['config']['license_email'] + "\\n" + config['config']['license_number'] + "\\n " + license_key + "\\n" + config['config']['license_reference'] + "\\n"

if __name__ == '__main__':

    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--json_file', type=str, dest="json_file", help='Full path to the input json config file.')
    ap.add_argument('-i', action='store_true', help='Return subject ID')
    ap.add_argument('-o', action='store_true', help='Return Recon-All Options')
    ap.add_argument('-s', action='store_true', help='Convert surfaces to obj')
    ap.add_argument('-n', action='store_true', help='Convert volume MGZ to NIfTI')
    ap.add_argument('-a', action='store_true', help='Convert ASEG stats to csv')
    ap.add_argument('-l', action='store_true', help='Generate License File')
    ap.add_argument('-c', action='store_true', help='Hippocampal subfields')
    ap.add_argument('-b', action='store_true', help='Brainstem processing')
    ap.add_argument('-r', action='store_true', help='Surface registration')
    args = ap.parse_args()

    parse_config(args)
