import json 

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
import scipy.stats as stats

def plotheatmap(mode,jsonfile):

    with open(jsonfile,'r') as jsonf:
        data = json.load(jsonf)

    chessdata = data[f'hm{mode}']

    board_values = np.zeros((8, 8))
    normalized = normalize(chessdata)

    for square, value in chessdata.items():
        file, rank = ord(square[0])-97, int(square[1])-1
        board_values[7 - rank, file] = normalized[8*file+rank]

    custom_cmap = mcolors.LinearSegmentedColormap.from_list(
    "custom_heatmap", [ "black", "maroon", "darkred", "firebrick", "red", "orangered", "orangered", "darkorange", "orange", "yellow", "white" ], N=256
    )

    bounds = [-2.2, -1.9, -1.7, -1.5, -1.3, -1.1, -0.9, -0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.2]

    norm = mcolors.BoundaryNorm(bounds, custom_cmap.N)

    fig, ax = plt.subplots(figsize=(6, 6))
    cax = ax.matshow(board_values, cmap=custom_cmap, norm=norm) 
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)

    plt.savefig(f'hm{mode}.png', bbox_inches='tight', pad_inches=0)

    cbar = plt.colorbar(cax, ticks=bounds)
    cbar.ax.set_yticklabels([str(b) for b in bounds]) 

    plt.savefig(f'hm{mode}-vals.png', bbox_inches='tight', pad_inches=0)

def normalize(data):

    values = [data[i] for i in data] 
    ranks = stats.rankdata(values) / (len(values) + 1)
    return stats.norm.ppf(ranks)