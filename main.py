import random
from graphics import *


class Game:
    def __init__(self):
        self.tutorial_text = ["Click the arrows to navigate the tutorial.",
                              "The objective of the game is to guess a random word.",
                              "You can choose from different categories of words.",
                              "There are 3 difficulty levels: Easy, Medium, and Hard.",
                              "It affects the number of hints you get",
                              "The number of hints for easy mode is half the length of the word (rounded down)."
                              "It is one third the length of the word for medium mode, and zero for hard."
                              "You can guess the letters of the word individually, by clicking on the on-screen keys",
                              "Or you can guess the entire word by typing it in the text box, and pressing enter to "
                              "submit.", "Invalid guesses will not use up lives",
                              "The number of lives you get is equal to the length of the word you must guess.",
                              "You can use a hint by pressing on the hint button.",
                              "It will reveal a random letter in the word."]
        self.tutorial_index = 0
        self.current_scene = "start_menu"
        self.correct_letters = 0
        self.correct_letters = 0
        self.category = ""
        self.difficulty = ""
        self.current_word = ""
        self.lives = len(self.current_word)
        self.guessed_letters = list()
        self.word_guess_progress = len(self.current_word) * "-"
        self.hints = 0
        self.guessed_words = list()


class Button:
    def __init__(self, p1: Point, p2: Point, label: str):
        self.body = Rectangle(p1, p2)
        self.label = Text(Point((p1.getX() + p2.getX()) / 2, (p1.getY() + p2.getY()) / 2), label)
        self.enabled = True

    def draw(self, window: GraphWin):
        self.body.draw(window)
        self.label.draw(window)
        win.items.append(self)

    def undraw(self):
        self.body.undraw()
        self.label.undraw()
        win.items.remove(self)

    def inside(self, click: Point) -> bool:
        p1x = min(self.body.getP1().getX(), self.body.getP2().getX())
        p1y = min(self.body.getP1().getY(), self.body.getP2().getY())
        p2x = max(self.body.getP1().getX(), self.body.getP2().getX())
        p2y = max(self.body.getP1().getY(), self.body.getP2().getY())
        return p1x < click.getX() < p2x and p1y < click.getY() < p2y


def draw_scene(window: GraphWin, scene: dict):
    if type(scene) == list:
        for obj in scene:
            if obj not in window.items:
                obj.draw(window)
    else:
        for obj in scene.values():
            if type(obj) != list:
                if obj not in window.items:
                    obj.draw(window)
            else:
                draw_scene(window, obj)

    win.tag_raise(exit_btn.body.id)
    win.tag_raise(exit_btn.label.id)


def undraw_scene(window: GraphWin, scene: dict):
    if type(scene) == list:
        for obj in scene:
            if obj in window.items:
                obj.undraw()
    else:
        for obj in scene.values():
            if type(obj) != list:
                if obj in window.items:
                    obj.undraw()
            else:
                undraw_scene(window, obj)


def start_game():
    for key in game_screen["keyboard"]:
        key.enabled = True
        key.body.setFill("white")
        key.label.setFill("black")

    game.guessed_letters.clear()
    game.guessed_words.clear()
    game.correct_letters = 0
    game_screen["guess_box"].setText("")

    game.word_guess_progress = len(game.current_word) * "-"
    game_screen["guess_progress"].setText(f"Word: {game.word_guess_progress}")
    game_screen["bridge"].setText(f"/{len(game.current_word) * '-'}\\")
    game_screen["player"].setText(f"{game.correct_letters * ' '} X"
                                  f" {(len(game.current_word) - game.correct_letters) * ' '}")

    game.lives = len(game.current_word)
    game_screen["lives_left"].setText(f"Lives left: {game.lives}")
    game_screen["hint_btn"].body.setFill(color_rgb(33, 151, 255))

    if game.difficulty == "easy":
        game.hints = int(len(game.current_word) / 2)
    elif game.difficulty == "medium":
        game.hints = int(len(game.current_word) / 3)
    elif game.difficulty == "hard":
        game.hints = 0
        game_screen["hint_btn"].body.setFill("gray")

    game_screen["hints_left"].setText(f"Hints left: {game.hints}")


