# Estimasi Harga Mobil Bekas di Jerman dengan Machine Learning

## Repository Outline

```
1. description.md - Penjelasan gambaran umum project
2. P1M2_rizqi_utama.ipynb - Notebook utama: data loading, data cleaning, EDA, feature engineering, model training, model evaluation, dan model saving
3. P1M2_rizqi_utama_inf.ipynb - Notebook untuk mencoba model pada data baru (model inference)
4. P1M2_rizqi_utama_conceptual.txt - Jawaban conceptual problems
5. url.txt - URL dataset, model, dan deployment
6. deployment/ - Source code aplikasi web untuk deployment
   ├── src/streamlit_app.py - Halaman utama dan menu navigasi aplikasi
   ├── src/eda.py - Halaman Exploratory Data Analysis
   ├── src/prediction.py - Halaman estimasi harga mobil
   ├── Dockerfile - Konfigurasi untuk menjalankan aplikasi di Hugging Face Spaces
   └── requirements.txt - Daftar library yang dibutuhkan aplikasi
```

## Problem Background

Orang yang mau menjual mobil bekas sering bingung harus memasang harga berapa, karena harga mobil bekas dipengaruhi banyak hal, seperti merek, model, tahun, tenaga mesin, jarak tempuh, transmisi, dan jenis bahan bakar. Tanpa acuan, penjual hanya mengira-ngira, sehingga harga yang dipasang bisa jauh dari harga pasaran.

Pada tahun 2023, saat data ini diambil, harga mobil bekas di Jerman juga sedang tidak stabil. Menurut laporan AutoScout24, rata-rata harga mobil bekas mencapai rekor tertinggi di bulan Maret 2023, lalu terus turun hingga sekitar **€27.883** di bulan September. Di saat yang sama, stok mobil bekas di dealer naik sekitar **17%** dibanding tahun sebelumnya, dan harga mobil listrik bekas turun sekitar **€10.000** sejak awal tahun. Dengan harga pasar yang terus bergerak, penjual membutuhkan acuan harga berbasis data, bukan sekadar perkiraan.

Project ini membangun model machine learning untuk memberikan **estimasi harga pasaran mobil bekas sebagai acuan awal** sebelum penjual memasang harga. Project ini hanya fokus pada estimasi harga dari data spesifikasi mobil, dan tidak memprediksi berapa lama mobil akan laku.

## Project Output

1. **Model machine learning (regresi)** untuk estimasi harga mobil bekas, yaitu **Random Forest** hasil hyperparameter tuning.
   - Performa di data test: **MAE sekitar €3.131** (rata-rata tebakan meleset sekitar €3.100) dan **R² sekitar 0,93**.
   - Model cukup akurat untuk mobil pada umumnya, tapi kurang akurat untuk mobil mahal karena datanya lebih sedikit.
2. **Aplikasi web (Streamlit)**
   - **Prediksi Harga**: pengguna memasukkan data mobil dan langsung mendapat estimasi harga.
   - **Exploratory Data Analysis**: ringkasan insight dari data.

## Data

- **Sumber:** [Germany Used Cars Dataset 2023 (Kaggle)](https://www.kaggle.com/datasets/wspirat/germany-used-cars-dataset-2023), berisi data iklan mobil bekas dari **AutoScout24**, salah satu situs jual-beli mobil online terbesar di Eropa.
- **Ukuran:** 251.079 baris dan 15 kolom.
- **Kolom:** merek, model, warna, tanggal registrasi, tahun, harga (€), tenaga mesin (kW dan PS), transmisi, jenis bahan bakar, konsumsi bahan bakar (liter per 100 km), emisi CO2 (gram per km), jarak tempuh (km), dan deskripsi iklan.
- **Target:** `price_in_euro` (harga iklan dalam euro).
- **Kondisi data:**
  - Ada sekitar 200 baris yang **bergeser kolom** akibat proses scraping (contohnya kolom tahun berisi "Petrol"), dan baris ini dibuang.
  - Kolom konsumsi bahan bakar dan emisi masih mengandung **satuan** (contohnya "5,7 l/100 km"), sehingga dibersihkan menjadi angka.
  - Ada **missing values**, terbanyak di kolom konsumsi bahan bakar (26.873 data), dan diisi menggunakan Pipeline.
  - Ada nilai yang **tidak masuk akal**, seperti harga di bawah €500, harga di atas €500.000, jarak tempuh di atas 1 juta km, dan tenaga mesin di bawah 5 PS, yang dibuang sebelum modeling.

## Method

Project ini menggunakan **supervised learning (regresi)**.

1. **Data cleaning:** memperbaiki tipe data, membuang data yang rusak, menghapus satuan, dan membuat fitur umur mobil (`age`).
2. **Exploratory Data Analysis:** mencari faktor yang memengaruhi harga, seperti umur, jarak tempuh, tenaga mesin, merek, bahan bakar, dan transmisi.
3. **Feature engineering:**
   - Memilih fitur: 5 kategorikal (`brand`, `model`, `color`, `transmission_type`, `fuel_type`) dan 4 numerik (`age`, `mileage_in_km`, `power_ps`, `fuel_consumption_l_100km`).
   - Train-test split 80:20.
   - Pipeline preprocessing: `SimpleImputer` untuk missing values, `StandardScaler` untuk scaling, dan `OneHotEncoder` untuk encoding.
4. **Model training:** membandingkan 6 model dengan **cross validation 5 fold**: Linear Regression (baseline), KNN, SVM, Decision Tree, Random Forest, dan Gradient Boosting. **Random Forest** memberikan hasil terbaik.
5. **Hyperparameter tuning:** Random Forest di-tuning dengan `RandomizedSearchCV`, lalu dilatih ulang di seluruh data train. Log transform pada harga juga dicoba, tapi tidak memperbaiki model.
6. **Model evaluation:** menggunakan **MAE** sebagai metrik utama, serta **RMSE** dan **R²** sebagai metrik pendukung.

## Stacks

- **Bahasa pemrograman:** Python 3.9
- **Tools:** Jupyter Notebook, Visual Studio Code
- **Library:**
  - Pengolahan data: pandas, numpy
  - Visualisasi: matplotlib, seaborn
  - Machine learning: scikit-learn
  - Aplikasi web: streamlit
  - Penyimpanan model: pickle

## Reference

- **Dataset:** [Germany Used Cars Dataset 2023 (Kaggle)](https://www.kaggle.com/datasets/wspirat/germany-used-cars-dataset-2023)
- **Latar belakang masalah:** [AutoScout24 MarktReport Q3 2023](https://www.autoscout24.de/unternehmen/daten/autoscout24-marktreport-fuer-das-dritte-quartal-umschwung-im-deutschen-gebrauchtwagenmarkt-setzt-sich-fort/)
- **Model:**
- **Deployment:** 
