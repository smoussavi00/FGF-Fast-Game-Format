import copy
import math

import afunctions # type: ignore
import clean #type: ignore
# from .. import clean 

def byopening(file,openings):
# CALCULATE AVERAGE MATERIAL IMBALANCE BY OPENINGS

    nop = len(openings)
    proops = [afunctions.procop(op) for op in openings]
    byop = [[(0,1),(0,1),(0,1)] for i in range(nop)]

    d2 = afunctions.dinit()
    
    skip = 6
            
    with open(file, "rb") as f:

        fpos = skip
        x = -1

        while True:

            f.seek(fpos)
            if not f.read(1): break

            enpassantsq = ''
            d2 = afunctions.dinit()

            wm = 39
            bm = 39

            imb = []
            opmatch = -1
            x += 1

            ops = copy.deepcopy(proops)

            while True:

                w,b,ns,t = afunctions.extract(f,fpos)

                for i in range(len(ops)):
                    if not ops[i]: continue
                    
                    if ops[i][0] == w or (afunctions.resultgt(w) and ops[i][0] == (w>>20)-2*11):
                        ops[i].pop(0)
                        if not ops[i]:
                            opmatch = i
                            break
                    else: ops[i] = []
                
                wp = afunctions.piecegt(w)
                wsq = afunctions.squaregt(w)

                if afunctions.capturec(w):
                    if not wp and enpassantsq and wsq == enpassantsq[0]+str(int(enpassantsq[1])+1): 
                        bm -= 1
                    else: bm -= afunctions.piecevaluegt(d2[wsq])
                
                if wp == 'O-O-O':
                    d2['d1'] = 'R'
                    d2['c1'] = 'K'

                elif wp == 'O-O':
                    d2['f1'] = 'R'
                    d2['g1'] = 'K'

                elif afunctions.promotiongt(w):
                    d2[wsq] = afunctions.promotiongt(w)[1]
                    wm += afunctions.piecevaluegt(afunctions.promotiongt(w)[1])-1

                else:
                    d2[wsq] = wp

                if not wp and not afunctions.capturec(w): enpassantsq = wsq
                else: enpassantsq = ''

                if t < 2:

                    for i in range(len(ops)):
                        if not ops[i]: continue
                        if ops[i][0] == b or (afunctions.resultgt(b) and ops[i][0] == (b>>16)-2*11):
                            ops[i].pop(0)
                            if not ops[i]:
                                opmatch = i
                                break
                        else: ops[i] = []
                    
                    bp = afunctions.piecegt(b)
                    bsq = afunctions.squaregt(b)

                    if afunctions.capturec(b):
                        if not bp and enpassantsq and bsq == enpassantsq[0]+str(int(enpassantsq[1])-1): 
                            wm -= 1
                        else: wm -= afunctions.piecevaluegt(d2[bsq])
                        
                    if bp == 'O-O-O':
                        d2['d8'] = 'R'
                        d2['c8'] = 'K'

                    elif bp == 'O-O':
                        d2['f8'] = 'R'
                        d2['g8'] = 'K'

                    elif afunctions.promotiongt(b):
                        d2[bsq] = afunctions.promotiongt(b)[1]
                        bm += afunctions.piecevaluegt(afunctions.promotiongt(b)[1])-1

                    else:
                        d2[bsq] = bp

                    if not bp and not afunctions.capturec(b): enpassantsq = bsq
                    else: enpassantsq = ''

                    imb.append(abs(wm-bm))

                fpos += ns
            
                if t:
                    fpos += skip
                    break
            
            n = len(imb)//3
            m = len(imb)//3 + len(imb) % 3

            if n > 0:
                imbalances = [sum(imb[:n])/n,sum(imb[n:n+m])/m,sum(imb[n+m:])/n]
                if opmatch > -1:
                    for i in range(3): byop[opmatch][i] = ((byop[opmatch][i][1]-1)/(byop[opmatch][i][1])*byop[opmatch][i][0]+1/byop[opmatch][i][1]*imbalances[i],byop[opmatch][i][1]+1)

    return [[val[0] for val in sublist] for sublist in byop]

