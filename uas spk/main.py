import streamlit as st
import numpy as np
import pandas as pd

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

L = np.array(['benefit', 'benefit', 'cost', 'benefit', 'cost'])

# Sesuaikan bobot dan arah preferensi sesuai dengan preferensi Anda
W = np.array([0.4, 0.4, 0.1, 0.05, 0.05])

def click_button():
    st.session_state.clicked = True

def sample_topsis(values, label):
    if not values.shape[0] == label.shape[0]:
        st.write('Jumlah kriteria dan label tidak sama')
        return

    norm_value = []

    for i in range(values.shape[0]):
        if label[i] == 'benefit':
            norm_c = values[i] / np.sqrt(np.sum(values[i]**2))
        elif label[i] == 'cost':
            norm_c = np.sqrt(np.sum(values[i]**2)) / values[i]

        norm_value.append(norm_c)

    norm_all = np.transpose(norm_value)
    return norm_all

def calculate_topsis(values, weight):
    if not values.shape[0] == weight.shape[0]:
        print('Jumlah kriteria dan bobot tidak sama')
        return

    alt_crit_value = []
    all_value = []
    all_topsis = []

    values = np.transpose(values)

    for i in range(values.shape[0]):
        for j in range(values[i].shape[0]):
            val = values[i][j] * weight[j]
            alt_crit_value.append(val)

        all_value.append(alt_crit_value)
        alt_crit_value = []

        topsis = np.sqrt(np.sum(np.array(all_value)**2))
        all_topsis.append(topsis)
        all_value = []

    return all_topsis

def ranking(vector):
    temp = vector.argsort()
    ranks = np.empty_like(temp)
    ranks[temp] = np.arange(len(vector))

    return len(vector) - ranks

def run():
    st.set_page_config(
        page_title="Implementasi TOPSIS",
        page_icon="🏢",
    )

    st.write("# Implementasi Metode TOPSIS")
    st.write("Dikembangkan oleh Heru Lukis Setiyawan untuk UAS")

    st.markdown( 
        """
        Metode Technique for Order of Preference by Similarity to Ideal Solution (TOPSIS) adalah salah satu metode dalam Sistem Pendukung Keputusan yang digunakan untuk memilih alternatif terbaik dari sekelompok alternatif berdasarkan kedekatan mereka dengan solusi ideal. Metode ini mempertimbangkan kedekatan positif dengan solusi ideal positif dan kedekatan negatif dengan solusi ideal negatif.
        
        Contoh kasus yang akan diimplementasikan pada aplikasi ini adalah sebagai berikut:

        Seorang wirausaha sedang mencari ruko yang tepat untuk membuka usaha jualan retail. Dia memiliki beberapa opsi ruko yang berbeda. Kriteria pemilihan ruko yang digunakan adalah sebagai berikut:

        - Lokasi Strategis (C1): Semakin strategis lokasi ruko, semakin baik. (Benefit)
        - Luas Ruang (C2): Semakin besar luas ruko, semakin baik. (Benefit)
        - Biaya Sewa (C3): Semakin rendah biaya sewa, semakin baik. (Cost)
        - Fasilitas Publik di Sekitar (C4): Semakin banyak fasilitas publik di sekitar, semakin baik. (Benefit)
        - Jumlah Pesaing di Area Terdekat (C5): Semakin sedikit pesaing, semakin baik. (Cost)
    """
    )

    st.divider()

    st.write("## Input Informasi Ruko")

    lokasi = st.slider("Lokasi Strategis (1-10)", min_value=1, max_value=10, value=1, step=1)
    luas_ruang = st.slider("Luas Ruang (1-10)", min_value=1, max_value=10, value=1, step=1)
    biaya_sewa = st.slider("Biaya Sewa (1-10)", min_value=1, max_value=10, value=1, step=1)
    fasilitas_publik = st.slider("Fasilitas Publik di Sekitar (1-10)", min_value=1, max_value=10, value=1, step=1)
    jumlah_pesaing = st.slider("Jumlah Pesaing di Area Terdekat (1-10)", min_value=1, max_value=10, value=1, step=1)

    if st.button("Simpan", type='primary', on_click=click_button):
        simpanData(lokasi, luas_ruang, biaya_sewa, fasilitas_publik, jumlah_pesaing)
    
    if st.session_state.clicked:
        data = st.session_state.nilai_ruko
        df = pd.DataFrame(data, columns=('Lokasi', 'Luas Ruang', 'Biaya Sewa', 'Fasilitas Publik', 'Jumlah Pesaing'))
        st.dataframe(df)

        if st.button("Proses"):
            prosesData()


def simpanData(lokasi, luas_ruang, biaya_sewa, fasilitas_publik, jumlah_pesaing):
    if 'nilai_ruko' not in st.session_state:
        st.session_state.nilai_ruko = np.array([[lokasi, luas_ruang, biaya_sewa, fasilitas_publik, jumlah_pesaing]])
    else:
        dataLama = st.session_state.nilai_ruko
        dataBaru = np.append(dataLama, [[lokasi, luas_ruang, biaya_sewa, fasilitas_publik, jumlah_pesaing]], axis=0)
        st.session_state.nilai_ruko = dataBaru

def prosesData():
    ruko = st.session_state.nilai_ruko

    if len(ruko) < 2:
        st.warning("Harap masukkan minimal 2 data untuk diproses.")
        return

    norm_ruko = sample_topsis(ruko, L)
    topsis_result = calculate_topsis(norm_ruko, W)
    rank = ranking(np.asarray(topsis_result))

    st.write("Informasi Ruko:")
    st.dataframe(pd.DataFrame(ruko, columns=('Lokasi', 'Luas Ruang', 'Biaya Sewa', 'Fasilitas Publik', 'Jumlah Pesaing')))

    st.write("Normalisasi Nilai Ruko:")
    st.dataframe(pd.DataFrame(norm_ruko, columns=('Lokasi', 'Luas Ruang', 'Biaya Sewa', 'Fasilitas Publik', 'Jumlah Pesaing')))

    st.write("Perhitungan Nilai TOPSIS:")
    st.dataframe(pd.DataFrame(topsis_result, columns=['Nilai TOPSIS']))

    st.write("Perankingan Ruko:")
    st.dataframe(pd.DataFrame(rank, columns=['Peringkat']))


if __name__ == "__main__":
    run()
