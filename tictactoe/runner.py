import pygame
import sys
import time
import tictactoe as ttt  # Import the tictactoe module

# Initialize Pygame
pygame.init()
size = width, height = 600, 400
screen = pygame.display.set_mode(size)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Fonts
MEDIUM_FONT = pygame.font.Font("OpenSans-Regular.ttf", 28)
LARGE_FONT = pygame.font.Font("OpenSans-Regular.ttf", 40)
MOVE_FONT = pygame.font.Font("OpenSans-Regular.ttf", 60)


def draw_title(surface, text, font, color, y_offset=0):
    """Draws a title on the screen."""
    title = font.render(text, True, color)
    title_rect = title.get_rect()
    title_rect.center = (width / 2, 50 + y_offset)  # Allow for vertical offset
    surface.blit(title, title_rect)


def draw_button(surface, rect, text, font, text_color, button_color):
    """Draws a button on the screen. Returns the Rect object."""
    pygame.draw.rect(surface, button_color, rect)
    button_text = font.render(text, True, text_color)
    button_text_rect = button_text.get_rect()
    button_text_rect.center = rect.center
    surface.blit(button_text, button_text_rect)
    return rect  # Return the Rect


def draw_board(surface, board, tile_size=80):
    """
    Draws the Tic-Tac-Toe board on the screen and returns a list of Rect
    objects representing the tiles.
    """
    tile_origin = (width / 2 - (1.5 * tile_size), height / 2 - (1.5 * tile_size))
    tiles = []
    for i in range(3):
        row = []
        for j in range(3):
            rect = pygame.Rect(
                tile_origin[0] + j * tile_size,
                tile_origin[1] + i * tile_size,
                tile_size,
                tile_size,
            )
            pygame.draw.rect(surface, WHITE, rect, 3)

            if board[i][j] != ttt.EMPTY:
                move = MOVE_FONT.render(board[i][j], True, WHITE)
                move_rect = move.get_rect()
                move_rect.center = rect.center
                surface.blit(move, move_rect)
            row.append(rect)
        tiles.append(row)
    return tiles  # Return the list of tile Rects


def get_user_input(surface, play_x_button, play_o_button):
    """Gets user input for X or O selection."""
    click, _, _ = pygame.mouse.get_pressed()
    if click == 1:
        mouse = pygame.mouse.get_pos()
        if play_x_button.collidepoint(mouse):
            time.sleep(0.2)
            return ttt.X
        elif play_o_button.collidepoint(mouse):
            time.sleep(0.2)
            return ttt.O
    return None


def handle_user_move(board, tiles, user):
    """
    Handles a user's move on the board.  Returns the new board state
    or None if no valid move.
    """
    click, _, _ = pygame.mouse.get_pressed()
    if click == 1:
        mouse = pygame.mouse.get_pos()
        for i in range(3):
            for j in range(3):
                if (
                    board[i][j] == ttt.EMPTY
                    and tiles[i][j].collidepoint(mouse)
                ):
                    try:
                        return ttt.result(board, (i, j))  # Apply move
                    except ValueError as e:
                        print(f"Error: {e}")  # Handle invalid move
                        return board # Return the old board
    return board  # Default: no move


def handle_play_again_button(surface, again_button):
    """Handles the 'Play Again' button click. Returns True if clicked."""
    click, _, _ = pygame.mouse.get_pressed()
    if click == 1:
        mouse = pygame.mouse.get_pos()
        if again_button.collidepoint(mouse):
            time.sleep(0.2)
            return True
    return False


def main():
    """Main function to run the Tic-Tac-Toe game."""
    user = None
    board = ttt.initial_state()
    ai_turn = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(BLACK)

        # Let user choose a player.
        if user is None:
            draw_title(screen, "Play Tic-Tac-Toe", LARGE_FONT, WHITE)
            play_x_button = draw_button(
                screen,
                pygame.Rect((width / 8), (height / 2), width / 4, 50),
                "Play as X",
                MEDIUM_FONT,
                BLACK,
                WHITE,
            )
            play_o_button = draw_button(
                screen,
                pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50),
                "Play as O",
                MEDIUM_FONT,
                BLACK,
                WHITE,
            )
            user = get_user_input(screen, play_x_button, play_o_button)

        else:
            tiles = draw_board(screen, board)
            game_over = ttt.terminal(board)
            player = ttt.player(board)

            # Show title
            if game_over:
                winner = ttt.winner(board)
                title_text = f"Game Over: {winner if winner else 'Tie'}."
            elif user == player:
                title_text = f"Play as {user}"
            else:
                title_text = "Computer thinking..."
            draw_title(screen, title_text, LARGE_FONT, WHITE, y_offset=-20)

            # AI move
            if user != player and not game_over:
                if ai_turn:
                    time.sleep(0.5)
                    move = ttt.minimax(board)
                    if move:
                        board = ttt.result(board, move)
                    ai_turn = False
                else:
                    ai_turn = True

            # User move
            if user == player and not game_over:
                new_board = handle_user_move(board, tiles, user)
                if new_board != board:
                    board = new_board

            if game_over:
                again_button = draw_button(
                    screen,
                    pygame.Rect(width / 3, height - 65, width / 3, 50),
                    "Play Again",
                    MEDIUM_FONT,
                    BLACK,
                    WHITE,
                )
                if handle_play_again_button(screen, again_button):
                    user = None
                    board = ttt.initial_state()
                    ai_turn = False

        pygame.display.flip()


if __name__ == "__main__":
    main()
