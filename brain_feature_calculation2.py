import hdf5storage
import numpy as np 
import seaborn as sns
import pandas as pd
import nibabel as nib
from nilearn import surface 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def collect_surface_area(sublist, statelist, labels):
    area_matrix = np.zeros([len(sublist),len(statelist),len(labels)])
    for s, sub in enumerate(sublist):
        for t, state in enumerate(statelist):
            midsurf_L_path = '/cbica/projects/HCP_Data_Releases/HCP_1200/{}/MNINonLinear/fsaverage_LR32k/{}.L.midthickness_MSMAll.32k_fs_LR.surf.gii'.format(sub, sub)
            midsurf_R_path = '/cbica/projects/HCP_Data_Releases/HCP_1200/{}/MNINonLinear/fsaverage_LR32k/{}.R.midthickness_MSMAll.32k_fs_LR.surf.gii'.format(sub, sub)
            
            resultdir = '/gpfs/fs001/cbica/home/malia/project/HCP_indi_script/Result/HCP_1200_p3/rest/FN_17/Individual'
            subparcellation = hdf5storage.loadmat('{}/{}/{}/HCP_sbj1_comp17_alphaS21_2_alphaL10_vxInfo0_ard1_eta0/final_UV.mat'.format(resultdir, sub, state))['V'][0,0]
            subparcellation = np.argmax(subparcellation, axis=1)  
            sub_label_L = S29kto32k(subparcellation[:29696], 'L' )
            sub_label_R = S29kto32k(subparcellation[29696:], 'R' )
            
            filestring = sub
            savedir = '/gpfs/fs001/cbica/home/malia/project/HCP_indi_script/brain_area/'
            area = cal_surf_area(midsurf_L_path, midsurf_R_path, sub_label_L, sub_label_R, labels, filestring, savedir)
            area_matrix[s, t, :] = area
    np.save('/gpfs/fs001/cbica/home/malia/project/HCP_indi_script/brain_area/surface_brain_area.npy',area_matrix)
    return None


def cal_vol_area(brain_filepath, labels):
    vollist = []
    data = nib.load(brain_filepath).get_fdata() 
    for ll in labels:
        counts = (data==ll).sum()
        volumn = counts*1.25*1.25*1.25
        vollist.append(volumn)   
    return vollist
    
    
def collect_vol_area(sublist):
    volumn_list = []
    for sub in sublist:
        print(sub)
        brain_fiber = 'G:/HCP_S1200_individual_MSM_atlas/{}/tractseg_output/bundle_segmentations.nii.gz'.format(sub)
        subvollist = cal_vol_area(brain_fiber, np.arange(1,73))
        # brain_filepath = '/cbica/projects/HCP_Data_Releases/HCP_1200/{}/T1w/Diffusion/nodif_brain_mask.nii.gz'.format(sub)
        brain_filepath = 'G:/HCP_S1200_individual_MSM_atlas/{}/DTI/nodif_brain_mask.nii.gz'.format(sub)
        vol = cal_vol_area(brain_filepath, [1])
        subvollist.append(vol[0])
        volumn_list.append(subvollist)

    np.save('H:/Functional_heritability_analysis/whole_brain_volumn.npy', np.array(volumn_list))
    
    
if __name__ == '__main__':
    MD_workdir ='H:/Functional_heritability_analysis'

    sublist = list(np.load(MD_workdir+'/ready_subject.npy'))
    
    print(len(sublist))

    collect_vol_area(sublist)