def on_click(click):
    pt = Point(click.x, click.y)

    if exit_btn.inside(pt):
        win.quit()

    if game.current_scene == "start_menu":

        if start_menu["play_btn"].inside(pt):
            game.current_scene = "choose_difficulty_menu"
            draw_scene(win, choose_difficulty_menu)

        elif start_menu["tutorial_btn"].inside(pt):
            game.current_scene = "tutorial_scene"
            draw_scene(win, tutorial_scene)

    elif game.current_scene == "choose_difficulty_menu":

        if choose_difficulty_menu["easy"].inside(pt) or choose_difficulty_menu["medium"].inside(pt) or \
                choose_difficulty_menu["hard"].inside(pt):

            if choose_difficulty_menu["easy"].inside(pt):
                game.difficulty = "easy"
            elif choose_difficulty_menu["medium"].inside(pt):
                game.difficulty = "medium"
            elif choose_difficulty_menu["hard"].inside(pt):
                game.difficulty = "hard"

            undraw_scene(win, choose_difficulty_menu)
            draw_scene(win, choose_category_menu)
            game.current_scene = "choose_category_menu"

        elif choose_difficulty_menu["back"].inside(pt):

            undraw_scene(win, choose_difficulty_menu)
            draw_scene(win, start_menu)
            game.current_scene = "start_menu"

    elif game.current_scene == "choose_category_menu":

        if choose_category_menu["fruits"].inside(pt) or choose_category_menu["animals"].inside(pt) or \
                choose_category_menu["computer_science"].inside(pt) or choose_category_menu["sports"].inside(pt):

            if choose_category_menu["fruits"].inside(pt):
                game.category = "fruits"
            elif choose_category_menu["animals"].inside(pt):
                game.category = "animals"
            elif choose_category_menu["computer_science"].inside(pt):
                game.category = "computer_science"
            elif choose_category_menu["sports"].inside(pt):
                game.category = "sports"

            undraw_scene(win, choose_category_menu)
            draw_scene(win, game_screen)
            game.current_scene = "game_screen"
            game.current_word = random.choice(words[game.category])
            start_game()

        elif choose_category_menu["back"].inside(pt):

            undraw_scene(win, choose_category_menu)
            draw_scene(win, choose_difficulty_menu)
            game.current_scene = "choose_difficulty_menu"

    elif game.current_scene == "game_screen":

        if game_screen["new_game_btn"].inside(pt):

            undraw_scene(win, game_screen)
            draw_scene(win, choose_difficulty_menu)
            game.current_scene = "choose_difficulty_menu"

        elif game_screen["main_menu_btn"].inside(pt):

            undraw_scene(win, game_screen)
            draw_scene(win, start_menu)
            game.current_scene = "start_menu"

        elif game_screen["hint_btn"].inside(pt):

            if game.hints > 0:

                game.hints -= 1
                game_screen["hints_left"].setText(f"Hints left: {game.hints}")
                hint_letter = random.choice(list(set(game.current_word)))

                new_str = ""
                for j in range(len(game.current_word)):
                    if game.current_word[j].lower() == hint_letter:
                        new_str += hint_letter
                        game.correct_letters += 1
                    else:
                        new_str += game.word_guess_progress[j]

                game.word_guess_progress = new_str
                game_screen["guess_progress"].setText(f"Word: {game.word_guess_progress}")
                game_screen["player"].setText(f"{game.correct_letters * ' '} X"
                                              f" {(len(game.current_word) - game.correct_letters) * ' '}")

            if game.hints == 0:
                game_screen["hint_btn"].enabled = False
                game_screen["hint_btn"].body.setFill("gray")

        else:

            for key in game_screen["keyboard"]:

                if key.inside(pt) and key.label.getText() not in game.guessed_letters and key.enabled:

                    new_str = ""
                    key.body.setFill(color_rgb(148, 148, 148))
                    game.guessed_letters.append(key.label.getText())
                    game.guessed_letters.sort()
                    key.enabled = False

                    if key.label.getText().lower() in game.current_word.lower():

                        for j in range(len(game.current_word)):

                            if game.current_word[j].lower() == key.label.getText().lower():
                                new_str += key.label.getText().lower()
                                game.correct_letters += 1
                            else:
                                new_str += game.word_guess_progress[j]

                        game.word_guess_progress = new_str
                        game_screen["guess_progress"].setText(f"Word: {game.word_guess_progress}")
                        game_screen["player"].setText(f"{game.correct_letters * ' '} X"
                                                      f" {(len(game.current_word) - game.correct_letters) * ' '}")

                    else:

                        game.lives -= 1
                        game_screen["lives_left"].setText(f"Lives left: {game.lives}")
                        game_screen["bridge"].setText(f"/{'-' * game.lives}"
                                                      f"{'#' * (len(game.current_word) - game.lives)}\\")
                    break

            if game.word_guess_progress == game.current_word.lower():

                undraw_scene(win, game_screen)
                draw_scene(win, win_screen)
                game.current_scene = "win_screen"
                win_screen["answer"].setText(f"The word was: '{game.current_word}'")

            elif game.lives == 0:

                undraw_scene(win, game_screen)
                draw_scene(win, lose_screen)
                game.current_scene = "lose_screen"
                lose_screen["answer"].setText(f"The word was: '{game.current_word}'")

    elif game.current_scene == "win_screen":

        if win_screen["main_menu_btn"].inside(pt):
            undraw_scene(win, win_screen)
            draw_scene(win, start_menu)
            game.current_scene = "start_menu"
        elif win_screen["play_again_btn"].inside(pt):
            undraw_scene(win, win_screen)
            draw_scene(win, choose_difficulty_menu)
            game.current_scene = "choose_difficulty_menu"

    elif game.current_scene == "lose_screen":

        if lose_screen["main_menu_btn"].inside(pt):
            undraw_scene(win, lose_screen)
            draw_scene(win, start_menu)
            game.current_scene = "start_menu"
        elif lose_screen["play_again_btn"].inside(pt):
            undraw_scene(win, lose_screen)
            draw_scene(win, choose_difficulty_menu)
            game.current_scene = "choose_difficulty_menu"

    elif game.current_scene == "tutorial_scene":

        if tutorial_scene["back_btn"].inside(pt):
            undraw_scene(win, tutorial_scene)
            draw_scene(win, start_menu)
            game.current_scene = "start_menu"


