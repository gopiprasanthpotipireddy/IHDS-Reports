# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import warnings


def read_household_data(file_path,file_name):
    """ 
    Reading IHDS HouseHolds Survey Data from tsv file
    
    """
    hh_path=os.path.join(file_path,file_name)
    hh_data=pd.read_csv(hh_path,sep='\t')
    return hh_data;


def preprocess_data(hh_data):
    """
    Cleaning the Data and adjust for easy plotting
    
    FROM data/DS0002/36151-0002-Codebook.pdf
    
    ID13: Caste category
    Value       Label                                 Count 
    1           Brahmin 1                               2192 
    2           Forward/General (except Brahmin) 2      9665 
    3           Other Backward Castes (OBC) 3           17056 
    4           Scheduled Castes (SC) 4                 8941 
    5           Scheduled Tribes (ST) 5                 3644 
    6           Others 6                                568
    Missing Data                                        86 
    Total                                               42,152
    
    
    TR4A: Practice untouchability
    
    Value   Label         
    0       No 0        
    1       Yes 1
    """

    for i in hh_data.ID13.unique():
        hh_data.loc[hh_data.ID13 ==i, 'ID13'] = str(i)

    hh_data.ID13.unique()

    for i in hh_data.TR4A.unique():
        hh_data.loc[hh_data.TR4A ==i, 'TR4A'] = str(i)
        
    return hh_data;
    


def total_untouchability_practice_percentage(hh_data_cleaned):
    """percentage of households practicing untouchability"""
    untouchability_percentage= (hh_data_cleaned.loc[hh_data_cleaned['TR4A']=='1',:].shape[0])/(hh_data_cleaned.shape[0])*100
    print(untouchability_percentage);
    



def get_social_groups_practice_untouchability(hh_data_cleaned):
    """
    Untouchabilyt Practice By Each Social Group
    
    """
    hh_social_groups=hh_data_cleaned.groupby(['ID13','TR4A']).size()
    sg_un_practice=hh_social_groups.groupby(level=0).apply(lambda x:100 * x / float(x.sum())).reset_index(name='Percentage')
    sg_un_practice=sg_un_practice.loc[sg_un_practice.TR4A=='1',:]
    sg_un_practice['SocialGroup']=["Not Mentioned","Brahmin","Forward/General (except Brahmin)","Other Backward Castes"," Scheduled Castes"," Scheduled Tribes","Others"]
    print(sg_un_practice)
    return sg_un_practice;

    
def plot_bar_x(sg_un_practice):
    """
    plotting social groups practicing untouchability
   
    """
    index = np.arange(len(sg_un_practice))
    plt.bar(index, sg_un_practice.Percentage)
    plt.xlabel('SocialGroup', fontsize=10)
    plt.ylabel('Percentage', fontsize=10)
    plt.xticks(index, sg_un_practice['SocialGroup'], fontsize=10,rotation=90)
    plt.title('Social Groups Practicing UnTouchability')
    plt.gcf().savefig('SG-UNTOUCHABILITY.png')
    plt.show()

    
        
def main():
    #Reading Data
    file_path="./data/DS0002"
    file_name="36151-0002-Data.tsv"
    print(read_household_data.__doc__)
    hh_data=read_household_data(file_path,file_name);
    
    
    #Clean and Preprocess 
    print(preprocess_data.__doc__)
    hh_data_cleaned=preprocess_data(hh_data);
    
    #Print untouchabulity practice percentage
    print(total_untouchability_practice_percentage.__doc__)
    total_untouchability_practice_percentage(hh_data_cleaned)
    
    #Percentage of Social Gropus Practicing 
    print(get_social_groups_practice_untouchability.__doc__)
    sg_un_practice=get_social_groups_practice_untouchability(hh_data_cleaned)
    
    #Plotting Percentages
    print(plot_bar_x.__doc__)
    plot_bar_x(sg_un_practice)
    

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    main()



