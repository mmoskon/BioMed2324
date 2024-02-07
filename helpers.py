import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

myColors = ((53/255, 96/255, 149/255, 1.0), (1.0, 1.0, 1.0, 1.0), (167/255, 56/255, 44/255, 1.0))
cmap = LinearSegmentedColormap.from_list('Custom', myColors, len(myColors))

# a function for calculating adjusted p-values according to Benjamini-Hochberg procedure
# could install statsmodels and use statsmodels.stats.multitest instead
# adapted from https://stackoverflow.com/questions/7450957/how-to-implement-rs-p-adjust-in-python/33532498#33532498
def bh(pvalues):
    pvalues = np.array(pvalues)
    n = len(pvalues)
    new_pvalues = np.zeros(n)
    
    values = [(pvalue, i) for i, pvalue in enumerate(pvalues) ]                                      
    values.sort(reverse=True)
    new_values = []
    for i, vals in enumerate(values):                                                                 
        rank = n - i
        pvalue, index = vals                                                                          
        new_values.append((n/rank) * pvalue)                                                          
    for i in range(0, int(n)-1):  
        if new_values[i] < new_values[i+1]:                                                           
            new_values[i+1] = new_values[i]                                                           
    for i, vals in enumerate(values):
        pvalue, index = vals
        new_pvalues[index] = new_values[i]                                                                                                                  
    return new_pvalues

def make_plot(df, enrichment_folder, file_name):
    ax1 = sns.heatmap(df, 
                cmap=cmap, 
                vmin=-1,
                vmax=1,
                yticklabels=True, 
                cbar=False,
                cbar_kws={'ticks': [-1, 0, 1], 'tickslabels':['down-regulated', 'unchanged', 'up-regulated']},
                linewidths = 2)
    cbar = ax1.figure.colorbar(ax1.collections[0])
    cbar.set_ticks([-1, 0, 1])
    cbar.set_ticklabels(['down-regulated', 'unchanged', 'up-regulated'])

    

    ax1.xaxis.set_ticks_position('top')

    #for item in ax1.get_yticklabels():
    #    item.set_rotation(30)

    for item in ax1.get_xticklabels():
        item.set_rotation(90)
    
    fig = plt.gcf()
    x,y = fig.get_size_inches()
    
    fig.set_size_inches(5,(df.shape[0]/90)*20)
    
    ax1.set_ylabel("")
    
    plt.savefig(enrichment_folder+'\\'+file_name+'.pdf', bbox_inches = 'tight')  
    plt.show()
    