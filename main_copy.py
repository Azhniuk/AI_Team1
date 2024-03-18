import tkinter as tk
from tkinter import ttk


#Node class

            
#----------------------------------------------------




#display the rules
def display_how_to_play():
    rules = """Rules:

- You choose a number 
- Each player divides the current number by 2 or 3.
! The number can be divided only if the result is a whole number !

if an even number  ==> +1 point 
if odd number  ==> -1 point
if ending with 0 or 5 is  ==> +1 pont to the bank
2 or 3 is acquired  ==> END

The player after whose turn the number 2 is acquired empties the bank by adding bank points to his points. 
The player with the most points at the end of the game wins. 

Enjoy the game!"
"""


    how_to_play_window = tk.Toplevel(root)
    how_to_play_window.title("How To Play?")
    how_to_play_label = ttk.Label(how_to_play_window, text=rules, font=("Helvetica", 12))
    how_to_play_label.pack(padx=20, pady=20)
    

def play():
    def handle_input():
        starting_number = int(entry_starting_number.get())
        # You can implement your game logic here using the starting_number
        play_window.destroy()

    play_window = tk.Toplevel(root)
    play_window.title("Play")

    play_label = ttk.Label(play_window, text="Enter the starting number:", font=("Helvetica", 12))
    play_label.pack(padx=20, pady=10)

    entry_starting_number = ttk.Entry(play_window)
    entry_starting_number.pack(padx=20, pady=10)

    submit_button = ttk.Button(play_window, text="Submit", command=handle_input)
    submit_button.pack(padx=20, pady=10)
   
    
    pass





#variables



#create window
root = tk.Tk()
root.title("NUMBER GAME")

frame = ttk.Frame(root)
frame.pack(padx=100, pady=100)

label_title = ttk.Label(frame, text="GAME✨", font=("Helvetica", 18, "bold"))
label_title.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

button_how_to_play = ttk.Button(frame, text="How To Play?", command=display_how_to_play )
button_how_to_play.grid(row=1, column=0, padx=20, pady=8, sticky="ew")

button_vs_computer = ttk.Button(frame, text="PLAY", command=play)
button_vs_computer.grid(row=2, column=0, padx=20, pady=8, sticky="ew")


frame.grid_columnconfigure(1, weight=1)

root.mainloop()