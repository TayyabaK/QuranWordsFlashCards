from tkinter import *
from tkinter import messagebox
import random
import json
from collections import namedtuple

Word = namedtuple("Word","Arabic English")

file = open("unknown_words.json","r")
unknown_words= json.load(file)

try:
    file = open("known_words.json","r")
    known_words = json.load(file)
except:
    known_words = {}

# --------------------------------------------------------------
current_side = "front"
current_word = None

def select_random_word():
    global  current_word
    arabic , english = random.choice(list(unknown_words.items()))
    current_word = Word(Arabic = arabic , English = english)

def flip_card(event=None):
    global current_side, current_word
    if current_side == "front":
        canvas.itemconfig(img_card, image=img_back)
        canvas.itemconfig(card_title, text="English", fill="white")
        canvas.itemconfig(card_word, text=f"{current_word.English}", fill="white")
        current_side = "back"
    else:
        canvas.itemconfig(card_title, text="Arabic", fill="black")
        canvas.itemconfig(card_word, text=f"{current_word.Arabic}", fill="black")
        canvas.itemconfig(img_card, image=img_front)
        current_side = "front"

def show_card():
    global current_word, flip_timer, current_side
    window.after_cancel(flip_timer)
    select_random_word()
    current_side = "back"
    flip_timer = window.after(2000, func=flip_card)
    flip_card()

def btn_wrong_click():
    show_card()


def btn_right_click():
    global current_word, flip_timer, current_side, known_words
    window.after_cancel(flip_timer)
    known_words[current_word.Arabic] = current_word.English
    del unknown_words[current_word.Arabic]
    current_side = "front"
    show_card()

def save_files():
    file = open("unknown_words.json", "w")
    json.dump(unknown_words, file)

    file = open("known_words.json", "w")
    json.dump(known_words, file)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        save_files()
        window.destroy()


# -------------------------GUI------------------------------
BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.title("Memory Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

window.protocol("WM_DELETE_WINDOW", on_closing)

flip_timer = window.after(2000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
img_front = PhotoImage(file="images/card_front.png")
img_card = canvas.create_image(415, 270, image=img_front)
canvas.grid(row=0, column=0, columnspan=2)
canvas.tag_bind(img_card,'<Button-1>', func=flip_card)

select_random_word()

img_back = PhotoImage(file="images/card_back.png")

card_title = canvas.create_text(400, 150, text="Arabic", font=("Arial", 30, "italic"), fill="black")
card_word = canvas.create_text(400, 263, text="word", font=("Arial", 40, "bold"), fill="black")

show_card()

img_wrong = PhotoImage(file="images/wrong.png")
btn_wrong = Button(image=img_wrong, highlightthickness=0, command=btn_wrong_click)
btn_wrong.grid(row=1, column=0)

img_right = PhotoImage(file="images/right.png")
btn_right = Button(image=img_right, highlightthickness=0, command=btn_right_click)
btn_right.grid(row=1, column=1)

window.mainloop()
