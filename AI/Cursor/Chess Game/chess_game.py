import streamlit as st
import copy
import random
from typing import List, Tuple, Optional, Dict
from enum import Enum

class PieceType(Enum):
    PAWN = "pawn"
    ROOK = "rook"
    KNIGHT = "knight"
    BISHOP = "bishop"
    QUEEN = "queen"
    KING = "king"

class Color(Enum):
    WHITE = "white"
    BLACK = "black"

class Piece:
    def __init__(self, piece_type: PieceType, color: Color):
        self.type = piece_type
        self.color = color
        self.has_moved = False
    
    def get_symbol(self) -> str:
        symbols = {
            (PieceType.PAWN, Color.WHITE): "♙",
            (PieceType.ROOK, Color.WHITE): "♖",
            (PieceType.KNIGHT, Color.WHITE): "♘",
            (PieceType.BISHOP, Color.WHITE): "♗",
            (PieceType.QUEEN, Color.WHITE): "♕",
            (PieceType.KING, Color.WHITE): "♔",
            (PieceType.PAWN, Color.BLACK): "♟",
            (PieceType.ROOK, Color.BLACK): "♜",
            (PieceType.KNIGHT, Color.BLACK): "♞",
            (PieceType.BISHOP, Color.BLACK): "♝",
            (PieceType.QUEEN, Color.BLACK): "♛",
            (PieceType.KING, Color.BLACK): "♚",
        }
        return symbols.get((self.type, self.color), "?")

