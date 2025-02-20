# lichess-fast

### Dataset Compression
- A reduction of [Lichess standard games dataset](https://database.lichess.org/#standard_games)
- More compact datasets holding only necessary information (White ELO, Black ELO, Time Control, and Moves Played - in algebraic notation)
- Classical events with Normal/Time Forfeit terminations considered only (no abandoned matches, bullet or blitz)
  - Rapid matches are included under classical
  - You may find five minute matches
- Evaluations are also removed from algebraic notation
- Examples:
  - Jan 2016 4.5 GB >> 150 MB --- 30x reduction --- (Contains 1.2M Games)
  - Nov 2015 3.5 GB >> 100 MB --- 35x reduction --- (Contains 840K Games)
  - Jun 2013 170 MB >> 10 MB --- 17x reduction --- (Contains 76K Games)

---
### Format
In bytes, each element of a match and their storage requirements
```
White ELO [2B]
Black ELO [2B]
Time Control Minutes Total [1B]
Time Control Increment Seconds [1B]
Moves [1.5B to 4B / Move]

  - Standard Moves are represented with 12 bits
  > [1b Extend Flag] Set if the move is the final move played in the game or includes a checkmate, disambiguation (eg. R"d"e1), pawn promotion.
    > If this bit is set, another 2B are           given to encode the move
  > [1b Capture Flag] Set if the move includes a capture 'x'
  > [1b Check Flag] Set if the move includes a check '+'
  > [3b Piece Encoding] 0/000: Queenside Castle, 1/001: kingside castle, 2/010: pawn, 3/011: knight, 4/100: bishop, 5/101: rook, 6/110: queen, 7/111: king
  > [6b Square Encoding] 0-7: a1-a8, 8-15: b1-b8 ... 56-63: h1-h8

  - Extensions are represented with 16 bits or 2B
  - Extensions are appended to the standard 12 bits 
  > [1b Checkmate Flag] Set if the move includes a checkmate '#'
  > [2b Disambiguation Case] 0/00: no disambiguation, 1/01: disambiguate by file (eg. R"d"e1), 2/10: disambiguate by rank (eg. R"1"g4), 3/11: disambiguate both (eg. Q"h4"e1) 
  > [3b Promotion Case]: 0/000: no promotion, 1/001: promotion to knight, 2/010: promotion to bishop, 3/011: promotion to rook, 4/100: promotion to queen
  > [6b Original Position] Same as the square encoding as above, used to store the rank, file, or both/square the piece was originally in.
    > File disambiguations are of the form ?1, where the rank is constant at 1 (rank not relevant)
    > Rank disambiguations are of the form a?, where the file is constant at a (file not relevant)
  > [2b Result] 0/00: no result (game still continues), 1/01: black win, 2/10: draw, 3/11: white win

  - If the white move is extended and the black move is not, or vice versa, 5B needed to store the pair of moves
  - If both moves are extended (eg. white's move must be disambiguated, and black's move is a checkmate), 7B needed to store the pair of moves
  - If neither moves are extended (eg. 1. e4 e5), 3B needed to store the pair of moves
  - Special case where the match terminates after white's move, black does not make a move, the 28 bits (as the final move warrants an extension -- 12 + 16) are padded to 32 to make 4B

```
Sample:
```
1406 - 1434 - 1200+0 - 1. e4 e5 2. Nf3 f6 3. d4 a5 4. dxe5 fxe5 5. Bc4 Nc6 6. Nc3 a4 7. Ng5 Na5 8. Qh5+ g6 9. Bf7+ Ke7 10. Nd5+ Kd6 11. b3 gxh5 12. Ba3+ Kc6 13. Nb4+ Kc5 14. O-O-O Kb5 15. Rd5+ Kb6 16. c4 Qxg5+ 17. Kb1 Qxg2 18. Rb5+ Ka7 19. Rb6 cxb6 20. Rc1 Qxe4+ 21. Ka1 Qd4+ 0-1
```
