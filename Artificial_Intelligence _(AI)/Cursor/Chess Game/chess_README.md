# ♔ Chess Game

A fully functional chess game built with Python and Streamlit! Play chess against yourself or with a friend in a beautiful web interface.

## 🎮 How to Play

- **Move Pieces**: Use the move input fields to enter moves in algebraic notation (e.g., e2-e4)
- **Game Controls**: Use the sidebar to start new games, undo moves, and view game status
- **Visual Board**: See the chess board with all pieces and their positions
- **Move History**: Track all moves made during the game
- **Captured Pieces**: View pieces captured by each player

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Install the required dependencies:
   ```bash
   pip install -r chess_requirements.txt
   ```

### Running the Game

1. Start the chess game by running:
   ```bash
   streamlit run chess_game.py
   ```

2. Open your web browser and go to the URL shown in the terminal (usually `http://localhost:8501`)

3. Start playing chess!

## ♟️ Game Features

- **Complete Chess Logic**: All standard chess rules implemented
- **Move Validation**: Prevents illegal moves and checks for check/checkmate
- **Visual Board**: Beautiful HTML/CSS chess board with piece symbols
- **Game Status**: Real-time check/checkmate detection
- **Move History**: Track all moves in algebraic notation
- **Captured Pieces**: Visual display of captured pieces
- **Responsive Design**: Works on different screen sizes

## 🎯 Chess Rules Implemented

- **Piece Movement**: All pieces move according to standard chess rules
- **Pawn Movement**: Including en passant and promotion (basic implementation)
- **Castling**: King and rook castling rules
- **Check Detection**: Identifies when a king is in check
- **Checkmate Detection**: Determines when the game is over
- **Stalemate Detection**: Identifies draw conditions
- **Move Validation**: Prevents moves that would put own king in check

## 🛠️ Technical Details

- **Object-Oriented Design**: Clean separation of game logic and UI
- **Piece Classes**: Each piece type has its own movement logic
- **Board Representation**: 8x8 array with piece objects
- **Move Validation**: Comprehensive legal move checking
- **Streamlit Integration**: Full web-based interface

## 📱 Controls

- **Move Input**: Enter moves using algebraic notation (e.g., e2-e4)
- **New Game**: Start a fresh game
- **Undo Move**: Undo the last move (basic implementation)
- **Game Status**: View current player, check status, and game state

## ♟️ Piece Symbols

- **White Pieces**: ♔♕♖♗♘♙ (King, Queen, Rook, Bishop, Knight, Pawn)
- **Black Pieces**: ♚♛♜♝♞♟ (King, Queen, Rook, Bishop, Knight, Pawn)

## 🎨 Board Features

- **Light/Dark Squares**: Traditional chess board coloring
- **Selected Square**: Highlight selected piece
- **Possible Moves**: Show valid moves for selected piece
- **Check Highlighting**: Highlight king when in check
- **Algebraic Notation**: Standard chess notation for moves

## 🔧 Customization

You can easily customize the game by modifying:
- Board colors and styling
- Piece symbols and appearance
- Move input methods
- Game rules and variations
- UI layout and design

## 🎯 Future Enhancements

- **AI Opponent**: Add computer player with different difficulty levels
- **Move Animation**: Animate piece movements
- **Sound Effects**: Add audio feedback for moves
- **Game Modes**: Different time controls and game variants
- **Save/Load Games**: Persist games between sessions
- **Online Play**: Multiplayer over network

Enjoy playing chess! ♔♕♖♗♘♙
