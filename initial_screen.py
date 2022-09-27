from _tkinter import ttk

USER_TYPES = [
    "admin",
    "user"
]

master = ttk.Tk()

variable = ttk.StringVar(master)
variable.set(USER_TYPES[0]) # default value

w = ttk.OptionMenu(master, variable, *USER_TYPES)
w.pack()

def ok():
    print ("value is:" + variable.get())

button = ttk.Button(master, text="OK", command=ok)
button.pack()

ttk.mainloop()