class ChessGame:
    def __init__(self):
        self.board = self.initialize_board()
        self.current_player = Color.WHITE
        self.game_over = False
        self.winner = None
        self.move_history = []
        self.selected_square = None
        self.possible_moves = []
        self.check_status = {"white": False, "black": False}
        self.captured_pieces = {"white": [], "black": []}
        self.last_move_notation: Optional[str] = None
    
    def get_all_legal_moves(self) -> List[Tuple[int, int, int, int]]:
        """Return a list of all legal moves for the current player as (from_row, from_col, to_row, to_col)."""
        all_moves: List[Tuple[int, int, int, int]] = []
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and piece.color == self.current_player:
                    for to_row, to_col in self.get_possible_moves(row, col):
                        all_moves.append((row, col, to_row, to_col))
        return all_moves

    def get_all_legal_moves_for(self, color: Color) -> List[Tuple[int, int, int, int]]:
        """Return all legal moves for the specified color without changing turn state."""
        saved_player = self.current_player
        self.current_player = color
        moves = self.get_all_legal_moves()
        self.current_player = saved_player
        return moves

    def autoplay(self, plies: int = 5) -> int:
        """Play a given number of plies automatically by picking the first legal move each turn.

        Returns the number of plies actually played (can be fewer if no legal moves).
        """
        played = 0
        for _ in range(plies):
            if self.is_checkmate() or self.is_stalemate():
                break
            legal_moves = self.get_all_legal_moves()
            if not legal_moves:
                break
            from_row, from_col, to_row, to_col = legal_moves[0]
            # make_move already validates using get_possible_moves and switches player
            if not self.make_move(from_row, from_col, to_row, to_col):
                break
            played += 1
        return played

    def ai_move(self) -> bool:
        """Simple AI: if it's Black's turn, pick a random legal move and play it."""
        if self.current_player != Color.BLACK:
            return False
        legal_moves = self.get_all_legal_moves()
        if not legal_moves:
            return False
        from_row, from_col, to_row, to_col = random.choice(legal_moves)
        moved = self.make_move(from_row, from_col, to_row, to_col)
        if moved and self.move_history:
            self.last_move_notation = self.move_history[-1]
        return moved

    def ai_move_for(self, color: Color) -> bool:
        """Pick a random legal move for the given color if it's that color's turn."""
        if self.current_player != color:
            return False
        legal_moves = self.get_all_legal_moves_for(color)
        if not legal_moves:
            return False
        from_row, from_col, to_row, to_col = random.choice(legal_moves)
        moved = self.make_move(from_row, from_col, to_row, to_col)
        if moved and self.move_history:
            self.last_move_notation = self.move_history[-1]
        return moved

    def initialize_board(self) -> List[List[Optional[Piece]]]:
        """Initialize the chess board with pieces in starting positions"""
        board = [[None for _ in range(8)] for _ in range(8)]
        
        # Place pawns
        for col in range(8):
            board[1][col] = Piece(PieceType.PAWN, Color.BLACK)
            board[6][col] = Piece(PieceType.PAWN, Color.WHITE)
        
        # Place other pieces
        piece_order = [PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP, PieceType.QUEEN,
                      PieceType.KING, PieceType.BISHOP, PieceType.KNIGHT, PieceType.ROOK]
        
        for col, piece_type in enumerate(piece_order):
            board[0][col] = Piece(piece_type, Color.BLACK)
            board[7][col] = Piece(piece_type, Color.WHITE)
        
        return board
    
    def get_piece(self, row: int, col: int) -> Optional[Piece]:
        """Get piece at given position"""
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None
    
    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if position is within board bounds"""
        return 0 <= row < 8 and 0 <= col < 8
    
    def get_possible_moves(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Get all possible moves for a piece at given position"""
        piece = self.get_piece(row, col)
        if not piece or piece.color != self.current_player:
            return []
        
        moves = []
        
        if piece.type == PieceType.PAWN:
            moves = self.get_pawn_moves(row, col, piece)
        elif piece.type == PieceType.ROOK:
            moves = self.get_rook_moves(row, col, piece)
        elif piece.type == PieceType.KNIGHT:
            moves = self.get_knight_moves(row, col, piece)
        elif piece.type == PieceType.BISHOP:
            moves = self.get_bishop_moves(row, col, piece)
        elif piece.type == PieceType.QUEEN:
            moves = self.get_queen_moves(row, col, piece)
        elif piece.type == PieceType.KING:
            moves = self.get_king_moves(row, col, piece)
        
        # Filter out moves that would put own king in check
        valid_moves = []
        for move_row, move_col in moves:
            if self.is_legal_move(row, col, move_row, move_col):
                valid_moves.append((move_row, move_col))
        
        return valid_moves
    
    def get_pawn_moves(self, row: int, col: int, piece: Piece) -> List[Tuple[int, int]]:
        """Get possible moves for a pawn"""
        moves = []
        direction = -1 if piece.color == Color.WHITE else 1
        start_row = 6 if piece.color == Color.WHITE else 1
        
        # Move forward one square
        if self.is_valid_position(row + direction, col) and not self.get_piece(row + direction, col):
            moves.append((row + direction, col))
            
            # Move forward two squares from starting position
            if row == start_row and not self.get_piece(row + 2 * direction, col):
                moves.append((row + 2 * direction, col))
        
        # Capture diagonally
        for dc in [-1, 1]:
            new_row, new_col = row + direction, col + dc
            if (self.is_valid_position(new_row, new_col) and 
                self.get_piece(new_row, new_col) and 
                self.get_piece(new_row, new_col).color != piece.color):
                moves.append((new_row, new_col))
        
        return moves
    
    def get_rook_moves(self, row: int, col: int, piece: Piece) -> List[Tuple[int, int]]:
        """Get possible moves for a rook"""
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = row + i * dr, col + i * dc
                if not self.is_valid_position(new_row, new_col):
                    break
                
                target_piece = self.get_piece(new_row, new_col)
                if not target_piece:
                    moves.append((new_row, new_col))
                elif target_piece.color != piece.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves
    
    def get_knight_moves(self, row: int, col: int, piece: Piece) -> List[Tuple[int, int]]:
        """Get possible moves for a knight"""
        moves = []
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        
        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if (self.is_valid_position(new_row, new_col) and 
                (not self.get_piece(new_row, new_col) or 
                 self.get_piece(new_row, new_col).color != piece.color)):
                moves.append((new_row, new_col))
        
        return moves
    
    def get_bishop_moves(self, row: int, col: int, piece: Piece) -> List[Tuple[int, int]]:
        """Get possible moves for a bishop"""
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = row + i * dr, col + i * dc
                if not self.is_valid_position(new_row, new_col):
                    break
                
                target_piece = self.get_piece(new_row, new_col)
                if not target_piece:
                    moves.append((new_row, new_col))
                elif target_piece.color != piece.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves
    
    def get_queen_moves(self, row: int, col: int, piece: Piece) -> List[Tuple[int, int]]:
        """Get possible moves for a queen"""
        return self.get_rook_moves(row, col, piece) + self.get_bishop_moves(row, col, piece)
    
    def get_king_moves(self, row: int, col: int, piece: Piece) -> List[Tuple[int, int]]:
        """Get possible moves for a king"""
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (self.is_valid_position(new_row, new_col) and 
                (not self.get_piece(new_row, new_col) or 
                 self.get_piece(new_row, new_col).color != piece.color)):
                moves.append((new_row, new_col))
        
        return moves
    
    def is_legal_move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Check if a move is legal (doesn't put own king in check)"""
        # Make a copy of the board
        temp_board = copy.deepcopy(self.board)
        
        # Make the move
        piece = temp_board[from_row][from_col]
        temp_board[to_row][to_col] = piece
        temp_board[from_row][from_col] = None
        
        # Check if own king is in check
        king_pos = self.find_king(self.current_player, temp_board)
        if king_pos:
            return not self.is_square_under_attack(king_pos[0], king_pos[1], 
                                                 Color.BLACK if self.current_player == Color.WHITE else Color.WHITE, 
                                                 temp_board)
        
        return True
    
    def find_king(self, color: Color, board: List[List[Optional[Piece]]]) -> Optional[Tuple[int, int]]:
        """Find the position of the king of given color"""
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.type == PieceType.KING and piece.color == color:
                    return (row, col)
        return None
    
    def is_square_under_attack(self, row: int, col: int, attacking_color: Color, board: List[List[Optional[Piece]]]) -> bool:
        """Check if a square is under attack by the given color"""
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece and piece.color == attacking_color:
                    if self.can_attack_square(r, c, row, col, piece, board):
                        return True
        return False
    
    def can_attack_square(self, from_row: int, from_col: int, to_row: int, to_col: int, 
                         piece: Piece, board: List[List[Optional[Piece]]]) -> bool:
        """Check if a piece can attack a specific square"""
        if piece.type == PieceType.PAWN:
            direction = -1 if piece.color == Color.WHITE else 1
            return (to_row == from_row + direction and 
                    abs(to_col - from_col) == 1)
        elif piece.type == PieceType.ROOK:
            return self.can_rook_attack(from_row, from_col, to_row, to_col, board)
        elif piece.type == PieceType.KNIGHT:
            knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
            return (to_row - from_row, to_col - from_col) in knight_moves
        elif piece.type == PieceType.BISHOP:
            return self.can_bishop_attack(from_row, from_col, to_row, to_col, board)
        elif piece.type == PieceType.QUEEN:
            return (self.can_rook_attack(from_row, from_col, to_row, to_col, board) or
                    self.can_bishop_attack(from_row, from_col, to_row, to_col, board))
        elif piece.type == PieceType.KING:
            return abs(to_row - from_row) <= 1 and abs(to_col - from_col) <= 1
        
        return False
    
    def can_rook_attack(self, from_row: int, from_col: int, to_row: int, to_col: int, 
                       board: List[List[Optional[Piece]]]) -> bool:
        """Check if rook can attack target square"""
        if from_row != to_row and from_col != to_col:
            return False
        
        dr = 0 if from_row == to_row else (1 if to_row > from_row else -1)
        dc = 0 if from_col == to_col else (1 if to_col > from_col else -1)
        
        r, c = from_row + dr, from_col + dc
        while r != to_row or c != to_col:
            if board[r][c] is not None:
                return False
            r += dr
            c += dc
        
        return True
    
    def can_bishop_attack(self, from_row: int, from_col: int, to_row: int, to_col: int, 
                         board: List[List[Optional[Piece]]]) -> bool:
        """Check if bishop can attack target square"""
        if abs(to_row - from_row) != abs(to_col - from_col):
            return False
        
        dr = 1 if to_row > from_row else -1
        dc = 1 if to_col > from_col else -1
        
        r, c = from_row + dr, from_col + dc
        while r != to_row or c != to_col:
            if board[r][c] is not None:
                return False
            r += dr
            c += dc
        
        return True
    
    def make_move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Make a move on the board"""
        if not self.is_legal_move(from_row, from_col, to_row, to_col):
            return False
        
        piece = self.get_piece(from_row, from_col)
        if not piece or piece.color != self.current_player:
            return False
        
        # Check if move is in possible moves
        possible_moves = self.get_possible_moves(from_row, from_col)
        if (to_row, to_col) not in possible_moves:
            return False
        
        # Capture piece if present
        captured_piece = self.get_piece(to_row, to_col)
        if captured_piece:
            self.captured_pieces[captured_piece.color.value].append(captured_piece)
        
        # Make the move
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None
        piece.has_moved = True
        
        # Record move
        move_notation = self.get_move_notation(from_row, from_col, to_row, to_col, piece, captured_piece)
        self.move_history.append(move_notation)
        self.last_move_notation = move_notation
        
        # Switch players
        self.current_player = Color.BLACK if self.current_player == Color.WHITE else Color.WHITE
        
        # Check for check/checkmate
        self.update_check_status()
        
        return True
    
    def get_move_notation(self, from_row: int, from_col: int, to_row: int, to_col: int, 
                         piece: Piece, captured_piece: Optional[Piece]) -> str:
        """Get algebraic notation for a move"""
        files = "abcdefgh"
        ranks = "87654321"
        
        from_square = files[from_col] + ranks[from_row]
        to_square = files[to_col] + ranks[to_row]
        
        if captured_piece:
            return f"{piece.get_symbol()} {from_square}x{to_square}"
        else:
            return f"{piece.get_symbol()} {from_square}-{to_square}"
    
    def update_check_status(self):
        """Update check status for both players"""
        white_king = self.find_king(Color.WHITE, self.board)
        black_king = self.find_king(Color.BLACK, self.board)
        
        if white_king:
            self.check_status["white"] = self.is_square_under_attack(
                white_king[0], white_king[1], Color.BLACK, self.board)
        
        if black_king:
            self.check_status["black"] = self.is_square_under_attack(
                black_king[0], black_king[1], Color.WHITE, self.board)
    
    def is_checkmate(self) -> bool:
        """Check if current player is in checkmate"""
        if not self.check_status[self.current_player.value]:
            return False
        
        # Check if any legal moves exist
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and piece.color == self.current_player:
                    if self.get_possible_moves(row, col):
                        return False
        
        return True
    
    def is_stalemate(self) -> bool:
        """Check if current player is in stalemate"""
        if self.check_status[self.current_player.value]:
            return False
        
        # Check if any legal moves exist
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and piece.color == self.current_player:
                    if self.get_possible_moves(row, col):
                        return False
        
        return True
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.board = self.initialize_board()
        self.current_player = Color.WHITE
        self.game_over = False
        self.winner = None
        self.move_history = []
        self.selected_square = None
        self.possible_moves = []
        self.check_status = {"white": False, "black": False}
        self.captured_pieces = {"white": [], "black": []}

def main():
    st.set_page_config(
        page_title="Chess Game",
        page_icon="♔",
        layout="wide"
    )
    
    st.title("♔ Chess Game")
    st.markdown("**Play a game of chess against yourself or with a friend!**")
    st.markdown("---")
    
    # Initialize game in session state
    if 'chess_game' not in st.session_state:
        st.session_state.chess_game = ChessGame()
    if 'black_starts' not in st.session_state:
        st.session_state.black_starts = False
    if 'ai_opening_done' not in st.session_state:
        st.session_state.ai_opening_done = False
    if 'board_style' not in st.session_state:
        st.session_state.board_style = 'Classic'
    
    game = st.session_state.chess_game
    
    # Sidebar with game controls and info
    with st.sidebar:
        st.header("🎮 Game Controls")
        
        st.checkbox("Black starts (AI)", key="black_starts")
        st.selectbox("Board style", ["Classic", "Green", "Blue", "Dark"], key="board_style")
        if st.button("🔄 New Game", key="new_game"):
            game.reset_game()
            # Respect Black starts setting
            if st.session_state.black_starts:
                game.current_player = Color.BLACK
                st.session_state.ai_opening_done = False
            else:
                st.session_state.ai_opening_done = False
            st.rerun()
        
        if st.button("↩️ Undo Move", key="undo"):
            if len(game.move_history) > 0:
                # Simple undo - just reset the game for now
                # In a full implementation, you'd store board states
                st.warning("Undo not fully implemented - starting new game")
                game.reset_game()
                if st.session_state.black_starts:
                    game.current_player = Color.BLACK
                    st.session_state.ai_opening_done = False
                else:
                    st.session_state.ai_opening_done = False
                st.rerun()

        st.markdown("---")
        st.subheader("🤖 Random Moves")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Random White move", key="rand_w"):
                if game.ai_move_for(Color.WHITE):
                    st.rerun()
        with c2:
            if st.button("Random Black move", key="rand_b"):
                if game.ai_move_for(Color.BLACK):
                    st.rerun()
        plies = st.slider("Autoplay plies (both)", min_value=1, max_value=20, value=4, step=1, key="autoplay_both_plies")
        if st.button("Play random plies (both)", key="rand_both"):
            for _ in range(plies):
                if game.is_checkmate() or game.is_stalemate():
                    break
                legal = game.get_all_legal_moves()
                if not legal:
                    break
                fr, fc, tr, tc = random.choice(legal)
                if not game.make_move(fr, fc, tr, tc):
                    break
            st.rerun()

        if st.button("🤖 Autoplay 5 plies", key="autoplay_5"):
            played = game.autoplay(plies=5)
            st.success(f"Autoplay made {played} plies")
            st.rerun()
        
        st.markdown("---")
        st.header("📊 Game Status")
        
        current_player_emoji = "⚪" if game.current_player == Color.WHITE else "⚫"
        color_name = "White" if game.current_player == Color.WHITE else "Black"
        st.markdown(f"**Current Player:** {current_player_emoji} {color_name}")
        st.caption("White moves first; Black is AI and plays after each White move.")
        
        if game.check_status["white"]:
            st.warning("⚪ White is in check!")
        if game.check_status["black"]:
            st.warning("⚫ Black is in check!")
        
        if game.is_checkmate():
            st.error("Checkmate! Game Over!")
            winner = "Black" if game.current_player == Color.WHITE else "White"
            st.success(f"🏆 {winner} wins!")
        elif game.is_stalemate():
            st.info("Stalemate! Game is a draw!")
        
        st.markdown("---")
        st.header("📝 Move History")
        if game.move_history:
            for i, move in enumerate(game.move_history[-10:], 1):  # Show last 10 moves
                st.text(f"{i}. {move}")
        else:
            st.text("No moves yet")
        
        st.markdown("---")
        st.header("♟️ Captured Pieces")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**White Captured:**")
            for piece in game.captured_pieces["white"]:
                st.text(piece.get_symbol())
        with col2:
            st.markdown("**Black Captured:**")
            for piece in game.captured_pieces["black"]:
                st.text(piece.get_symbol())
    
    # Main game area
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.markdown("### Chess Board (Click to Move as White)")

        # If Black should start and hasn't moved yet, make opening AI move
        if game.current_player == Color.BLACK and not st.session_state.ai_opening_done:
            if game.ai_move():
                st.session_state.ai_opening_done = True
                st.rerun()
        
        # Click-to-move interaction using Streamlit session state
        if 'selected_square' not in st.session_state:
            st.session_state.selected_square = None
        if 'possible_moves' not in st.session_state:
            st.session_state.possible_moves = []

        # If internal game state differs, sync it (display purposes)
        game.selected_square = st.session_state.selected_square
        game.possible_moves = st.session_state.possible_moves

        # Render interactive board of 8x8 buttons with labels
        files = "abcdefgh"
        ranks = "87654321"
        top_labels = st.columns(9)
        top_labels[0].markdown("&nbsp;")
        for c in range(8):
            top_labels[c+1].markdown(f"**{files[c]}**")
        last_click_key = "last_board_click"
        if last_click_key not in st.session_state:
            st.session_state[last_click_key] = None
        clicked_cell = None
        for row in range(8):
            row_cols = st.columns(9)
            row_cols[0].markdown(f"**{ranks[row]}**")
            for col in range(8):
                piece = game.get_piece(row, col)
                in_moves = (row, col) in st.session_state.possible_moves
                # Label rules:
                # - Piece: show its symbol
                # - Empty and in_moves: show a dot to indicate legal destination
                # - Empty otherwise: nbsp to keep layout stable
                if piece:
                    label = piece.get_symbol()
                else:
                    # Theme-colored squares when empty
                    if in_moves:
                        label = "🟢"
                    else:
                        if st.session_state.board_style == 'Classic':
                            label = "🟫" if ((row + col) % 2) else "⬜"
                        elif st.session_state.board_style == 'Green':
                            label = "🟩" if ((row + col) % 2) else "🟦"
                        elif st.session_state.board_style == 'Blue':
                            label = "🟦" if ((row + col) % 2) else "⬜"
                        else:  # Dark
                            label = "⬛" if ((row + col) % 2) else "⬜"
                is_light = (row + col) % 2 == 0
                key = f"sq_{row}_{col}"
                if row_cols[col+1].button(label, key=key, help=position_to_square(row, col), use_container_width=True):
                    clicked_cell = (row, col)

        # Process click once after rendering grid
        if clicked_cell is not None:
            row, col = clicked_cell
            piece = game.get_piece(row, col)
            if game.current_player == Color.WHITE:
                if st.session_state.selected_square is None:
                    if piece and piece.color == Color.WHITE:
                        st.session_state.selected_square = (row, col)
                        st.session_state.possible_moves = game.get_possible_moves(row, col)
                        st.rerun()
                else:
                    from_row, from_col = st.session_state.selected_square
                    if (row, col) in st.session_state.possible_moves:
                        if game.make_move(from_row, from_col, row, col):
                            st.session_state.selected_square = None
                            st.session_state.possible_moves = []
                            if not game.is_checkmate() and not game.is_stalemate():
                                # AI move must trigger a rerun after execution to update board
                                if game.ai_move():
                                    st.rerun()
                            st.rerun()
                    else:
                        if piece and piece.color == Color.WHITE:
                            st.session_state.selected_square = (row, col)
                            st.session_state.possible_moves = game.get_possible_moves(row, col)
                        else:
                            st.session_state.selected_square = None
                            st.session_state.possible_moves = []
                        st.rerun()
            else:
                st.info("Wait for Black (AI) to play; it's not White's turn.")

        # Selection status + legend
        sel = st.session_state.selected_square
        if sel is None:
            st.caption("Select a White piece to see its legal moves.")
        else:
            sq = position_to_square(sel[0], sel[1])
            st.caption(f"Selected: {sq} • Legal moves: {len(st.session_state.possible_moves)}")
        st.caption("Click a White piece, then click a dotted square to move. Black moves automatically.")
        st.markdown("---")
        st.markdown("**Legend**")
        st.markdown("White: ♔ ♕ ♖ ♗ ♘ ♙")
        st.markdown("Black: ♚ ♛ ♜ ♝ ♞ ♟")

        # Last move and counters
        if game.last_move_notation:
            st.info(f"Last move: {game.last_move_notation} • Total moves: {len(game.move_history)}")
    
    # Footer
    st.markdown("---")
    st.markdown("♔ **Chess Game** - Made with ❤️ using Python and Streamlit")
    st.markdown("*Click on squares or use the move input to play!*")

def square_to_position(square: str) -> Optional[Tuple[int, int]]:
    """Convert algebraic notation to board position"""
    if len(square) != 2:
        return None
    
    file = square[0].lower()
    rank = square[1]
    
    if file not in "abcdefgh" or rank not in "12345678":
        return None
    
    col = ord(file) - ord('a')
    row = 8 - int(rank)
    
    return (row, col)

def position_to_square(row: int, col: int) -> str:
    """Convert board position to algebraic notation"""
    file = chr(ord('a') + col)
    rank = str(8 - row)
    return file + rank

def create_chess_board_html(game: ChessGame) -> str:
    """Create HTML representation of the chess board (unused in click-to-move UI)."""
    html = """
    <style>
    .chess-board {
        display: grid;
        grid-template-columns: repeat(8, 1fr);
        grid-template-rows: repeat(8, 1fr);
        width: 500px;
        height: 500px;
        border: 2px solid #333;
        margin: 20px auto;
    }
    .chess-square {
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        cursor: pointer;
        border: 1px solid #666;
    }
    .light-square {
        background-color: #f0d9b5;
    }
    .dark-square {
        background-color: #b58863;
    }
    .selected {
        background-color: #ffff00 !important;
    }
    .possible-move {
        background-color: #90EE90 !important;
    }
    .in-check {
        background-color: #ff6b6b !important;
    }
    </style>
    <div class="chess-board">
    """
    
    for row in range(8):
        for col in range(8):
            is_light = (row + col) % 2 == 0
            square_class = "light-square" if is_light else "dark-square"
            
            piece = game.get_piece(row, col)
            piece_symbol = piece.get_symbol() if piece else ""
            
            square_name = position_to_square(row, col)
            
            # Add special classes
            if game.selected_square == (row, col):
                square_class += " selected"
            elif (row, col) in game.possible_moves:
                square_class += " possible-move"
            
            # Check if king is in check
            if piece and piece.type == PieceType.KING and game.check_status[piece.color.value]:
                square_class += " in-check"
            
            html += f'<div class="chess-square {square_class}" onclick="selectSquare({row}, {col})" title="{square_name}">{piece_symbol}</div>'
    
    html += """
    </div>
    <script>
    function selectSquare(row, col) {
        // This would need to be connected to Streamlit
        console.log('Selected square:', row, col);
    }
    </script>
    """
    
    return html

if __name__ == "__main__":
    main()
