import json 

import matplotlib.pyplot as plt

def plotshares(mode,jsonfile):

    colours = {
        3: ['darkblue', 'blue', '#879bff'],
        6: ['darkblue','blue','#3254fc','#879bff','#abb9ff','#d2d9fc'],
        8: ['midnightblue','mediumblue','blue','#3254fc','#6881fc','#879bff','#abb9ff','#d2d9fc']
    }

    with open(jsonfile,'r') as jsonf:
        data = json.load(jsonf)

    chessdata = data[f'sh{mode}']

    for e in range(3):

        plt.figure(figsize=(6, 6))
        plt.pie(chessdata[e], colors=colours[len(chessdata[e])])

        plt.axis("off")
        plt.savefig(f'sh{mode}-{e}.png', bbox_inches='tight', pad_inches=0)
