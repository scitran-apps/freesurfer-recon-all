#! /usr/bin/env python2.7
# Create the two hemispheres

def createHemiMaskFromAseg(asegFile):
    import os
    import nibabel as nib
    import numpy as np
    # Read the aseg file
    aseg = nib.load(asegFile)
    asegData = aseg.get_data()
    # Read the Look up table
    fLUT = open(os.path.join(os.getenv('FREESURFER_HOME'),'FreeSurferColorLUT.txt'),'r')
    LUT = fLUT.readlines()
    fLUT.close()
    cleanLUT = [s for s in LUT if not '#' in s]
    # Obtain the labels per each hemi
    leftLUT  = [int(s.split()[0]) for s in cleanLUT if 'Left' in s or 'lh' in s]
    rightLUT = [int(s.split()[0]) for s in cleanLUT if 'Right' in s or 'rh' in s]
    # Create the two hemispheres
    leftMask   = nib.Nifti1Image(np.isin(asegData, leftLUT), aseg.affine, aseg.header)
    rightMask  = nib.Nifti1Image(np.isin(asegData, rightLUT), aseg.affine, aseg.header)
    # Write the new niftis
    (head,tail) = os.path.split(asegFile)
    nib.save(leftMask, os.path.join(head,'lh.AsegMask.nii.gz'))
    nib.save(rightMask, os.path.join(head,'rh.AsegMask.nii.gz'))
    print('Created ?h.AsegMask.nii.gz in the same folder as the input file')

   	

def segThalamus():
    import os
    import subprocess as sp
    fLUT = open(args.ThLUT)
    LUT = fLUT.readlines()
    fLUT.close()
    cleanLUT = [s for s in LUT if '-' in s and not '#' in s]
    # Obtain the labels of thalamic nuclei
    index  = [int(s.split()[0]) for s in cleanLUT if 8100<int(s.split()[0]) and int(s.split()[0])<8300]
    label  = [str(s.split()[1]) for s in cleanLUT if 8100<int(s.split()[0]) and int(s.split()[0])<8300]
    (head, tail) = os.path.split(args.ThN)
    for i in range(len(index)):
        # extract nuclei
		sp.call(str('mri_extract_label ' + args.ThN + ' ' + 
				str(index[i]) + ' ' + os.path.join(head, 'ROIs', str(label[i] + 
				'.nii.gz'))), shell=True) 
        # extrac nuclei and dilate 1 time
		sp.call(str('mri_extract_label ' + '-dilate 1 '+ args.ThN + ' ' + 
				str(index[i]) + ' ' + os.path.join(head, 'ROIs', str(label[i] + 
				'_dil-1.nii.gz'))), shell=True) 
        # extrac nuclei and dilate 2 times
		sp.call(str('mri_extract_label ' + '-dilate 2 ' + args.ThN + ' ' + 
				str(index[i]) + ' ' + os.path.join(head, 'ROIs', str(label[i] +
				 '_dil-2.nii.gz'))), shell=True) 

def segBensonVarea():
	import os
	import subprocess as sp
	dic_ben = {1:  'V1',   2: 'V2',  3: 'V3',  4: 'hV4',  5: 'VO1',
			   6:  'VO2',  7: 'LO1', 8: 'LO2', 9: 'TO1', 10: 'TO2',
		       11: 'V3b', 12: 'V3a'}
	(head, tail) = os.path.split(args.benV)
 
	for index in dic_ben:
		roi       = os.path.join(head, 'ROIs', str(dic_ben[index] + '.nii.gz'))
		roi_dil_1 = os.path.join(head, 'ROIs', str(dic_ben[index] + '_dil-1.nii.gz'))
 		roi_dil_2 = os.path.join(head, 'ROIs', str(dic_ben[index] + '_dil-2.nii.gz'))
 		 # extract benson varea
		sp.call(str('mri_extract_label ' + args.benV + ' ' + 
				str(index) + ' ' + roi), shell=True) 
        # extrac and dilate 1 time
		sp.call(str('mri_extract_label ' + '-dilate 1 '+ args.benV + ' ' + 
				str(index) + ' ' + roi_dil_1), shell=True) 
        # extrac and dilate 2 times
		sp.call(str('mri_extract_label ' + '-dilate 2 ' + args.benV + ' ' + 
				str(index) + ' ' + roi_dil_2), shell=True) 
		# mask left and right hemisphere
		for i in [roi, roi_dil_1, roi_dil_2]:
			# extract the left
			lhname = str(i.split('.')[0] + '_L.nii.gz')
			rhname = str(i.split('.')[0] + '_R.nii.gz')
			# extract the left
			sp.call(str('mri_binarize --mask ' + os.path.join(head, 'lh.AsegMask.nii.gz') +
				' --min 0.1 --i ' + i +
				' --o '+ lhname), shell = True)
			# extract the right
			sp.call(str('mri_binarize --mask ' + os.path.join(head, 'rh.AsegMask.nii.gz') +
				' --min 0.1 --i ' + i +
				' --o '+ rhname), shell = True)
			os.remove(i)