def bycheckdifference(file):
# CALCULATE AVERAGE MATERIAL IMBALANCE BY CHECK DIFFERENCE
# CHECK DIFFERENCE > 0 : WHITE HAS GIVEN MORE CHECKS THAN BLACK
# CHECK DIFFERENCE < 0 : BLACK HAS GIVEN MORE CHECKS THAN WHITE
# CHECK DIFFERENCE = 0 : WHITE AND BLACK GAVE EQUAL CHECKS

    bychd = [[(0,1),(0,1),(0,1)] for i in range(8)]

    d2 = afunctions.dinit()
    
    skip = 6
            
    with open(file, "rb") as f:

        fpos = skip
        x = -1

        while True:

            f.seek(fpos)
            if not f.read(1): break

            enpassantsq = ''
            d2 = afunctions.dinit()

            wm = 39
            bm = 39

            imb = []
            chd = 0
            x += 1

            while True:

                w,b,ns,t = afunctions.extract(f,fpos)

                if afunctions.checkc(w) or afunctions.checkmatec(w):
                    chd += 1
                
                wp = afunctions.piecegt(w)
                wsq = afunctions.squaregt(w)

                if afunctions.capturec(w):
                    if not wp and enpassantsq and wsq == enpassantsq[0]+str(int(enpassantsq[1])+1): 
                        bm -= 1
                    else: bm -= afunctions.piecevaluegt(d2[wsq])
                
                if wp == 'O-O-O':
                    d2['d1'] = 'R'
                    d2['c1'] = 'K'

                elif wp == 'O-O':
                    d2['f1'] = 'R'
                    d2['g1'] = 'K'

                elif afunctions.promotiongt(w):
                    d2[wsq] = afunctions.promotiongt(w)[1]
                    wm += afunctions.piecevaluegt(afunctions.promotiongt(w)[1])-1

                else:
                    d2[wsq] = wp

                if not wp and not afunctions.capturec(w): enpassantsq = wsq
                else: enpassantsq = ''

                if t < 2:

                    if afunctions.checkc(b) or afunctions.checkmatec(b):
                        chd -= 1
                    
                    bp = afunctions.piecegt(b)
                    bsq = afunctions.squaregt(b)

                    if afunctions.capturec(b):
                        if not bp and enpassantsq and bsq == enpassantsq[0]+str(int(enpassantsq[1])-1): 
                            wm -= 1
                        else: wm -= afunctions.piecevaluegt(d2[bsq])
                        
                    if bp == 'O-O-O':
                        d2['d8'] = 'R'
                        d2['c8'] = 'K'

                    elif bp == 'O-O':
                        d2['f8'] = 'R'
                        d2['g8'] = 'K'

                    elif afunctions.promotiongt(b):
                        d2[bsq] = afunctions.promotiongt(b)[1]
                        bm += afunctions.piecevaluegt(afunctions.promotiongt(b)[1])-1

                    else:
                        d2[bsq] = bp

                    if not bp and not afunctions.capturec(b): enpassantsq = bsq
                    else: enpassantsq = ''

                    imb.append(abs(wm-bm))

                fpos += ns
            
                if t:
                    fpos += skip
                    break
            
            n = len(imb)//3
            m = len(imb)//3 + len(imb) % 3

            if n > 0:
                imbalances = [sum(imb[:n])/n,sum(imb[n:n+m])/m,sum(imb[n+m:])/n]
                chdmatch = min(math.ceil((max(0,chd+9))/3),7)
                
                for i in range(3): bychd[chdmatch][i] = ((bychd[chdmatch][i][1]-1)/(bychd[chdmatch][i][1])*bychd[chdmatch][i][0]+1/bychd[chdmatch][i][1]*imbalances[i],bychd[chdmatch][i][1]+1)
   
    return [[val[0] for val in sublist] for sublist in bychd]

def bycheckmatequadrant(file,mode):
# CALCULATE AVERAGE MATERIAL IMBALANCE BY CHECKMATE QUADRANTS (if there was a checkmate)
# QUADRANT NUMBER CALCULATED IN afunction.py VIA quadrantgt

    bycmq = [[(0,1),(0,1),(0,1)] for i in range(4)]

    d2 = afunctions.dinit()
    
    skip = 6
            
    with open(file, "rb") as f:

        fpos = skip
        x = -1

        while True:

            f.seek(fpos)
            if not f.read(1): break

            enpassantsq = ''
            d2 = afunctions.dinit()

            wm = 39
            bm = 39

            imb = []
            cmq = -1
            x += 1

            while True:

                w,b,ns,t = afunctions.extract(f,fpos)
                
                wp = afunctions.piecegt(w)
                wsq = afunctions.squaregt(w)

                if mode == 'w' and afunctions.checkmatec(w):
                    cmq = afunctions.quadrantgt(w)

                if afunctions.capturec(w):
                    if not wp and enpassantsq and wsq == enpassantsq[0]+str(int(enpassantsq[1])+1): 
                        bm -= 1
                    else: bm -= afunctions.piecevaluegt(d2[wsq])
                
                if wp == 'O-O-O':
                    d2['d1'] = 'R'
                    d2['c1'] = 'K'

                elif wp == 'O-O':
                    d2['f1'] = 'R'
                    d2['g1'] = 'K'

                elif afunctions.promotiongt(w):
                    d2[wsq] = afunctions.promotiongt(w)[1]
                    wm += afunctions.piecevaluegt(afunctions.promotiongt(w)[1])-1

                else:
                    d2[wsq] = wp

                if not wp and not afunctions.capturec(w): enpassantsq = wsq
                else: enpassantsq = ''

                if t < 2:

                    if mode == 'b' and afunctions.checkmatec(b):
                        cmq = afunctions.quadrantgt(b)
                    
                    bp = afunctions.piecegt(b)
                    bsq = afunctions.squaregt(b)

                    if afunctions.capturec(b):
                        if not bp and enpassantsq and bsq == enpassantsq[0]+str(int(enpassantsq[1])-1): 
                            wm -= 1
                        else: wm -= afunctions.piecevaluegt(d2[bsq])
                        
                    if bp == 'O-O-O':
                        d2['d8'] = 'R'
                        d2['c8'] = 'K'

                    elif bp == 'O-O':
                        d2['f8'] = 'R'
                        d2['g8'] = 'K'

                    elif afunctions.promotiongt(b):
                        d2[bsq] = afunctions.promotiongt(b)[1]
                        bm += afunctions.piecevaluegt(afunctions.promotiongt(b)[1])-1

                    else:
                        d2[bsq] = bp

                    if not bp and not afunctions.capturec(b): enpassantsq = bsq
                    else: enpassantsq = ''

                    imb.append(abs(wm-bm))

                fpos += ns
            
                if t:
                    fpos += skip
                    break
            
            n = len(imb)//3
            m = len(imb)//3 + len(imb) % 3

            if n > 0:
                imbalances = [sum(imb[:n])/n,sum(imb[n:n+m])/m,sum(imb[n+m:])/n]
                
                if cmq > -1:
                    for i in range(3): bycmq[cmq][i] = ((bycmq[cmq][i][1]-1)/(bycmq[cmq][i][1])*bycmq[cmq][i][0]+1/bycmq[cmq][i][1]*imbalances[i],bycmq[cmq][i][1]+1)
   
    return [[val[0] for val in sublist] for sublist in bycmq]