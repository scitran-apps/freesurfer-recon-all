[![Docker Pulls](https://img.shields.io/docker/pulls/scitran/freesurfer-recon-all.svg)](https://hub.docker.com/r/scitran/freesurfer-recon-all/)
[![Docker Stars](https://img.shields.io/docker/stars/scitran/freesurfer-recon-all.svg)](https://hub.docker.com/r/scitran/freesurfer-recon-all/)
# scitran/freesurfer-recon-all

This build context will create an image built to the [Flywheel Gear Specification](https://github.com/flywheel-io/gears/tree/master/spec), which can execute Freesurfer's `recon-all` (**v6.0.1**) within [Flywheel](https://flywheel.io), or locally.

* You *MUST* read and agree to the license agreement and [register with MGH before you use the software](https://surfer.nmr.mgh.harvard.edu/registration.html).
* Once you get your license you can apply this license in one of three ways (order of precedence):
    1. Browse to an instance of `license.txt` stored at any level of the Flywheel container hierarchy from the input `freesurfer_license_file`
    2. Enter a space-delimited version of the license in the configuration `freesurfer_license`
    3. Ensure that `license.txt` is a file at the project level.
* This image is built with the Matlab MCRv80 included. The MCR is required to run the optional Hippocampal Subfields and Brainstem Structures processing (see [`manifest.json`](manifest.json)).
* The resulting image is ~12GB and builds in ~15min.


### Configuration Options ###
Configuration for running the algorithm are defined within `manifest.json`. The options available, along with their defaults, are described in the [`manifest.json`](manifest.json) file.

If you would like to use specific options in a local run of this gear you can modify the `default` key for each option, which will be used during the local run - executed when executed with Docker.

### Recent Updates
Recent updates (3/2020) grant control over `recon-all` paralellization.  The `-parallel` flag is set to run certain stages of `recon-all` on all available computational cores.  To limit the number of cores set `n_cpus` to the desired number.

### Example Local Usage ###
This Gear is designed to run within [Flywheel](https://flywheel.io), however you can run this Gear locally. To run ```recon-all``` from this image you can do the following:
```
# Note that the `recon-all` command is omitted as it is called from the `Entrypoint`.
docker run --rm -ti \
    -v </path/to/input/data>:/input/flywheel/v0/input/anatomical \
    -v </path/for/output/data>:/output \
    scitran/freesurfer-recon-all:<version-tag>
```

#### Usage Notes ####
* You must mount the directory (using the `-v` flag) which contains your anatomical data (nifti or dicoms) in the container at `/input/flywheel/v0/input/anatomical` and also mount the directory where you want your output data stored at `/output`, see the example above.
* Configuration options (including the license key) must be set in the `manifest.json` file **before building** the container.
