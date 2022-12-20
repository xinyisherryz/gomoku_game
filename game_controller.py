from game_board import GameBoard
from stone import Stone
from ai import AI

CONTINUE = -1
DRAW = 0
HUMAN_STONE = 1
AI_STONE = 2
FIVE = 5


class GameController():
    """
    Game controller class
    """

    def __init__(self, boardsize=15):
        """
        Initialize game Controller
        """
        self.board = GameBoard(boardsize)
        # not sure if this is useful in part2
        self.cur_step = 0
        self.allowMousePress = True
        self.ai = AI(self)
        self.name_score = dict()

    def create_stone(self, x, y, size, player):
        """
        Drop the stone on the board
        """
        # check if the position is occupied
        if self.board.board[x][y] == 0:
            if player == "Human":
                self.board.board[x][y] = HUMAN_STONE
                self.cur_step += 1
                self.the_stone = Stone(x, y, size, "Human")
                return self.the_stone
            if player == "AI":
                self.board.board[x][y] = AI_STONE
                # print("num_board: ", self.board.board)
                self.cur_step += 1
                self.the_stone = Stone(x, y, size, "AI")
                # self.the_stone.display(BORDER, UNIT_WIDTH)
                return self.the_stone
        if self.board.board[x][y] != 0:
            print("position is", (x, y))
            print("Position occupied, please try agian")
            return

    def game_reuslt(self):
        """
        Assess the status of game
        -1 stans for playing, 0 stands for draw,
        1 stands for human winner (black)
        2 stands for AI winner (white)
        """
        # 5 in a row
        for x in range(self.board.boardsize - FIVE):
            for y in range(self.board.boardsize):
                check_human = 0
                check_ai = 0
                for i in range(0, FIVE):
                    if self.board.board[x + i][y] == HUMAN_STONE:
                        check_human += 1
                    if self.board.board[x + i][y] == AI_STONE:
                        check_ai += 1
                if check_human == FIVE:
                    return HUMAN_STONE
                if check_ai == FIVE:
                    return AI_STONE

        # 5 in a column
        for y in range(self.board.boardsize - FIVE):
            for x in range(self.board.boardsize):
                check_human = 0
                check_ai = 0
                for i in range(0, FIVE):
                    if self.board.board[x][y + i] == HUMAN_STONE:
                        check_human += 1
                    if self.board.board[x][y + i] == AI_STONE:
                        check_ai += 1
                if check_human == FIVE:
                    return HUMAN_STONE
                if check_ai == FIVE:
                    return AI_STONE

        # 5 from top right to down left
        for x in range(self.board.boardsize - FIVE + 1):
            for y in range(self.board.boardsize - FIVE + 1):
                check_human = 0
                check_ai = 0
                for i in range(0, FIVE):
                    if self.board.board[x
                                        + i][y + FIVE - 1 - i] == HUMAN_STONE:
                        check_human += 1
                    if self.board.board[x + i][y + FIVE - 1 - i] == AI_STONE:
                        check_ai += 1
                if check_human == FIVE:
                    return HUMAN_STONE
                if check_ai == FIVE:
                    return AI_STONE

        # 5 from top left to down right
        for x in range(self.board.boardsize - FIVE + 1):
            for y in range(self.board.boardsize - FIVE + 1):
                check_human = 0
                check_ai = 0
                for i in range(0, FIVE):
                    if self.board.board[x + FIVE - 1 - i][y
                       + FIVE - 1 - i] == HUMAN_STONE:
                        check_human += 1
                    if self.board.board[x + FIVE - 1 - i][y
                       + FIVE - 1 - i] == AI_STONE:
                        check_ai += 1
                if check_human == FIVE:
                    return HUMAN_STONE
                if check_ai == FIVE:
                    return AI_STONE

        # determine whether it is a draw or continue to play
        for x in range(self.board.boardsize):
            for y in range(self.board.boardsize):
                # if there is a position that is not occupied
                # then continue to play
                if self.board.board[x][y] == 0:
                    return CONTINUE
        # draw
        return DRAW

    def get_distance(self, x1, y1, x2, y2):
        return ((x2 - x1)**2 + (y2 - y1)**2)**(0.5)

    @property
    def allowMousePress(self):
        """
        Getter for allowKeyPress
        None --> Boolean
        """
        return self._allowMousePress

    # Setter decorator. @property with the same
    # name must be defined above.
    @allowMousePress.setter
    def allowMousePress(self, value):
        """
        Setter for allowKeyPress
        Boolean --> None
        """
        self._allowMousePress = value

    def human_drop_stone(self, mouseX, mouseY,
                         BORDER, PIXEL_WIDTH, UNIT_WIDTH):
        """
        1. Drop the stone to the nearest when mouse is pressed
        2. Auto-switch the color when there are two human players
        3. Display end text in terminal when the board is full
        """
        ELLIPSE_SIZE = 0.5 * UNIT_WIDTH
        if self.allowMousePress is True:
            if (BORDER <= mouseX <= (PIXEL_WIDTH - BORDER)) and\
               (BORDER <= mouseY <= (PIXEL_WIDTH - BORDER)):
                for i in range(self.board.boardsize):
                    for j in range(self.board.boardsize):
                        if self.get_distance(BORDER + i * UNIT_WIDTH,
                           BORDER + j * UNIT_WIDTH, mouseX,
                           mouseY) < 0.5 * UNIT_WIDTH:
                            player = self.color_choose()
                            human_stone = self.create_stone(i, j, ELLIPSE_SIZE,
                                                            player)
                            human_stone.display(BORDER, UNIT_WIDTH)
            self.end_text()
            self.allowMousePress = False

    def ai_drop_stone(self, BORDER, UNIT_WIDTH):
        """
        let AI place the stone at certain coord
        Int, Int -> None
        """
        x, y = self.ai.choose_spot()
        ELLIPSE_SIZE = 0.5 * UNIT_WIDTH
        ai_stone = self.create_stone(x, y, ELLIPSE_SIZE, "AI")
        ai_stone.display(BORDER, UNIT_WIDTH)

    def color_choose(self):
        """
        Choose the color of the stone for each step
        None -> String
        """
        if self.cur_step % 2 == 0:
            player = "Human"
        else:
            player = "AI"
        return player

    def end_text(self):
        """
        Display the end text in terminal
        None -> None
        """
        if self.game_reuslt() != CONTINUE:
            print("It's an end.")
            if self.game_reuslt() == AI_STONE:
                print("White Wins!")
            if self.game_reuslt() == HUMAN_STONE:
                print("Black Wins!")

    def player_score(self, answer):
        """
        record the player score in txt file
        String -> None
        """
        winner_score = dict()
        all_lines = []
        # read the file to get information in it
        file = open("scores.txt", "r")
        for line in file:
            all_lines.append(line.strip())
        for line in all_lines:
            print("line: ", line)
            name_score = line.split("\t")
            print("name score: ", name_score)
            winner_score[name_score[0]] = int(name_score[1])
        # compare the input with existing names
        if answer in winner_score.keys():
            winner_score[answer] += 1
        else:
            winner_score[answer] = 1
        sorted_name = sorted(
            winner_score.items(),
            key=lambda x: x[1],
            reverse=True
        )
        file.close()
        # write the file to update the information
        file = open("scores.txt", "w")
        for i in sorted_name:
            file.write(i[0])
            file.write("\t")
            file.write(str(i[1]))
            file.write("\n")
