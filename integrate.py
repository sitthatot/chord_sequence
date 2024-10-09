import os
import mido
import tkinter as tk

def adjust_length(msg, factor):
    """Adjust the length of MIDI messages based on a length factor."""
    if msg.type in ['note_on', 'note_off']:
        msg.time = int(msg.time * factor)
    return msg

def concat_midi_files_single_track(directory, length_factors, output_file):
    combined_midi = mido.MidiFile()
    combined_track = mido.MidiTrack()
    
    for midi_file in length_factors.keys():
        midi_path = os.path.join(directory, midi_file)
        midi = mido.MidiFile(midi_path)
        length_factor = length_factors[midi_file]
        
        for track in midi.tracks:
            for msg in track:
                combined_track.append(adjust_length(msg.copy(), length_factor))
    
    combined_midi.tracks.append(combined_track)
    combined_midi.save(output_file)
    print(f"Combined MIDI saved as: {output_file}")

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

        # Button to concatenate MIDI files
        self.concat_button = tk.Button(self.master, text="Concatenate MIDI", command=self.concatenate_midi)
        self.concat_button.pack(pady=5)

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

    def concatenate_midi(self):
        """Concatenate MIDI files based on user input and predefined length factors."""
        # Specify the directory containing MIDI files
        directory = 'chords_midi'  # Your MIDI files should be in this folder
        
        # Define length factors for each MIDI file based on entries
        length_factors = {}
        for row in self.chord_entries:
            for entry in row:
                chord_name = entry.get()
                if chord_name:  # Only add non-empty entries
                    length_factors[chord_name + '.mid'] = 1  # Default factor is 1 (no change)

        # You can customize the length factors here based on user input
        # Example: length_factors['A#7sus4.mid'] = 0.5
        
        # Define the output filename
        output_file = 'combined_output_single_track.mid'
        
        # Concatenate the MIDI files into a single track
        concat_midi_files_single_track(directory, length_factors, output_file)


if __name__ == "__main__":
    root = tk.Tk()
    app = ChordApp(root)
    root.mainloop()
