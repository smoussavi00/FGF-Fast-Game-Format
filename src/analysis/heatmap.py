import afunctions  # type: ignore



def transit(file):
# PIECE TRANSIT HEATMAP GENERATE

    d = {f'{f}{r}': (0, 1) for f in [chr(i) for i in range(97,105)] for r in range(1, 9)}
    skip = 6

    with open(file, "rb") as f:

        fpos = skip

        while True:

            f.seek(fpos)
            if not f.read(1): break

            while True:

                w,b,ns,t = afunctions.extract(f,fpos)

                wp = afunctions.piecegt(w)
                wsq = afunctions.squaregt(w)
                
                if wp == 'O-O-O': 
                    d['d1'] = ( ((d['d1'][1]-1)/d['d1'][1]) * d['d1'][0] + (1/d['d1'][1]) * afunctions.piecevaluegt('R') , d['d1'][1]+1 )
                    d['c1'] = ( ((d['c1'][1]-1)/d['c1'][1]) * d['c1'][0] + (1/d['c1'][1]) * afunctions.piecevaluegt('K',9) , d['c1'][1]+1 )
                elif wp == 'O-O':
                    d['f1'] = ( ((d['f1'][1]-1)/d['f1'][1]) * d['f1'][0] + (1/d['f1'][1]) * afunctions.piecevaluegt('R') , d['f1'][1]+1 )
                    d['g1'] = ( ((d['g1'][1]-1)/d['g1'][1]) * d['g1'][0] + (1/d['g1'][1]) * afunctions.piecevaluegt('K',9) , d['g1'][1]+1 )
                elif afunctions.promotiongt(w):
                    d[wsq] = ( ((d[wsq][1]-1)/d[wsq][1]) * d[wsq][0] + (1/d[wsq][1]) *  afunctions.piecevaluegt(afunctions.promotiongt(w)[1]) , d[wsq][1]+1 )
                else:
                    d[wsq] = ( ((d[wsq][1]-1)/d[wsq][1]) * d[wsq][0] + (1/d[wsq][1]) * afunctions.piecevaluegt(wp) , d[wsq][1]+1 )

                if t < 2:

                    bp = afunctions.piecegt(b)
                    bsq = afunctions.squaregt(b)

                    if bp == 'O-O-O': 
                        d['d8'] = ( ((d['d8'][1]-1)/d['d8'][1]) * d['d8'][0] + (1/d['d8'][1]) * afunctions.piecevaluegt('R') , d['d8'][1]+1 )
                        d['c8'] = ( ((d['c8'][1]-1)/d['c8'][1]) * d['c8'][0] + (1/d['c8'][1]) * afunctions.piecevaluegt('K',9) , d['c8'][1]+1 )
                    elif bp == 'O-O':
                        d['f8'] = ( ((d['f8'][1]-1)/d['f8'][1]) * d['f8'][0] + (1/d['f8'][1]) * afunctions.piecevaluegt('R') , d['f8'][1]+1 )
                        d['g8'] = ( ((d['g8'][1]-1)/d['g8'][1]) * d['g8'][0] + (1/d['g8'][1]) * afunctions.piecevaluegt('K',9) , d['g8'][1]+1 )
                    elif afunctions.promotiongt(b):
                        d[bsq] = ( ((d[bsq][1]-1)/d[bsq][1]) * d[bsq][0] + (1/d[bsq][1]) *  afunctions.piecevaluegt(afunctions.promotiongt(b)[1]) , d[bsq][1]+1 )
                    else:
                        d[bsq] = ( ((d[bsq][1]-1)/d[bsq][1]) * d[bsq][0] + (1/d[bsq][1]) * afunctions.piecevaluegt(bp) , d[bsq][1]+1 )

                fpos += ns
            
                if t:
                    fpos += skip
                    break

    for sq in d:
        d[sq] = round(d[sq][0],2)

    return d

