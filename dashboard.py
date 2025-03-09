import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='white')

# Load Data
df = pd.read_csv("https://github.com/username/repository_name/.csv'")
df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
df['year_month'] = df['datetime'].dt.to_period('M')

# Sidebar
st.sidebar.header("Pilih Rentang Tanggal")
start_date = st.sidebar.date_input("Tanggal Mulai", df['datetime'].min())
end_date = st.sidebar.date_input("Tanggal Akhir", df['datetime'].max())

# Filter Data
filtered_df = df[(df['datetime'] >= pd.to_datetime(start_date)) & (df['datetime'] <= pd.to_datetime(end_date))]

st.title("🌍 POLLUTION DASHBOARD - KOTA WANLIU ☁️")

# Rata-rata tingkat polusi
st.subheader("📌 Rata-rata Konsentrasi Polutan")
pollutants = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
avg_pollution = filtered_df[pollutants].mean()

st.dataframe(avg_pollution.reset_index().rename(columns={0: "Rata-rata Konsentrasi"}))

# Tren polusi bulanan
st.subheader("📈 Tren Polusi Bulanan")
monthly_trend = filtered_df.groupby("year_month")[pollutants].mean()
fig, ax = plt.subplots(figsize=(10, 5))
for pollutant in pollutants:
    ax.plot(monthly_trend.index.astype(str), monthly_trend[pollutant], marker='o', linestyle='-', label=pollutant)
ax.set_xlabel("Bulan")
ax.set_ylabel("Konsentrasi Rata-rata")
ax.set_title("Tren Polusi Bulanan di Kota Wanliu")
ax.legend()
plt.xticks(rotation=45)
st.pyplot(fig)

# Korelasi polusi dengan cuaca
st.subheader("🌦️ Korelasi Cuaca terhadap Polusi")
weather_params = ["TEMP", "PRES", "DEWP", "RAIN"]
korelasi = filtered_df[weather_params + pollutants].corr()
st.dataframe(korelasi.loc[weather_params, pollutants])

# Scatter plot korelasi suhu dan polusi
st.subheader("🌡️ Korelasi Suhu dengan Polusi")
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
for i, pollutant in enumerate(pollutants):
    ax = axes[i // 3, i % 3]
    sns.scatterplot(data=filtered_df, x='TEMP', y=pollutant, alpha=0.5, ax=ax)
    ax.set_title(f"TEMP vs {pollutant}")
    ax.set_xlabel("Suhu")
    ax.set_ylabel(pollutant)
st.pyplot(fig)

st.markdown("---")
st.markdown("Data ini berasal dari Stasiun Pengamatan Polusi Udara di Kota Wanliu.")
