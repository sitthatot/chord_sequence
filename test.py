import tkinter as tk
from tkinter import ttk

def main():
    # Create the main window
    root = tk.Tk()
    root.title("ComboBox with Green Square")

    # Create a frame to hold the ComboBox and the green square
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    # Create a small green square using a Label
    green_square = tk.Label(frame, width=2, height=1, bg='green')
    green_square.pack(side=tk.LEFT, padx=(0, 5))  # Add padding to the right

    # Create a style for the ComboBox
    style = ttk.Style()
    style.configure("TCombobox", fieldbackground="white", foreground="black")  # Set background and text color

    # Create the ComboBox with the custom style
    combo = ttk.Combobox(frame, style="TCombobox")
    combo['values'] = ('Option 1', 'Option 2', 'Option 3')  # Add options to the ComboBox
    combo.pack(side=tk.LEFT)

    # Start the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    main()
