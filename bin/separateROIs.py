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
    dilstr = ['', '_dil-1', '_dil-2']; diloption = ['', '-dilate 1', '-dilate 2']
    for i in range(len(index)):
        # extract nuclei
        for x in range(len(dilstr)):
            roiname = os.path.join(head, 'ROIs', str(label[i] + dilstr[x] + '.nii.gz'))
            cmdstr = str('mri_extract_label ' + diloption[x] + ' ' + args.ThN + ' ' + 
                str(index[i]) + ' ' + roiname)
            print(cmdstr) 
            sp.call(cmdstr, shell=True) 
            # binarize the ROIs
            cmdstr = str('mri_binarize ' + '--min 0.1 ' + '--i ' + roiname + ' ' + '--o ' + roiname)
            print(cmdstr)
            sp.call(cmdstr, shell=True) 

def segBensonVarea():
    import os
    import subprocess as sp
    dic_ben = {1:  'V1',   2: 'V2',  3: 'V3',  4: 'hV4',  5: 'VO1',
               6:  'VO2',  7: 'LO1', 8: 'LO2', 9: 'TO1', 10: 'TO2',
               11: 'V3b', 12: 'V3a'}
    (head, tail) = os.path.split(args.benV)
 
    for index in dic_ben:
        dilstr = ['', '_dil-1', '_dil-2']; diloption = ['', '-dilate 1 ', '-dilate 2 ']
        for i in range(len(dilstr)):
            roiname = os.path.join(head, 'ROIs', str(dic_ben[index] +dilstr[i] + '.nii.gz'))
            # extract benson varea
            
            cmdstr = str('mri_extract_label ' + diloption[i] + args.benV + ' ' + 
                str(index) + ' ' + roiname )
            print(cmdstr)
            sp.call(cmdstr, shell=True) 
            # mask left and right hemisphere
            # extract the left
            head_tail = os.path.split(roiname)
            lhname = str(head_tail[0] + '/Left-' + head_tail[1])
            rhname = str(head_tail[0] + '/Right-' + head_tail[1])
            # extract the left
            cmdstr = str('mri_binarize --mask ' + os.path.join(head, 'lh.AsegMask.nii.gz') +
                         ' --min 0.1 --i ' + roiname + ' --o '+ lhname)
            print(cmdstr)    
            sp.call(cmdstr, shell = True)
            # extract the right
            cmdstr = str('mri_binarize --mask ' + os.path.join(head, 'rh.AsegMask.nii.gz') +
                        ' --min 0.1 --i ' + roiname + ' --o '+ rhname)
            print(cmdstr)    
            sp.call(cmdstr, shell = True)
            os.remove(roiname)


def segCB():
    # extract Cerebellum
    import os
    import subprocess as sp
    (head, tail) = os.path.split(args.cb)
    for index in range(1,18):
        dilstr = ['', '_dil-1', '_dil-2']; diloption = ['', '-dilate 1 ', '-dilate 2 ']
        for i in range(len(dilstr)):
            # extract Cerebellum based on the 17Networks
            roiname = os.path.join(head, 'ROIs', str('17Networks_' + str(index) + dilstr[i] + '.nii.gz'))
            cmdstr = str('mri_extract_label ' + args.cb + ' ' + str(index) + ' ' + roiname )
            print(cmdstr)    
            sp.call(cmdstr, shell = True)
            
            # mask left and right hemisphere
            # extract the left
            head_tail = os.path.split(roiname)
            lhname = str(head_tail[0] + '/Left-' + head_tail[1])
            rhname = str(head_tail[0] + '/Right-' + head_tail[1])
            cmdstr = str('mri_binarize --mask ' + os.path.join(head, 'lh.AsegMask.nii.gz') +
                ' --min 0.1 --i ' + roiname + ' --o '+ lhname)
            print(cmdstr)    
            sp.call(cmdstr, shell = True)
            # extract the right
            cmdstr = str('mri_binarize --mask ' + os.path.join(head, 'rh.AsegMask.nii.gz') +
                ' --min 0.1 --i ' + roiname + ' --o '+ rhname)
            print(cmdstr)    
            sp.call(cmdstr, shell = True)
            os.remove(roiname)


def segAparc2009():
    import os
    import subprocess as sp
    (head, tail) = os.path.split(args.aparc2009)
    fLUT = open(os.path.join(os.getenv('FREESURFER_HOME'),'FreeSurferColorLUT.txt'),'r')
    LUT = fLUT.readlines()
    fLUT.close()
    cleanLUT = [s for s in LUT if '-' in s and not '#' in s]
    # Obtain the labels of aparc+aseg.nii.gz
    index  = [int(s.split()[0]) for s in cleanLUT if (11100<int(s.split()[0]) and int(s.split()[0])<12175) or (0<int(s.split()[0]) and int(s.split()[0])<180) ]
    label  = [str(s.split()[1]) for s in cleanLUT if (11100<int(s.split()[0]) and int(s.split()[0])<12175 ) or (0<int(s.split()[0]) and int(s.split()[0])<180) ]

    for i in range(len(index)):
        dilstr = ['', '_dil-1', '_dil-2']; diloption = ['', '-dilate 1 ', '-dilate 2 ']
        for x in range(len(dilstr)):
            #  extract nuclei
            roiname = os.path.join(head, 'ROIs', str(label[i] + dilstr[x] + '.nii.gz'))
            cmdstr = str('mri_extract_label -exit_none_found ' + diloption[x] + args.aparc2009 + ' ' + 
                str(index[i]) + ' ' + roiname )
            print(cmdstr)
            sp.call(cmdstr, shell=True)
            # extrac nuclei and dilate 1 time
            
            cmdstr = str('mri_binarize ' + '--min 0.1 ' + '--i ' + roiname + 
                        ' --o ' + roiname) 
            print(cmdstr)
            sp.call(cmdstr, shell=True)

 


def separateROIs(args):
    import os
    import subprocess as sp
    if args.ThN:
        print('separating thalamic nuclei')
        segThalamus()
    if args.aparc2009:
        print('separating aparc+aseg.nii.gz')
        segAparc2009()
    if args.benV:
        print('benV')
        (head, tail) = os.path.split(args.benV)
        # if Aseg do not have left and right mask, generate them
        aseg = os.path.join(head,'aparc+aseg.nii.gz')
        if not os.path.isfile(str(head + '/lh.AsegMask.nii.gz')):
            createHemiMaskFromAseg(aseg) 
        segBensonVarea()
    if args.cb:
        print('CB')
        (head, tail) = os.path.split(args.cb)
        # if Aseg do not have left and right mask, generate them
        aseg = os.path.join(head,'aparc+aseg.nii.gz')
        if not os.path.isfile(str(head + '/lh.AsegMask.nii.gz')):
            createHemiMaskFromAseg(aseg) 
        segCB()













if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('-ThN', type=str,  help='Full path to ThalamicNuclei.T1.FSvoxelSpace.nii.gzi, specify LookupTable by -ThLUT')
    ap.add_argument('-ThLUT', type=str,  help='Full path to ThalamicNuclei LUT')
    ap.add_argument('-aparc2009', type=str, help='Full path to aparc.2009.nii.gz')
    ap.add_argument('-benV', type=str, help='Full path to benson Varea image')
    ap.add_argument('-cb', type=str, help='Full path to Bucker cerebellm image')
    args = ap.parse_args()
    separateROIs(args)
    
