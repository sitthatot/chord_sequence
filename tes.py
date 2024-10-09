import pygame

def play_midi(file_path):
    """Play a MIDI file using pygame."""
    # Initialize pygame mixer
    pygame.mixer.init()
    
    # Load and play the MIDI file
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    # Keep the program running until the MIDI file finishes
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # wait for the MIDI to finish

# Example usage
if __name__ == "__main__":
    midi_file_path = "chords_midi/A.mid"  # Replace with your actual MIDI file path
    play_midi(midi_file_path)
