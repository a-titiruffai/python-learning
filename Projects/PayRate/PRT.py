import tkinter as tk

def calculate_pay():
    name = name_entry.get()
    payrate = float(payrate_entry.get())
    hours = float(hours_entry.get())

    gross_pay = payrate * hours
    take_home = gross_pay * 0.80

    result_label.config(
        text=f"{name}, your estimated take-home pay is ${take_home:.2f}"
    )

window = tk.Tk()
window.title("Pay Calculator")
window.geometry("400x250")

tk.Label(window, text="Enter your name:").pack()
name_entry = tk.Entry(window)
name_entry.pack()

tk.Label(window, text="Enter your pay rate:").pack()
payrate_entry = tk.Entry(window)
payrate_entry.pack()

tk.Label(window, text="Enter your hours worked:").pack()
hours_entry = tk.Entry(window)
hours_entry.pack()

calculate_button = tk.Button(window, text="Calculate Pay", command=calculate_pay)
calculate_button.pack(pady=10)

result_label = tk.Label(window, text="")
result_label.pack()

window.mainloop()