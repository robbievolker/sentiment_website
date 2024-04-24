options(repos = "https://cloud.r-project.org")

#Check for syuzhet installation!
if (!requireNamespace("syuzhet", quietly = TRUE)) {
  install.packages("syuzhet")
}

library(syuzhet)
# Specify the file path
file_path <- "C:/Users/mrrob/Desktop/Code/sentiment_intensity/cleaned_lines.txt"

# Read the lines of the file into a list
lines_list <- readLines(file_path, encoding = "UTF-8")
num_lines <- length(lines_list)

sentiment_data <- data.frame(
  LineNumber = 1:num_lines,
  EmotionalIntensity = numeric(num_lines),
  DominantEmotion = character(num_lines)
)

colnames(sentiment_data) <- c("Line_Number", "Emotional_Intensity", "Dominant_Emotion")

for (i in 1:num_lines) {
  line <- lines_list[i]
  
  # Get sentiment score for the line
  sentiment_score <- get_nrc_sentiment(line, lang = "english")
  
  # Calculate emotional intensity and extract dominant emotion
  emotional_intensity <- sum(sentiment_score)
  dominant_emotion <- names(sentiment_score)[which.max(sentiment_score)]
  
  # Update dataframe with sentiment score and dominant emotion for the line
  sentiment_data[i, "Emotional_Intensity"] <- emotional_intensity
  sentiment_data[i, "Dominant_Emotion"] <- dominant_emotion
}

csv_file_path <- "C:/Users/mrrob/Desktop/Code/sentiment_intensity/sentiment_analysis.csv"
write.csv(sentiment_data, file = csv_file_path, row.names = FALSE)




