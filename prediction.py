# Import libraries
import pickle
import pandas as pd
import streamlit as st

# Load model final 
with open('model_final.pkl', 'rb') as file_1:
  model_final = pickle.load(file_1)

# ambil daftar kategori
encoder = model_final.named_steps['preprocessor'].named_transformers_['kategori'].named_steps['encoder']
list_brand = sorted(encoder.categories_[0])
list_model = sorted(encoder.categories_[1])
list_color = sorted(encoder.categories_[2])
list_transmission = sorted(encoder.categories_[3])
list_fuel = sorted(encoder.categories_[4])


# fungsi inputan user
def run():
    # heading
    st.write('# ***Estimasi Harga Mobil Bekas***')
    st.write('Masukkan data mobil untuk mendapatkan estimasi harga pasaran sebagai acuan awal.')

    # pembuatan form
    with st.form('mobil-bekas-hck-046'):
        brand = st.selectbox('Merek', list_brand)
        model = st.selectbox('Model', list_model, help='Pilih model yang sesuai dengan merek')
        color = st.selectbox('Warna', list_color)
        st.markdown('-----')
        year = st.number_input('Tahun Mobil', min_value=1995, max_value=2023, value=2018, step=1, help='Tahun mobil dibuat')
        mileage = st.number_input('Jarak Tempuh (km)', min_value=0, max_value=1000000, value=50000, step=1000)
        power = st.number_input('Tenaga Mesin (PS)', min_value=5, max_value=1000, value=150)
        st.markdown('-----')
        transmission = st.selectbox('Transmisi', list_transmission)
        fuel = st.selectbox('Bahan Bakar', list_fuel)
        consumption = st.number_input('Konsumsi Bahan Bakar (liter per 100 km)', min_value=0.0, max_value=30.0, value=6.0, step=0.1)

        submitted = st.form_submit_button('Estimasi Harga')

    data_inf = {
        'brand': brand,
        'model': model,
        'color': color,
        'transmission_type': transmission,
        'fuel_type': fuel,
        'age': 2023 - year,  
        'mileage_in_km': mileage,
        'power_ps': power,
        'fuel_consumption_l_100km': consumption
    }

    data_inf = pd.DataFrame([data_inf])
    st.dataframe(data_inf)

    if submitted:
        y_pred_inf = model_final.predict(data_inf)
        st.write('# Estimasi Harga: €', str(int(y_pred_inf[0])))
        st.caption('Estimasi ini berdasarkan data iklan mobil bekas di Jerman tahun 2023 '
                   'dan belum memperhitungkan kondisi fisik mobil.')


if __name__ == '__main__':
    run()