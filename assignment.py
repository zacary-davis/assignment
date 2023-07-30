import tkinter as tk
import random

class GridGame(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set up the window
        self.title("Grid Game")
        self.geometry("450x411")

        
        # Create the game board
        self.board = [[None for _ in range(10)] for _ in range(10)]
        self.turn = "user"

        # Create buttons for each cell in the board
        for i in range(10):
            for j in range(10):
                # Create a button with a command that triggers the place_line() method
                button = tk.Button(self, text=" ", command=lambda i=i, j=j: self.place_line(i, j), width=5, height=2)
                button.grid(row=i, column=j)
                self.board[i][j] = button
 # Create the menu bar
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Create the "Difficulty" menu
        difficulty_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Difficulty", menu=difficulty_menu)
        difficulty_menu.add_command(label="Easy", command=lambda: self.set_difficulty("easy"))
        difficulty_menu.add_command(label="Medium", command=lambda: self.set_difficulty("medium"))
        difficulty_menu.add_command(label="Hard", command=lambda: self.set_difficulty("hard"))

        # Default difficulty level is "Medium"
        self.difficulty_level = "medium"

    def set_difficulty(self, difficulty):
        self.difficulty_level = difficulty

    def place_line(self, i, j):
        # Check if the clicked cell is empty
        if self.board[i][j]["text"] == " ":
            # Check whose turn it is and update the cell accordingly
            if self.turn == "user":
                self.board[i][j]["text"] = "U"
                self.board[i][j]["fg"] = "blue"
                self.turn = "ai"
                # Check if the user's score is 5 or more
                if self.check_win(i, j, "U") >= 5:#self.calculate_score("U") >= 5:
                    self.display_winner("User")
                    self.reset_board()
                    return
                self.ai_move()
            else:
                self.board[i][j]["text"] = "A"
                self.board[i][j]["fg"] = "red"
                self.turn = "user"
                # Check if the AI's score is 5 or more
                if self.check_win(i, j, "A") >= 5:#self.calculate_score("A") >= 5:
                    self.display_winner("AI")
                    self.reset_board()
                    return

            # Check if the board is full
            if self.is_full():
                self.display_winner()
                self.reset_board()
    def reset_board(self):
        for i in range(10):
            for j in range(10):
                self.board[i][j]["text"] = " "
                self.board[i][j]["fg"] = "black"
        self.turn = "user"

    def calculate_score(self, player):
        max_score = 0
        for y in range(10):
            for x in range(10):
                if self.board[y][x]["text"] == player:
                    max_score = max(max_score, self.check_win(y, x, player))
        return max_score
    
    def check_win(self, i, j, player):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        counts = []
        for dx, dy in directions:
            count = -1
            count += self.count_continuous(i, j, dx, dy, player)
            count += self.count_continuous(i, j, -dx, -dy, player)
            counts.append(count)
        return max(counts)

    def count_continuous(self, i, j, dx, dy, player):
        count = 0
        while 0 <= i < 10 and 0 <= j < 10 and self.board[i][j].cget("text") == player:
            i += dx
            j += dy
            count += 1
        return count

    def ai_move(self):
        # Make a random move for the AI by selecting an empty cell
        empty_cells = [(i, j) for i in range(10) for j in range(10) if self.board[i][j]["text"] == " "]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.place_line(i, j)

    def is_full(self):
        # Check if the board is full by iterating over each cell
        for i in range(10):
            for j in range(10):
                if self.board[i][j]["text"] == " ":
                    return False
        return True

    def display_winner(self, winner=None):
        # Calculate scores for both players
        user_score = self.calculate_score("U")
        ai_score = self.calculate_score("A")

        # Determine the winner based on scores and print the result
        if not winner:
            winner = "User" if user_score > ai_score else "AI"
        print(f"{winner} wins! User score: {user_score}, AI score: {ai_score}")

if __name__ == "__main__":
    # Create an instance of the game and start the main event loop
    game = GridGame()
    game.mainloop()