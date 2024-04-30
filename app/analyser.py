import lines
import os
import subprocess


def analyser(file, character):
        try:
            lines.capture_dialogue(file, character)
            script_path = os.path.join(os.path.dirname(__file__), "sentiment_analysis.R")
            subprocess.run(["Rscript", script_path])
        except Exception as error:
            print("An error has occurred, please try again.", error)
