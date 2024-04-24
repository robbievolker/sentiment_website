import os
import re
from docx import Document

def is_character(paragraph, character):
    # Iterate through each run in the paragraph
    for run in paragraph.runs:
        # Check if the run contains the text "JOKER"
        if character in run.text:
            # Check if the run is bold and all caps
            if run.bold and run.text.strip().isupper():
                return True
    return False

def capture_dialogue(filename, character, app):
    # Open the DOCX file
    doc = Document(filename)

    dialogue = []

    capture_dialogue = False

    # Iterate through each paragraph in the document
    for paragraph in doc.paragraphs:
        if character in paragraph.text:
            # Check character matches character user is looking for.
            if is_character(paragraph, character):
                capture_dialogue = True
                valid_line = paragraph.text.strip().split(character)[-1].strip()
            else:
                capture_dialogue = False
            continue

        # If currently capturing character's dialogue
        if capture_dialogue:
            # Add the paragraph text to character's dialogue
            if paragraph.text.strip():  # Check if the paragraph is not blank
                valid_line += ' ' + paragraph.text.strip()
            else:
                # Stop capturing character's dialogue if the paragraph is blank
                capture_dialogue = False
                # Add character's dialogue to the list
                dialogue.append(valid_line)

    # Write character's dialogues to a new text file
    output_path = os.path.join(app.root_path, 'data', 'cleaned_lines.txt')


    with open(output_path, "w", encoding="utf-8") as file:
        for line in dialogue:
            if not line == "":
                clean_line = ''.join(char for char in line if ord(char) < 128)
                file.write(clean_line.strip() + "\n")