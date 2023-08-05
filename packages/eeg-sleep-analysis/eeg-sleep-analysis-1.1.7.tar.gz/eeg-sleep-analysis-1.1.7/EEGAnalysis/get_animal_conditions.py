import os
import sys
import pandas as pd
import numpy as np

def create_conditions(filedir,condname,fname_conv):
    animal_conditions = pd.DataFrame()
    
    n_subs = len(fname_conv)
    for f in os.listdir(filedir):
        if (f.split('.')[1] == 'csv') & (f != condname):
            print("Data file read in: {}".format(f))
            
            dict_ac = {'raw_filename':f}
            for i in np.arange(n_subs):   
                if len(fname_conv[i]) > 0:
                    dict_ac = {**dict_ac,**{fname_conv[i]:f.split('_')[i]}}

            animal_conditions = animal_conditions.append(pd.DataFrame(dict_ac,index=[0]),ignore_index=True, sort=False)
            
    animal_conditions.to_csv(condname,index=False)