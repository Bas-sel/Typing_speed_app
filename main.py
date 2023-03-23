from tkinter import *
from tkinter import ttk
import random

# GET THE TEXT TO BE WRITTEN FROM A TEXT FILE
with open('text.txt', mode='r') as file:
    data = list(set(file.readlines(-1)))
    data.remove('\n')

root = Tk()
root.configure(bg='red')
root.title("Feet to Meters")

total_key_pressed = 0
char_index = 0
typed_chars = []


def on_key_press(event):
    global char_index, total_key_pressed

    # CLEAR ENTERED TEXT WHEN USER PRESS SPACE
    if event.char == ' ':
        typed_chars.clear()
        text_entry.delete('1.0', 'end')

    # REDUCE TEXT CHARACTER INDEX WHEN PRESS BACKSPACE
    if event.char == '\x08' and char_index > 0:
        char_index -= 1

    # COMPARE ENTERED CHARACTERS WITH TEXT CHARACTERS
    elif event.char != '\x08' and event.char != ' ':
        tag = f'tag{char_index}'
        typed_chars.append(event.char)
        if text.get(f'1.{char_index}') == ' ':
            char_index += 1

        if typed_chars[-1] == text.get(f'1.{char_index}'):

            # START POINT
            if starting_time == 60:
                time_manager()

            text.tag_add(tag, f"1.{char_index}",
                         f"1.{char_index + 1}")
            text.tag_configure(tag, foreground='white')
            total_key_pressed += 1

        elif typed_chars[-1] != text.get(f'1.{char_index}'):
            text.tag_add(tag, f"1.{char_index}",
                         f"1.{char_index + 1}")
            text.tag_configure(tag, foreground='red')

        char_index += 1


# Time manager
def time_manager():
    global starting_time
    current_time.config(text=starting_time)
    if starting_time > 0:
        root.after(1000, time_manager)
        starting_time -= 1

        # Calculate WPM and CPM each sec
        wpm.set(str(int((total_key_pressed / 5) / 1)))
        cpm.set(str(total_key_pressed))

    # View score when time is over
    else:
        ttk.Label(mainframe, text=f'your CPM is {cpm.get()} and your WPM is {wpm.get()}').grid(row=6, column=1,
                                                                                               columnspan=1)
        text_entry.unbind("<Key>")
        text_entry.config(state='disabled')
        ttk.Label(mainframe, text='To Play Again Press Enter').grid(row=7, column=1, columnspan=1,
                                                                    pady=20, padx=20)


style = ttk.Style()
style.configure('TFrame', background='#E8E8E8')
style.configure('TLabel', background='#E8E8E8')

# App widgets
mainframe = ttk.Frame(root, padding="3 3 12 12", border=50, style='TFrame')
mainframe.grid(column=0, row=0, sticky='NWES')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
ttk.Label(mainframe, text='To Play Again Press Enter').grid(row=7, column=1, columnspan=1,
                                                                    pady=20, padx=20)
cpm = StringVar()
ttk.Label(mainframe, text='CPM', font='Arial 12 bold', style='TLabel').grid(row=1, column=0)
ttk.Label(mainframe, textvariable=cpm, font='Arial 12 bold').grid(row=2, column=0)

wpm = StringVar()
ttk.Label(mainframe, text='WPM', font='Arial 12 bold').grid(row=1, column=1)
ttk.Label(mainframe, textvariable=wpm, font='Arial 12 bold').grid(row=2, column=1)

starting_time = 60
ttk.Label(mainframe, text='Time', font='Arial 12 bold').grid(row=1, column=2)
current_time = ttk.Label(mainframe, text=starting_time, font='Arial 12 bold')
current_time.grid(row=2, column=2)

tx = ''.join(char for char in random.choice(data).lower() if char.isalpha() or char.isspace())
text = Text(mainframe, font='Arial 12', height=5, width=70, bg='#BBBFCA')
text.insert(END, tx)
text.grid(row=3, column=1, rowspan=2, padx=10, pady=20)


text_entry = Text(mainframe, width=50, height=2, font='Arial 15 normal')
text_entry.grid(row=5, column=1, padx=10, pady=10)

text_entry.focus_set()
text_entry.bind("<Key>", on_key_press)

root.mainloop()
