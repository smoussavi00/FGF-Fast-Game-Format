import re 
import sys

def procm(m,rs=None,only=False):

    n = 0
    ext = False

    if rs in [-1,0,1]:
    # FINAL MOVE -- EXTEND AND ENCODE RESULT 
        ext = True
        n += 2**27
        n += (rs+3) * (2**2)    
    if m[-1] == '#':
    # MATE (set extend flag)
        if not ext:
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
        n += (['N','B','R','Q'].index(m[-1]) + 1) * 2**10
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
        n += 2**10 * ((2**16) ** ext)
        m = m[:-1]
    
    if m[0] in ['N','B','R','Q','K']:
    # PIECE / KING
        n += (['N','B','R','Q','K'].index(m[0]) + 3) * (2**6) * ((2**16) ** ext)
        m = m[1:]
    else: 
    # PAWN
        n += 2**7 * ((2**16) ** ext)
    
    if only: n *= 2**4
    if not m: return n
    
    # DISAMBIGUATION (set extend flag)
    if not ext:
        n *= 2**16
        n += 2**27
    if len(m) == 2:
    # DOUBLE DISAMBIGUATION
        n += (int(m[-1]) - 1) * (2**4)
        n += (8 * (ord(m[-2]) - 97)) * (2**4)
        n += 3 * 2**13
    elif m.isnumeric():
    # RANK DISAMBIGUATION
        n += (int(m) - 1) * (2**4)
        n += 2 * 2**13
    else:
    # FILE DISAMBIGUATION
        n += (8 * (ord(m) - 97)) * (2**4)
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
        a = parts[i].split()[0]

        if i < len(parts)-1:
            b = parts[i].split()[1]
            x = procm(a)
            y = procm(b)
            fpo.write((2**(12+16*(y//(2**27))) * x + y).to_bytes(3 + 2*(x//(2**27)) + 2*(y//(2**27)),'big'))
        else:
            c = parts[i].split()[-1]
            rs = (['0-1','1/2-1/2','1-0'].index(c)) - 1
            if len(parts[i].split()) == 3:
                b = parts[i].split()[1] 
                x = procm(a)
                y = procm(b,rs)
                fpo.write((2**(12+16*(y//(2**27))) * x + y).to_bytes(3 + 2*(x//(2**27)) + 2*(y//(2**27)),'big'))
            else:
                x = procm(a,rs,True)
                fpo.write(x.to_bytes(4,'big'))

    return parts

def main():
# SCRIPT COMPRESSES LICHESS STANDARD DATASET - MORE NECESSARY ITEMS KEPT, MORE USEABLE

    file = sys.argv[1]
    
    fs = False
    buf = {}
    i = 0
    with open(file) as fp:
        with open("gen", "wb") as fpo:
            for line in fp:
                
                if not line.strip() and fs:
                    if buf['Termination'] in ['Normal','Time forfeit'] and 'Classical' in buf['Event'].split() and (buf["WhiteElo"].isnumeric() and buf["BlackElo"].isnumeric()):
                        
                        fpo.write(int(buf["WhiteElo"]).to_bytes(2,'big'))
                        fpo.write(int(buf["BlackElo"]).to_bytes(2,'big'))
                        fpo.write((int(buf["TimeControl"].split('+')[0])//60).to_bytes(1,'big'))
                        fpo.write(int(buf["TimeControl"].split('+')[1]).to_bytes(1,'big'))
                        clean_moves(fpo,buf['the-moves'])
                        
                        i += 1
                        if i % 50000 == 0: print(i) 
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
    - Last Move

16 BITS > 2By

1 - Checkmate
2 - Disambiguation Type (none, file, rank, both)
3 - Promotion Type (none, queen, rook, bishop or knight)
6 - Position

[1 Checkmate] [11 Disambiguation] [111 Promotion] [111111 Original Position -- for disambiguation] [11 Result] [11 NIL]

# THIRTEEN AND FOURTEENTH BITS DETERMINE RESULT

'''