def victim(file):
# PIECE VICTIM HEATMAP GENERATE

    d = {f'{f}{r}': (0, 1) for f in [chr(i) for i in range(97,105)] for r in range(1, 9)}
    d2 = afunctions.dinit()
    skip = 6
            
    with open(file, "rb") as f:

        fpos = skip

        while True:

            f.seek(fpos)
            if not f.read(1): break

            enpassantsq = ''
            d2 = afunctions.dinit()

            while True:

                w,b,ns,t = afunctions.extract(f,fpos)

                wp = afunctions.piecegt(w)
                wsq = afunctions.squaregt(w)

                if afunctions.capturec(w):
                    if not wp and enpassantsq and wsq == enpassantsq[0]+str(int(enpassantsq[1])+1): 
                        d[enpassantsq] = ( ((d[enpassantsq][1]-1)/d[enpassantsq][1]) * d[enpassantsq][0] + (1/d[enpassantsq][1]) , d[enpassantsq][1]+1 )
                    else: d[wsq] = ( ((d[wsq][1]-1)/d[wsq][1]) * d[wsq][0] + (1/d[wsq][1]) * afunctions.piecevaluegt(d2[wsq]) , d[wsq][1]+1 )
                
                if wp == 'O-O-O':
                    d2['d1'] = 'R'
                    d2['c1'] = 'K'

                elif wp == 'O-O':
                    d2['f1'] = 'R'
                    d2['g1'] = 'K'

                else:
                    d2[wsq] = wp

                if not wp and not afunctions.capturec(w): enpassantsq = wsq
                else: enpassantsq = ''

                if t < 2:

                    bp = afunctions.piecegt(b)
                    bsq = afunctions.squaregt(b)

                    if afunctions.capturec(b):
                        if not bp and enpassantsq and bsq == enpassantsq[0]+str(int(enpassantsq[1])-1): 
                            d[enpassantsq] = ( ((d[enpassantsq][1]-1)/d[enpassantsq][1]) * d[enpassantsq][0] + (1/d[enpassantsq][1]) , d[enpassantsq][1]+1 )
                        else: d[bsq] = ( ((d[bsq][1]-1)/d[bsq][1]) * d[bsq][0] + (1/d[bsq][1]) * afunctions.piecevaluegt(d2[bsq]) , d[bsq][1]+1 )
                        
                    if bp == 'O-O-O':
                        d2['d8'] = 'R'
                        d2['c8'] = 'K'

                    elif bp == 'O-O':
                        d2['f8'] = 'R'
                        d2['g8'] = 'K'

                    elif afunctions.promotiongt(b):
                        d2[wsq] = afunctions.promotiongt(b)[1]

                    else:
                        d2[bsq] = bp

                    if not bp and not afunctions.capturec(b): enpassantsq = bsq
                    else: enpassantsq = ''

                fpos += ns
            
                if t:
                    fpos += skip
                    break

    for sq in d:
        d[sq] = round(d[sq][0],2)

    return d

def checkandmates(file,mode):
# CHECKMATE / MATE LOCATIONS HEATMAP GENERATE
    
    d = {f'{f}{r}': 0 for f in [chr(i) for i in range(97,105)] for r in range(1, 9)}
    skip = 6

    with open(file, "rb") as f:

        fpos = skip

        while True:

            f.seek(fpos)
            if not f.read(1): break

            while True:

                w,b,ns,t = afunctions.extract(f,fpos)

                wsq = afunctions.squaregt(w)
                if mode == '+': c = int(bool(afunctions.checkc(w)))
                else: c = int(bool(afunctions.checkmatec(w)))

                if c: d[wsq] += 1

                if t < 2:

                    bsq = afunctions.squaregt(b)
                    if mode == '+': c = int(bool(afunctions.checkc(b)))
                    else: c = int(bool(afunctions.checkmatec(b)))

                    if c: d[bsq] += 1

                fpos += ns
            
                if t:
                    fpos += skip
                    break
    
    return d