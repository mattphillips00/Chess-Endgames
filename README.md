# Chess-Endgames

This project uses retrograde analysis techniques to find the shortest possible distance to checkmate (number of plys required to reach checkmate) from any winning position on the board under the perfect play assumption. This technique involves searching backwards from every possible checkmate and finding all board positions in which a checkmate can logically be forced by the winning side with perfect play. If played for the losing side, the optimal move is selected to maximise the distance to checkmate or achieve a draw wherever possible. Therefore, for all endgames with up to 5 pieces remaining on the board, this program plays chess perfectly.

main.py handles the user interface of the board, stores information about the game state and relays appropriate messages to the user. Users can play for black or white, and there is the option to play against another user or play against the computer.

engine.py handles the main engine of the program and is responsible for ensuring that all the pieces and moves work as intended so that the game of chess can be played without fault. 

RetrogradeAnalysis.py handles the main algorithms which are responsible for calculating the DTM from every single position on the board.

Here is the link to the full PDF:
https://drive.google.com/file/d/1dHFkkH3FBE4auRk-1M2uMfjs_65sh0DZ/view?usp=sharing
