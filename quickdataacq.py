import tkinter as tk
from tkinter import messagebox, scrolledtext
import re

def process_data(raw_text, constant_value):
    rows = []
    for line in raw_text.splitlines():
        nums = re.findall(r"-?\d+\.?\d*", line)
        if len(nums) == 5:
            rows.append([float(n) for n in nums])

    # Remove first + last row
    rows = rows[1:-1]

    # Reorder & insert constant
    formatted_lines = []
    for rep_count, last_vel, vel_loss, rir, slope in rows:
        row = [
            constant_value,
            last_vel,
            int(rep_count),
            vel_loss,
            slope,
            rir
        ]
        formatted_lines.append(f"add_training_example({','.join(str(x) for x in row)})")

    return "\n".join(formatted_lines)

def run_processing():
    raw_text = input_box.get("1.0", tk.END).strip()
    const_value_str = constant_entry.get().strip()

    if not const_value_str:
        messagebox.showerror("Error", "Please enter a constant value.")
        return

    try:
        constant_value = float(const_value_str)
    except:
        messagebox.showerror("Error", "Constant value must be numeric.")
        return

    result = process_data(raw_text, constant_value)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, result)

def copy_to_clipboard():
    text = output_box.get("1.0", tk.END)
    window.clipboard_clear()
    window.clipboard_append(text)
    messagebox.showinfo("Copied", "Output copied to clipboard!")

# ---------------- GUI WINDOW ----------------

window = tk.Tk()
window.title("Data Formatter")
window.geometry("800x600")

# Constant input
tk.Label(window, text="Constant Value:", font=("Arial", 12)).pack()
constant_entry = tk.Entry(window, font=("Arial", 12), width=20)
constant_entry.pack()

# Raw input label
tk.Label(window, text="\nPaste Raw Data Below:", font=("Arial", 12)).pack()

# Raw data text box
input_box = scrolledtext.ScrolledText(window, width=90, height=10, font=("Courier", 10))
input_box.pack(pady=5)

# Process button
process_button = tk.Button(window, text="Process Data", font=("Arial", 12), command=run_processing)
process_button.pack(pady=10)

# Output label
tk.Label(window, text="Formatted Output:", font=("Arial", 12)).pack()

# Output text box
output_box = scrolledtext.ScrolledText(window, width=90, height=10, font=("Courier", 10))
output_box.pack(pady=5)

# Copy button
copy_button = tk.Button(window, text="Copy to Clipboard", font=("Arial", 12), command=copy_to_clipboard)
copy_button.pack(pady=10)

window.mainloop()
