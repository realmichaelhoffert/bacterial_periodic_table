import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.transforms import ScaledTranslation
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as plticker
import matplotlib.colors as mc
import colorsys

def tufte_box(data, x, y, sort=True, hue=None, kwargs={}):    
    
    q1_func = lambda x: np.quantile(x, 0.25)
    q3_func = lambda x: np.quantile(x, 0.75)
    plotdf = data.groupby(x)[y].agg(Median=np.median, Max=max, Min=min, Q1=q1_func, Q3=q3_func)
    
    if type(sort) == bool:
        if sort:
            plotdf = plotdf.sort_values('Median')
    else:
        plotdf = plotdf.reindex(sort)
        
    sns.scatterplot(data=plotdf, x=x, y='Median', color='white', zorder=2, linewidth=1, edgecolor='k')
    
    index_int = 0
    for index, row in plotdf.iterrows():
        plt.plot([index_int,index_int], [row.loc['Q3'], row.loc['Max']], zorder=1, linewidth=1, color='k')
        plt.plot([index_int,index_int], [row.loc['Min'], row.loc['Q1']], zorder=1, linewidth=1, color='k')
        plt.plot([index_int,index_int], [row.loc['Q1'], row.loc['Q3']], zorder=0, linewidth=3, color='k')
        index_int += 1
    
    # general formatting
    xticks = plt.xticks(rotation=70, ha='right')
    
    plt.tick_params(labelsize=14)
    plt.ylabel(y, fontsize=16)
    plt.xlabel(x, fontsize=16)
    sns.despine()
    
def fix_rotation(fig, ax):
    # reformat x labels to improve readability
    dx, dy = 5, 0
    offset = ScaledTranslation(dx/fig.dpi, dy/fig.dpi, scale_trans=fig.dpi_scale_trans)

    # apply offset transform to all xticklabels
    for label in ax.xaxis.get_majorticklabels():
        label.set_transform(label.get_transform() + offset)
        
def reorder_by_phylum(md_df, y):
    phylum_order = pd.Series(pd.Categorical(md_df['Phylum'].values, md_df.groupby('Phylum')[y].agg(Median=np.median).sort_values('Median').index, ordered=True))
    return md_df.assign(phylum_cat=phylum_order.values).sort_values('phylum_cat')

def watermark(text, ax):
    ax.annotate(text, (0,0), fontsize=50, alpha=0.25, color='gray', rotation=30)
    
def adjust_lightness(color, amount=0.5):

    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])

def phylo_dist_rugplot(fig, ax, distance_dict):
    # sns.rugplot(genus_dist_series)
    rug_y = -0.125
    annot_y = 0.75
    keys = ['Genus', 'Family', 'Order', 'Class', 'Phylum']
    rug_palette = sns.color_palette('Greys', 5)
    
    for key, c in zip(keys, rug_palette):
        ax.vlines(x=[distance_dict[key].mean()], ymin=0, ymax=0.7, color=[c], zorder=0, alpha=0.65)
        ax.annotate(key, xy=(distance_dict[key].mean(), 0.71), rotation=45) 
                    # xytext=(dist_dict[key].mean(), annot_y), 
                    # arrowprops={'arrowstyle':'->'}, ha='center')
        sns.scatterplot(x=distance_dict[key], y=rug_y, marker='|', linewidth=0.5, alpha=0.65, color=c)
        rug_y += 0.025
        annot_y += 0.025