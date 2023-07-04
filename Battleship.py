import numpy as np
import random as rand
play = True

while play:
    hidden_board = np.zeros((8, 8), dtype='int32')
    player_board = np.zeros((8, 8), dtype='int32')

    ships = {
        'Battleship': 4,
        'Cruiser': 3,
        'Destroyer': 3,
        'Submarine': 2,
        'Carrier': 5
    }


    def create_ships(board):
        ship_coordinates = {}  # To store ship coordinates for distinguishing ships
        for ship_name, ship_length in ships.items():
            ship_placed = False
            while not ship_placed:
                ship_row = rand.randint(0, 7)
                ship_column = rand.randint(0, 7)
                orientation = rand.randint(0, 1)  # 0 for horizontal, 1 for vertical

                if orientation == 0:
                    end_column = ship_column + ship_length - 1
                    if end_column <= 7 and np.all(board[ship_row, ship_column:end_column + 1] == 0):
                        board[ship_row, ship_column:end_column + 1] = 1
                        ship_coordinates[ship_name] = [(ship_row, col) for col in range(ship_column, end_column + 1)]
                        ship_placed = True
                else:
                    end_row = ship_row + ship_length - 1
                    if end_row <= 7 and np.all(board[ship_row:end_row + 1, ship_column] == 0):
                        board[ship_row:end_row + 1, ship_column] = 1
                        ship_coordinates[ship_name] = [(row, ship_column) for row in range(ship_row, end_row + 1)]
                        ship_placed = True

        return board, ship_coordinates

    def choose_difficulty():
        global turn_count
        turn_count = 0
        valid_difficulty = False
        while not valid_difficulty:
            difficulty = input("Choose a difficulty (Enter a number 1-3): 1-Easy 2-Medium 3-Hard: ")
            if difficulty not in ['1','2','3']:
                print("Invalid difficulty. Please enter a number from 1-3.")
            else:
                valid_difficulty = True
                difficulty = int(difficulty)
                if difficulty == 1:
                    turn_count = 55
                elif difficulty == 2:
                    turn_count = 45
                else:
                    turn_count = 35

    def guess_ship():
        global turn_count
        game_over = False
        while turn_count != 0:
            hits = 0
            ship_coordinates = create_ships(hidden_board)[1]
            while hits != 17:
                print("  " + " ".join([str(i + 1) for i in range(8)]))
                for i in range(8):
                    row_str = chr(65 + i) + " "
                    for j in range(8):
                        if player_board[i, j] == 0:
                            row_str += "  "
                        elif player_board[i, j] == 2:
                            row_str += "X "
                        elif player_board[i, j] == 3:
                            row_str += "O "
                    print(row_str)
                guess = input("Enter a coordinate (e.g., A1): ").lower()
                if len(guess) != 2 or not guess[0].isalpha() or not guess[1].isdigit():
                    print("Invalid coordinate. Please enter a valid coordinate.")
                    continue

                row = ord(guess[0]) - 97
                column = int(guess[1]) - 1

                if not (0 <= row < 8) or not (0 <= column < 8):
                    print("Invalid coordinate. Please enter a valid coordinate.")
                    continue

                if player_board[row, column] != 0:
                    print("You've already guessed that coordinate. Try again.")
                    continue

                if hidden_board[row, column] == 1:
                    player_board[row, column] = 2
                    print("Hit!")

                    # Check if a ship is sunk
                    ships_to_remove = []
                    for ship_name, coordinates in ship_coordinates.items():
                        if (row, column) in coordinates:
                            coordinates.remove((row, column))
                            if len(coordinates) == 0:
                                ships_to_remove.append(ship_name)
                                print(f"You sunk my {ship_name}!")

                    # Remove sunk ships from the ship_coordinates dictionary
                    for ship_name in ships_to_remove:
                        del ship_coordinates[ship_name]

                    hits += 1
                else:
                    player_board[row, column] = 3
                    print("You missed.")
                turn_count -= 1
                print(f"You have {turn_count} turns remaining.")
                if turn_count == 0:
                    print("Out of turns! Game over.")
                    game_over = True
                    break
        if not game_over:
            print("Congratulations! You've sunk all the ships!")


    def play_again():
        global play
        play_again = input("Do you want to play again? (Y/N) ")
        if play_again.lower() == 'y':
            play = True
        else:
            play = False
            print("Thank you for playing!")

    choose_difficulty()
    guess_ship()
    play_again()