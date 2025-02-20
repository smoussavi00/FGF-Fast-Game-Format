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
            if bfbyte & 12: ns = 0
        else:
        # ONLY WHITE MOVE EXTENDED -- NO TERMINATION 5 BYTES NEEDED -- YES TERMINATION 4 BYTES NEEDED
        # CHECK RESULT BITS FOR WHITE MOVE (2**4 * (2**3 + 2**4) = 192) -- IF CONDITION IS TRUE TERMINATE AT WHITE MOVE
            
            if bfbyte & 192: 
                fp.seek(start)
                bfbyte = int.from_bytes(fp.read(4), byteorder='big')
                w = bfbyte >> 4

                ns = -1

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
            if bfbyte & 12: ns = 0

        else:
        # NEITHER MOVE IS EXTENDED -- 3 BYTES NEEDED

            fp.seek(start)
            bfbyte = int.from_bytes(fp.read(3), byteorder='big')
            w = bfbyte >> 12
            b = bfbyte & (2**12-1)

            ns = 3

    return w,b,ns
    
def extensionc(m):
# EXTENSION CHECK -- TRUE IF EXTENDED -- FALSE OTHERWISE
    return m // 2**27

def capturec(m):
# CAPTURE CHECK -- TRUE IF CAPTURE -- FALSE OTHERWISE
    return m & 2**10 * ((2**16) ** extensionc(m))

def checkc(m):
# CHECK CHECK -- TRUE IF CHECK -- FALSE OTHERWISE
    return m & 2**9 * ((2**16) ** extensionc(m))

def squaregt(m):
# SQUARE GET -- RETURN DESTINATION SQUARE IN MOVE
    sq = (m & (2**6-1) * ((2**16) ** extensionc(m))) >> 16 * extensionc(m)
    return chr(sq//8+97) + str(sq%8+1)

def piecegt(m):
# PIECE GET -- RETURN PIECE IN MOVE
# CHECK PIECE BITS FOR MOVE (2**8 + 2**7 + 2**6 = 448)
    return ['O-O-O','O-O','','N','B','R','Q','K'][(m & 448 * ((2**16) ** extensionc(m))) >> 6 + 16 * extensionc(m)]

def piecevaluegt(pc,kingvalue=9):
# PIECE VALUE GET -- RETURN PIECE VALUE IN PIECE
    return {'':1,'N':3,'B':3,'R':5,'Q':9,'K':kingvalue}[pc]

'''
0,1 ->  (0/1) * 0 + (1/1) * pvgt(m), 1 + 1
4,3 ->  (2/3) * 4 + (1/3) * pvgt(m), 3 + 1

if piecegt(m) == 'O-O-O': -- UPDATE THE KING NEW SQUARE AND UPDATE THE ROOK NEW SQUARE
elif piecegt(m) == 'O-O': -- '' --
else: d[squaregt(m)] = (((d[squaregt(m)][1]-1)/d[squaregt(m)][1]) * d[squaregt(m)][0] + (1/d[squaregt(m)][1]) * piecevaluegt(m) , d[squaregt(m)][1]+1)

'''