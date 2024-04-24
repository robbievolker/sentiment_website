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


library(syuzhet)
library(RColorBrewer)
library(wordcloud)
library(tm)


# Specify the file path

file_path <- "C:/Users/mrrob/Desktop/Code/sentiment_website/app/data/cleaned_lines.txt"

# Read the lines of the file into a list
lines_list <- readLines(file_path, encoding = "UTF-8")
num_lines <- length(lines_list)
text_string <- scan(file = file_path, fileEncoding = "UTF-8", what = character(), sep = "\n", allowEscapes = T)
text_words <- get_tokens(text_string)

sentiment_scores <- get_nrc_sentiment(lines_list, lang="english")
sentiment_valence <- (sentiment_scores$negative *-1) + sentiment_scores$positive
plot_path <- "static/images/sentiment_valence_plot.png"
png(plot_path)
simple_plot(sentiment_valence)
dev.off()

summary(sentiment_scores)


write.csv(sentiment_scores, file = "sentiment_analysis.csv", row.names = FALSE)




