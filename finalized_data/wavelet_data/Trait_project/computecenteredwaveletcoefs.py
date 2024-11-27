#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 18:12:16 2024

@author: evan
"""

import numpy as np
import scipy
import pandas as pd
from ete3 import Tree 
import matplotlib.pyplot as plt

tree = Tree("/Users/evan/Downloads/projfiles/gtdb_tree.nw",format=1)


#Traverse the tree to collect internal node names
internalnodes=[]
i=0
for node in tree.traverse("postorder"):
    if not node.is_leaf():
        internalnodes.append(node.name)
        i=i+1
        
#Add the outrooting (corresponds to "scaling" wavelet)        
internalnodes.append("outroot")
        
        
trait_data=pd.read_csv('/Users/evan/Downloads/projfiles/trait_data.tsv',sep='\t') 
traits=trait_data.columns[1:]
trait_data = trait_data.drop('Unnamed: 0', axis=1)

#Mean-center each trait
trait_data_centered=trait_data.apply(lambda x: x-x.mean())


#Load wavelet transform
haarlike=scipy.sparse.load_npz('/Users/evan/Desktop/Trait_project/Haarlike.npz')

#Recover the wavelet coefficients for each centered trait
waveletcoefs_centered=np.zeros((11,50745))
i=0
for column in trait_data_centered.columns:
    if column !='Unnamed: 0':
        subdata=[]
        subdata.append(column)
        trait=trait_data_centered[column].values
        wavelet=haarlike@trait
        waveletcoefs_centered[i,:]=wavelet
        i=i+1


waveletcoefficients_centered=pd.DataFrame(data=waveletcoefs_centered, index=traits, columns=internalnodes)  


#Calculate explained variance for each trait
explained_variance=np.zeros((11,50745))
for i in range(11):
    percentages=[]
    #Sort the wavelet coefficients in descending order
    wavecoefssort=-np.sort(-abs(waveletcoefs_centered[i,:]))
    for j in range(50745):
        #Compute percent variance explained
        percentages.append(np.linalg.norm(wavecoefssort[0:j])/np.linalg.norm(trait_data_centered.iloc[:,i].values))
    explained_variance[i,:]=percentages
    
    
#Absolute value method you were doing 
explained_absval=np.zeros((11,50745))
for i in range(11):
    percentages=[]
    #Sort the wavelet coefficients in descending order
    wavecoefssort=-np.sort(-abs(waveletcoefs_centered[i,:]))
    for j in range(50745):
        #Compute percent variance explained
        percentages.append(np.sum(wavecoefssort[0:j])/np.sum(wavecoefssort))
    explained_absval[i,:]=percentages    
    
    
#Plot first 5000 coefficients     
for i in range(11):
    plt.plot(explained_variance[i,1:5000], label=traits[i])    
plt.xlabel("# of Wavelet Coefficients")
plt.ylabel('% Variance Explained')
plt.legend()

#Plot first 5000 coefficients     
for i in range(11):
    plt.plot(explained_variance[i,1:5000], label=traits[i])    
plt.xlabel("# of Wavelet Coefficients")
plt.ylabel('% Absolute Value Collected')
plt.legend()
    
    