# This Dockerfile constructs a docker image, based on the vistalab/freesurfer
# docker image to execute recon-all as a Flywheel Gear.
#
# Example build:
#   docker build --no-cache --tag scitran/freesurfer-recon-all `pwd`
#
# Example usage:
#   docker run -v /path/to/your/subject:/input scitran/freesurfer-recon-all
#

FROM scitran/freesurfer-dev:20200104
LABEL MAINTAINER="Michael Perry <lmperry@stanford.edu>"

# The brainstem and hippocampal subfield modules in FreeSurfer-dev require the Matlab R2014b runtime
RUN apt-get install -y libxt-dev libxmu-dev
ENV FREESURFER_HOME /opt/freesurfer

RUN wget -N -qO- "https://surfer.nmr.mgh.harvard.edu/fswiki/MatlabRuntime?action=AttachFile&do=get&target=runtime2014bLinux.tar.gz" | tar -xz -C $FREESURFER_HOME && chown -R root:root /opt/freesurfer/MCRv84

RUN apt-get install python-pip
# Install neuropythy
RUN pip install --upgrade pip && \
    pip2.7 install neuropythy

# Make directory for flywheel spec (v0)
ENV FLYWHEEL /flywheel/v0
RUN mkdir -p ${FLYWHEEL}

# Copy and configure run script and metadata code
COPY bin/run \
      bin/parse_config.py \
      bin/srf2obj \
      manifest.json \
      ${FLYWHEEL}/

# Handle file properties for execution
RUN chmod +x \
      ${FLYWHEEL}/run \
      ${FLYWHEEL}/srf2obj \
      ${FLYWHEEL}/parse_config.py

# Run the run.sh script on entry.
ENTRYPOINT ["/flywheel/v0/run"]
