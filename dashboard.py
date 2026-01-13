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

daily_df = main_df.groupby(["dteday", "yr"])["cnt"].sum().reset_index()

fig, ax = plt.subplots(figsize=(14,6))

for yr, label in [(0, "2011"), (1, "2012")]:
    subset = daily_df[daily_df["yr"] == yr]
    ax.plot(subset["dteday"], subset["cnt"], label=label)

max_day = daily_df.loc[daily_df["cnt"].idxmax()]
ax.scatter(max_day["dteday"], max_day["cnt"])
ax.annotate(
    f"Puncak: {int(max_day['cnt'])}",
    (max_day["dteday"], max_day["cnt"]),
    xytext=(10,10),
    textcoords="offset points"
)

ax.set_title("Tren Peminjaman Sepeda Harian (2011–2012)")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Peminjaman")
ax.legend(title="Tahun")
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
    legend=False,
    ax=ax
)

ax.set_title("Peminjaman Sepeda Berdasarkan Musim (2011–2012)")
ax.set_xlabel("Musim")
ax.set_ylabel("Rata-rata Jumlah Peminjaman")
st.pyplot(fig)

# USER CONTRIBUTION
st.subheader("👤 Kontribusi Casual vs Registered")

yearly = main_df.groupby("yr")[["casual", "registered", "cnt"]].sum().reset_index()
yearly["yr"] = yearly["yr"].map({0: "2011", 1: "2012"})

yearly_melt = yearly.melt(
    id_vars=["yr", "cnt"],
    value_vars=["casual", "registered"],
    var_name="User Type",
    value_name="Total Peminjaman"
)

fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(
    data=yearly_melt,
    x="yr",
    y="Total Peminjaman",
    hue="User Type",
    ax=ax
)

ax.ticklabel_format(style='plain', axis='y')
ax.set_title("Kontribusi Pengguna Casual vs Registered\n(2011–2012)")
ax.set_xlabel("Tahun")
ax.set_ylabel("Jumlah Peminjaman")
st.pyplot(fig)

# WORKINGDAY vs WEEKEND
st.subheader("⏰ Pola Jam: Hari Kerja vs Akhir Pekan")

hour_pattern = main_df.groupby(["hr", "workingday"])["cnt"].mean().reset_index()

fig, ax = plt.subplots(figsize=(10,5))

for wd, label in [(0, "Akhir Pekan"), (1, "Hari Kerja")]:
    subset = hour_pattern[hour_pattern["workingday"] == wd]
    ax.plot(subset["hr"], subset["cnt"], marker="o", label=label)

ax.set_title("Peminjaman Sepeda per Jam (2011–2012)")
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Peminjaman")
ax.legend()
st.pyplot(fig)

# WEATHER IMPACT (RUSH HOUR)
st.subheader("🌧️ Pengaruh Cuaca pada Jam Sibuk")

rush_hour = main_df[
    (main_df["hr"].between(7,9)) |
    (main_df["hr"].between(16,18))
]

fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(
    data=rush_hour,
    x="hr",
    y="cnt",
    hue="weathersit",
    estimator="mean",
    ax=ax
)

ax.set_title("Rata-rata Peminjaman pada Jam Sibuk\nBerdasarkan Jam & Cuaca")
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Jumlah Peminjaman")
st.pyplot(fig)

# TIME CLUSTER
st.subheader("🕒 Cluster Waktu Peminjaman")

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
    "Evening Rush": "#72BCD4",
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
ax.set_xlabel("Cluster Waktu")
ax.set_ylabel("Rata-rata Peminjaman")
st.pyplot(fig)

# SPATIAL PROXY ANALYSIS (Season vs Weekday)
st.subheader("🗺️ Pola Peminjaman: Musim vs Hari")

season_weekday = main_df.pivot_table(
    values="cnt",
    index="season_hour",
    columns="weekday",
    aggfunc="mean"
)

fig, ax = plt.subplots(figsize=(10,6))
sns.heatmap(
    season_weekday,
    annot=True,
    fmt=".0f",
    cmap="YlGnBu",
    ax=ax
)
ax.set_title("Heatmap Rata-rata Peminjaman\nMusim vs Hari")
ax.set_xlabel("Weekday")
ax.set_ylabel("Season")

st.pyplot(fig)

st.caption("Bike Sharing Analysis • Dicoding Submission")


