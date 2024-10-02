import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Mengatur lebar layout streamlit
st.set_page_config(layout="wide")

# Membaca dataset
day_df = pd.read_csv('C:/Users/Lenovo/OneDrive/Documents/studi independen bangkit/dashboard/data_clean_day.csv')
hour_df = pd.read_csv('C:/Users/Lenovo/OneDrive/Documents/studi independen bangkit/dashboard/data_clean_hour.csv')

# Sidebar untuk memilih dataset
st.sidebar.title("Bike Rental Dashboard")
selected_dataset = st.sidebar.selectbox("Pilih Dataset", ["day.csv", "hour.csv"])

# Pilihan analisis di sidebar
st.sidebar.title("Opsi Analisis")
analysis_type = st.sidebar.selectbox("Pilih Analisis", ["Cuaca dan Peminjaman", "Peminjaman per Hari Kerja", "Peminjaman per Bulan", "Peminjaman Berdasarkan Pengguna", "Visualisasi Waktu"])

# Menampilkan dataset berdasarkan pilihan
if selected_dataset == "day.csv":
    df = day_df
    st.title("Analisis Dataset Day")
else:
    df = hour_df
    st.title("Analisis Dataset Hour")

# 1. Pengelompokan data berdasarkan cuaca
if analysis_type == "Cuaca dan Peminjaman":
    st.subheader("Cuaca dan Jumlah Peminjaman Sepeda")
    # Menampilkan scatter plot (misalnya dalam analisis suhu vs jumlah peminjaman)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.scatterplot(x='temp', y='cnt', data=df, ax=ax)
    ax.set_title('Pengaruh Suhu terhadap Jumlah Peminjaman Sepeda')
    ax.set_xlabel('Suhu (Normalized)')
    ax.set_ylabel('Jumlah Peminjaman Sepeda')
    st.pyplot(fig)

# 2. Peminjaman berdasarkan hari kerja
elif analysis_type == "Peminjaman per Hari Kerja":
    st.subheader("Peminjaman Sepeda Berdasarkan Hari Kerja")
    
    # Pastikan plt.figure() diinisialisasi dengan benar
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x="workingday", y="cnt", data=df, estimator="mean", errorbar=None, ax=ax)
    ax.set_title("Rata-rata Peminjaman Sepeda pada Hari Kerja dan Hari Libur")
    ax.set_xlabel("Hari Kerja (0 = Libur, 1 = Kerja)")
    ax.set_ylabel("Rata-rata Jumlah Peminjaman Sepeda")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Libur', 'Kerja'])
    st.pyplot(fig)

# 3. Peminjaman sepeda per bulan
elif analysis_type == "Peminjaman per Bulan":
    st.subheader("Rata-rata Peminjaman Sepeda per Bulan")

    plt.figure(figsize=(8, 4))
    sns.barplot(x='mnth', y='cnt', data=df.groupby('mnth')['cnt'].mean().reset_index())
    plt.title('Rata-rata Peminjaman Sepeda per Bulan')
    plt.xlabel('Bulan')
    plt.ylabel('Rata-rata Jumlah Peminjaman Sepeda')
    plt.xticks(ticks=range(12), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)
    st.pyplot(plt)

# 5. Peminjaman Berdasarkan Pengguna (Registered vs Casual)
elif analysis_type == "Peminjaman Berdasarkan Pengguna":
    st.subheader("Peminjaman Sepeda Berdasarkan Tipe Pengguna (Registered vs Casual)")
    
    # Menghitung total peminjaman oleh pengguna registered dan casual
    total_registered = df['registered'].sum()
    total_casual = df['casual'].sum()

    # Data untuk pie chart
    labels = ['Registered', 'Casual']
    sizes = [total_registered, total_casual]
    colors = ['#ff9999','#66b3ff']
    explode = (0.1, 0)  # meledakkan bagian registered untuk penekanan

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    ax.set_title('Distribusi Peminjaman Sepeda Berdasarkan Pengguna')
    st.pyplot(fig)

# 4. Visualisasi Waktu (untuk hour.csv)
if selected_dataset == "hour.csv" and analysis_type == "Visualisasi Waktu":
    # Pastikan dataset hour.csv yang digunakan memiliki kolom 'hr'
    df['time_category'] = pd.cut(df['hr'], 
                                 bins=[-1, 6, 10, 16, 20, 24], 
                                 labels=['Night (Late)', 'Morning Rush', 'Midday', 'Evening Rush', 'Night (Early)'])

    fig, ax = plt.subplots(figsize=(10, 6))
    time_clustering = df.groupby('time_category')['cnt'].mean().reset_index()
    ax.bar(time_clustering['time_category'], time_clustering['cnt'], color='lightcoral')
    ax.set_title('Rata-rata Peminjaman Sepeda Berdasarkan Kategori Waktu')
    ax.set_xlabel('Kategori Waktu')
    ax.set_ylabel('Rata-rata Jumlah Peminjaman')
    ax.set_xticklabels(time_clustering['time_category'], rotation=45)
    st.pyplot(fig)