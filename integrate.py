import os
import mido
import tkinter as tk
from tkinter import ttk

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
        self.master.title("Chord to MIDI by CheezeCakeMusic")

        # Load available chord names from the chords_midi directory
        self.available_chords = self.load_available_chords()

        # File name entry
        self.file_name_label = tk.Label(self.master, text="File name:")
        self.file_name_label.pack(pady=5)
        
        self.file_name_entry = tk.Entry(self.master, width=30)
        self.file_name_entry.pack(pady=5)
        self.file_name_entry.insert(0, "untitled_name")

        self.entries = []
        self.row_count = 0

        # Frame for chord entries
        self.frame = tk.Frame(self.master)
        self.frame.pack(pady=10)

        # Add initial chord entries (4 columns)
        self.add_chord_row()

        # Button to add more chord rows
        self.add_button = tk.Button(self.master, text="Add Chord Row", command=self.add_chord_row)
        self.add_button.pack(pady=5)

        # Concatenate MIDI button
        self.concat_button = tk.Button(self.master, text="Generate MIDI", command=self.concatenate_midi)
        self.concat_button.pack(pady=5)

    def load_available_chords(self):
        """Load available chord names from the chords_midi directory"""
        chord_dir = 'chords_midi'
        available_chords = []
        try:
            for file in os.listdir(chord_dir):
                if file.endswith('.mid'):
                    chord_name = os.path.splitext(file)[0]
                    available_chords.append(chord_name)
        except FileNotFoundError:
            print(f"Warning: '{chord_dir}' directory not found")
        return sorted(available_chords)

    def create_chord_combobox(self, parent):
        """Create a Combobox for chord input with autocomplete"""
        combo = ttk.Combobox(parent, width=12, values=self.available_chords)
        combo.bind('<KeyRelease>', lambda event, cb=combo: self.update_chord_suggestions(event, cb))
        return combo

    def update_chord_suggestions(self, event, combo):
        """Update chord suggestions based on current input."""
        current_text = combo.get().lower()
        suggestions = [chord for chord in self.available_chords 
                       if current_text in chord.lower()]
        combo['values'] = suggestions

        # If there's only one suggestion and it matches exactly what's typed
        # (ignoring case), update the background color
        if len(suggestions) == 1 and current_text == suggestions[0].lower():
            combo.state(['!invalid'])
            # Open the dropdown only if the suggestion is a valid match
            if current_text == suggestions[0].lower():
                combo.event_generate('<Down>')

    def add_chord_row(self):
        """Add a new row of chord entry boxes and length factor entry boxes."""
        row_frame = tk.Frame(self.frame)
        row_frame.pack(pady=5)

        row_entries = []
        for _ in range(4):
            # Create Label for indicator
            indicator_label = tk.Label(row_frame, width=2, bg="white")
            indicator_label.pack(side=tk.LEFT, padx=(0, 5))

            # Create Combobox for chord input
            chord_combo = self.create_chord_combobox(row_frame)
            chord_combo.pack(side=tk.LEFT, padx=5)
            
            # Bind selection event to update background color
            chord_combo.bind('<<ComboboxSelected>>', 
                             lambda event, cb=chord_combo, ind_label=indicator_label: self.check_chord_entry(cb, ind_label))
            chord_combo.bind('<FocusOut>', 
                             lambda event, cb=chord_combo, ind_label=indicator_label: self.check_chord_entry(cb, ind_label))

            # Create length entry
            length_entry = tk.Entry(row_frame, width=5)
            length_entry.pack(side=tk.LEFT, padx=5)
            length_entry.insert(0, "1.0")
            length_entry.config(bg="aquamarine2")
            
            length_entry.bind("<FocusOut>", 
                              lambda event, entry=length_entry: self.check_length_entry(entry))

            row_entries.append((chord_combo, length_entry, indicator_label))

        self.entries.append(row_entries)
        self.row_count += 1

    def check_length_entry(self, entry):
        """Check the length entry and append '.0' if missing, and color the box."""
        length_value = entry.get()
        if length_value and length_value[-1].isdigit() and '.' not in length_value:
            entry.insert(tk.END, '.0')

        if length_value != "1.0":
            entry.config(bg="yellow")
        else:
            entry.config(bg="aquamarine2")

    def check_chord_entry(self, combo, indicator_label):
        """Check if the chord exists and update the combobox appearance."""
        chord = combo.get()
        midi_path = os.path.join('chords_midi', f"{chord}.mid")
        
        if os.path.isfile(midi_path):
            combo.state(['!invalid'])
            combo.config(style='Valid.TCombobox')
            indicator_label.config(bg="green")  # Set indicator to green
        else:
            combo.state(['invalid'])
            combo.config(style='Invalid.TCombobox')
            indicator_label.config(bg="red")  # Set indicator to red

    def concatenate_midi(self):
        """Concatenate the MIDI files based on chord names and length factors."""
        directory = 'chords_midi'
        output_file = self.file_name_entry.get() + '.mid'
        
        chord_sequence = []
        
        for row in self.entries:
            for chord_combo, length_entry, _ in row:
                chord = chord_combo.get()
                length = length_entry.get()
                if chord and length:
                    if '.' not in length:
                        length += '.0'
                    try:
                        chord_sequence.append((chord, float(length)))
                    except ValueError:
                        print(f"Invalid length factor: {length} for chord {chord}")

        print("Chord sequence:", chord_sequence)
        
        if chord_sequence:
            try:
                concat_midi_files_single_track(directory, chord_sequence, output_file)
            except Exception as e:
                print(f"Error during MIDI concatenation: {e}")
        else:
            print("No valid chord sequence found. MIDI concatenation aborted.")

if __name__ == "__main__":
    root = tk.Tk()
    
    # Create custom styles for valid/invalid comboboxes
    style = ttk.Style()
    style.configure('Valid.TCombobox', fieldbackground='green')
    style.configure('Invalid.TCombobox', fieldbackground='red')
    
    app = ChordApp(root)
    root.mainloop()

