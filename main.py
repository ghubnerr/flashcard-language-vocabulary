from tkinter import *
import pandas as pd
from tkinter import ttk
from tkinter import messagebox
import random

# ---------------------------- Constants  -------------------------- #
SELECT_SCREEN_SIZE = "536x400"

BG_COLOR = "#6FEDDF"
CARD_BG = "#E2FFE9"
FONT1 = "Arial"
FONT2 = "Euphemia"
LANGUAGES = ['Afrikaans', 'Arabic', 'Bulgarian', 'Bosnian', 'Catalan', 'Czech', 'Danish', 'German', 'Greek', 'English',
             'Esperanto', 'Spanish', 'Estonian', 'Basque', 'Persian', 'Finnish', 'French', 'Galician', 'Hebrew',
             'Croatian', 'Hungarian', 'Armenian', 'Indonesian', 'Icelandic', 'Italian', 'Japanese', 'Georgian',
             'Kazakh', 'Korean', 'Italian', 'Latvian', 'Macedonian', 'Malay', 'Dutch', 'Norwegian', 'Polish',
             'Portuguese', 'Brazilian Portuguese', 'Romanian', 'Russian', 'Slovak', 'Slovenian', 'Albanian', 'Serbian',
             'Swedish', 'Thai', 'Tagalog', 'Turkish', 'Urdu', 'Vietnamese']

language_1 = "none"
language_2 = "none"

next_screen_valid = False

current_word = ""


# ---------------------------- Database SETUP ------------------------------- #
df = pd.read_csv('./words-database.csv')
df.columns = ['Afrikaans', 'Arabic', 'Bulgarian', 'Bosnian', 'Catalan', 'Czech', 'Danish', 'German', 'Greek', 'English',
              'Esperanto', 'Spanish', 'Estonian', 'Basque', 'Persian', 'Finnish', 'French', 'Galician', 'Hebrew',
              'Croatian', 'Hungarian', 'Armenian', 'Indonesian', 'Icelandic', 'Italian', 'Japanese', 'Georgian',
              'Kazakh', 'Korean', 'Italian', 'Latvian', 'Macedonian', 'Malay', 'Dutch', 'Norwegian', 'Polish',
              'Portuguese', 'Brazilian Portuguese', 'Romanian', 'Russian', 'Slovak', 'Slovenian', 'Albanian', 'Serbian',
              'Swedish', 'Thai', 'Tagalog', 'Turkish', 'Urdu', 'Vietnamese']


# ---------------------------- Game Functionality ------------------------------- #
def change_flashcard():
    """Selects a random word from language_1 vocabulary and changes the card to it"""

    global current_word, flip_timer
    main_window.after_cancel(flip_timer)

    current_word = random.choice(df[language_1].values)
    canvas.itemconfig(card_title, text=language_1, fill="black")
    canvas.itemconfig(card_word, text=current_word, fill="black")
    canvas.itemconfig(card_background, image=front_image)
    flip_timer = main_window.after(1500, flip_card)


def flip_card():
    """Shows the translation of the word into the selected language"""
    canvas.itemconfig(card_title, text=language_2, fill="white")
    translation_word = df[df[language_1] == current_word][language_2].values[0]
    canvas.itemconfig(card_word, text=translation_word, fill="white")
    canvas.itemconfig(card_background, image=back_image)


# TODO: Setup buttons and functions
# TODO: Flashcard reveal // add or remove from list of words with buttons

# ---------------------------- Vocabulary Tracker  ------------------------------- #

# TODO: Keep track of words learned inside a JSON file with "language" / "word" / "translation"
# TODO: Different commit: More languages and keeps track of words known. Restart option.


# ---------------------------- Initial UI SETUP ------------------------------- #
# Root Setup
selection_screen = Tk()
selection_screen.title("Select your Language")
selection_screen.config(padx=50, pady=30, bg=BG_COLOR)
selection_screen.geometry(SELECT_SCREEN_SIZE)

# Canvas Widget with Image
selection_canvas = Canvas(width=456, height=178, highlightthickness=0, background=BG_COLOR)
selection_canvas.config()
image = PhotoImage(file="./images/select-language-card.png")
selection_canvas.create_image(228, 89, image=image)
panel_text = selection_canvas.create_text(228, 89, text="Select Languages", fill="black", font=(FONT1, 15, "normal"))

# Labels for selection
from_language_label = Label(text='I want to practice:', background=BG_COLOR, font=(FONT2, 14, "normal"), padx=30)
to_language_label = Label(text='I speak:', background=BG_COLOR, font=(FONT2, 14, "normal"), padx=30)


def append_text_1(*args):
    """Renames Card based on first selection"""
    current_text = selection_canvas.itemcget(panel_text, "text")
    if current_text == "Select Languages":
        selection_canvas.itemconfig(panel_text, text=f"{option_var1.get()} to ")

    # Checking for existent text
    elif 'to' in current_text:
        try:
            other_language = current_text.split(' ')[2]
        except IndexError:
            selection_canvas.itemconfig(panel_text, text=f"{option_var1.get()} to ")
        else:
            selection_canvas.itemconfig(panel_text, text=f"{option_var1.get()} to {other_language}")
    else:
        new_text = f"{option_var1.get()} to {current_text}"
        selection_canvas.itemconfig(panel_text, text=new_text)


