## scitran/freesurfer-recon-all

This build context will create a Gear built to the Flywheel v0 spec with Freesurfer (v5.3.0) that executes ```recon-all```.

* You MUST read and agree to the license agreement and [register with MGH before you use the software](https://surfer.nmr.mgh.harvard.edu/registration.html).
* Once you get your license please CREATE A LICENCE FILE AND SAVE IT TO THIS BUILD CONTEXT. The build will fail otherwise.
* You can also change ```build.sh``` to edit the tag for the image (default=scitran/freesurfer-recon-all).
* The resulting image is ~8GB


### Entrypoint ###
An 'Entrypoint' has been configured for this image at ```/opt/run```, which will do the following:
1. Look for inputs and show help as necessary
2. Run ```recon-all``` using the inputs provided
3. Optionally convert volume files to nifti, surface files to .obj and aseg.stats to csv.
4. Compress (using ```zip```) the subject directory

### Config ###
TODO - `config.json` usage.

### Example Usage ###
To run ```recon-all``` from this image (not in the Flywheel System)  you can do the following (note that the ```recon-all``` command is omitted as it is called from the ```Entrypoint```):
```
docker run --rm -ti \
    -v </path/to/input/data>:/input/flywheel/v0/input/anatomical \
    -v </path/for/output/data>:/ouput \
    scitran/freesurfer-recon-all
```
* Note that you are mounting the directory (```-v``` flag) which contains your data in the container at ```/input/flywheel/v0/input/anatomical``` and mounting the directory where you want your output data within the container at ```/output```.

* ```recon-all``` args (relative to the container) should be provided at the end of the ```docker run``` command, as shown above. Remember that if those inputs are files or other resources, they must also be mounted in the container and the full path to them (again, relative to the container) must be provided.
