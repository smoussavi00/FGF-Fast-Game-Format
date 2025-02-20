# lichess-fast

### Dataset Compression
- A reduction of [Lichess standard games dataset](https://database.lichess.org/#standard_games)
- More compact datasets holding only necessary information (White ELO, Black ELO, Time Control, and Moves Played - in algebraic notation)
- Classical events with Normal/Time Forfeit terminations considered only (no abandoned matches, bullet or blitz)
  - Rapid matches are included under classical
  - You may find five minute matches
- Evaluations are also removed from algebraic notation
- Examples:
  - Jan 2016 4.5 GB > 150 MB (Contains 1.2M Games -- 30x reduction)
  - Nov 2015 3.5 GB > 100 MB (Contains 840K Games -- 35x reduction)
  - Jun 2013 170 MB > 10 MB (Contains 76K Games - 17x reduction)

---
### Format
In bytes, each element of a match and their storage requirements
```
White ELO [2B] - Black ELO [2B] - Time Control Minutes Total [1B] - Time Control Increment Seconds [1B] - Moves [1.5B to 4B / Move]
```
Sample:
```
1406 - 1434 - 1200+0 - 1. e4 e5 2. Nf3 f6 3. d4 a5 4. dxe5 fxe5 5. Bc4 Nc6 6. Nc3 a4 7. Ng5 Na5 8. Qh5+ g6 9. Bf7+ Ke7 10. Nd5+ Kd6 11. b3 gxh5 12. Ba3+ Kc6 13. Nb4+ Kc5 14. O-O-O Kb5 15. Rd5+ Kb6 16. c4 Qxg5+ 17. Kb1 Qxg2 18. Rb5+ Ka7 19. Rb6 cxb6 20. Rc1 Qxe4+ 21. Ka1 Qd4+ 0-1
```
