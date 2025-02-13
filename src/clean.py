import re 
import sys

def procm(m):

    n = 0
    ext = False

    if not m:
        pass
    if m[-1] == '#':
    # MATE (set extend flag)
        ext = True
        n += 2**27
        n += 2**15
        m = m[:-1]
    elif m[-1] == '+':
    # CHECK (set check flag, 11th position)
        n += 2**9
        m = m[:-1]
    if m == 'O-O-O':
    # QUEENSIDE CASTLE (piece 000)
        return n
    if m == 'O-O':
    # KINGSIDE CASTLE (piece 001)
        n += 2**6 * ((2**16) ** ext)
        return n
    if m[-2] == '=':
    # PROMOTION
        if not ext:
            ext = True
            n *= 2**16
            n += 2**27
        n += (['K','B','R','Q'].index(m[-1]) + 1) * 2**10
        m = m[:-2]
    
    # FIRST DETERMINE RANK
    # THEN DETERMINE FILE
    n += (int(m[-1]) - 1) * ((2**16) ** ext)
    n += (8 * (ord(m[-2]) - 97)) * ((2**16) ** ext)
    m = m[:-2]

    if not m:
    # PAWN
        n += 2**7 * ((2**16) ** ext)
        return n

    if m[-1] == 'x':
    # CAPTURE
        n += 2*10 * ((2**16) ** ext)
        m = m[:-1]
    
    if m[0] in ['N','B','R','Q','K']:
    # PIECE / KING
        n += (['N','B','R','Q','K'].index(m[0]) + 3) * (2**6) * ((2**16) ** ext)
        m = m[1:]
    else: 
    # PAWN
        n += 2**7 * ((2**16) ** ext)
    
    if not m:
        # [1 Extend] [1 Capture] [1 Check] [111 Piece] [111111 Position]
        s = bin(n)[2:].rjust(12, '0')
        print(f'main-12: {s[0]} {s[1]} {s[2]} {s[3:6]} {s[6:12]} {s[12:]}')
        return n
    
    # DISAMBIGUATION (set extend flag)
    if not ext:
        n *= 2**16
        n += 2**27
    if len(m) == 2:
    # DOUBLE DISAMBIGUATION
        n += 3 * 2**13
    elif m.isnumeric():
    # RANK DISAMBIGUATION
        n += 2 * 2**13
    else:
    # FILE DISAMBIGUATION
        n += 2**13

    return n
    
    
    
    

def clean_moves(fpo,moves):
# FIRST REMOVES ALL EVAL NOTATION (ellipsis, exclamation/quotation marks etc.)
# NEXT LOOP ITERATES THROUGH EACH TURN --- CONVERTS VIA procm ALL MOVES INTO BYTE REPRESENTATION

    moves = re.sub(r'[!?]', '', moves)
    moves = re.sub(r' \d+\.\.\.', '', moves)
    moves = re.sub(r' \{.*?\}', '', moves)

    parts = re.split(r'\b\w+\.', moves)[1:]

    for i in range(len(parts)):
        if i < len(parts)-1:
            x = procm(parts[i][0])
            y = procm(parts[i][1])
            fpo.write((2**(12+16*(y//(2**27))) * x + y).to_bytes(3 + x//(2**27) + y//(2**27),'big'))
        else:
            if len(parts[i]) == 2: parts[i][0].insert(1,'')
            fpo.write((2**12 * procm(parts[i][0]) + procm(parts[i][1])).to_bytes(3,'big'))
            fpo.write(procm(parts[i][-1]))

    return parts

def main():
# SCRIPT COMPRESSES LICHESS STANDARD DATASET - MORE NECESSARY ITEMS KEPT, MORE USEABLE

    file = sys.argv[1]
    
    fs = False
    buf = {}

    with open(file) as fp:
        with open("gen", "wb") as fpo:
            for line in fp:
                
                if not line.strip() and fs:
                    if buf['Termination'] in ['Normal','Time forfeit'] and 'Classical' in buf['Event'].split():

                        fpo.write(int(buf["WhiteElo"]).to_bytes(2,'big'))
                        fpo.write(int(buf["BlackElo"]).to_bytes(2,'big'))
                        fpo.write((int(buf["TimeControl"].split('+')[0])//60).to_bytes(1,'big'))
                        fpo.write(int(buf["TimeControl"].split('+')[1]).to_bytes(1,'big'))
                        clean_moves(fpo,buf['the-moves'])

                        break

                    fs = False
                    buf = {}
                elif not line.strip() and not fs:
                    fs = True
                else:
                    if not fs: 
                        s = (line.strip()[1:-1]).split(" ",1)
                        buf[s[0]] = s[1][1:-1]
                    else: buf['the-moves'] = line.strip()
                            


if __name__ == "__main__":
    main()


'''

EXAMPLES: Qhxg7# | g7#

2 x 12 BITS > 3By

[1 Extend] [1 Capture] [1 Check] [111 Piece] [111111 Position]

6 - Position
3 - Piece
1 - Capture
1 - Check
1 - Extend


EXTEND IN CASES OF:
    - Disambiguation
    - Promotion
    - Checkmate

16 BITS > 2By

1 - Checkmate
2 - Disambiguation Type (none, file, rank, both)
3 - Promotion Type (none, queen, rook, bishop or knight)
6 - Position

[1 Checkmate] [11 Disambiguation] [111 Promotion] [111111 Original Position -- for disambiguation] 

'''