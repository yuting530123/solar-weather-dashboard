import pandas as pd

def ingest_weather():
    df = pd.read_csv("weather_data.csv")
    df.to_csv("data/raw/weather_raw.csv", index=False)

if __name__ == "__main__":
    ingest_weather()
