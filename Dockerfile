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

# Create Docker container that can run Matlab (mrDiffusion and afq analysis), ANTs, FSL, mrTrix.

# Start with the Matlab r2018b runtime container


RUN apt-get update --fix-missing \
 && apt-get install -y wget bzip2 ca-certificates \
      libglib2.0-0 libxext6 libsm6 libxrender1 \
      git mercurial subversion curl grep sed dpkg gcc g++ libeigen3-dev zlib1g-dev libqt4-opengl-dev libgl1-mesa-dev libfftw3-dev libtiff5-dev
RUN apt-get install -y libxt6 libxcomposite1 libfontconfig1 libasound2

###########################
# Configure neurodebian (https://github.com/neurodebian/dockerfiles/blob/master/dockerfiles/xenial-non-free/Dockerfile)
RUN set -x \
	&& apt-get update \
	&& { \
		which gpg \
		|| apt-get install -y --no-install-recommends gnupg \
	; } \
	&& { \
		gpg --version | grep -q '^gpg (GnuPG) 1\.' \
		|| apt-get install -y --no-install-recommends dirmngr \
	; } \
	&& rm -rf /var/lib/apt/lists/*

RUN set -x \
	&& export GNUPGHOME="$(mktemp -d)" \
	&& gpg --keyserver ha.pool.sks-keyservers.net --recv-keys DD95CC430502E37EF840ACEEA5D32F012649A5A9 \
	&& gpg --export DD95CC430502E37EF840ACEEA5D32F012649A5A9 > /etc/apt/trusted.gpg.d/neurodebian.gpg \
	&& rm -rf "$GNUPGHOME" \
	&& apt-key list | grep neurodebian

RUN { \
	echo 'deb http://neuro.debian.net/debian xenial main'; \
	echo 'deb http://neuro.debian.net/debian data main'; \
	echo '#deb-src http://neuro.debian.net/debian-devel xenial main'; \
} > /etc/apt/sources.list.d/neurodebian.sources.list

RUN sed -i -e 's,main *$,main contrib non-free,g' /etc/apt/sources.list.d/neurodebian.sources.list; grep -q 'deb .* multiverse$' /etc/apt/sources.list || sed -i -e 's,universe *$,universe multiverse,g' /etc/apt/sources.list


############################
# Install dependencies
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --force-yes \
    xvfb \
    xfonts-100dpi \
    xfonts-75dpi \
    xfonts-cyrillic \
    zip \
    unzip \
    python \
    imagemagick \
    wget \
    subversion \
    jq \
	vim \
	bsdtar \
    ants
	

############################
# The brainstem and hippocampal subfield modules in FreeSurfer-dev require the Matlab R2014b runtime
RUN apt-get install -y libxt-dev libxmu-dev
ENV FREESURFER_HOME /opt/freesurfer

RUN wget -N -qO- "https://surfer.nmr.mgh.harvard.edu/fswiki/MatlabRuntime?action=AttachFile&do=get&target=runtime2014bLinux.tar.gz" | tar -xz -C $FREESURFER_HOME && chown -R root:root /opt/freesurfer/MCRv84

RUN apt-get install python-pip
# Install neuropythy

ENV neuropythyCOMMIT=4dd300aca611bbc11a461f4c39d8548d7678d96c
RUN curl -#L https://github.com/noahbenson/neuropythy/archive/$neuropythyCOMMIT.zip | bsdtar -xf- -C /usr/lib
WORKDIR /usr/lib/
RUN mv neuropythy-$neuropythyCOMMIT neuropythy
RUN chmod -R +rwx /usr/lib/neuropythy
RUN pip install --upgrade pip && \
	pip2.7 install numpy && \
    pip2.7 install -e /usr/lib/neuropythy

# Make directory for flywheel spec (v0)
ENV FLYWHEEL /flywheel/v0
RUN mkdir -p ${FLYWHEEL}
RUN mkdir /flywheel/v0/templates/

# Download and unzip Buckner's Cerebellum atlas
RUN cd $WORKDIR
RUN wget ftp://surfer.nmr.mgh.harvard.edu/pub/data/Buckner_JNeurophysiol11_MNI152.zip
RUN unzip -j "Buckner_JNeurophysiol11_MNI152.zip" "Buckner_JNeurophysiol11_MNI152/Buckner2011_17Networks_MNI152_FreeSurferConformed1mm_LooseMask.nii.gz" -d "/flywheel/v0/templates/"
RUN mv /flywheel/v0/templates/Buckner2011_17Networks_MNI152_FreeSurferConformed1mm_LooseMask.nii.gz /flywheel/v0/templates/Buckner_CB.nii.gz
RUN unzip -j "Buckner_JNeurophysiol11_MNI152.zip" "Buckner_JNeurophysiol11_MNI152/FSL_MNI152_FreeSurferConformed_1mm.nii.gz" -d "/flywheel/v0/templates/"
RUN mv /flywheel/v0/templates/FSL_MNI152_FreeSurferConformed_1mm.nii.gz /flywheel/v0/templates/MNI_152.nii.gz

# Download the MORI ROIs 
RUN wget --retry-connrefused --waitretry=5 --read-timeout=20 --timeout=15 -t 0 -q -O MORI_ROIs.zip "https://osf.io/zxdt9/download"
RUN unzip MORI_ROIs.zip -d /flywheel/v0/templates/

# Add Thalamus FS LUT
COPY FreesurferColorLUT_THALAMUS.txt /flywheel/v0/templates/FreesurferColorLUT_THALAMUS.txt

## Add HCP Atlas and LUT
COPY local/MNI_Glasser_HCP_v1.0.nii.gz /flywheel/v0/templates/MNI_Glasser_HCP_v1.0.nii.gz
COPY local/LUT_HCP.txt /flywheel/v0/templates/LUT_HCP.txt

# Copy and configure run script and metadata code
COPY bin/run \
      bin/parse_config.py \
	  bin/separateROIs.py \
      bin/srf2obj \
      manifest.json \
      ${FLYWHEEL}/

# Handle file properties for execution
RUN chmod +x \
      ${FLYWHEEL}/run \
      ${FLYWHEEL}/srf2obj \
      ${FLYWHEEL}/parse_config.py \
	  ${FLYWHEEL}/separateROIs.py
WORKDIR ${FLYWHEEL}
# Run the run.sh script on entry.
ENTRYPOINT ["/flywheel/v0/run"]


