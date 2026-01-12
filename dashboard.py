import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style="dark")

# LOAD DATA 
df = pd.read_csv("all_bike_data.csv")
df["dteday"] = pd.to_datetime(df["dteday"])

# SIDEBAR
st.sidebar.header("🚲 Bike Sharing Dashboard")

min_date = pd.to_datetime("2011-01-01")
max_date = pd.to_datetime("2012-12-31")

start_date, end_date = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

main_df = df[
    (df["dteday"] >= pd.to_datetime(start_date)) &
    (df["dteday"] <= pd.to_datetime(end_date))
]

if main_df.empty:
    st.warning("Tidak ada data pada rentang tanggal yang dipilih.")
    st.stop()

# HEADER
st.title("🚴 Bike Sharing Dashboard")
st.caption("Analisis Pola Peminjaman Sepeda (2011–2012)")

# METRICS
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Rentals", int(main_df["cnt"].sum()))
with col2:
    st.metric("Casual Users", int(main_df["casual"].sum()))
with col3:
    st.metric("Registered Users", int(main_df["registered"].sum()))

# DAILY TREND
st.subheader("📈 Tren Peminjaman Harian")

daily_df = main_df.groupby("dteday")["cnt"].sum().reset_index()

fig, ax = plt.subplots(figsize=(14,6))
sns.lineplot(data=daily_df, x="dteday", y="cnt")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Peminjaman")
st.pyplot(fig)

# SEASON ANALYSIS
st.subheader("🌦️ Rata-rata Peminjaman per Musim")

season_avg = main_df.groupby("season_hour")["cnt"].mean().reset_index()
max_season = season_avg.loc[season_avg["cnt"].idxmax(), "season_hour"]

palette = {
    s: "#72BCD4" if s == max_season else "#D3D3D3"
    for s in season_avg["season_hour"]
}

fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(
    data=season_avg,
    x="season_hour",
    y="cnt",
    hue="season_hour",
    palette=palette,
    legend=False
)
ax.set_xlabel("Musim")
ax.set_ylabel("Rata-rata Peminjaman")
st.pyplot(fig)

# USER CONTRIBUTION
st.subheader("👤 Kontribusi Casual vs Registered")

daily_user_mean = main_df[["casual", "registered"]].mean().reset_index()
daily_user_mean.columns = ["User Type", "Average Count"]

palette = {
    "casual": "#D3D3D3",
    "registered": "#72BCD4"
}

fig, ax = plt.subplots(figsize=(7,5))
sns.barplot(
    data=daily_user_mean,
    x="User Type",
    y="Average Count",
    hue="User Type",
    palette=palette,
    legend=False
)
ax.set_xlabel("Tipe Pengguna")
ax.set_ylabel("Rata-rata Peminjaman")
st.pyplot(fig)

# WORKINGDAY vs WEEKEND
st.subheader("⏰ Pola Jam: Hari Kerja vs Akhir Pekan")

fig, ax = plt.subplots(figsize=(12,6))
sns.lineplot(
    data=main_df,
    x="hr",
    y="cnt",
    hue="workingday",
    estimator="mean",
    ci=None
)
ax.legend(title="Working Day", labels=["Akhir Pekan", "Hari Kerja"])
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Peminjaman")
st.pyplot(fig)

# WEATHER IMPACT (RUSH HOUR)
st.subheader("🌧️ Pengaruh Cuaca pada Jam Sibuk")

rush_hour = main_df[
    (main_df["hr"].between(7,9)) |
    (main_df["hr"].between(16,18))
]

palette = {
    1: "#72BCD4",
    2: "#D3D3D3",
    3: "#D3D3D3",
    4: "#D3D3D3"
}

fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(
    data=rush_hour,
    x="weathersit",
    y="cnt",
    estimator="mean",
    hue="weathersit",
    palette=palette,
    legend=False
)
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Rata-rata Peminjaman")
st.pyplot(fig)

# DEMAND CLUSTER
st.subheader("📊 Clustering Permintaan Harian")

daily_demand = main_df.groupby("dteday")["cnt"].sum().reset_index()

daily_demand["demand_level"] = pd.cut(
    daily_demand["cnt"],
    bins=[0, 2000, 5000, daily_demand["cnt"].max()],
    labels=["Low Demand", "Medium Demand", "High Demand"]
)

palette = {
    "Low Demand": "#D3D3D3",
    "Medium Demand": "#72BCD4",
    "High Demand": "#D3D3D3"
}

fig, ax = plt.subplots(figsize=(7,5))
sns.countplot(
    data=daily_demand,
    x="demand_level",
    hue="demand_level",
    palette=palette,
    legend=False
)
ax.set_xlabel("Tingkat Permintaan")
ax.set_ylabel("Jumlah Hari")
st.pyplot(fig)

# TIME CLUSTER
st.subheader("🕒 Klaster Waktu Peminjaman")

def hour_cluster(hr):
    if hr in range(7,10):
        return "Morning Rush"
    elif hr in range(16,19):
        return "Evening Rush"
    elif hr in range(10,16):
        return "Daytime"
    else:
        return "Night / Off Peak"

main_df["time_cluster"] = main_df["hr"].apply(hour_cluster)

order = ["Morning Rush", "Daytime", "Evening Rush", "Night / Off Peak"]

palette = {
    "Morning Rush": "#D3D3D3",
    "Evening Rush": "#4FA3C7",
    "Daytime": "#D3D3D3",
    "Night / Off Peak": "#D3D3D3"
}

fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(
    data=main_df,
    x="time_cluster",
    y="cnt",
    estimator="mean",
    hue="time_cluster",
    palette=palette,
    order=order,
    legend=False
)
ax.set_xlabel("Klaster Waktu")
ax.set_ylabel("Rata-rata Peminjaman")
st.pyplot(fig)

# USER DOMINANCE
st.subheader("👥 Dominasi Pengguna per Jam")

main_df["user_dominance"] = main_df.apply(
    lambda x: "Registered Dominant"
    if x["registered"] > x["casual"]
    else "Casual Dominant",
    axis=1
)

palette = {
    "Registered Dominant": "#72BCD4",
    "Casual Dominant": "#D3D3D3"
}

fig, ax = plt.subplots(figsize=(7,5))
sns.countplot(
    data=main_df,
    x="user_dominance",
    hue="user_dominance",
    palette=palette,
    legend=False
)
ax.set_xlabel("Dominasi Pengguna")
ax.set_ylabel("Jumlah Jam")
st.pyplot(fig)

st.caption("Bike Sharing Analysis • Dicoding Submission")