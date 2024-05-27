from tkinter import *
import pandas
from random import choice

BACKGROUND_COLOR = "#B1DDC6"
FONT = "Ariel"


def next_card():
	curr_word = choice(data)
	word_fr = curr_word["French"]
	canvas.itemconfig(title_tag, text="French")
	canvas.itemconfig(word_tag, text=f"{word_fr}")


# Get words from csv data
data = pandas.read_csv("data/french_words.csv").to_dict(orient="records")

# Screen
window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# GUI
image_right = PhotoImage(file="images/right.png")
image_wrong = PhotoImage(file="images/wrong.png")
image_front = PhotoImage(file="images/card_front.png")
image_back = PhotoImage(file="images/card_back.png")

canvas = Canvas(width=800, height=526)
canvas.create_image(400, 263, image=image_front)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

title_tag = canvas.create_text(400, 150, text="French", font=(FONT, 40, "italic"))
word_tag = canvas.create_text(400, 275, text="Word", font=(FONT, 60, "bold"))

button_wrong = Button(image=image_wrong, command=next_card)
button_wrong.config(bg=BACKGROUND_COLOR, highlightthickness=0)
button_wrong.grid(row=1, column=0)

button_correct = Button(image=image_right, command=next_card)
button_correct.config(bg=BACKGROUND_COLOR, highlightthickness=0)
button_correct.grid(row=1, column=1)

next_card()

window.mainloop()
