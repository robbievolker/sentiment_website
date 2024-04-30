import os
import re
from docx import Document


"""
Helper function to check the character of each paragraph, to ensure we extract the correct lines. 
"""
def is_character(paragraph, character):
    # Iterate through each run in the paragraph
    for run in paragraph.runs:
        # Check if the run contains the text "JOKER"
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

    # Iterate through each paragraph in the document
    for paragraph in doc.paragraphs:
        if character in paragraph.text:
            # Check character matches character input on the website.
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
                # Update to state that we are no longer capturing the character's dialogue.
                capture_dialogue = False
                # Add character's dialogue to the list of lines to be appended to the file.
                dialogue.append(valid_line)

    # Write each element of dialogue list to the cleaned_lines.txt file.
    output_path = os.path.join(app.root_path, 'data', 'cleaned_lines.txt')


    with open(output_path, "w", encoding="utf-8") as file:
        for line in dialogue:
            if not line == "":
                clean_line = ''.join(char for char in line if ord(char) < 128) #Make sure char is ASCII for syuzhet.
                file.write(clean_line.strip() + "\n")