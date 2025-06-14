import pandas as pd
import matplotlib.pyplot as plt

def plot_sentiment(csv_file):
    df = pd.read_csv(csv_file)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df.sort_values("Timestamp", inplace=True)

    plt.figure(figsize=(10, 5))
    for platform in df["Platform"].unique():
        platform_df = df[df["Platform"] == platform]
        plt.plot(platform_df["Timestamp"], platform_df["Sentiment"], marker='o', label=platform)

    plt.xlabel("Time")
    plt.ylabel("Sentiment Score")
    plt.title("Sentiment Over Time: Twitter vs Reddit")
    plt.legend()
    plt.tight_layout()
    plt.xticks(rotation=30)
    plt.grid(True)
    plt.show()