def segCB():
	# extract Cerebellum
	import os
	import subprocess as sp
	(head, tail) = os.path.split(args.cb)
	for index in range(1,18):
		# extract Cerebellum based on the 17Networks
		roi       =  os.path.join(head, 'ROIs', str('17Networks_' + str(index) + '.nii.gz'))
		roi_dil_1 =  os.path.join(head, 'ROIs', str('17Networks_' + str(index) + '_dil-1.nii.gz'))
 		roi_dil_2 =  os.path.join(head, 'ROIs', str('17Networks_' + str(index) + '_dil-2.nii.gz'))
 		sp.call(str('mri_extract_label ' + args.cb + ' ' + 
				str(index) + ' ' + roi ), shell=True) 
   		 # extrac and dilate 1 time
		sp.call(str('mri_extract_label ' + '-dilate 1 '+ args.cb + ' ' + 
				str(index) + ' ' + roi_dil_1), shell=True) 
        # extrac and dilate 2 times
		sp.call(str('mri_extract_label ' + '-dilate 2 ' + args.cb + ' ' + 
				str(index) + ' ' + roi_dil_2), shell=True) 
		# mask left and right hemisphere
		for i in [roi, roi_dil_1, roi_dil_2]:
			# extract the left
			lhname = str(i.split('.')[0] + '_L.nii.gz')
			rhname = str(i.split('.')[0] + '_R.nii.gz')
			sp.call(str('mri_binarize --mask ' + os.path.join(head, 'lh.AsegMask.nii.gz') +
				' --min 0.1 --i ' + i + 
				' --o '+ lhname), shell = True)
			# extract the right
			sp.call(str('mri_binarize --mask ' + os.path.join(head, 'rh.AsegMask.nii.gz') +
				' --min 0.1 --i ' + i +
				' --o '+ rhname), shell = True)
			os.remove(i)




def separateROIs(args):
    import os
    import subprocess as sp
    if args.ThN:
        print('x')
        segThalamus()
    if args.aparcaseg:
        asegDir = os.path.dirname(os.path.abspath(args.aparcaseg))
        if not os.path.isfile(str(asegDir + '/lh.AsegMask.nii.gz')):
            createHemiMaskFromAseg(args.aparcaseg) 
	if args.benV:
		print('benV')
		segBensonVarea()	
	if args.cb:
		print('CB')
		segCB()














if __name__ == '__main__':
	import argparse
	ap = argparse.ArgumentParser()
	ap.add_argument('-ThN', type=str,  help='Full path to ThalamicNuclei.T1.FSvoxelSpace.nii.gz')
	ap.add_argument('-ThLUT', type=str,  help='Full path to ThalamicNuclei LUT')
	ap.add_argument('-aparcaseg', type=str, help='Full path to aparc+aseg.nii.gz')
	ap.add_argument('-benV', type=str, help='Full path to benson Varea image')
	ap.add_argument('-cb', type=str, help='Full path to Bucker cerebellm image')
	args = ap.parse_args()
	separateROIs(args)
	