def on_enter(event=None):
    if game.current_scene == "game_screen":

        if len(game_screen["guess_box"].getText()) == len(game.current_word) and \
                game_screen["guess_box"].getText().isalpha() and \
                game_screen["guess_box"].getText().lower() not in game.guessed_words:

            game.guessed_words.append(game_screen["guess_box"].getText().lower())

            if game_screen["guess_box"].getText().lower() == game.current_word.lower():

                undraw_scene(win, game_screen)
                draw_scene(win, win_screen)
                game.current_scene = "win_screen"
                win_screen["answer"].setText(f"The word was: '{game.current_word}'")

            else:

                game_screen["lives_left"].setText(f"Lives left: {game.lives}")
                game.lives -= 1
                game_screen["bridge"].setText(f"/{'-' * game.lives}"
                                              f"{'#' * (len(game.current_word) - game.lives)}\\")
                game_screen["guess_box"].setText("")
                game_screen["word_guess_text"].setText("Wrong guess!")

                if game.lives == 0:
                    undraw_scene(win, game_screen)
                    draw_scene(win, lose_screen)
                    game.current_scene = "lose_screen"
                    lose_screen["answer"].setText(f"The word was: '{game.current_word}'")

        elif game_screen["guess_box"].getText().isalpha() is False:
            game_screen["word_guess_text"].setText("Guess must only contain letters")

        elif len(game_screen["guess_box"].getText()) != len(game.current_word):
            game_screen["word_guess_text"].setText("Length of the word was too short or too long")

        elif game_screen["guess_box"].getText().lower() in game.guessed_words:
            game_screen["word_guess_text"].setText("You have already guessed this word")


