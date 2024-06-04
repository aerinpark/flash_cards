from tkinter import *
from tkinter import messagebox
import pandas
from random import choice

BACKGROUND_COLOR = "white"
FONT = "Ariel"

curr_word = {}
not_memorized = []
memorized = []
original_list = []
front = True


# Flips the card between 'word' and 'definition'
def flip_card():
    global curr_word, front
    if front:
        canvas.itemconfig(canvas_image, image=image_back)
        canvas.itemconfig(title_tag, text="Definition", fill="white")
        if curr_word == "":
            canvas.itemconfig(word_tag, text="", fill="white")
        else:
            canvas.itemconfig(word_tag, text=f"{curr_word['Definition']}", fill="white")
        front = False
    else:
        canvas.itemconfig(canvas_image, image=image_front)
        canvas.itemconfig(title_tag, text="Word", fill="white")
        if curr_word == "":
            canvas.itemconfig(word_tag, text="", fill="white")
        else:
            canvas.itemconfig(word_tag, text=f"{curr_word['Word']}", fill="white")
        front = True


# Add a new word to the original_word_list.csv
# A popup window will appear for user inputs on new word and its definition
def add_new_word():
    input_popup = Toplevel()
    input_popup.title("New word")
    input_popup.config(padx=20, pady=20)

    label = Label(input_popup, text="Enter a new word: ", font=(FONT, 15, "bold"))
    label.grid(row=0, column=0)

    tag_word = Label(input_popup, text="Word: ")
    tag_word.grid(row=1, column=0)
    entry_word = Entry(input_popup)
    entry_word.focus()
    entry_word.grid(row=1, column=1)

    tag_def = Label(input_popup, text="Definition: ")
    tag_def.grid(row=2, column=0)
    entry_def = Entry(input_popup)
    entry_def.grid(row=2, column=1)

    # The word is saved to the file 'original_word_list.csv' if ok clicked
    def word_added():
        global original_list
        if entry_def.get() == "" or entry_def.get() == "":
            messagebox.showerror(title="Error", message="Entry box(es) cannot be empty.")
            add_new_word()
            return
        new_word = {'Word': entry_word.get(),
                    'Definition': entry_def.get()}
        not_memorized.append(new_word)
        messagebox.showinfo(title="Success", message=f"Your word ({entry_word.get()}) has been saved Hsuccessfully.")
        original_list = not_memorized

        # Update original_word_list.csv
        new_word_list = pandas.DataFrame(original_list)
        new_word_list.to_csv("data/original_word_list.csv", index=False)

        next_card()

    # Cancel and destroy the popup window when 'cancel' is clicked.
    def destroyed():
        input_popup.destroy()

    button_ok = Button(input_popup, text="OK", width=7, command=lambda: [word_added(), destroyed()])
    button_ok.grid(row=3, column=0)

    button_cancel = Button(input_popup, text="CANCEL", width=7, command=destroyed)
    button_cancel.grid(row=3, column=1)


# Move on to the next word in the list
def next_card():
    global curr_word

    canvas.itemconfig(canvas_image, image=image_front)
    if len(not_memorized) != 0:
        curr_word = choice(not_memorized)
        word = curr_word['Word']
        canvas.itemconfig(title_tag, text="Word", fill="white")
        canvas.itemconfig(word_tag, text=f"{word}", fill="white")
    else:
        curr_word = {}
        canvas.itemconfig(title_tag, text="", fill="white")
        canvas.itemconfig(word_tag, text="", fill="white")


# Remove the curr_word from the list of words to learn
def remove_word():
    not_memorized.remove(curr_word)
    memorized.append(curr_word)
    memorized_file = pandas.DataFrame(memorized)
    memorized_file.to_csv("data/words_memorized.csv", index=False)


# Save all the words in the data into data/words_to_learn.csv
def save_words():
    not_memorized_file = pandas.DataFrame(not_memorized)
    not_memorized_file.to_csv("data/words_to_learn.csv", index=False)


# Screen
window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
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

title_tag = canvas.create_text(400, 150, text="Word", font=(FONT, 40, "italic"))
word_tag = canvas.create_text(400, 275, text="Word", font=(FONT, 60, "bold"))

button_wrong = Button(image=image_wrong, command=lambda: [save_words(), next_card()])
button_wrong.config(bg=BACKGROUND_COLOR, highlightthickness=0)
button_wrong.grid(row=2, column=1)

button_correct = Button(image=image_right, command=lambda: [remove_word(), save_words(), next_card()])
button_correct.config(bg=BACKGROUND_COLOR, highlightthickness=0)
button_correct.grid(row=2, column=2)

button_flip = Button(image=image_flip, command=flip_card)
button_flip.config(highlightthickness=0)
button_flip.grid(row=0, column=3)

button_add = Button(image=image_plus, command=add_new_word)
button_add.config(highlightthickness=0)
button_add.grid(row=0, column=0)

# Get the words from data/words_to_learn.csv if exists
# Or else, get the words from data/Word_words.csv
try:
    not_memorized = pandas.read_csv("data/words_to_learn.csv").to_dict(orient="records")
except (FileNotFoundError, pandas.errors.EmptyDataError):
    try:
        not_memorized = pandas.read_csv("data/original_word_list.csv").to_dict(orient="records")
        original_list = not_memorized
    except (FileNotFoundError, pandas.errors.EmptyDataError):
        add_new_word()
    else:
        next_card()
else:
    next_card()

window.mainloop()
