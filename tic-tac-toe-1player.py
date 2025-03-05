import sys
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QVBoxLayout, QWidget, QMessageBox, QLabel, QSpinBox, QHBoxLayout
from PyQt6.QtGui import QScreen, QFont
#from PyQt6.QtCore import Qt

class TicTacToe(QMainWindow):
    """A tic-tac-toe game using python and pyqt6. The game has a square 3x3 board that takes up to 60% of the screen height."""
    def __init__(self):
        super().__init__()
        self.winning_buttons = None
        self.setWindowTitle('Tic-Tac-Toe')  # Set the window title

        screen = QScreen.availableGeometry(QApplication.primaryScreen())
        screen_height = screen.height()
        window_size = int(screen_height * 0.6)  # Set window size to 60% of screen height
        self.setGeometry(100, 100, window_size, window_size)  # Set the window size

        self.central_widget = QWidget()  # Create a central widget
        self.setCentralWidget(self.central_widget)  # Set the central widget

        self.layout = QVBoxLayout()  # Create a vertical layout
        self.central_widget.setLayout(self.layout)  # Set the layout for the central widget

        self.grid_layout = QGridLayout()  # Create a grid layout
        self.layout.addLayout(self.grid_layout)  # Add the grid layout to the vertical layout

        self.reset_button: QPushButton = QPushButton('Reset')  # Create a reset button (with type hint)
        # self.reset_button = QPushButton('Reset')  # Create a reset button (without type hint)
        self.reset_button.clicked.connect(self.reset_game)  # Connect the reset button to the reset_game method
        self.layout.addWidget(self.reset_button)  # Add the reset button to the vertical layout

        self.score_label = QLabel('X: 0 | O: 0 | Ties: 0 | Games Played: 0')  # Create a label to display the scores
        self.layout.addWidget(self.score_label)  # Add the score label to the vertical layout

        self.turn_label = QLabel('Current Turn: X')  # Create a label to display the current player's turn
        self.layout.addWidget(self.turn_label)  # Add the turn label to the vertical layout

        self.max_games = 20  # Set the maximum number of games before resetting the scores
        self.max_games_label = QLabel('Max Games:')  # Create a label for max games
        self.max_games_spinbox: QSpinBox = QSpinBox()  # Create a spinbox for max games (with type hint)
        # self.max_games_spinbox = QSpinBox()  # Create a spinbox for max games (without type hint)
        self.max_games_spinbox.setValue(self.max_games)  # Set default value
        self.max_games_spinbox.setMinimum(1)  # Set minimum value
        self.max_games_spinbox.valueChanged.connect(self.update_max_games)  # Connect value change to handler

        max_games_layout = QHBoxLayout()  # Create a horizontal layout for max games
        max_games_layout.addWidget(self.max_games_label)
        max_games_layout.addWidget(self.max_games_spinbox)
        self.layout.addLayout(max_games_layout)  # Add the max games layout to the vertical layout

        self.current_player = 'X'  # Initialize the current player
        self.scores = {'X': 0, 'O': 0, 'Ties': 0, 'Games Played': 0}  # Initialize the scores

        self.buttons = []  # List to store buttons
        self.create_board(window_size)  # Call the method to create the board

    def create_board(self, window_size):
        button_size = window_size // 3  # Calculate button size based on window size
        font_size = int(button_size * 0.8)  # Calculate font size to be 80% of button size
        font = QFont()
        font.setPointSize(font_size)
        # Create a 3x3 grid of buttons
        for row in range(3):
            row_buttons = []
            for col in range(3):
                button: QPushButton | QPushButton = QPushButton('')  # Create a button with no text (with type hint)
                button.setFixedSize(button_size, button_size)  # Set each button size
                button.setFont(font)  # Set the font size for the button text
                button.clicked.connect(self.handle_button_click)  # Connect the button click to the handler
                self.grid_layout.addWidget(button, row, col)  # Add the button to the grid layout
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def handle_button_click(self):
        button = self.sender()  # Get the button that was clicked
        assert isinstance(button, QPushButton)  # Force the type of the button variable
        button: QPushButton  # Type hint for the button variable
        if button.text() == '' and self.current_player == 'X':  # If the button is not already clicked, and it's the user's turn
            button.setText(self.current_player)  # Set the button text to the current player
            if self.check_winner():
                self.highlight_winner()
                self.scores[self.current_player] += 1  # Update the score for the current player
                self.scores['Games Played'] += 1  # Update the number of games played
                self.update_score_label()  # Update the score label
                self.end_game(f'Player {self.current_player} wins!')
            elif self.check_tie():
                self.scores['Ties'] += 1  # Update the number of ties
                self.scores['Games Played'] += 1  # Update the number of games played
                self.update_score_label()  # Update the score label
                self.end_game('Tie')
            else:
                self.current_player = 'O'  # Switch to computer's turn
                self.update_turn_label()  # Update the turn label
                self.computer_move()  # Make the computer move

            if self.scores['Games Played'] >= self.max_games:
                self.reset_scores()

    def computer_move(self):
        """This code first checks if the computer can win by placing an 'O' in any empty spot.
            If it finds a winning move, it makes that move.
            If not, it checks if the user can win by placing an 'X' in any empty spot and blocks that move.
            If neither condition is met, it chooses a random move."""

        # Check if the computer can win in the next move
        for row in self.buttons:
            for button in row:
                if button.text() == '':
                    button.setText('O')
                    if self.check_winner():
                        self.highlight_winner()
                        self.scores['O'] += 1  # Update the score for the computer
                        self.scores['Games Played'] += 1  # Update the number of games played
                        self.update_score_label()  # Update the score label
                        self.end_game('Computer wins!')
                        return
                    button.setText('')

        # Check if the user can win in the next move and block it
        for row in self.buttons:
            for button in row:
                if button.text() == '':
                    button.setText('X')
                    if self.check_winner():
                        button.setText('O')  # Make the move to block user's winning move
                        if self.check_tie():
                            self.scores['Ties'] += 1  # Update the number of ties
                            self.scores['Games Played'] += 1  # Update the number of games played
                            self.update_score_label()  # Update the score label
                            self.end_game('Tie')
                            return
                        self.current_player = 'X'  # Switch back to user's turn
                        self.update_turn_label()  # Update the turn label
                        return
                    button.setText('')

        # Choose a random move
        available_buttons = [button for row in self.buttons for button in row if button.text() == '']
        if available_buttons:
            button = random.choice(available_buttons)
            button.setText('O')
            if self.check_winner():
                self.highlight_winner()
                self.scores['O'] += 1  # Update the score for the computer
                self.scores['Games Played'] += 1  # Update the number of games played
                self.update_score_label()  # Update the score label
                self.end_game('Computer wins!')
            elif self.check_tie():
                self.scores['Ties'] += 1  # Update the number of ties
                self.scores['Games Played'] += 1  # Update the number of games played
                self.update_score_label()  # Update the score label
                self.end_game('Tie')
            else:
                self.current_player = 'X'  # Switch back to user's turn
                self.update_turn_label()  # Update the turn label

    def check_winner(self):
        # Check rows, columns, and diagonals for a win
        for i in range(3):
            if self.buttons[i][0].text() == self.buttons[i][1].text() == self.buttons[i][2].text() != '':
                self.winning_buttons = [self.buttons[i][0], self.buttons[i][1], self.buttons[i][2]]
                return True
            if self.buttons[0][i].text() == self.buttons[1][i].text() == self.buttons[2][i].text() != '':
                self.winning_buttons = [self.buttons[0][i], self.buttons[1][i], self.buttons[2][i]]
                return True
        if self.buttons[0][0].text() == self.buttons[1][1].text() == self.buttons[2][2].text() != '':
            self.winning_buttons = [self.buttons[0][0], self.buttons[1][1], self.buttons[2][2]]
            return True
        if self.buttons[0][2].text() == self.buttons[1][1].text() == self.buttons[2][0].text() != '':
            self.winning_buttons = [self.buttons[0][2], self.buttons[1][1], self.buttons[2][0]]
            return True
        return False

    def check_tie(self):
        for row in self.buttons:
            for button in row:
                if button.text() == '':
                    return False
        return True

    def highlight_winner(self):
        for button in self.winning_buttons:
            button.setStyleSheet('background-color: yellow')

    def end_game(self, message):
        QMessageBox.information(self, 'Game Over', message)
        self.reset_game()

    def reset_game(self):
        self.current_player = 'X' if self.scores['Games Played'] % 2 == 0 else 'O'  # Alternate starting player
        self.update_turn_label()  # Update the turn label
        for row in self.buttons:
            for button in row:
                button.setText('')
                button.setStyleSheet('')
        if self.current_player == 'O':
            self.computer_move()  # Computer starts if it's its turn

    def reset_scores(self):
        self.scores = {'X': 0, 'O': 0, 'Ties': 0, 'Games Played': 0}
        self.update_score_label()

    def update_score_label(self):
        self.score_label.setText(f'X: {self.scores["X"]} | O: {self.scores["O"]} | Ties: {self.scores["Ties"]} | Games Played: {self.scores["Games Played"]}')

    def update_turn_label(self):
        self.turn_label.setText(f'Current Turn: {self.current_player}')

    def update_max_games(self):
        self.max_games = self.max_games_spinbox.value()

if __name__ == '__main__':
    app = QApplication(sys.argv)  # Create the application
    window = TicTacToe()  # Create an instance of the TicTacToe class
    window.show()  # Show the main window
    sys.exit(app.exec())  # Execute the application
