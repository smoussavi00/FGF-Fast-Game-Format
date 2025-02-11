import re 
import sys



def clean_moves(fpo,moves):
    moves = re.sub(r'[!?]', '', moves)
    moves = re.sub(r' \d+\.\.\.', '', moves)
    moves = re.sub(r' \{.*?\}', '', moves)
    fpo.write(f'{moves}\n')


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

                        # TESTING EVEN FURTHER COMPRESSIONS
                        fpo.write(int(buf["WhiteElo"]).to_bytes(2,'big'))
                        fpo.write(int(buf["BlackElo"]).to_bytes(2,'big'))
                        fpo.write((int(buf["TimeControl"].split('+')[0])//60).to_bytes(1,'big'))
                        fpo.write(int(buf["TimeControl"].split('+')[1]).to_bytes(1,'big'))
                        break
                        #fpo.write(f'{buf["WhiteElo"]} - {buf["BlackElo"]} - {buf["TimeControl"]} - ')
                        clean_moves(fpo,buf['the-moves'])

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