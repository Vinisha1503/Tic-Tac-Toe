import tkinter as tk
from tkinter import messagebox
import random


class GameBoard:
    def __init__(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"

    def make_move(self, row, col):
        if self.board[row][col] == "":
            self.board[row][col] = self.current_player
            return True
        return False

    def check_winner(self, player):
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)):
                return [(i, j) for j in range(3)]
        for j in range(3):
            if all(self.board[i][j] == player for i in range(3)):
                return [(i, j) for i in range(3)]
        if all(self.board[i][i] == player for i in range(3)):
            return [(i, i) for i in range(3)]
        if all(self.board[i][2 - i] == player for i in range(3)):
            return [(i, 2 - i) for i in range(3)]
        return None

    def is_draw(self):
        return all(self.board[i][j] != "" for i in range(3) for j in range(3))

    def reset(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"


class AIPlayer:
    def __init__(self, symbol="O"):
        self.symbol = symbol

    def get_move(self, board):
        empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ""]
        if empty_cells:
            return random.choice(empty_cells)
        return None


class TicTacToeApp:
    def __init__(self, master, vs_ai=True):
        self.master = master
        self.vs_ai = vs_ai
        self.board = GameBoard()
        self.ai = AIPlayer("O") if vs_ai else None

        self.score_x = 0
        self.score_o = 0

        self.master.title("Tic Tac Toe")
        self.master.configure(bg="#222222")

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                btn = tk.Button(master, text="", font=("Arial", 32), width=5, height=2,
                                bg="#DDDDDD", fg="black",
                                command=lambda row=i, col=j: self.player_move(row, col))
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.buttons[i][j] = btn

        self.label = tk.Label(master, text="Player X's turn", font=("Arial", 16, "bold"), bg="#222222", fg="white")
        self.label.grid(row=3, column=0, columnspan=3, pady=10)

        self.score_label = tk.Label(master, text=f"X: {self.score_x} | O: {self.score_o}",
                                    font=("Arial", 14), bg="#222222", fg="white")
        self.score_label.grid(row=4, column=0, columnspan=3)

        self.home_btn = tk.Button(master, text="Home", font=("Arial", 14), bg="orange", fg="black",
                                  width=10, command=self.go_home)
        self.home_btn.grid(row=5, column=0, columnspan=3, pady=10)

    def player_move(self, row, col):
        if self.board.make_move(row, col):
            self.update_ui()
            win_coords = self.board.check_winner(self.board.current_player)
            if win_coords:
                self.highlight_winner(win_coords)
                self.label.config(text=f"Player {self.board.current_player} wins!")
                self.update_score(self.board.current_player)
                self.master.update_idletasks()
                messagebox.showinfo("Game Over", f"Player {self.board.current_player} wins!")
                self.reset_game()
                return
            elif self.board.is_draw():
                self.label.config(text="It's a draw!")
                self.master.update_idletasks()
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_game()
                return

            self.board.current_player = "O" if self.board.current_player == "X" else "X"
            self.label.config(text=f"Player {self.board.current_player}'s turn")

            if self.vs_ai and self.board.current_player == self.ai.symbol:
                self.master.after(500, self.ai_move)

    def ai_move(self):
        move = self.ai.get_move(self.board.board)
        if move:
            self.board.make_move(move[0], move[1])
            self.update_ui()
            win_coords = self.board.check_winner(self.ai.symbol)
            if win_coords:
                self.highlight_winner(win_coords)
                self.label.config(text=f"Player {self.ai.symbol} wins!")
                self.update_score(self.ai.symbol)
                self.master.update_idletasks()
                messagebox.showinfo("Game Over", f"Player {self.ai.symbol} wins!")
                self.reset_game()
                return
            elif self.board.is_draw():
                self.label.config(text="It's a draw!")
                self.master.update_idletasks()
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_game()
                return

            self.board.current_player = "X"
            self.label.config(text="Player X's turn")

    def update_ui(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=self.board.board[i][j])

    def highlight_winner(self, coords):
        for i, j in coords:
            self.buttons[i][j].config(bg="lightgreen")

    def update_score(self, winner):
        if winner == "X":
            self.score_x += 1
        else:
            self.score_o += 1
        self.score_label.config(text=f"Score - X: {self.score_x} | O: {self.score_o}")

    def reset_game(self):
        self.board.reset()
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", bg="#DDDDDD")
        self.label.config(text="Player X's turn")

    def go_home(self):
        self.master.destroy()
        HomeScreen()


class HomeScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.root.configure(bg="#222222")
        self.root.geometry("300x400")

        title_label = tk.Label(self.root, text="Tic Tac Toe", font=("Arial", 18, "bold"), bg="#222222", fg="white")
        title_label.pack(pady=40)

        play_ai_btn = tk.Button(self.root, text="Play vs AI", font=("Arial", 16), bg="#00CC66", fg="black",
                                width=12, height=2, command=lambda: self.start_game(True))
        play_ai_btn.pack(pady=10)

        play_two_btn = tk.Button(self.root, text="2 Players", font=("Arial", 16), bg="#0066CC", fg="black",
                                 width=12, height=2, command=lambda: self.start_game(False))
        play_two_btn.pack(pady=10)

        exit_btn = tk.Button(self.root, text="Exit", font=("Arial", 16), bg="red", fg="black",
                             width=12, height=2, command=self.root.destroy)
        exit_btn.pack(pady=10)

        self.root.mainloop()

    def start_game(self, vs_ai):
        self.root.destroy()
        game_window = tk.Tk()
        TicTacToeApp(game_window, vs_ai)
        game_window.mainloop()


if __name__ == "__main__":
    HomeScreen()