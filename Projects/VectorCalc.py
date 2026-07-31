import tkinter as tk
from tkinter import ttk, messagebox


class Vector2D:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float):
        return Vector2D(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float):
        if scalar == 0:
            raise ZeroDivisionError("A vector cannot be divided by zero.")
        return Vector2D(self.x / scalar, self.y / scalar)

    def magnitude(self):
        return (self.x**2 + self.y**2) ** 0.5

    def normalize(self):
        magnitude = self.magnitude()
        if magnitude == 0:
            raise ValueError("The zero vector cannot be normalized.")
        return self / magnitude

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def __repr__(self):
        return f"Vector2D({self.x:g}, {self.y:g})"


class Vector3D:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector3D(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )

    def __sub__(self, other):
        return Vector3D(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
        )

    def __mul__(self, scalar: float):
        return Vector3D(
            self.x * scalar,
            self.y * scalar,
            self.z * scalar,
        )

    def __truediv__(self, scalar: float):
        if scalar == 0:
            raise ZeroDivisionError("A vector cannot be divided by zero.")
        return Vector3D(
            self.x / scalar,
            self.y / scalar,
            self.z / scalar,
        )

    def magnitude(self):
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

    def normalize(self):
        magnitude = self.magnitude()
        if magnitude == 0:
            raise ValueError("The zero vector cannot be normalized.")
        return self / magnitude

    def dot(self, other):
        return (
            self.x * other.x
            + self.y * other.y
            + self.z * other.z
        )

    def __repr__(self):
        return f"Vector3D({self.x:g}, {self.y:g}, {self.z:g})"


