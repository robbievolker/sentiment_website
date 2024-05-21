This is a sentiment analysis tool that allows you to generate sentiment analysis plots for various characters in screenplays. Screenplays must be supplied in doc, docx or odt format. Recommended source for screenplays is https://imsdb.com/. 

With thanks to the developers of the syuzhet pacakge for R, which is used for conducting the sentiment analysis in this application.

NOTE: The first time you run the application it may take a couple of minutes to install and run the relevant R scripts. This web application runs on Flask, with the backend written in Python and R.

QUICK USE GUIDE:

1) Ensure you have all the necessary packages installed in your Python environment (Flask, docx etc.). A requirements file for conda and pip is included in the repo to speed up
the installation of dependent packages. Ensure you have R installed.
2) Run the webpage locally and access using localhost:5000
3) Go to the imsdb website and find a screenplay you want to analyse.
4) Copy the contents of the screenplay into a Word document and save it.
5) Fill out the boxes on the website, uploading your screenplay, then hit the button to analyse.


Make sure to save the plots when they are generated as these are not persistent across sessions.
