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

                w,b,ns = afunctions.extract(f,fpos)
                print(f'{afunctions.piecegt(w)}{afunctions.squaregt(w)} {afunctions.piecegt(b)}{afunctions.squaregt(b)}')
                fpos += ns
            
                if ns < 1:
                    fpos += skip
                    break
            

transit('gen')
        