"""
Experimental Tkinter UI prototype.

The original command-line calculator was written independently.
This interface was generated with AI assistance and will be
rewritten as I learn more about Tkinter and GUI development.
"""
import tkinter as tk
from tkinter import ttk, messagebox


def calculate():
    selected = calculation_type.get()

    try:
        first_number = float(first_entry.get())
        second_number = float(second_entry.get())

        if selected == "Voltage":
            # V = I × R
            answer = first_number * second_number
            result_label.config(text=f"{answer:g} Volts")

        elif selected == "Current":
            # I = V ÷ R
            if second_number == 0:
                raise ZeroDivisionError

            answer = first_number / second_number
            result_label.config(text=f"{answer:g} Amps")

        elif selected == "Resistance":
            # R = V ÷ I
            if second_number == 0:
                raise ZeroDivisionError

            answer = first_number / second_number
            result_label.config(text=f"{answer:g} Ohms")

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Enter numbers in both input boxes."
        )

    except ZeroDivisionError:
        messagebox.showerror(
            "Math Error",
            "The second value cannot be zero."
        )


def update_labels(event=None):
    selected = calculation_type.get()

    if selected == "Voltage":
        first_label.config(text="Current (Amps)")
        second_label.config(text="Resistance (Ohms)")

    elif selected == "Current":
        first_label.config(text="Voltage (Volts)")
        second_label.config(text="Resistance (Ohms)")

    elif selected == "Resistance":
        first_label.config(text="Voltage (Volts)")
        second_label.config(text="Current (Amps)")

    first_entry.delete(0, tk.END)
    second_entry.delete(0, tk.END)
    result_label.config(text="Result will appear here")


def clear_fields():
    first_entry.delete(0, tk.END)
    second_entry.delete(0, tk.END)
    result_label.config(text="Result will appear here")
    first_entry.focus()


# Create the window
window = tk.Tk()
window.title("Ohm's Law Calculator")
window.geometry("420x400")
window.resizable(False, False)

# Main heading
title_label = ttk.Label(
    window,
    text="Ohm's Law Calculator",
    font=("Arial", 22, "bold")
)
title_label.pack(pady=(25, 5))

formula_label = ttk.Label(
    window,
    text="V = I × R",
    font=("Arial", 13)
)
formula_label.pack(pady=(0, 20))

# Calculation selection
selection_label = ttk.Label(
    window,
    text="Calculate:"
)
selection_label.pack()

calculation_type = ttk.Combobox(
    window,
    values=["Voltage", "Current", "Resistance"],
    state="readonly",
    width=25
)
calculation_type.set("Voltage")
calculation_type.pack(pady=5)
calculation_type.bind("<<ComboboxSelected>>", update_labels)

# First input
first_label = ttk.Label(window, text="Current (Amps)")
first_label.pack(pady=(15, 3))

first_entry = ttk.Entry(window, width=28)
first_entry.pack()

# Second input
second_label = ttk.Label(window, text="Resistance (Ohms)")
second_label.pack(pady=(15, 3))

second_entry = ttk.Entry(window, width=28)
second_entry.pack()

# Buttons
button_frame = ttk.Frame(window)
button_frame.pack(pady=22)

calculate_button = ttk.Button(
    button_frame,
    text="Calculate",
    command=calculate
)
calculate_button.grid(row=0, column=0, padx=6)

clear_button = ttk.Button(
    button_frame,
    text="Clear",
    command=clear_fields
)
clear_button.grid(row=0, column=1, padx=6)

# Result
result_label = ttk.Label(
    window,
    text="Result will appear here",
    font=("Arial", 15, "bold")
)
result_label.pack(pady=5)

# Let Enter activate the calculator
window.bind("<Return>", lambda event: calculate())

first_entry.focus()

# Keep the window running
window.mainloop()