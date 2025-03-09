import afunctions  # type: ignore
import math



pros = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
prorf = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
procastle = [[0,0,0],[0,0,0],[0,0,0]] 

pc = ['','N','B','R','Q','K']

def shares(file,mode):
# SHARE OF MOVEMENTS -- BROKEN DOWN BY ELO RANGE 0 - 1499 , 1500 - 1999 , 2000+
# (if mode == 'r') PARSE EACH MOVE FOR ITS RANK -- CASTLING IGNORED -- INCREMENT RANK TALLY 
# (if mode == 'f') PARSE EACH MOVE FOR ITS FILE -- CASTLING IGNORED -- INCREMENT FILE TALLY 
# (if mode == 'pc') PARSE EACH MOVE FOR ITS PIECE -- CASTLING IGNORED -- INCREMENT PIECE TALLY 
# (if mode == 'castle') ANALYZE EACH GAME -- INCREMENT QUEENSIDE CASTLE TALLY, KINGSIDE CASTLE TALLY, OR NO CASTLE TALLY
    
    rf = []
    s = []
    castle = []

    if mode == 'r' or mode == 'f': rf = prorf.copy()
    elif mode == 'pc': s = pros.copy()
    elif mode == 'castle': castle = procastle.copy()

    skip = 6

    with open(file, "rb") as f:

        fpos = 0
        
        while True:

            f.seek(fpos)
            if not f.read(1): break
            f.seek(fpos)

            welo = int.from_bytes(f.read(2), byteorder='big')
            belo = int.from_bytes(f.read(2), byteorder='big')
            fpos += skip

            while True:

                w,b,ns,t = afunctions.extract(f,fpos)
                wcastle = 0
                bcastle = 0

                if mode == 'r' or mode == 'f': wsq = afunctions.squaregt(w)
                wp = afunctions.piecegt(w)

                if mode == 'f' and wp in pc: rf[afunctions.elogroup(welo)][ord(wsq[0])-97] += 1
                elif mode == 'r' and wp in pc: rf[afunctions.elogroup(welo)][int(wsq[1])-1] += 1
                elif mode == 'pc' and wp in pc: s[afunctions.elogroup(welo)][pc.index(wp)] += 1
                elif mode == 'castle' and (wp == 'O-O-O' or wp == 'O-O'): 
                    castle[afunctions.elogroup(welo)][-(len(wp)//5)+2] += 1
                    wcastle = 1

                if t < 2:

                    if mode == 'r' or mode == 'f': bsq = afunctions.squaregt(b)
                    bp = afunctions.piecegt(b)

                    if mode == 'f' and bp in pc: rf[afunctions.elogroup(belo)][ord(bsq[0])-97] += 1
                    elif mode == 'r' and bp in pc: rf[afunctions.elogroup(belo)][int(bsq[1])-1] += 1
                    elif mode == 'pc' and bp in pc: s[afunctions.elogroup(belo)][pc.index(bp)] += 1
                    elif mode == 'castle' and (bp == 'O-O-O' or bp == 'O-O'): 
                        castle[afunctions.elogroup(belo)][-(len(bp)//5)+2] += 1
                        bcastle = 1

                fpos += ns
            
                if t:
                    if mode == 'castle' and not wcastle: castle[afunctions.elogroup(welo)][0] += 1
                    elif mode == 'castle' and not bcastle: castle[afunctions.elogroup(belo)][0] += 1
                    break
        
        return [[math.floor(j/sum(i) * 10000) / 100.0 for j in i] for i in {'f':rf, 'r':rf, 'pc':s, 'castle':castle}[mode]]