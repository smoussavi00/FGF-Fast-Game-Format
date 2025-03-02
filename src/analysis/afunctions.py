import ../clean.py

def extract(fp,start):
# GETS MOVE(S) FROM FAST-DATASET FILE
# RETURNS WHITE MOVE, RETURNS BLACK MOVE (IF THERE IS ONE), AND RETURNS SEEK INCREMENT 
    
    '''
    b - black move 
    w - white move
    ns - next seek increment ()
    '''

    b = -1
    w = -1
    ns = -1
    t = 0

    fp.seek(start)
    bfbyte = int.from_bytes(fp.read(1), byteorder='big')

    if bfbyte & 128:
    # WHITE MOVE EXTENSION FLAGGED -- 4 BYTES TO READ GUARANTEED

        fp.seek(start)
        bfbyte = int.from_bytes(fp.read(4), byteorder='big')

        if bfbyte & 8:
        # BOTH MOVES EXTENDED -- 7 BYTES NEEDED
        # CHECK RESULT BITS FOR BLACK MOVE (2**3 + 2**4 = 12) -- IF CONDITION IS TRUE TERMINATE AT BLACK MOVE

            fp.seek(start)
            bfbyte = int.from_bytes(fp.read(7), byteorder='big')
            w = bfbyte >> 28
            b = bfbyte & (2**28-1)

            ns = 7
            if bfbyte & 12: t = 1
        else:
        # ONLY WHITE MOVE EXTENDED -- NO TERMINATION 5 BYTES NEEDED -- YES TERMINATION 4 BYTES NEEDED
        # CHECK RESULT BITS FOR WHITE MOVE (2**4 * (2**3 + 2**4) = 192) -- IF CONDITION IS TRUE TERMINATE AT WHITE MOVE
            
            if bfbyte & 192: 
                fp.seek(start)
                bfbyte = int.from_bytes(fp.read(4), byteorder='big')
                w = bfbyte >> 4

                ns = 4
                t = 2

            else:
                fp.seek(start)
                bfbyte = int.from_bytes(fp.read(5), byteorder='big')
                w = bfbyte >> 12
                b = bfbyte & (2**12-1)

                ns = 5
    
    else:
        fp.seek(start)
        bfbyte = int.from_bytes(fp.read(2), byteorder='big')

        if bfbyte & 8:
        # ONLY BLACK MOVE EXTENDED -- 5 BYTES NEEDED
        # CHECK RESULT BITS FOR BLACK MOVE (2**3 + 2**4 = 12) -- IF CONDITION IS TRUE TERMINATE AT BLACK MOVE
            fp.seek(start)
            bfbyte = int.from_bytes(fp.read(5), byteorder='big')
            w = bfbyte >> 28
            b = bfbyte & (2**28-1)

            ns = 5
            if bfbyte & 12: t = 1

        else:
        # NEITHER MOVE IS EXTENDED -- 3 BYTES NEEDED

            fp.seek(start)
            bfbyte = int.from_bytes(fp.read(3), byteorder='big')
            w = bfbyte >> 12
            b = bfbyte & (2**12-1)

            ns = 3

    return w,b,ns,t
    
def extensionc(m):
# EXTENSION CHECK -- TRUE IF EXTENDED -- FALSE OTHERWISE
    return m // 2**27

def capturec(m):
# CAPTURE CHECK -- TRUE IF CAPTURE -- FALSE OTHERWISE
    return m & 2**10 * ((2**16) ** extensionc(m))

def checkc(m):
# CHECK CHECK -- TRUE IF CHECK -- FALSE OTHERWISE
    return m & 2**9 * ((2**16) ** extensionc(m))

def checkmatec(m):
# CHECKMATE CHECK -- TRUE IF CHECKMATE -- FALSE OTHERWISE
    return extensionc(m) * (m & 2**15)

def piecegt(m):
# PIECE GET -- RETURN PIECE IN MOVE
# CHECK PIECE BITS FOR MOVE (2**8 + 2**7 + 2**6 = 448)
    return ['O-O-O','O-O','','N','B','R','Q','K'][(m & 448 * ((2**16) ** extensionc(m))) >> 6 + 16 * extensionc(m)]

def squaregt(m):
# SQUARE GET -- RETURN DESTINATION SQUARE IN MOVE
    sq = (m & (2**6-1) * ((2**16) ** extensionc(m))) >> 16 * extensionc(m)
    return chr(sq//8+97) + str(sq%8+1)

def disambiguationgt(m):
# DISAMBIGUATION GET -- RETURN DISAMBIGUATION
# CHECK DISAMBIGUATION CASE BITS (2**13 + 2**14 = 24576)
# RETURN DISAMBIGUATION BASED ON DISAMBIGUATION CASE
    dca = (m & 24576) >> 13
    if not dca or not extensionc(m): return ''
    elif dca == 1: return squaregt((m >> 4) & (2**6-1))[0]
    elif dca == 2: return squaregt((m >> 4) & (2**6-1))[1]
    return squaregt((m >> 4) & (2**6-1))

def promotiongt(m):
# PROMOTION GET -- RETURN PROMOTION
# CHECK PROMOTION BITS (2**10 + 2**11 + 2**12 = 7168)
    pro = (m & 7168) >> 10
    if not pro or not extensionc(m): return ''
    return ['=N','=B','=R','=Q'][pro-1]

def resultgt(m):
# RESULT GET -- RETURN RESULT
# CHECK RESULT BITS (2**2 + 2**3 = 12)
    res = (m & 12) >> 2
    if not res or not extensionc(m): return ''
    return ['0-1','1/2-1/2','1-0'][res-1]

def piecevaluegt(pc,kingvalue=9):
# PIECE VALUE GET -- RETURN PIECE VALUE IN PIECE
    return {'':1,'N':3,'B':3,'R':5,'Q':9,'K':kingvalue}[pc]

def dinit():
    d = {f'{f}{r}': '-' for f in [chr(i) for i in range(97,105)] for r in range(1, 9)}

    for sq in d:
        if sq in [f'{f}{r}' for f in [chr(i) for i in range(97,105)] for r in [2,7]]: d[sq] = ''
        elif sq in ['b1','b8','g1','g8']: d[sq] = 'N'
        elif sq in ['c1','c8','f1','f8']: d[sq] = 'B'
        elif sq in ['a1','a8','h1','h8']: d[sq] = 'R'
        elif sq in ['d1','d8']: d[sq] = 'Q'
        elif sq in ['e1','e8']: d[sq] = 'K'

    return d

def procop(op):
    # PROCESS OPENING

    opr = []
    for m in op:
        opr.append(clean.procm(m))
    
    return opr
