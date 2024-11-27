#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 19:55:35 2024

@author: evan
"""
#Smallest Greengenes tree with 22 leaves
tree = Tree("/Users/evan/Downloads/gg_13_8_otus 2/trees/61_otus_unannotated.tree",format=1)
allleaves=tree.get_leaves()

i=0 #ordering of nodes in post order traversal
for node in tree.traverse("postorder"):
    node.add_features(pos=find_matching_index(node,allleaves)) #store indices of leaves under each internal node

from ete3 import tree


[haarlike,pseudodiag]=sparsify(tree)
pseudodiag=pseudodiag.todense()
haarlike=haarlike.todense()

#Generate continuous [0,1]
#Divergence at internal node indices 19,11
trait1=np.array([0,0,0,0,0,0,0,0,0,0,.5,.5,.5,.5,.5,1,1,.5,.5,.5,.5,.5])
trait1noisy=trait1+np.random.multivariate_normal(np.zeros(22), .001*np.eye(22))
trait1noisy[trait1noisy>1]=1
trait1noisy[trait1noisy<0]=0


#Generate binary [0,1] (noise added manually)
#Divergence at internal node index 6
trait2=np.array([0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
trait2noisy=np.array([0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0])


#Generate continuous [0,5000]
#Divergence at internal node indices 11,6
trait3=np.array([3000,3000,3000,3000,3000,3000,1500,1500,3000,3000,3000,3000,3000,3000,3000,5000,5000,3000,3000,3000,3000,3000])
trait3noisy=trait3+np.random.multivariate_normal(np.zeros(22), 50000*np.eye(22))


data=np.vstack([trait1noisy,trait2noisy,trait3noisy])


trait_data=pd.DataFrame(data.T,columns=['Trait 1','Trait 2','Trait 3'])



