# This Dockerfile constructs a docker image, based on the vistalab/freesurfer
# docker image to execute recon-all as a Flywheel Gear.
#
# Example build:
#   docker build --no-cache --tag scitran/freesurfer-recon-all `pwd`
#
# Example usage: #TODO
#   docker run -v /path/to/your/subject:/input scitran/freesurfer-recon-all
#

# Start with the Freesurfer container
FROM ubuntu:trusty

# Note the Maintainer
MAINTAINER Michael Perry <lmperry@stanford.edu>

# Install dependencies for FreeSurfer
RUN apt-get update && apt-get -y install \
        bc \
        tar \
        wget \
        gawk \
        tcsh \
        python \
        libgomp1 \
        python2.7 \
        perl-modules

# Download FS_v5.3.0 from MGH and untar to /opt
RUN wget -N -qO- ftp://surfer.nmr.mgh.harvard.edu/pub/dist/freesurfer/5.3.0/freesurfer-Linux-centos4_x86_64-stable-pub-v5.3.0.tar.gz | tar -xzv -C /opt

# FREESURFER Licsense (Must have this file to build)
COPY license /opt/freesurfer/.license

# Make directory for flywheel spec (v0)
ENV FLYWHEEL /flywheel/v0
RUN mkdir -p ${FLYWHEEL}

# Copy and configure run script and metadata code
COPY bin/run \
      bin/parse_config.py \
      bin/srf2obj \
      manifest.json \
      ${FLYWHEEL}/

# Copy the default config.json file to the container
COPY bin/config.json ${FLYWHEEL}/default_config.json

ADD https://raw.githubusercontent.com/scitran/utilities/daf5ebc7dac6dde1941ca2a6588cb6033750e38c/metadata_from_gear_output.py \
      ${FLYWHEEL}/metadata_create.py

# Handle file properties for execution
RUN chmod +x \
      ${FLYWHEEL}/run \
      ${FLYWHEEL}/srf2obj \
      ${FLYWHEEL}/parse_config.py \
      ${FLYWHEEL}/metadata_create.py

# Run the run.sh script on entry.
ENTRYPOINT ["/flywheel/v0/run"]
