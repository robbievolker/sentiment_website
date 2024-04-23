import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Read data from CSV file
data = pd.read_csv("sentiment_analysis.csv")

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

# Customize plot
plt.xlabel('Proportion')
plt.title('Sentiment Analysis')
plt.yticks(np.arange(len(emotions)), emotions)
plt.gca().invert_yaxis()  # Invert y-axis to match R's barplot orientation

plt.show()