def append_text_2(*args):
    """Renames Card based on second selection"""
    current_text = selection_canvas.itemcget(panel_text, "text")
    if current_text == "Select Languages":
        selection_canvas.itemconfig(panel_text, text=f"{option_var2.get()}")
    else:
        new_text = f"{current_text.split(' ')[0] + ' ' + current_text.split(' ')[1]} {option_var2.get()}"
        selection_canvas.itemconfig(panel_text, text=new_text)


# String Variable objects for Object Menu
option_var1 = StringVar()
option_var2 = StringVar()

# Object Menus Creation
from_option_menu = ttk.OptionMenu(selection_screen, option_var1, 'Select', *sorted(LANGUAGES), command=append_text_1)
to_option_menu = ttk.OptionMenu(selection_screen, option_var2, 'Select', 'English', command=append_text_2)


def close_selection():
    """Checks selections and closes window, validating that the next screen may appear"""
    # Setting Up Languages
    global language_1, language_2
    language_1 = option_var1.get()
    language_2 = option_var2.get()
    # Dialog Box and Pop-up -- Checking Selection
    if language_1 == "Select" or language_2 == "Select":
        messagebox.showinfo(title="Error", message="Please select a language")
    elif language_1 == language_2:
        messagebox.showinfo(title="Error", message="Please select different languages")
    else:
        global next_screen_valid
        next_screen_valid = True
        selection_screen.destroy()


# Go Button
go_button_image = PhotoImage(file="./images/go-button.png")
go_button = Button(padx=0, pady=0, image=go_button_image, highlightthickness=0, background=BG_COLOR, bd=0,
                   activebackground=BG_COLOR, command=close_selection)

# Placing elements on grid
selection_canvas.grid(row=0, column=0, columnspan=2)
from_language_label.grid(row=1, column=0, sticky="w")
to_language_label.grid(row=2, column=0, sticky="w")
from_option_menu.grid(row=1, column=1, sticky="w")
to_option_menu.grid(row=2, column=1, sticky="w")
go_button.grid(row=3, column=0, columnspan=2)

# Formatting Rows
selection_screen.rowconfigure(1, minsize=35)
selection_screen.rowconfigure(2, minsize=35)

# Centering Window
selection_screen.eval("tk::PlaceWindow . center")

selection_screen.mainloop()

# ---------------------------- Post-selection SETUP ------------------------------- #
if next_screen_valid:  # If the languages were properly selected

    start_text = df[df['French'] == 'commencer'][language_1].values[0]
    current_word = start_text

    # Main Root Setup
    main_window = Tk()
    main_window.title("Vocabulary Flashcard")
    main_window.config(padx=10, pady=30, bg=BG_COLOR)

    flip_timer = main_window.after(5000, flip_card)

    # Creating Card Canvas with Image
    canvas = Canvas(width=448, height=330, highlightthickness=0, background=BG_COLOR)
    front_image = PhotoImage(file="./images/card.png")
    back_image = PhotoImage(file="./images/flipped-card.png")
    card_background = canvas.create_image(224, 165, image=front_image)
    card_title = canvas.create_text(224, 95, text=language_1, font=("Arial", 14, "italic"))
    card_word = canvas.create_text(224, 165, text=start_text.lower(), font=("Arial", 30, "normal"))

    # Buttons
    red_button_image = PhotoImage(file="./images/button-red.png")
    red_button = Button(padx=0, pady=0, image=red_button_image, highlightthickness=0, background=BG_COLOR, bd=0,
                        activebackground=BG_COLOR, command=change_flashcard)
    green_button_image = PhotoImage(file="./images/button-green.png")
    green_button = Button(padx=0, pady=0, image=green_button_image, highlightthickness=0, background=BG_COLOR, bd=0,
                          activebackground=BG_COLOR, command=change_flashcard)

    # Flag Icons
    flag_left_image = PhotoImage(file="./images/empty-flag.png")
    flag_left_label = Label(image=flag_left_image, background=BG_COLOR)

    flag_right_image = PhotoImage(file="./images/en-flag.png")
    flag_right_label = Label(image=flag_right_image, background=BG_COLOR)

    # Placing elements on Grid
    canvas.grid(row=0, column=1, columnspan=2, rowspan=3)
    red_button.grid(row=3, column=1)
    green_button.grid(row=3, column=2)
    flag_left_label.grid(row=1, column=0)
    flag_right_label.grid(row=1, column=3)

    # Centering window on screen
    main_window.eval("tk::PlaceWindow . center")

    main_window.mainloop()

# TODO: Improve Modularity
# TODO: Enhance ttk styling with inheritance
# TODO: Improve overall UX
