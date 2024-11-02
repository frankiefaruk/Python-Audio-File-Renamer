```
import os
from tkinter import Tk, filedialog, simpledialog
import csv

def get_audio_directory():
    """Ask user to select directory containing audio files."""
    root = Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title="Select directory containing audio files")
    return directory

def list_audio_files(directory):
    """Get sorted list of audio files in directory."""
    audio_files = []
    for filename in os.listdir(directory):
        if filename.lower().endswith('.wav'):
            audio_files.append(filename)

    # Robust sorting: extract numbers from filenames and sort numerically
    def extract_number(filename):
        for part in filename.split('-'):
            if part.isdigit():
                return int(part)
        return 0  # Default to 0 if no number found

    return sorted(audio_files, key=extract_number)

def display_audio_files(audio_files):
    """Display the list of found audio files."""
    print("\nFound Audio Files:")
    for file in audio_files:
        print(file)

def get_user_format():
    """Show popup to get user's desired naming format."""
    root = Tk()
    root.withdraw()
    
    format_suggestion = "Enter Audio File Name (e.g., 'A#2, Guitar, Tremolo, RR1')"
    user_format = simpledialog.askstring("File Format", format_suggestion)
    return user_format

def create_note_mapping(csv_path):
    """Create mapping from MIDI note numbers to note names."""
    mapping = {}
    reverse_mapping = {}
    try:
        with open(csv_path, 'r') as csv_file:
            csv_data = csv.reader(csv_file)
            for row in csv_data:
                try:
                    if len(row) >= 2:
                        note_num = int(row[0].strip())
                        note_name = row[1].strip()
                        mapping[note_num] = note_name
                        reverse_mapping[note_name] = note_num
                except ValueError:
                    continue
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
    return mapping, reverse_mapping

def rename_audio_files(directory, audio_files, start_note, mapping, reverse_mapping):
    """Rename audio files sequentially starting from the specified note."""
    if start_note not in reverse_mapping:
        print(f"Error: Starting note {start_note} not found in mapping!")
        return
    
    start_midi_num = reverse_mapping[start_note]
    current_midi_num = start_midi_num
    
    print("\nRenaming files:")
    for filename in audio_files:
        try:
            if current_midi_num in mapping:
                note_name = mapping[current_midi_num]
                new_name = f"{current_midi_num}-Guitar_{note_name}-Tremolo_RR1.wav"
                
                old_path = os.path.join(directory, filename)
                new_path = os.path.join(directory, new_name)
                
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_name}")
                current_midi_num += 1
                
        except Exception as e:
            print(f"Error renaming {filename}: {str(e)}")

def main():
    # 1: Ask audio files location
    print("1. Select directory containing audio files...")
    directory = get_audio_directory()
    if not directory or not os.path.exists(directory):
        print("Invalid directory selected. Exiting...")
        return
        
    # 2: Get and display audio file names
    print("\n2. Finding audio files...")
    audio_files = list_audio_files(directory)
    if not audio_files:
        print("No audio files found. Exiting...")
        return
    display_audio_files(audio_files)
    
    # 3: Present popup menu and get user input
    print("\n3. Getting user input for new file names...")
    user_format = get_user_format()
    if not user_format:
        print("No format specified. Exiting...")
        return
    
    # Get the starting note from the user format
    start_note = user_format.split(',')[0].strip()
    
    # Load note mapping
    csv_path = os.path.join(directory, 'note_mapping.csv')
    if not os.path.exists(csv_path):
        print("note_mapping.csv not found in the selected directory! Exiting...")
        return
    
    mapping, reverse_mapping = create_note_mapping(csv_path)
    if not mapping:
        print("No valid note mappings found in CSV file. Exiting...")
        return
    
    # Perform the renaming
    rename_audio_files(directory, audio_files, start_note, mapping, reverse_mapping)

if __name__ == "__main__":
    main()
```
,,,
