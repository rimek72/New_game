from tkinter import Tk, Label, Button
clicks = 0

def click_action():
    print("Test")


def click_action2(button):
    button.config(text="Hej")

def click_action3(button):
    global clicks
    clicks += 1
    button.config(text=f"Miau  x{clicks}")
def create_function(func, *args, **kwargs):
    def command():
        return func(*args, **kwargs)
    return command


root = Tk()
root.title("Moja Aplikacja")
root.geometry("300x300")
First_Button = Button(root, text="New Button", width=8, borderwidth=4, activebackground="red",
                     command=click_action)
Second_Button = Button(root, text="Second Button", width=8, borderwidth=4, activebackground="red",
                     command=click_action2)

Third_Button = Button(root, text="Second Button", width=8, borderwidth=4, activebackground="green",
                     command=click_action3)

label = Label(root, text="To jest moj text", font=30, fg="blue")
label.pack()
First_Button.pack()
Second_Button.pack()
Third_Button.pack()

Second_Button.config(command=create_function(click_action2, Second_Button))
Third_Button.config(command=lambda: click_action3(Third_Button))

root.mainloop()