win = GraphWin("Bridge Word Game", 1280, 720)

exit_btn = Button(Point(0, 0), Point(50, 50), "X")
exit_btn.body.setFill("red")
exit_btn.label.setFill("white")
exit_btn.label.setSize(20)
exit_btn.label.setStyle("bold")
exit_btn.draw(win)

start_menu = dict()

start_menu["bg"] = Image(Point(640, 360), "./images/start_bg.png")

start_menu["name"] = Text(Point(640, 150), "Bridge Word Game")
start_menu["name"].setSize(36)
start_menu["name"].setStyle("bold")

start_menu["play_btn"] = Button(Point(500, 350), Point(780, 450), "Play")
start_menu["play_btn"].body.setFill("white")
start_menu["play_btn"].label.setSize(36)

start_menu["tutorial_btn"] = Button(Point(500, 500), Point(780, 600), "Tutorial")
start_menu["tutorial_btn"].body.setFill("white")
start_menu["tutorial_btn"].label.setSize(36)
start_menu["tutorial_btn"].body.setFill("orange")

choose_difficulty_menu = dict()

choose_difficulty_menu["bg"] = Image(Point(640, 360), "./images/choose_diff_bg.png")

choose_difficulty_menu["choose_text"] = Text(Point(640, 200), "Choose a difficulty")
choose_difficulty_menu["choose_text"].setSize(36)
choose_difficulty_menu["choose_text"].setStyle("bold")
choose_difficulty_menu["choose_text"].setTextColor("white")

choose_difficulty_menu["easy"] = Button(Point(240, 350), Point(440, 450), "Easy")
choose_difficulty_menu["easy"].body.setFill("green")
choose_difficulty_menu["easy"].label.setSize(36)

choose_difficulty_menu["medium"] = Button(Point(540, 350), Point(740, 450), "Medium")
choose_difficulty_menu["medium"].body.setFill("yellow")
choose_difficulty_menu["medium"].label.setSize(36)

choose_difficulty_menu["hard"] = Button(Point(840, 350), Point(1040, 450), "Hard")
choose_difficulty_menu["hard"].body.setFill("red")
choose_difficulty_menu["hard"].label.setSize(36)

choose_difficulty_menu["back"] = Button(Point(0, 620), Point(200, 720), "Back")
choose_difficulty_menu["back"].body.setFill("white")
choose_difficulty_menu["back"].label.setSize(36)

choose_category_menu = dict()

choose_category_menu["bg"] = Image(Point(640, 360), "./images/choose_cat_bg.png")

choose_category_menu["choose_text"] = Text(Point(640, 200), "Choose a category")
choose_category_menu["choose_text"].setSize(36)
choose_category_menu["choose_text"].setStyle("bold")
choose_category_menu["choose_text"].setTextColor("white")

choose_category_menu["animals"] = Button(Point(90, 350), Point(290, 450), "Animals")
choose_category_menu["animals"].body.setFill("white")
choose_category_menu["animals"].label.setSize(36)

choose_category_menu["fruits"] = Button(Point(390, 350), Point(590, 450), "Fruits")
choose_category_menu["fruits"].body.setFill("white")
choose_category_menu["fruits"].label.setSize(36)

choose_category_menu["computer_science"] = Button(Point(690, 350), Point(890, 450), "Computer Science")
choose_category_menu["computer_science"].body.setFill("white")
choose_category_menu["computer_science"].label.setSize(16)

choose_category_menu["sports"] = Button(Point(990, 350), Point(1190, 450), "Sports")
choose_category_menu["sports"].body.setFill("white")
choose_category_menu["sports"].label.setSize(36)

choose_category_menu["back"] = Button(Point(0, 620), Point(200, 720), "Back")
choose_category_menu["back"].body.setFill("white")
choose_category_menu["back"].label.setSize(36)

game_screen = dict()

game_screen["bg"] = Image(Point(640, 360), "./images/play_bg_1.png")

game_screen["new_game_btn"] = Button(Point(0, 100), Point(200, 200), "New Game")
game_screen["new_game_btn"].body.setFill(color_rgb(8, 255, 107))
game_screen["new_game_btn"].label.setSize(24)

