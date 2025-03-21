import sys
import json
import pprint

import heatmap #type: ignore
import shares #type: ignore
import imbalances #type: ignore

file = sys.argv[1]

analysis = {}

openings = [
# ITALIAN GAME
# RUY LOPEZ
# SCANDINAVIAN DEFENSE
# QUEEN'S GAMBIT ACCEPTED
    ['e4', 'e5', 'Nf3', 'Nc6', 'Bc4'], 
    ['e4', 'e5', 'Nf3', 'Nc6', 'Bb5'],
    ['e4', 'd5', 'exd5', 'Qxd5'],
    ['d4', 'd5', 'c4', 'dxc4']
]

# HEATMAP ANALYSES
analysis['hmtr'] = heatmap.transit(file)
analysis['hmvc'] = heatmap.victim(file)
analysis['hmch'] = heatmap.checkandmates(file,'+')
analysis['hmcm'] = heatmap.checkandmates(file,'#')

# SHARES ANALYSES
analysis['shfi'] = shares.shares(file,'f')
analysis['shrn'] = shares.shares(file,'r')
analysis['shpc'] = shares.shares(file,'pc')
analysis['shca'] = shares.shares(file,'castle')

# IMBALANCES ANALYSES
analysis['imop'] = imbalances.byopening(file,openings)
analysis['imcd'] = imbalances.bycheckdifference(file)
analysis['immw'] = imbalances.bycheckmatequadrant(file,'w')
analysis['immb'] = imbalances.bycheckmatequadrant(file,'b')

pprint.pprint(analysis)

# WRITE ANALYSIS IN JSON FORMAT FOR FUTURE USE
analysisjson = json.dumps(analysis)

with open('analysis.json','w') as f:
    f.write(analysisjson)

'''

Each analysis is explained in depth in the report

hmtr -- Transit Heatmap
hmvc -- Victim Heatmap
hmch -- Checks Given Heatmap
hmcm -- Checkmates Heatmap

shfi -- File Shares
shrn -- Rank Shares
shpc -- Piece Shares
shca -- Castling Shares

imop -- Opening Imbalances
imcd -- Check Difference Imbalances
immw -- Checkmate Quadrant Imbalances (for white)
iimq -- Checkmate Quadrant Imbalances (for black)

'''


