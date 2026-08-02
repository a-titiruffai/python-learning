import math
import tkinter as tk
from tkinter import ttk, messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


VECTOR_COLORS = {
    "Vector 1": "tab:blue",
    "Vector 2": "tab:green",
    "Result": "tab:red",
}


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

    def __rmul__(self, scalar: float):
        return self * scalar

    def __truediv__(self, scalar: float):
        if scalar == 0:
            raise ZeroDivisionError("A vector cannot be divided by zero.")
        return Vector2D(self.x / scalar, self.y / scalar)

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        magnitude = self.magnitude()
        if magnitude == 0:
            raise ValueError("The zero vector cannot be normalized.")
        return self / magnitude

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def angle_with(self, other):
        denominator = self.magnitude() * other.magnitude()
        if denominator == 0:
            raise ValueError("The angle is undefined for a zero vector.")

        cosine = self.dot(other) / denominator
        cosine = max(-1.0, min(1.0, cosine))
        return math.degrees(math.acos(cosine))

    def components(self):
        return self.x, self.y

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

    def __rmul__(self, scalar: float):
        return self * scalar

    def __truediv__(self, scalar: float):
        if scalar == 0:
            raise ZeroDivisionError("A vector cannot be divided by zero.")
        return Vector3D(
            self.x / scalar,
            self.y / scalar,
            self.z / scalar,
        )

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

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

    def angle_with(self, other):
        denominator = self.magnitude() * other.magnitude()
        if denominator == 0:
            raise ValueError("The angle is undefined for a zero vector.")

        cosine = self.dot(other) / denominator
        cosine = max(-1.0, min(1.0, cosine))
        return math.degrees(math.acos(cosine))

    def components(self):
        return self.x, self.y, self.z

    def __repr__(self):
        return f"Vector3D({self.x:g}, {self.y:g}, {self.z:g})"