alphabet_qwerty = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "A", "S", "D", "F", "G", "H", "J", "K", "L", "Z",
                   "X", "C", "V", "B", "N", "M"]

game_screen["keyboard"] = list()

for i in range(10):
    game_screen["keyboard"].append(Button(Point(390 + (i * 50), 450), Point(440 + (i * 50), 500), alphabet_qwerty[i]))
    game_screen["keyboard"][i].body.setFill("white")
    game_screen["keyboard"][i].label.setSize(16)
    game_screen["keyboard"][i].label.setStyle("bold")

for i in range(9):
    game_screen["keyboard"].append(
        Button(Point(415 + (i * 50), 500), Point(465 + (i * 50), 550), alphabet_qwerty[i + 10]))
    game_screen["keyboard"][i + 10].body.setFill("white")
    game_screen["keyboard"][i + 10].label.setSize(16)
    game_screen["keyboard"][i + 10].label.setStyle("bold")

for i in range(7):
    game_screen["keyboard"].append(Button(Point(430 + (i * 50), 550), Point(480 + (i * 50), 600),
                                          alphabet_qwerty[i + 19]))
    game_screen["keyboard"][i + 19].body.setFill("white")
    game_screen["keyboard"][i + 19].label.setSize(16)
    game_screen["keyboard"][i + 19].label.setStyle("bold")

game_screen["guess_box"] = Entry(Point(1000, 150), 15)
game_screen["guess_box"].setFace("courier")
game_screen["guess_box"].setSize(24)
game_screen["guess_box"].setFill("white")

words = {"fruits": ["apple", "banana", "orange", "grape", "watermelon"],
         "animals": ["dog", "cat", "bird", "fish", "rabbit"],
         "computer_science": ["python", "string", "integer", "java", "binary"],
         "sports": ["soccer", "basketball", "baseball", "tennis", "volleyball"]}

game = Game()

game_screen["word_guess_text"] = Text(Point(1000, 100), "Guess the entire word:")
game_screen["word_guess_text"].setSize(16)
game_screen["word_guess_text"].setStyle("bold")
game_screen["word_guess_text"].setTextColor("white")

game_screen["bridge"] = Text(Point(640, 300), f"/{len(game.current_word) * '-'}\\")
game_screen["bridge"].setSize(36)
game_screen["bridge"].setStyle("bold")
game_screen["bridge"].setFace("courier")
game_screen["bridge"].setTextColor("white")

game_screen["player"] = Text(Point(640, 250), f"{' ' * game.correct_letters}X"
                                              f"{' ' * (len(game.current_word) - game.correct_letters)}")
game_screen["player"].setSize(36)
game_screen["player"].setStyle("bold")
game_screen["player"].setFace("courier")
game_screen["player"].setTextColor("white")

game_screen["guess_progress"] = Text(Point(1000, 380), f"Word: {game.word_guess_progress}")
game_screen["guess_progress"].setSize(24)
game_screen["guess_progress"].setStyle("bold")
game_screen["guess_progress"].setFace("courier")
game_screen["guess_progress"].setTextColor("white")

game_screen["lives_left"] = Text(Point(1100, 500), f"Lives Left: {game.lives}")
game_screen["lives_left"].setSize(24)
game_screen["lives_left"].setStyle("bold")
game_screen["lives_left"].setFace("courier")
game_screen["lives_left"].setTextColor("white")

game_screen["hints_left"] = Text(Point(1100, 550), f"Hints Left: {game.hints}")
game_screen["hints_left"].setSize(24)
game_screen["hints_left"].setStyle("bold")
game_screen["hints_left"].setFace("courier")
game_screen["hints_left"].setTextColor("white")

game_screen["hint_btn"] = Button(Point(0, 300), Point(200, 400), "Hint")
game_screen["hint_btn"].body.setFill(color_rgb(33, 151, 255))
game_screen["hint_btn"].label.setSize(24)

game_screen["main_menu_btn"] = Button(Point(0, 500), Point(200, 600), "Exit To Main Menu")
game_screen["main_menu_btn"].body.setFill(color_rgb(255, 255, 255))
game_screen["main_menu_btn"].label.setSize(16)

