from tkinter import *
import pandas
from random import choice

BACKGROUND_COLOR = "white"
FONT = "Ariel"

curr_word = {}


# Flips the card
def flip_card():
    global curr_word
    canvas.itemconfig(canvas_image, image=image_back)
    canvas.itemconfig(title_tag, text="English", fill="white")
    canvas.itemconfig(word_tag, text=f"{curr_word['English']}", fill="white")


# Move on to the next word in the list
def next_card():
    global curr_word, flip_timer
    window.after_cancel(flip_timer)
    curr_word = choice(data)
    word_fr = curr_word["French"]
    canvas.itemconfig(canvas_image, image=image_front)
    canvas.itemconfig(title_tag, text="French", fill="white")
    canvas.itemconfig(word_tag, text=f"{word_fr}", fill="white")
    flip_timer = window.after(3000, func=flip_card)


# Remove the curr_word from the list of words to learn
def remove_word():
    data.remove(curr_word)

# Save all the words in the data into data/words_to_learn.csv
def save_words():
    new_words_list = pandas.DataFrame(data)
    new_words_list.to_csv("data/words_to_learn.csv", index=False)


# Screen
window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, flip_card)
# GUI
image_right = PhotoImage(file="images/right.png")
image_wrong = PhotoImage(file="images/wrong.png")
image_front = PhotoImage(file="images/card_front.png")
image_back = PhotoImage(file="images/card_back.png")
image_flip = PhotoImage(file="images/rotate.png")
image_plus = PhotoImage(file="images/plus.png")

canvas = Canvas(width=800, height=526)
canvas_image = canvas.create_image(400, 263, image=image_front)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=1, column=1, columnspan=2)

title_tag = canvas.create_text(400, 150, text="French", font=(FONT, 40, "italic"))
word_tag = canvas.create_text(400, 275, text="Word", font=(FONT, 60, "bold"))

button_wrong = Button(image=image_wrong, command=lambda: [save_words(), next_card()])
button_wrong.config(bg=BACKGROUND_COLOR, highlightthickness=0)
button_wrong.grid(row=2, column=1)

button_correct = Button(image=image_right, command=lambda: [remove_word(), save_words(), next_card()])
button_correct.config(bg=BACKGROUND_COLOR, highlightthickness=0)
button_correct.grid(row=2, column=2)

button_flip = Button(image=image_flip)
button_flip.config(highlightthickness=0)
button_flip.grid(row=0, column=3)

button_add = Button(image=image_plus)
button_add.config(highlightthickness=0)
button_add.grid(row=0, column=0)

# Get the words from data/words_to_learn.csv if exists
# Or else, get the words from data/french_words.csv
try:
    data = pandas.read_csv("data/words_to_learn.csv").to_dict(orient="records")
except FileNotFoundError or pandas.errors.EmptyDataError:
    data = pandas.read_csv("data/french_words.csv").to_dict(orient="records")
finally:
    next_card()

window.mainloop()
