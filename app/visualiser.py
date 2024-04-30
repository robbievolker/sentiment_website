import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from app import app


def create_plots():
    # Read data from CSV file
    data = pd.read_csv(os.path.join(app.config['DATA_FOLDER'], "sentiment_analysis.csv"))

    # Extract sentiment scores and emotions
    sentiment_scores = data.iloc[:, 0:]
    emotions = data.columns

    # Convert sentiment scores to float
    sentiment_scores = sentiment_scores.astype(float)

    # Calculate proportions
    proportions = sentiment_scores.sum() / sentiment_scores.sum().sum()

    # Create a horizontal bar plot
    plt.figure(figsize=(8, 6))
    plt.barh(np.arange(len(emotions)), proportions, color=plt.cm.Set3(np.arange(len(emotions))), height=0.5)

    # Label axis and invert the axes.
    plt.xlabel('Proportion')
    plt.title('Sentiment Analysis')
    plt.yticks(np.arange(len(emotions)), emotions)
    plt.gca().invert_yaxis()

    #Save plot in data/images folder.
    data_folder = os.path.join(app.root_path, 'static', 'images')
    plot_path = os.path.join(data_folder, 'sentiment_analysis_plot1.png')
    plt.savefig(plot_path, bbox_inches='tight', dpi=300)
    return plot_path



