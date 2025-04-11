import pandas as pd

df = pd.read_csv(r"C:\Users\Asawari\PycharmProjects\venv310\stockTracker\stock_sentiment.csv")
# Aggregate tweets at Stock & Sentiment level
aggregated_df = df.groupby(["Stock", "Sentiment"])["Tweet"].apply(lambda x: " ".join(x)).reset_index()

# Rename columns to match the required format
aggregated_df.columns = ["Category", "Sentiment", "Aggregated_Tweets"]

# Save as CSV for Power BI
aggregated_df.to_csv(r"C:\Users\Asawari\PycharmProjects\venv310\stockTracker\wordcloud_data.csv", index=False)

# Save as CSV for Power BI
# combined_df.to_csv(r"C:\Users\ritu.arvind.hire\Downloads\wordcloud_data.csv", index=False)

print("CSV file 'wordcloud_data.csv' saved successfully!")