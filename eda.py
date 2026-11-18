import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


def run():
    # membuat title
    st.title('Aplikasi Estimasi Harga Mobil Bekas di Jerman')

    # membuat sub header
    st.subheader('Page ini berisi Exploratory Data Analysis')

    # menulis baris
    st.write('By *Rizqi Utama*')
    st.write('Data iklan mobil bekas dari AutoScout24 tahun 2023, sudah dibersihkan seperti di notebook utama.')

    # loading dataset
    df_eda = pd.read_csv('data_eda.csv')
    st.write('Jumlah data:', len(df_eda), 'baris')
    st.dataframe(df_eda.head(100))

        # 1. Sebaran harga mobil bekas
    st.write('### 1. Berapa harga mobil bekas pada umumnya?')
    harga_umum = df_eda[df_eda['price_in_euro'] <= 100000]
    fig = plt.figure(figsize=(10, 5))
    sns.histplot(harga_umum['price_in_euro'], bins=50)
    plt.title('Sebaran Harga Mobil Bekas (di bawah €100.000)')
    plt.xlabel('Harga (€)')
    st.pyplot(fig)
    st.write('**Insight:** sebagian besar mobil bekas dijual di kisaran **€5.000 sampai €30.000**, '
             'paling banyak di sekitar **€15.000 sampai €20.000**. Mobil di atas €40.000 jauh lebih jarang.')

    # 2. Harga berdasarkan tahun mobil
    st.write('### 2. Bagaimana harga mobil berdasarkan tahunnya?')
    harga_per_tahun = df_eda.groupby('year')['price_in_euro'].median()
    fig = plt.figure(figsize=(12, 5))
    harga_per_tahun.plot(marker='o')
    plt.title('Median Harga Mobil per Tahun')
    plt.xlabel('Tahun')
    plt.ylabel('Median Harga (€)')
    plt.grid(alpha=0.3)
    st.pyplot(fig)
    st.write('**Insight:** semakin baru mobilnya, semakin mahal harganya. Mobil tahun 2010 sekitar **€8.000**, '
             'tahun 2015 sekitar **€16.000**, dan tahun 2023 sekitar **€33.000**. '
             'Mobil yang sangat tua (klasik) harganya bisa naik lagi.')

    # 3. Harga berdasarkan jarak tempuh
    st.write('### 3. Apakah jarak tempuh (odometer) memengaruhi harga?')
    kelompok_km = pd.cut(df_eda['mileage_in_km'],
                         bins=[0, 25000, 50000, 100000, 150000, 200000, float('inf')],
                         labels=['0-25rb', '25-50rb', '50-100rb', '100-150rb', '150-200rb', '>200rb'],
                         include_lowest=True)
    harga_per_km = df_eda.groupby(kelompok_km, observed=True)['price_in_euro'].median()
    fig = plt.figure(figsize=(10, 5))
    sns.barplot(x=harga_per_km.index, y=harga_per_km.values)
    plt.title('Median Harga Berdasarkan Odometer (Mileage)')
    plt.xlabel('Jarak Tempuh (km)')
    plt.ylabel('Median Harga (€)')
    st.pyplot(fig)
    st.write('**Insight:** semakin jauh jarak tempuhnya, semakin murah harganya. '
             'Mobil di bawah 25 ribu km sekitar **€30.000**, sedangkan mobil di atas 200 ribu km hanya sekitar **€6.500**.')

    # 4. Mobil biasa vs mobil mewah
    st.write('### 4. Apakah mobil mewah tetap mahal walaupun jarak tempuhnya sudah jauh?')
    merek_mewah = ['porsche', 'ferrari', 'lamborghini', 'bentley', 'rolls-royce',
                   'maserati', 'aston-martin', 'mclaren']
    df_eda['kategori'] = 'Biasa'
    df_eda.loc[df_eda['brand'].isin(merek_mewah), 'kategori'] = 'Mewah'
    df_eda['kelompok_km'] = kelompok_km
    harga_perbandingan = df_eda.groupby(['kelompok_km', 'kategori'], observed=True)['price_in_euro'].median().reset_index()
    fig = plt.figure(figsize=(12, 5))
    sns.barplot(data=harga_perbandingan, x='kelompok_km', y='price_in_euro', hue='kategori')
    plt.title('Median Harga Mobil Biasa vs Mewah Berdasarkan Odometer (Mileage)')
    plt.xlabel('Jarak Tempuh (km)')
    plt.ylabel('Median Harga (€)')
    st.pyplot(fig)
    st.write('**Insight:** iya. Mobil mewah (Porsche, Ferrari, Bentley, dll) yang sudah jalan lebih dari 200 ribu km '
             'masih sekitar **€26.000**, hampir sama dengan mobil biasa yang masih di bawah 25 ribu km. '
             'Tapi harga mobil mewah turun hampir **setengah** di 25 ribu km pertama.')

    # 5. Penurunan harga 5 merek terbanyak
    st.write('### 5. Merek mobil mana yang harganya paling stabil?')
    top5 = df_eda['brand'].value_counts().head(5).index
    data_top5 = df_eda[(df_eda['brand'].isin(top5)) & (df_eda['age'] <= 10)]
    harga_merek_umur = data_top5.groupby(['age', 'brand'])['price_in_euro'].median().reset_index()
    fig = plt.figure(figsize=(12, 6))
    sns.lineplot(data=harga_merek_umur, x='age', y='price_in_euro', hue='brand', marker='o')
    plt.title('Penurunan Harga 5 Merek Terbanyak Berdasarkan Umur Mobil')
    plt.xlabel('Umur Mobil (tahun)')
    plt.ylabel('Median Harga (€)')
    plt.grid(alpha=0.3)
    st.pyplot(fig)
    st.write('**Insight:** Mercedes-Benz dan BMW paling mahal, tapi setelah 10 tahun harganya tinggal sekitar '
             '**seperempat**. Audi, Volkswagen, dan Opel lebih stabil, masih tersisa sekitar **sepertiga**. '
             'BMW turun paling cepat di 2 tahun pertama.')

    # 6. Harga berdasarkan pilihan user (bahan bakar atau transmisi)
    st.write('### 6. Harga berdasarkan jenis bahan bakar dan transmisi')
    opsi = st.selectbox('Pilih kategori', ('fuel_type', 'transmission_type'))
    harga_per_opsi = df_eda.groupby(opsi)['price_in_euro'].median().sort_values(ascending=False)
    fig = plt.figure(figsize=(10, 5))
    sns.barplot(x=harga_per_opsi.values, y=harga_per_opsi.index)
    plt.title(f'Median Harga Mobil Bekas Berdasarkan {opsi}')
    plt.xlabel('Median Harga (€)')
    plt.ylabel(opsi)
    st.pyplot(fig)
    st.write('**Insight:** mobil **hybrid dan listrik** (sekitar €30.000) lebih mahal dibanding bensin dan diesel '
             '(sekitar €18.000 sampai €20.000). Mobil **automatic** (sekitar €27.000) hampir 2 kali lebih mahal '
             'dibanding mobil manual (sekitar €14.000).')

    # kesimpulan untuk penjual
    st.write('### Kesimpulan')
    st.write('- Faktor yang paling memengaruhi harga adalah **umur mobil, jarak tempuh, tenaga mesin, dan merek**.')
    st.write('- Mobil yang lebih baru, jarak tempuhnya rendah, dan bertransmisi automatic cenderung bisa dijual lebih mahal.')
    st.write('- Mobil merek premium lebih mahal, tapi harganya juga turun lebih cepat.')
    st.write('- Untuk estimasi harga mobil kamu, buka halaman **Prediksi Harga**.')


if __name__ == '__main__':
    run()