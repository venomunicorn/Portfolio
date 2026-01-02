"""
Tic-Tac-Toe vs AI GUI Application
Built with Tkinter - Part of 21APEX Challenge
Features: Minimax AI, modern UI, game statistics
"""

import tkinter as tk
from tkinter import messagebox
import math
import random

class TicTacToeGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe vs AI")
        self.root.geometry("450x600")
        self.root.resizable(False, False)
        self.root.configure(bg='#1a1a2e')
        
        # Colors
        self.colors = {
            'bg': '#1a1a2e',
            'card': '#16213e',
            'grid': '#0f3460',
            'x_color': '#e94560',
            'o_color': '#00d4ff',
            'win_line': '#ffd700',
            'text': '#eaeaea',
            'text_dim': '#8b949e'
        }
        
        # Game state
        self.board = [' ' for _ in range(9)]
        self.human = 'X'
        self.ai = 'O'
        self.current_player = 'X'
        self.game_active = True
        self.buttons = []
        
        # Statistics
        self.stats = {'player': 0, 'ai': 0, 'ties': 0}
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="❌ Tic-Tac-Toe ⭕",
            font=('Segoe UI', 28, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=(0, 10))
        
        # Status/turn display
        self.status_label = tk.Label(
            main_frame,
            text="Your turn (X)",
            font=('Segoe UI', 16),
            fg=self.colors['x_color'],
            bg=self.colors['bg']
        )
        self.status_label.pack(pady=10)
        
        # Game board frame
        board_frame = tk.Frame(main_frame, bg=self.colors['grid'], relief='flat')
        board_frame.pack(pady=20)
        
        # Create 3x3 grid
        for i in range(9):
            row = i // 3
            col = i % 3
            
            btn = tk.Button(
                board_frame,
                text='',
                font=('Segoe UI', 48, 'bold'),
                width=3,
                height=1,
                fg=self.colors['text'],
                bg=self.colors['card'],
                activebackground=self.colors['grid'],
                relief='flat',
                command=lambda idx=i: self.make_move(idx)
            )
            btn.grid(row=row, column=col, padx=4, pady=4)
            self.buttons.append(btn)
        
        # Statistics card
        stats_frame = tk.Frame(main_frame, bg=self.colors['card'])
        stats_frame.pack(fill='x', pady=20, ipady=15)
        
        stats_title = tk.Label(
            stats_frame,
            text="📊 Statistics",
            font=('Segoe UI', 14, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['card']
        )
        stats_title.pack()
        
        stats_container = tk.Frame(stats_frame, bg=self.colors['card'])
        stats_container.pack(pady=10)
        
        # Player wins
        player_frame = tk.Frame(stats_container, bg=self.colors['card'])
        player_frame.pack(side='left', padx=25)
        tk.Label(player_frame, text="You", font=('Segoe UI', 12),
                fg=self.colors['x_color'], bg=self.colors['card']).pack()
        self.player_wins_label = tk.Label(player_frame, text="0", 
                font=('Segoe UI', 24, 'bold'), fg=self.colors['x_color'], 
                bg=self.colors['card'])
        self.player_wins_label.pack()
        
        # Ties
        tie_frame = tk.Frame(stats_container, bg=self.colors['card'])
        tie_frame.pack(side='left', padx=25)
        tk.Label(tie_frame, text="Ties", font=('Segoe UI', 12),
                fg=self.colors['text_dim'], bg=self.colors['card']).pack()
        self.ties_label = tk.Label(tie_frame, text="0", 
                font=('Segoe UI', 24, 'bold'), fg=self.colors['text_dim'], 
                bg=self.colors['card'])
        self.ties_label.pack()
        
        # AI wins
        ai_frame = tk.Frame(stats_container, bg=self.colors['card'])
        ai_frame.pack(side='left', padx=25)
        tk.Label(ai_frame, text="AI", font=('Segoe UI', 12),
                fg=self.colors['o_color'], bg=self.colors['card']).pack()
        self.ai_wins_label = tk.Label(ai_frame, text="0", 
                font=('Segoe UI', 24, 'bold'), fg=self.colors['o_color'], 
                bg=self.colors['card'])
        self.ai_wins_label.pack()
        
        # Control buttons
        control_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        control_frame.pack(fill='x')
        
        new_game_btn = tk.Button(
            control_frame,
            text="🔄 New Game",
            font=('Segoe UI', 12, 'bold'),
            fg='white',
            bg='#00b894',
            activebackground='#00d9a5',
            relief='flat',
            padx=25,
            pady=10,
            command=self.new_game
        )
        new_game_btn.pack(side='left', padx=5)
        
        reset_stats_btn = tk.Button(
            control_frame,
            text="📊 Reset Stats",
            font=('Segoe UI', 12, 'bold'),
            fg='white',
            bg='#6c5ce7',
            activebackground='#a29bfe',
            relief='flat',
            padx=25,
            pady=10,
            command=self.reset_stats
        )
        reset_stats_btn.pack(side='left', padx=5)
    
    def make_move(self, idx):
        if not self.game_active or self.board[idx] != ' ' or self.current_player != self.human:
            return
        
        # Human move
        self.board[idx] = self.human
        self.buttons[idx].config(text='X', fg=self.colors['x_color'])
        
        if self.check_winner(self.human):
            self.game_won('player')
            return
        
        if ' ' not in self.board:
            self.game_tied()
            return
        
        # AI's turn
        self.current_player = self.ai
        self.status_label.config(text="AI is thinking...", fg=self.colors['o_color'])
        self.root.update()
        
        # Delay for effect
        self.root.after(400, self.ai_move)
    
    def ai_move(self):
        if not self.game_active:
            return
        
        # Use minimax to find best move
        best_move = self.get_best_move()
        
        if best_move is not None:
            self.board[best_move] = self.ai
            self.buttons[best_move].config(text='O', fg=self.colors['o_color'])
            
            if self.check_winner(self.ai):
                self.game_won('ai')
                return
            
            if ' ' not in self.board:
                self.game_tied()
                return
        
        self.current_player = self.human
        self.status_label.config(text="Your turn (X)", fg=self.colors['x_color'])
    
    def get_best_move(self):
        """Minimax algorithm to find the best move for AI"""
        # First move optimization - take center if available
        if self.board.count(' ') == 8 and self.board[4] == ' ':
            return 4
        
        best_score = -math.inf
        best_move = None
        
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = self.ai
                score = self.minimax(False)
                self.board[i] = ' '
                
                if score > best_score:
                    best_score = score
                    best_move = i
        
        return best_move
    
    def minimax(self, is_maximizing):
        # Check terminal states
        if self.check_winner(self.ai):
            return 10
        if self.check_winner(self.human):
            return -10
        if ' ' not in self.board:
            return 0
        
        if is_maximizing:
            best_score = -math.inf
            for i in range(9):
                if self.board[i] == ' ':
                    self.board[i] = self.ai
                    score = self.minimax(False)
                    self.board[i] = ' '
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for i in range(9):
                if self.board[i] == ' ':
                    self.board[i] = self.human
                    score = self.minimax(True)
                    self.board[i] = ' '
                    best_score = min(score, best_score)
            return best_score
    
    def check_winner(self, player):
        """Check if the given player has won"""
        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        
        for pattern in win_patterns:
            if all(self.board[i] == player for i in pattern):
                return pattern
        return None
    
    def game_won(self, winner):
        self.game_active = False
        win_pattern = self.check_winner(self.human if winner == 'player' else self.ai)
        
        # Highlight winning cells
        if win_pattern:
            for idx in win_pattern:
                self.buttons[idx].config(bg=self.colors['win_line'])
        
        if winner == 'player':
            self.stats['player'] += 1
            self.player_wins_label.config(text=str(self.stats['player']))
            self.status_label.config(text="🎉 You Win!", fg=self.colors['x_color'])
        else:
            self.stats['ai'] += 1
            self.ai_wins_label.config(text=str(self.stats['ai']))
            self.status_label.config(text="🤖 AI Wins!", fg=self.colors['o_color'])
    
    def game_tied(self):
        self.game_active = False
        self.stats['ties'] += 1
        self.ties_label.config(text=str(self.stats['ties']))
        self.status_label.config(text="🤝 It's a Tie!", fg=self.colors['text_dim'])
    
    def new_game(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = self.human
        self.game_active = True
        
        for btn in self.buttons:
            btn.config(text='', bg=self.colors['card'])
        
        self.status_label.config(text="Your turn (X)", fg=self.colors['x_color'])
    
    def reset_stats(self):
        self.stats = {'player': 0, 'ai': 0, 'ties': 0}
        self.player_wins_label.config(text="0")
        self.ties_label.config(text="0")
        self.ai_wins_label.config(text="0")
        self.new_game()
    
    def run(self):
        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.root.mainloop()

if __name__ == "__main__":
    app = TicTacToeGUI()
    app.run()
