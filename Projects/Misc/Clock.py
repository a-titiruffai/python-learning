from tkinter import *
from time import strftime

myWindow = Tk()
myWindow.title("MyClock")
def time():
    MyTime = strftime('%H:%M:%S %p')
    clock.config(text= MyTime)
    clock.after(1000, time)
clock = Label(myWindow, font=('Times New Roman', 40, 'bold'), background='black', foreground='white')
clock.pack(anchor='center')
time()

mainloop()