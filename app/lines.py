import os
import re
from docx import Document


"""
Helper function to check the character of each paragraph, to ensure we extract the correct lines. Uses docx library
to handle formatting (such as character name being in bold).
"""
def is_character(paragraph, character):
    # Iterate through each run in the paragraph
    for run in paragraph.runs:
        # Check if the run contains the character.
        if character in run.text:
            # Check if the run is bold and all caps
            if run.bold and run.text.strip().isupper():
                return True
    return False


"""
Read docx script and extract character's lines of dialogue. Does not return anything, just writes the data to 
the cleaned_lines.txt file. 
"""
def capture_dialogue(filename, character, app):
    # Open the DOCX file
    doc = Document(filename)

    dialogue = []

    capture_dialogue = False

    for paragraph in doc.paragraphs:
        if character in paragraph.text:
            if is_character(paragraph, character):
                capture_dialogue = True
                valid_line = paragraph.text.strip().split(character)[-1].strip() #This bit isolates just the dialogue and not the character name part part.
            else:
                capture_dialogue = False
            continue

        if capture_dialogue:
            if paragraph.text.strip():
                valid_line += ' ' + paragraph.text.strip()
            else:
                capture_dialogue = False
                dialogue.append(valid_line)

    #The part where the dialogue array is written to cleaned_lines.txt.
    output_path = os.path.join(app.root_path, 'data', 'cleaned_lines.txt')
    with open(output_path, "w", encoding="utf-8") as file:
        for line in dialogue:
            if not line == "":
                clean_line = ''.join(char for char in line if ord(char) < 128) #Make sure char is an ASCII letter.
                file.write(clean_line.strip() + "\n")