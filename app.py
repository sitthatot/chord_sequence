import tkinter as tk

class ChordApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Chord Input App")

        self.chord_entries = []  # List to hold chord entries
        self.row_count = 0  # To track the number of rows

        # Frame for chord entries
        self.frame = tk.Frame(self.master)
        self.frame.pack(pady=10)

        # Add initial chord entries (4 columns)
        self.add_chord_row()  # Create the first row

        # Button to add more chord rows
        self.add_button = tk.Button(self.master, text="Add Chord Row", command=self.add_chord_row)
        self.add_button.pack(pady=5)

        # Run button to save chords and print to terminal
        self.run_button = tk.Button(self.master, text="Run", command=self.run)
        self.run_button.pack(pady=5)

    def add_chord_row(self):
        """Add a new row of chord entry boxes."""
        # Create a new frame for the row
        row_frame = tk.Frame(self.frame)
        row_frame.pack(pady=5)

        # Add four chord entries to the new row
        row_entries = []
        for _ in range(4):
            chord_entry = tk.Entry(row_frame, width=15)
            chord_entry.pack(side=tk.LEFT, padx=5)
            row_entries.append(chord_entry)

        # Store the entries in the list
        self.chord_entries.append(row_entries)
        self.row_count += 1

    def run(self):
        """Collect chord names and print them."""
        chords = []
        for row in self.chord_entries:
            row_chords = [entry.get() for entry in row if entry.get()]  # Get non-empty entries from each row
            if row_chords:  # Only add non-empty rows
                chords.append(row_chords)

        print("Chords:", chords)  # Print chords to the terminal


if __name__ == "__main__":
    root = tk.Tk()
    app = ChordApp(root)
    root.mainloop()
