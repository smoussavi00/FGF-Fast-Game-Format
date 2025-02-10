# lichess-fast

- A reduction of [Lichess standard games dataset](https://database.lichess.org/#standard_games)
- More compact datasets holding only necessary information (White ELO, Black ELO, Time Control, and Moves Played - in algebraic notation)
- Classical events with Normal/Time Forfeit terminations considered only (no abandoned matches, bullet or blitz)
- Evaluations are also removed from algebraic notation
- Examples:
  - Jan 2016 4.5 GB > 500 MB (Contains 1.2M Games)
  - Nov 2015 3.5 GB > 350 MB (Contains 840K Games)
  - Jun 2013 170 MB > 31 MB (Contains 76K Games)
  