win_screen = dict()

win_screen["bg"] = Image(Point(640, 360), "./images/win_bg.png")

win_screen["win_text_bg"] = Rectangle(Point(500, 320), Point(780, 400))
win_screen["win_text_bg"].setFill("white")

win_screen["win_text"] = Text(Point(640, 360), "You Win!")
win_screen["win_text"].setSize(36)
win_screen["win_text"].setStyle("bold")
win_screen["win_text"].setTextColor("black")

win_screen["main_menu_btn"] = Button(Point(480, 500), Point(800, 600), "Main Menu")
win_screen["main_menu_btn"].body.setFill("white")
win_screen["main_menu_btn"].label.setSize(36)

win_screen["answer_bg"] = Rectangle(Point(300, 200), Point(980, 300))
win_screen["answer_bg"].setFill("white")

win_screen["answer"] = Text(Point(640, 250), f"The word was {game.current_word}")
win_screen["answer"].setSize(24)
win_screen["answer"].setStyle("bold")
win_screen["answer"].setTextColor("black")

win_screen["play_again_btn"] = Button(Point(100, 500), Point(400, 600), "Play Again")
win_screen["play_again_btn"].body.setFill("green")
win_screen["play_again_btn"].label.setSize(36)

lose_screen = dict()

lose_screen["bg"] = Image(Point(640, 360), "./images/lose_bg.png")

lose_screen["lose_text_bg"] = Rectangle(Point(500, 320), Point(780, 400))
lose_screen["lose_text_bg"].setFill("white")

lose_screen["lose_text"] = Text(Point(640, 360), "You Lose!")
lose_screen["lose_text"].setSize(36)
lose_screen["lose_text"].setStyle("bold")
lose_screen["lose_text"].setTextColor("black")

lose_screen["main_menu_btn"] = Button(Point(480, 500), Point(800, 600), "Main Menu")
lose_screen["main_menu_btn"].body.setFill("white")
lose_screen["main_menu_btn"].label.setSize(36)

lose_screen["answer_bg"] = Rectangle(Point(300, 200), Point(980, 300))
lose_screen["answer_bg"].setFill("white")

lose_screen["answer"] = Text(Point(640, 250), f"The word was: '{game.current_word}'")
lose_screen["answer"].setSize(24)
lose_screen["answer"].setStyle("bold")
lose_screen["answer"].setTextColor("black")

lose_screen["play_again_btn"] = Button(Point(100, 500), Point(400, 600), "Play Again")
lose_screen["play_again_btn"].body.setFill("green")
lose_screen["play_again_btn"].label.setSize(36)

tutorial_scene = dict()

tutorial_scene["bg"] = Image(Point(640, 360), "./images/tutorial_bg.png")

tutorial_scene["back_btn"] = Button(Point(0, 200), Point(200, 300), "Back")
tutorial_scene["back_btn"].body.setFill(color_rgb(255, 255, 255))
tutorial_scene["back_btn"].label.setSize(24)

tutorial_scene["text_bg"] = Rectangle(Point(0, 500), Point(1280, 720))
tutorial_scene["text_bg"].setFill("white")

tutorial_scene["tutorial_text"] = Text(Point(640, 600), game.tutorial_text[0])
tutorial_scene["tutorial_text"].setSize(24)
tutorial_scene["tutorial_text"].setStyle("bold")

tutorial_scene["forward_btn"] = Button(Point(1180, 450), Point(1280, 500), "->")
tutorial_scene["forward_btn"].body.setFill(color_rgb(0, 255, 0))
tutorial_scene["forward_btn"].label.setSize(24)

tutorial_scene["backwards_btn"] = Button(Point(0, 450), Point(100, 500), "<-")
tutorial_scene["backwards_btn"].body.setFill("gray")
tutorial_scene["backwards_btn"].label.setSize(24)

draw_scene(win, start_menu)

win.bind_all("<Button-1>", on_click)
win.bind_all("<Return>", on_enter)

win.mainloop()