class VectorCalculatorApp:
    OPERATIONS = (
        "Addition",
        "Subtraction",
        "Dot Product",
        "Magnitude",
        "Normalize",
        "Scalar Multiplication",
        "Scalar Division",
    )

    def __init__(self, root):
        self.root = root
        self.root.title("Vector Calculator")
        self.root.geometry("540x560")
        self.root.resizable(False, False)

        self.dimension_var = tk.StringVar(value="2D")
        self.operation_var = tk.StringVar(value=self.OPERATIONS[0])
        self.scalar_var = tk.StringVar()

        self.vector1_entries = {}
        self.vector2_entries = {}

        self.build_ui()
        self.update_dimension_fields()
        self.update_operation_fields()

    def build_ui(self):
        title = ttk.Label(
            self.root,
            text="Vector Calculator",
            font=("Segoe UI", 20, "bold"),
        )
        title.pack(pady=(18, 10))

        options_frame = ttk.LabelFrame(self.root, text="Calculation Settings")
        options_frame.pack(fill="x", padx=20, pady=8)

        ttk.Label(options_frame, text="Vector type:").grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )

        dimension_box = ttk.Combobox(
            options_frame,
            textvariable=self.dimension_var,
            values=("2D", "3D"),
            state="readonly",
            width=16,
        )
        dimension_box.grid(row=0, column=1, padx=10, pady=10)
        dimension_box.bind("<<ComboboxSelected>>", self.update_dimension_fields)

        ttk.Label(options_frame, text="Operation:").grid(
            row=1, column=0, padx=10, pady=10, sticky="w"
        )

        operation_box = ttk.Combobox(
            options_frame,
            textvariable=self.operation_var,
            values=self.OPERATIONS,
            state="readonly",
            width=22,
        )
        operation_box.grid(row=1, column=1, padx=10, pady=10)
        operation_box.bind("<<ComboboxSelected>>", self.update_operation_fields)

        vectors_frame = ttk.Frame(self.root)
        vectors_frame.pack(fill="x", padx=20, pady=8)

        self.vector1_frame = ttk.LabelFrame(vectors_frame, text="Vector 1")
        self.vector1_frame.grid(row=0, column=0, padx=(0, 8), sticky="nsew")

        self.vector2_frame = ttk.LabelFrame(vectors_frame, text="Vector 2")
        self.vector2_frame.grid(row=0, column=1, padx=(8, 0), sticky="nsew")

        vectors_frame.columnconfigure(0, weight=1)
        vectors_frame.columnconfigure(1, weight=1)

        self.scalar_frame = ttk.LabelFrame(self.root, text="Scalar")
        self.scalar_frame.pack(fill="x", padx=20, pady=8)

        ttk.Label(self.scalar_frame, text="Scalar value:").pack(
            side="left", padx=10, pady=10
        )
        self.scalar_entry = ttk.Entry(
            self.scalar_frame,
            textvariable=self.scalar_var,
            width=18,
        )
        self.scalar_entry.pack(side="left", padx=10, pady=10)

        calculate_button = ttk.Button(
            self.root,
            text="Calculate",
            command=self.calculate,
        )
        calculate_button.pack(pady=12)

        result_frame = ttk.LabelFrame(self.root, text="Result")
        result_frame.pack(fill="both", expand=True, padx=20, pady=(0, 18))

        self.result_text = tk.Text(
            result_frame,
            height=7,
            wrap="word",
            state="disabled",
            font=("Consolas", 11),
        )
        self.result_text.pack(fill="both", expand=True, padx=8, pady=8)

    def update_dimension_fields(self, event=None):
        coordinates = ("x", "y") if self.dimension_var.get() == "2D" else ("x", "y", "z")

        for widget in self.vector1_frame.winfo_children():
            widget.destroy()
        for widget in self.vector2_frame.winfo_children():
            widget.destroy()

        self.vector1_entries.clear()
        self.vector2_entries.clear()

        for row, coordinate in enumerate(coordinates):
            ttk.Label(self.vector1_frame, text=f"{coordinate}:").grid(
                row=row, column=0, padx=8, pady=7
            )
            entry1 = ttk.Entry(self.vector1_frame, width=15)
            entry1.grid(row=row, column=1, padx=8, pady=7)
            self.vector1_entries[coordinate] = entry1

            ttk.Label(self.vector2_frame, text=f"{coordinate}:").grid(
                row=row, column=0, padx=8, pady=7
            )
            entry2 = ttk.Entry(self.vector2_frame, width=15)
            entry2.grid(row=row, column=1, padx=8, pady=7)
            self.vector2_entries[coordinate] = entry2

    def update_operation_fields(self, event=None):
        operation = self.operation_var.get()

        uses_scalar = operation in (
            "Scalar Multiplication",
            "Scalar Division",
        )
        uses_two_vectors = operation in (
            "Addition",
            "Subtraction",
            "Dot Product",
        )

        if uses_scalar:
            self.scalar_frame.pack(fill="x", padx=20, pady=8)
        else:
            self.scalar_frame.pack_forget()

        if uses_two_vectors:
            self.vector2_frame.grid()
        else:
            self.vector2_frame.grid_remove()

    def read_vector(self, entries):
        try:
            x = float(entries["x"].get())
            y = float(entries["y"].get())

            if self.dimension_var.get() == "2D":
                return Vector2D(x, y)

            z = float(entries["z"].get())
            return Vector3D(x, y, z)

        except ValueError as error:
            raise ValueError("All vector coordinates must be valid numbers.") from error

    def calculate(self):
        try:
            vector1 = self.read_vector(self.vector1_entries)
            operation = self.operation_var.get()

            if operation in ("Addition", "Subtraction", "Dot Product"):
                vector2 = self.read_vector(self.vector2_entries)

            if operation == "Addition":
                result = vector1 + vector2

            elif operation == "Subtraction":
                result = vector1 - vector2

            elif operation == "Dot Product":
                result = vector1.dot(vector2)

            elif operation == "Magnitude":
                result = vector1.magnitude()

            elif operation == "Normalize":
                result = vector1.normalize()

            elif operation == "Scalar Multiplication":
                scalar = self.read_scalar()
                result = vector1 * scalar

            elif operation == "Scalar Division":
                scalar = self.read_scalar()
                result = vector1 / scalar

            else:
                raise ValueError("Select a valid operation.")

            self.show_result(f"{operation}\n\nResult: {result}")

        except (ValueError, ZeroDivisionError) as error:
            messagebox.showerror("Calculation Error", str(error))

    def read_scalar(self):
        try:
            return float(self.scalar_var.get())
        except ValueError as error:
            raise ValueError("The scalar must be a valid number.") from error

    def show_result(self, message):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, message)
        self.result_text.config(state="disabled")


def main():
    root = tk.Tk()
    VectorCalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()