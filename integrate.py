import os
import mido
import tkinter as tk

def adjust_length(msg, factor):
    """Adjust the length of MIDI messages based on a length factor."""
    if msg.type in ['note_on', 'note_off']:
        msg.time = int(msg.time * factor)
    return msg

def concat_midi_files_single_track(directory, chord_sequence, output_file):
    combined_midi = mido.MidiFile()
    combined_track = mido.MidiTrack()
    
    for chord, length_factor in chord_sequence:
        midi_path = os.path.join(directory, f"{chord}.mid")
        try:
            midi = mido.MidiFile(midi_path)
            for track in midi.tracks:
                for msg in track:
                    combined_track.append(adjust_length(msg.copy(), length_factor))
        except FileNotFoundError:
            print(f"Warning: MIDI file for chord '{chord}' not found. Skipping.")
    
    combined_midi.tracks.append(combined_track)
    combined_midi.save(output_file)
    print(f"Combined MIDI saved as: {output_file}")

class ChordApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Chord Input App")

        # File name entry
        self.file_name_label = tk.Label(self.master, text="File name:")
        self.file_name_label.pack(pady=5)
        
        self.file_name_entry = tk.Entry(self.master, width=30)
        self.file_name_entry.pack(pady=5)
        self.file_name_entry.insert(0, "untitled_name")  # Default file name

        self.entries = []  # List to hold both chord and length entries
        self.row_count = 0  # To track the number of rows

        # Frame for chord entries
        self.frame = tk.Frame(self.master)
        self.frame.pack(pady=10)

        # Add initial chord entries (4 columns)
        self.add_chord_row()  # Create the first row

        # Button to add more chord rows
        self.add_button = tk.Button(self.master, text="Add Chord Row", command=self.add_chord_row)
        self.add_button.pack(pady=5)

        # Concatenate MIDI button
        self.concat_button = tk.Button(self.master, text="Generate MIDI", command=self.concatenate_midi)
        self.concat_button.pack(pady=5)

    def add_chord_row(self):
        """Add a new row of chord entry boxes and length factor entry boxes."""
        # Create a new frame for the row
        row_frame = tk.Frame(self.frame)
        row_frame.pack(pady=5)

        # Add four pairs of chord and length entries to the new row
        row_entries = []
        for _ in range(4):
            chord_entry = tk.Entry(row_frame, width=15)
            chord_entry.pack(side=tk.LEFT, padx=5)
            length_entry = tk.Entry(row_frame, width=5)
            length_entry.pack(side=tk.LEFT, padx=5)
            length_entry.insert(0, "1.0")  # Set default value for length to 1.0
            length_entry.config(bg="aquamarine2")  # Set default background color to light gray
            
            # Bind the focus out event to the length entry
            length_entry.bind("<FocusOut>", lambda event, entry=length_entry: self.check_length_entry(entry))

            row_entries.append((chord_entry, length_entry))

        # Store the entries in the list
        self.entries.append(row_entries)
        self.row_count += 1

    def check_length_entry(self, entry):
        """Check the length entry and append '.0' if missing, and color the box."""
        length_value = entry.get()
        if length_value and length_value[-1].isdigit() and '.' not in length_value:
            entry.insert(tk.END, '.0')  # Append '.0' if it's missing

        # Check if the length is not 1.0
        if length_value != "1.0":
            entry.config(bg="yellow")  # Change background to yellow
        else:
            entry.config(bg="aquamarine2")

    def concatenate_midi(self):
        """Concatenate the MIDI files based on chord names and length factors."""
        directory = 'chords_midi'  # Folder containing the MIDI files
        output_file = self.file_name_entry.get() + '.mid'  # Get the filename from the entry
        
        chord_sequence = []
        
        # Collect all chord and length factor pairs
        for row in self.entries:
            for chord_entry, length_entry in row:
                chord = chord_entry.get()
                length = length_entry.get()
                if chord and length:  # Ensure both chord and length are non-empty
                    # Ensure length is formatted correctly
                    if '.' not in length:
                        length += '.0'  # Add decimal point if missing
                    try:
                        chord_sequence.append((chord, float(length)))
                    except ValueError:
                        print(f"Invalid length factor: {length} for chord {chord}")

        print("Chord sequence:", chord_sequence)  # Debugging statement to show collected chord sequence
        
        # Now concatenate the MIDI files
        if chord_sequence:  # Only proceed if there are chords to process
            try:
                concat_midi_files_single_track(directory, chord_sequence, output_file)
            except Exception as e:
                print(f"Error during MIDI concatenation: {e}")
        else:
            print("No valid chord sequence found. MIDI concatenation aborted.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChordApp(root)
    root.mainloop()