class VectorCalculatorApp:
    TWO_VECTOR_OPERATIONS = {
        "Addition",
        "Subtraction",
        "Dot Product",
        "Angle Between Vectors",
    }

    SCALAR_OPERATIONS = {
        "Scalar Multiplication",
        "Scalar Division",
    }

    OPERATIONS = (
        "Addition",
        "Subtraction",
        "Dot Product",
        "Angle Between Vectors",
        "Magnitude",
        "Normalize",
        "Scalar Multiplication",
        "Scalar Division",
    )

    def __init__(self, root):
        self.root = root
        self.root.title("Vector Calculator")
        self.root.geometry("1120x720")
        self.root.minsize(940, 640)

        self.dimension_var = tk.StringVar(value="2D")
        self.operation_var = tk.StringVar(value="Addition")
        self.scalar_var = tk.StringVar()
        self.show_components_var = tk.BooleanVar(value=True)
        self.show_parallelogram_var = tk.BooleanVar(value=True)

        self.vector1_entries = {}
        self.vector2_entries = {}

        self.build_ui()
        self.update_dimension_fields()
        self.update_operation_fields()

    def build_ui(self):
        main = ttk.Frame(self.root, padding=16)
        main.pack(fill="both", expand=True)

        main.columnconfigure(0, weight=0)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(0, weight=1)

        controls = ttk.Frame(main)
        controls.grid(row=0, column=0, sticky="nsw", padx=(0, 18))

        plot_area = ttk.Frame(main)
        plot_area.grid(row=0, column=1, sticky="nsew")
        plot_area.rowconfigure(0, weight=1)
        plot_area.columnconfigure(0, weight=1)

        ttk.Label(
            controls,
            text="Vector Calculator",
            font=("Segoe UI", 20, "bold"),
        ).pack(anchor="w", pady=(0, 14))

        settings = ttk.LabelFrame(controls, text="Settings", padding=10)
        settings.pack(fill="x", pady=(0, 12))

        ttk.Label(settings, text="Vector type").grid(
            row=0, column=0, sticky="w", padx=(0, 10), pady=6
        )

        dimension_box = ttk.Combobox(
            settings,
            textvariable=self.dimension_var,
            values=("2D", "3D"),
            state="readonly",
            width=20,
        )
        dimension_box.grid(row=0, column=1, pady=6)
        dimension_box.bind("<<ComboboxSelected>>", self.on_dimension_change)

        ttk.Label(settings, text="Operation").grid(
            row=1, column=0, sticky="w", padx=(0, 10), pady=6
        )

        operation_box = ttk.Combobox(
            settings,
            textvariable=self.operation_var,
            values=self.OPERATIONS,
            state="readonly",
            width=20,
        )
        operation_box.grid(row=1, column=1, pady=6)
        operation_box.bind("<<ComboboxSelected>>", self.update_operation_fields)

        display_frame = ttk.LabelFrame(controls, text="Display", padding=10)
        display_frame.pack(fill="x", pady=(0, 12))

        ttk.Checkbutton(
            display_frame,
            text="Show component guides",
            variable=self.show_components_var,
        ).pack(anchor="w")

        ttk.Checkbutton(
            display_frame,
            text="Show addition parallelogram",
            variable=self.show_parallelogram_var,
        ).pack(anchor="w", pady=(4, 0))

        self.vector1_frame = ttk.LabelFrame(
            controls,
            text="Vector 1",
            padding=10,
        )
        self.vector1_frame.pack(fill="x", pady=(0, 12))

        self.vector2_frame = ttk.LabelFrame(
            controls,
            text="Vector 2",
            padding=10,
        )
        self.vector2_frame.pack(fill="x", pady=(0, 12))

        self.scalar_frame = ttk.LabelFrame(
            controls,
            text="Scalar",
            padding=10,
        )

        ttk.Label(self.scalar_frame, text="Value").grid(
            row=0, column=0, sticky="w", padx=(0, 10)
        )

        ttk.Entry(
            self.scalar_frame,
            textvariable=self.scalar_var,
            width=20,
        ).grid(row=0, column=1)

        button_frame = ttk.Frame(controls)
        button_frame.pack(fill="x", pady=(0, 12))

        ttk.Button(
            button_frame,
            text="Calculate",
            command=self.calculate,
        ).pack(side="left")

        ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_inputs,
        ).pack(side="left", padx=(8, 0))

        result_frame = ttk.LabelFrame(
            controls,
            text="Result",
            padding=10,
        )
        result_frame.pack(fill="both", expand=True)

        self.result_text = tk.Text(
            result_frame,
            width=38,
            height=10,
            wrap="word",
            state="disabled",
            font=("Consolas", 10),
        )
        self.result_text.pack(fill="both", expand=True)

        self.figure = Figure(figsize=(7, 6), dpi=100)
        self.axis = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=plot_area)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        ttk.Label(
            plot_area,
            text="3D graphs can be rotated by dragging with the mouse.",
        ).grid(row=1, column=0, sticky="w", pady=(8, 0))

        self.draw_empty_plot()

    def on_dimension_change(self, event=None):
        self.update_dimension_fields()
        self.draw_empty_plot()

    def update_dimension_fields(self):
        coordinates = (
            ("x", "y")
            if self.dimension_var.get() == "2D"
            else ("x", "y", "z")
        )

        for widget in self.vector1_frame.winfo_children():
            widget.destroy()

        for widget in self.vector2_frame.winfo_children():
            widget.destroy()

        self.vector1_entries.clear()
        self.vector2_entries.clear()

        for row, coordinate in enumerate(coordinates):
            ttk.Label(
                self.vector1_frame,
                text=f"{coordinate.upper()}:",
            ).grid(row=row, column=0, padx=(0, 8), pady=5, sticky="w")

            entry1 = ttk.Entry(self.vector1_frame, width=20)
            entry1.grid(row=row, column=1, pady=5)
            self.vector1_entries[coordinate] = entry1

            ttk.Label(
                self.vector2_frame,
                text=f"{coordinate.upper()}:",
            ).grid(row=row, column=0, padx=(0, 8), pady=5, sticky="w")

            entry2 = ttk.Entry(self.vector2_frame, width=20)
            entry2.grid(row=row, column=1, pady=5)
            self.vector2_entries[coordinate] = entry2

    def update_operation_fields(self, event=None):
        operation = self.operation_var.get()

        if operation in self.TWO_VECTOR_OPERATIONS:
            if not self.vector2_frame.winfo_ismapped():
                self.vector2_frame.pack(fill="x", pady=(0, 12))
        else:
            self.vector2_frame.pack_forget()

        if operation in self.SCALAR_OPERATIONS:
            if not self.scalar_frame.winfo_ismapped():
                self.scalar_frame.pack(fill="x", pady=(0, 12))
        else:
            self.scalar_frame.pack_forget()

    def read_vector(self, entries):
        try:
            x = float(entries["x"].get())
            y = float(entries["y"].get())

            if self.dimension_var.get() == "2D":
                return Vector2D(x, y)

            z = float(entries["z"].get())
            return Vector3D(x, y, z)

        except ValueError as error:
            raise ValueError(
                "All required vector coordinates must be valid numbers."
            ) from error

    def read_scalar(self):
        try:
            return float(self.scalar_var.get())
        except ValueError as error:
            raise ValueError("The scalar must be a valid number.") from error

    def calculate(self):
        try:
            operation = self.operation_var.get()
            vector1 = self.read_vector(self.vector1_entries)
            vector2 = None
            result = None

            if operation in self.TWO_VECTOR_OPERATIONS:
                vector2 = self.read_vector(self.vector2_entries)

            if operation == "Addition":
                result = vector1 + vector2
                message = f"{vector1} + {vector2}\n\nResult: {result}"

            elif operation == "Subtraction":
                result = vector1 - vector2
                message = f"{vector1} - {vector2}\n\nResult: {result}"

            elif operation == "Dot Product":
                result = vector1.dot(vector2)
                message = (
                    f"{vector1} · {vector2}\n\n"
                    f"Dot product: {result:g}"
                )

            elif operation == "Angle Between Vectors":
                result = vector1.angle_with(vector2)
                message = (
                    f"Vector 1: {vector1}\n"
                    f"Vector 2: {vector2}\n\n"
                    f"Angle: {result:.2f}°"
                )

            elif operation == "Magnitude":
                result = vector1.magnitude()
                message = (
                    f"Vector: {vector1}\n\n"
                    f"Magnitude: {result:g}"
                )

            elif operation == "Normalize":
                result = vector1.normalize()
                message = (
                    f"Vector: {vector1}\n\n"
                    f"Normalized vector: {result}"
                )

            elif operation == "Scalar Multiplication":
                scalar = self.read_scalar()
                result = vector1 * scalar
                message = (
                    f"{vector1} × {scalar:g}\n\n"
                    f"Result: {result}"
                )

            elif operation == "Scalar Division":
                scalar = self.read_scalar()
                result = vector1 / scalar
                message = (
                    f"{vector1} ÷ {scalar:g}\n\n"
                    f"Result: {result}"
                )

            else:
                raise ValueError("Choose a valid operation.")

            self.show_result(message)
            self.plot_vectors(vector1, vector2, result, operation)

        except (ValueError, ZeroDivisionError) as error:
            messagebox.showerror("Calculation Error", str(error))

    def plot_vectors(self, vector1, vector2, result, operation):
        if self.dimension_var.get() == "2D":
            self.plot_2d(vector1, vector2, result, operation)
        else:
            self.plot_3d(vector1, vector2, result, operation)

    def get_vectors_to_plot(self, vector1, vector2, result):
        vectors = [("Vector 1", vector1)]

        if vector2 is not None:
            vectors.append(("Vector 2", vector2))

        if isinstance(result, (Vector2D, Vector3D)):
            vectors.append(("Result", result))

        return vectors

    def plot_2d(self, vector1, vector2, result, operation):
        self.figure.clear()
        self.axis = self.figure.add_subplot(111)
        vectors_to_plot = self.get_vectors_to_plot(vector1, vector2, result)

        for label, vector in vectors_to_plot:
            self.axis.quiver(
                0,
                0,
                vector.x,
                vector.y,
                angles="xy",
                scale_units="xy",
                scale=1,
                color=VECTOR_COLORS[label],
                width=0.008,
                label=label,
            )

            if self.show_components_var.get():
                self.axis.plot(
                    [0, vector.x],
                    [vector.y, vector.y],
                    linestyle="--",
                    linewidth=1,
                    color=VECTOR_COLORS[label],
                    alpha=0.6,
                )
                self.axis.plot(
                    [vector.x, vector.x],
                    [0, vector.y],
                    linestyle="--",
                    linewidth=1,
                    color=VECTOR_COLORS[label],
                    alpha=0.6,
                )

        if (
            operation == "Addition"
            and vector2 is not None
            and self.show_parallelogram_var.get()
        ):
            self.axis.plot(
                [vector1.x, vector1.x + vector2.x],
                [vector1.y, vector1.y + vector2.y],
                linestyle=":",
                linewidth=1.6,
                color="gray",
            )
            self.axis.plot(
                [vector2.x, vector1.x + vector2.x],
                [vector2.y, vector1.y + vector2.y],
                linestyle=":",
                linewidth=1.6,
                color="gray",
            )

        max_value = max(
            [abs(value) for _, vector in vectors_to_plot for value in vector.components()]
            + [1]
        )
        limit = max_value * 1.25 + 0.5

        self.axis.set_xlim(-limit, limit)
        self.axis.set_ylim(-limit, limit)
        self.axis.axhline(0, linewidth=0.8, color="black")
        self.axis.axvline(0, linewidth=0.8, color="black")
        self.axis.set_aspect("equal", adjustable="box")
        self.axis.grid(True)
        self.axis.set_xlabel("X")
        self.axis.set_ylabel("Y")
        self.axis.set_title(f"2D Visualization — {operation}")
        self.axis.legend()
        self.canvas.draw()

    def plot_3d(self, vector1, vector2, result, operation):
        self.figure.clear()
        self.axis = self.figure.add_subplot(111, projection="3d")
        vectors_to_plot = self.get_vectors_to_plot(vector1, vector2, result)

        for label, vector in vectors_to_plot:
            self.axis.quiver(
                0,
                0,
                0,
                vector.x,
                vector.y,
                vector.z,
                color=VECTOR_COLORS[label],
                linewidth=2,
                arrow_length_ratio=0.12,
                label=label,
            )

            if self.show_components_var.get():
                self.axis.plot(
                    [0, vector.x],
                    [0, 0],
                    [0, 0],
                    linestyle="--",
                    linewidth=1,
                    color=VECTOR_COLORS[label],
                    alpha=0.55,
                )
                self.axis.plot(
                    [vector.x, vector.x],
                    [0, vector.y],
                    [0, 0],
                    linestyle="--",
                    linewidth=1,
                    color=VECTOR_COLORS[label],
                    alpha=0.55,
                )
                self.axis.plot(
                    [vector.x, vector.x],
                    [vector.y, vector.y],
                    [0, vector.z],
                    linestyle="--",
                    linewidth=1,
                    color=VECTOR_COLORS[label],
                    alpha=0.55,
                )

        if (
            operation == "Addition"
            and vector2 is not None
            and self.show_parallelogram_var.get()
        ):
            result_vector = vector1 + vector2

            self.axis.plot(
                [vector1.x, result_vector.x],
                [vector1.y, result_vector.y],
                [vector1.z, result_vector.z],
                linestyle=":",
                linewidth=1.6,
                color="gray",
            )
            self.axis.plot(
                [vector2.x, result_vector.x],
                [vector2.y, result_vector.y],
                [vector2.z, result_vector.z],
                linestyle=":",
                linewidth=1.6,
                color="gray",
            )

        max_value = max(
            [abs(value) for _, vector in vectors_to_plot for value in vector.components()]
            + [1]
        )
        limit = max_value * 1.25 + 0.5

        self.axis.set_xlim(-limit, limit)
        self.axis.set_ylim(-limit, limit)
        self.axis.set_zlim(-limit, limit)
        self.axis.set_box_aspect((1, 1, 1))
        self.axis.set_xlabel("X")
        self.axis.set_ylabel("Y")
        self.axis.set_zlabel("Z")
        self.axis.set_title(f"3D Visualization — {operation}")
        self.axis.legend()
        self.canvas.draw()

    def draw_empty_plot(self):
        self.figure.clear()

        if self.dimension_var.get() == "3D":
            self.axis = self.figure.add_subplot(111, projection="3d")
            self.axis.set_xlim(-5, 5)
            self.axis.set_ylim(-5, 5)
            self.axis.set_zlim(-5, 5)
            self.axis.set_box_aspect((1, 1, 1))
            self.axis.set_xlabel("X")
            self.axis.set_ylabel("Y")
            self.axis.set_zlabel("Z")
        else:
            self.axis = self.figure.add_subplot(111)
            self.axis.axhline(0, linewidth=0.8, color="black")
            self.axis.axvline(0, linewidth=0.8, color="black")
            self.axis.grid(True)
            self.axis.set_xlim(-5, 5)
            self.axis.set_ylim(-5, 5)
            self.axis.set_aspect("equal", adjustable="box")
            self.axis.set_xlabel("X")
            self.axis.set_ylabel("Y")

        self.axis.set_title("Enter vectors and calculate")
        self.canvas.draw()

    def clear_inputs(self):
        for entry in self.vector1_entries.values():
            entry.delete(0, tk.END)

        for entry in self.vector2_entries.values():
            entry.delete(0, tk.END)

        self.scalar_var.set("")
        self.show_result("")
        self.draw_empty_plot()

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