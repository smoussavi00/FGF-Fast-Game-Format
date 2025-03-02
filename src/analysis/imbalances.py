import afunctions # type: ignore
import clean #type: ignore
# from .. import clean 

'''
Imbalances by opening
Imbalances by check concentration
Imbalances by checkmate quadrant black
Imbalances by checkmate quadrant white
'''

def byopening(file,openings):
# CALCULATE AVERAGE MATERIAL IMBALANCE BY OPENINGS

    nop = len(openings)
    proops = [afunctions.procop(op) for op in openings]
    byop = [[(0,1),(0,1),(0,1)] for i in range(nop)]

    d2 = afunctions.dinit()
    
    skip = 6
            
    with open(file, "rb") as f:

        fpos = skip

        while True:

            f.seek(fpos)
            if not f.read(1): break

            enpassantsq = ''

            wm = 39
            bm = 39

            imb = []
            opmatch = -1

            ops = proops.copy()

            while True:

                w,b,ns,t = afunctions.extract(f,fpos)

                for i in range(len(ops)):
                    if not ops[i]: continue
                    if ops[i][0] == w or (afunctions.resultgt(w) and ops == (w>>16)-2*11):
                        if len(ops[i]) == 1:
                            opmatch = i
                            break
                        else: ops[i].pop(0)
                    else: ops[i] = []
                
                wp = afunctions.piecegt(w)
                wsq = afunctions.squaregt(w)

                if afunctions.capturec(w):
                    if not wp and enpassantsq and wsq == enpassantsq[0]+str(int(enpassantsq[1])+1): 
                        bm -= 1
                    else: bm -= d2[wsq]
                
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
                        if ops[i][0] == b or (afunctions.resultgt(b) and ops == (b>>16)-2*11):
                            if len(ops[i]) == 1:
                                opmatch = i
                                ops = []
                                break
                            else: ops[i].pop(0)
                        else: ops[i] = []
                    
                    bp = afunctions.piecegt(b)
                    bsq = afunctions.squaregt(b)

                    if afunctions.capturec(b):
                        if not bp and enpassantsq and bsq == enpassantsq[0]+str(int(enpassantsq[1])-1): 
                            wm -= 1
                        else: wm -= d2[bsq]
                        
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
        imbalances = [sum(imb[:n])/n,sum(imb[n:n+m]/(n+m),sum(imb[n+m:]/n))]
        if opmatch > -1:
            for i in range(3): byop[opmatch][i] = ((byop[opmatch][i][1]-1)/(byop[opmatch][i][1])*byop[opmatch][i][0]+1/byop[opmatch][i][1]*imbalances[i],byop[opmatch][i][1]+1)

    for entry in byop:
        entry = [x for x,_ in entry]
    return byop
'''
def bycheckamount(file):

    byca = [[(0,1),(0,1),(0,1)] for i in range(5)]

    d2 = afunctions.dinit()
    
    skip = 6
            
    with open(file, "rb") as f:

        fpos = skip

        while True:

            f.seek(fpos)
            if not f.read(1): break

            ca = 0
            enpassantsq = ''

            wm = 39
            bm = 39

            imb = []

            while True:
            
                w,b,ns,t = afunctions.extract(f,fpos)

                wp = afunctions.piecegt(w)
                wsq = afunctions.squaregt(w)

                if afunctions.capturec(w):
                    if not wp and enpassantsq and wsq == enpassantsq[0]+str(int(enpassantsq[1])+1): 
                        bm -= 1
                    else: bm -= d2[wsq]
                
                if wp == 'O-O-O':
                    d2['d1'] = 'R'
                    d2['c1'] = 'K'

                elif wp == 'O-O':
                    d2['f1'] = 'R'
                    d2['g1'] = 'K'

                elif afunctions.promotiongt(w):
                    d2[wsq] = afunctions.promotiongt(w)[1]
                    wm += afunctions.piecevaluegt(afunctions.promotiongt(w)[1])

                else:
                    d2[wsq] = wp

                if not wp and not afunctions.capturec(w): enpassantsq = wsq
                else: enpassantsq = ''


                if t < 2:

                    bp = afunctions.piecegt(b)
                    bsq = afunctions.squaregt(b)

                    if afunctions.capturec(b):
                        if not bp and enpassantsq and bsq == enpassantsq[0]+str(int(enpassantsq[1])-1): 
                            wm -= 1
                        else: wm -= d2[bsq]
                        
                    if bp == 'O-O-O':
                        d2['d8'] = 'R'
                        d2['c8'] = 'K'

                    elif bp == 'O-O':
                        d2['f8'] = 'R'
                        d2['g8'] = 'K'

                    elif afunctions.promotiongt(b):
                        d2[bsq] = afunctions.promotiongt(b)[1]
                        bm += afunctions.piecevaluegt(afunctions.promotiongt(b)[1])

                    else:
                        d2[bsq] = bp

                    if not bp and not afunctions.capturec(b): enpassantsq = bsq
                    else: enpassantsq = ''

                    imb.append(abs(wm-bm))

'''
