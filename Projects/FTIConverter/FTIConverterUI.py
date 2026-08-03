import tkinter as tk
from tkinter import messagebox

# Function to convert feet to inches
def convert():
    try:
        name = name_entry.get()
        feet = float(feet_entry.get())
        inches = feet * 12

        greeting.config(text=f"Hello, {name}!")
        result.config(text=f"{feet} feet = {inches} inches")

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for feet.")

# Create window
root = tk.Tk()
root.title("Feet to Inches Converter")
root.geometry("400x250")
root.resizable(False, False)

# Title
title = tk.Label(root, text="Feet to Inches Converter",
                 font=("Arial", 18, "bold"))
title.pack(pady=10)

# Name
tk.Label(root, text="Who are you?").pack()
name_entry = tk.Entry(root, width=30)
name_entry.pack()

# Feet
tk.Label(root, text="How many feet?").pack(pady=(10, 0))
feet_entry = tk.Entry(root, width=30)
feet_entry.pack()

# Button
convert_button = tk.Button(root,
                           text="Convert",
                           command=convert,
                           font=("Arial", 12))
convert_button.pack(pady=15)

# Output Labels
greeting = tk.Label(root, text="", font=("Arial", 11))
greeting.pack()

result = tk.Label(root, text="", font=("Arial", 12, "bold"))
result.pack()

# Run the app
root.mainloop()