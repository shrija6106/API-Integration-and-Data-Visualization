import streamlit as st
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

# ✅ Your OpenWeatherMap API key
API_KEY = '1b523fedf857f4bdfaee3574d2e9a725'

def get_forecast_data(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def process_data(data):
    forecast_list = data['list']
    dates = []
    temps = []
    descs = []

    for item in forecast_list:
        dates.append(datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S'))
        temps.append(item['main']['temp'])
        descs.append(item['weather'][0]['description'])

    df = pd.DataFrame({
        'Date': dates,
        'Temperature (°C)': temps,
        'Weather': descs
    })
    return df

def get_weather_emoji(description):
    desc = description.lower()
    if 'cloud' in desc:
        return '☁️'
    elif 'rain' in desc:
        return '🌧️'
    elif 'clear' in desc:
        return '☀️'
    elif 'storm' in desc or 'thunder' in desc:
        return '⛈️'
    elif 'snow' in desc:
        return '❄️'
    elif 'mist' in desc or 'fog' in desc:
        return '🌫️'
    else:
        return '🌈'

def display_summary(df):
    st.write("### 🌦️ Forecast Summary with Emojis")
    summary_df = df.groupby('Weather').size().reset_index(name='Count')
    
    for index, row in summary_df.iterrows():
        emoji = get_weather_emoji(row['Weather'])
        st.write(f"{emoji} **{row['Weather'].capitalize()}** — {row['Count']} times")

def main():
    st.set_page_config(page_title="Weather Dashboard", layout="wide")
    st.title("🌤️ Weather Forecast Dashboard")
    st.markdown("Visualize 5-Day Temperature Trend with Weather Descriptions & Emojis")

    # ✅ Text input allows all cities — not hardcoded
    city = st.text_input("Enter any city name (e.g., Chennai, Tokyo, Paris, New York)", "Chennai")
    
    if st.button("Show Forecast"):
        data = get_forecast_data(city)
        if data and data.get('cod') == "200":
            df = process_data(data)
            st.write(f"### 📍 Forecast Data for `{city.title()}`")
            st.dataframe(df)

            # 📈 Line Chart
            plt.figure(figsize=(12,6))
            sns.lineplot(x='Date', y='Temperature (°C)', data=df, marker='o', color='darkblue')
            plt.title(f"Temperature Trend for {city.title()} (Next 5 Days)")
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(plt)

            # 📊 Bar Chart for Description
            st.write("### 📊 Weather Description Count")
            desc_count = df['Weather'].value_counts()
            st.bar_chart(desc_count)

            # 🌦️ Emoji Summary
            display_summary(df)
        else:
            st.error("❌ Invalid city name or API error. Please try again.")

if __name__ == "__main__":
    main()
