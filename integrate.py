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

        # Run button to save chords and print to terminal
        self.run_button = tk.Button(self.master, text="Run", command=self.run)
        self.run_button.pack(pady=5)

        # Concatenate MIDI button
        self.concat_button = tk.Button(self.master, text="Concatenate MIDI", command=self.concatenate_midi)
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
            row_entries.append((chord_entry, length_entry))

        # Store the entries in the list
        self.entries.append(row_entries)
        self.row_count += 1

    def run(self):
        """Collect chord names and length factors, and print them."""
        chords_and_lengths = []
        for row in self.entries:
            for chord_entry, length_entry in row:
                chord = chord_entry.get()
                length = length_entry.get()
                if chord and length:  # Only add non-empty pairs
                    chords_and_lengths.append((chord, length))

        print("Chords and Lengths:", chords_and_lengths)  # Print chords and lengths to the terminal

    def concatenate_midi(self):
        """Concatenate the MIDI files based on chord names and length factors."""
        directory = 'chords_midi'  # Folder containing the MIDI files
        output_file = 'combined_output_single_track.mid'  # Output MIDI filename
        
        chord_sequence = []
        
        # Collect all chord and length factor pairs
        for row in self.entries:
            for chord_entry, length_entry in row:
                chord = chord_entry.get()
                length = length_entry.get()
                if chord and length:  # Ensure both chord and length are non-empty
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