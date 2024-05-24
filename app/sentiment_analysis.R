options(repos = "https://cloud.r-project.org")

#Check for syuzhet installation!
if (!requireNamespace("syuzhet", quietly = TRUE)) {
  install.packages("syuzhet")
}
if (!requireNamespace("RColorBrewer", quietly = TRUE)) {
  install.packages("RColorBrewer")
}
if (!requireNamespace("wordcloud", quietly = TRUE)) {
  install.packages("wordcloud")
}
if (!requireNamespace("tm", quietly = TRUE)) {
  install.packages("tm")
}

if (!requireNamespace("here", quietly = TRUE)) {
  install.packages("here")
}

library(syuzhet)
library(RColorBrewer)
library(wordcloud)
library(tm)
library(here)

# Specify the file paths relative to the R script location
file_path <- "./app/data/cleaned_lines.txt"
# Read the lines of the file into a list
lines_list <- readLines(file_path, encoding = "UTF-8")

sentiment_scores <- get_nrc_sentiment(lines_list, lang="english")
write.csv(sentiment_scores, file = "./app/data/sentiment_analysis.csv", row.names = FALSE)

sentiment_valence <- (sentiment_scores$negative *-1) + sentiment_scores$positive
plot_path <- "./app/static/images/sentiment_valence_plot.png"

#Stacked area chart in R for third graph plot.

if (file.exists(plot_path)) {
  file.remove(plot_path)
}

png(plot_path)
simple_plot(sentiment_valence)
dev.off()
