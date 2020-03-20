#! /usr/bin/env python2.7
#
# Parse config.json and return strings that can be passed back to the calling
# function.
#
import argparse
import json
import multiprocessing as mp
import os
import os.path as op
import zipfile

import flywheel


def parse_config(args):
    """
    parse_config Parses the config.json file

    Args:
        args (argparse.Namespace): The namespace of arguments to parse

    Raises:
        SystemExit: If the config.json file does not exist, exit.
    """

    # If the config file does not exist then exit
    if not os.path.isfile(args.json_file):
        raise SystemExit('File does not exist: %s!' % args.json_file)

    if args.json_file.endswith('manifest.json'):
        manifest = True
    else:
        manifest = False

    # Read the config json file
    with open(args.json_file, 'r') as jsonfile:
        config = json.load(jsonfile)

    # Load defaults from manifest
    if manifest:
        default_config = config['config']
        config = {}
        config['config'] = {}
        for k in default_config.iterkeys():
            if default_config[k].get('default'):
                config['config'][k] = default_config[k]['default']
    else:
        context = flywheel.GearContext(
            gear_path=op.dirname(args.json_file)
        )
        fw = context.client
        destination_id = context.destination.get('id')

    if args.i:
        if context.config.get('subject_id'):
            print(config['config']['subject_id'])
        else:
            subject_id = fw.get_analysis(destination_id).parents.subject
            subject = fw.get(subject_id)
            print(subject.label)

    # Print options for recon-all
    if args.o:
        option_string = config['config']['reconall_options']
        # This is mixing old and new manners of doing this quite a bit
        # It will work for a PoC, but going forward it would be good to
        # standardize.
        if context.config['parallel']:
            option_string += ' -parallel '
            # grab number of cpus from host.
            max_cpus = mp.cpu_count()
            # use of -parallel defaults to cpu_count unless specified
            if context.config.get('n_cpus'):
                # However, we will do strict checking on max_cpus
                if context.config['n_cpus'] <= max_cpus:
                    option_string += '-openmp ' + str(context.config['n_cpus'])
                else:
                    option_string += '-openmp ' + str(max_cpus)
            else:
                option_string += '-openmp ' + str(max_cpus)

        print(option_string)

    # Print options for recon-all
    if args.r:
        print(config['config']['register_surfaces'])

    # Convert surfaces to obj
    if args.s:
        print(config['config']['convert_surfaces'])

    # Convert mgz to nifti
    if args.n:
        print(config['config']['convert_volumes'])

    # Convert aseg stats to csv
    if args.a:
        print(config['config']['convert_stats'])

    # Process hippocampal subfields
    if args.c:
        print(config['config']['hippocampal_subfields'])

    # Process brainstem substructures
    if args.b:
        print(config['config']['brainstem_structures'])

    # Get subject code from archive input
    if args.z:
        try:
            zip = zipfile.ZipFile(
                config['inputs']['anatomical']['location']['path'])
            print(zip.namelist()[0].split('/')[0])
        except:
            print('')

    # Parse config for license elements
    if args.l:
        # This will look for project level and input level freesurfer license
        # files

        # grab input, config, project file, and project metadata in order
        # they are checked
        # from input:
        fs_license_file = context.get_input_path('freesurfer_license_file')
        # from config:
        fs_license = context.config.get('freesurfer_license')
        # from project file attachments:
        project_id = fw.get_analysis(destination_id).parents.project
        project = fw.get_project(project_id)
        project_license = project.get_file('license.txt')
        # from project metadata
        fs_license_info = project.info.get('FREESURFER_LICENSE')

        # Check for freesurfer license in precedence order:
        # Check the inputs for the license file
        if fs_license_file:
            print(open(fs_license_file, 'r').read())
        # else use the space-delimited config
        elif fs_license:
            print(fs_license.replace(" ", "\\n"))
        # else look for it in the associated project file attachments
        elif project_license:
            local_license = op.join(context.work_dir, 'license.txt')
            project.download_file('license.txt', local_license)
            print(open(local_license, 'r').read())
        # else look for it in the project metadata
        elif fs_license_info:
            print(fs_license.replace(" ", "\\n"))
        # else we don't have one... and give an error in the bash script
        else:
            print("")


# This works better for testing
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json_file', type=str, dest="json_file",
                    help='Full path to the input json config file.')
    ap.add_argument('-i', action='store_true', help='Return subject ID')
    ap.add_argument('-p', action='store_true', help='Recon-All -parallel flag')
    ap.add_argument('-N', type=str, dest='n_cpus',
                    help='Sets the -openmp <num> flag, where <num> is the number of processors to use')
    ap.add_argument('-o', action='store_true',
                    help='Return Recon-All Options')
    ap.add_argument('-s', action='store_true',
                    help='Convert surfaces to obj')
    ap.add_argument('-n', action='store_true',
                    help='Convert volume MGZ to NIfTI')
    ap.add_argument('-a', action='store_true',
                    help='Convert ASEG stats to csv')
    ap.add_argument('-l', action='store_true',
                    help='Generate License File')
    ap.add_argument('-c', action='store_true',
                    help='Hippocampal subfields')
    ap.add_argument('-b', action='store_true', help='Brainstem processing')
    ap.add_argument('-r', action='store_true', help='Surface registration')
    ap.add_argument('-z', action='store_true',
                    help='Get sub code from zip input')
    args = ap.parse_args()

    parse_config(args)


if __name__ == '__main__':
    main()
