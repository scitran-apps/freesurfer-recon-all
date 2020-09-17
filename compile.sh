#!/bin/bash

cat > build.m <<END

addpath(genpath('/opt/freesurfer-7.1.1/matlab'));
mcc -m -R -nodisplay -a *.m -d ../compiled fixAllSegmentations.m 

exit
END
matlab -nodisplay -nosplash -r build && rm build.m

