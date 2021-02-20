from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Arial"
RELIEF = "flat"
blank_space = " "
current_card = {}
to_learn = {}
# ---------------------------- Random word ------------------------------- #
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words2.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    # orient records, each column value as a list
    to_learn = data.to_dict(orient='records')


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card['French'], fill="black")
    canvas.itemconfig(canvas_image, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)

# ---------------------------- Flip cards -------------------------------- #


def flip_card():

    canvas.itemconfig(canvas_image, image=card_back_img)
    canvas.itemconfig(card_title, fill="white", text="Spanish")
    canvas.itemconfig(card_word, fill="white", text=current_card['Spanish'])
    # window.after(3000, next_card)


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

# ---------------------------- UI SETUP ---------------------------------- #


window = Tk()
window.title(130 * blank_space + "Flash cards!")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_back_img = PhotoImage(file="images/card_back.png")
card_front_img = PhotoImage(file="images/card_front.png")
canvas_image = canvas.create_image(400, 263, image=card_front_img)
canvas.grid(column=0, row=0, columnspan=2)

card_title = canvas.create_text(400, 150, text="", font=(FONT_NAME, 30, "italic"))
card_word = canvas.create_text(400, 263, text="", font=(FONT_NAME, 50, "bold"))

check_image = PhotoImage(file="images/right.png")
cross_image = PhotoImage(file="images/wrong.png")

known_button = Button(image=check_image, highlightthickness=0, relief=RELIEF, borderwidth=0, command=is_known)
known_button.grid(column=1, row=1)

unknown_button = Button(image=cross_image, highlightthickness=0, relief=RELIEF, borderwidth=0, command=next_card)
unknown_button.grid(column=0, row=1)

next_card()

window.mainloop()
