from tkinter import Tk, Button, Label
from random import choice

available_choices = ['Paper', 'Rock', 'Scissors']


def play(player, cpu):
    win_with = {"Paper": "Rock", "Rock": "Scissors", "Scissors": "Paper"}
    if player == cpu:
        return None
    elif win_with[player] == cpu:
        return True
    else:
        return False
#test

def play_cmd(player):
    global text_label
    cpu = choice(available_choices)
    is_user_winner = play(player, cpu)
    if is_user_winner is None:
        text_label.config(text="Tie, Try Again ", fg="blue")
    elif is_user_winner:
        text_label.config(text="You win... Lets play Again", fg="green")
    else:
        text_label.config(text="AI wins, Try Again ", fg="red")


root = Tk()
root.title("Paper, Rock, Scissors")
root.geometry("300x200")

text_label = Label(fg="black", font=40, text="Let's play  Paper, Rock, Scissors")
text_label.pack()

Button(root, text="📃 Paper", font=40, width=10, command=lambda: play_cmd("Paper")).pack()
Button(root, text="🤘 Rock", font=40, width=10, command=lambda: play_cmd("Rock")).pack()
Button(root, text="✂️ Scissors", font=40, width=10, command=lambda: play_cmd("Scissors")).pack()

root.mainloop()
