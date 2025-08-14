import streamlit as st  # Streamlit arayüz elemanları için

# --- Veri Girişi ---

def load_default_products():
    """
    Varsayılan ürün verilerini döner.
    Her ürün bir sözlük ile tanımlanır: 
        't_i' -> çevrim süresi (saniye)
        'q_i' -> yıllık sipariş adedi
    """
    return [
        {'t_i': 67, 'q_i': 260000},
        # {'t_i': 82, 'q_i': 260000},
        # {'t_i': 32, 'q_i': 260000},
        # {'t_i': 84, 'q_i': 260000},
        {'t_i': 20, 'q_i': 130000},
        # {'t_i': 20, 'q_i': 130000},
        {'t_i': 58, 'q_i': 130000},
        # {'t_i': 58, 'q_i': 130000},
        # {'t_i': 48, 'q_i': 130000},
        # {'t_i': 48, 'q_i': 130000},
        # {'t_i': 78, 'q_i': 130000},
        # {'t_i': 78, 'q_i': 130000},
        # {'t_i': 75, 'q_i': 130000},
        # {'t_i': 75, 'q_i': 130000},
        # {'t_i': 56, 'q_i': 130000},
        # {'t_i': 56, 'q_i': 130000},
        # {'t_i': 53, 'q_i': 130000},
        # {'t_i': 53, 'q_i': 130000},
        # {'t_i': 41, 'q_i': 130000},
        # {'t_i': 41, 'q_i': 130000},
        # {'t_i': 64, 'q_i': 130000},
        # {'t_i': 64, 'q_i': 130000},
        # {'t_i': 51, 'q_i': 130000},
    ]

def get_manual_products(num_parts):
    """
    Kullanıcının manuel olarak ürün bilgisi girmesini sağlar.
    num_parts: girilecek ürün sayısı
    Her ürün için Streamlit input alanları oluşturulur:
        - Çevrim süresi (t_i)
        - Yıllık sipariş adedi (q_i)
    Girilen veriler bir liste halinde döndürülür.
    """
    products = []
    for i in range(num_parts):
        st.write(f"**Ürün {i+1}**")  # Ürün başlığı
        # Çevrim süresi input
        t_i = st.number_input(
            f"Çevrim süresi (saniye) - Ürün {i+1}", 
            min_value=1, value=1000, step=1, key=f"t{i}"
        )
        # Yıllık sipariş adedi input
        q_i = st.number_input(
            f"Yıllık sipariş adedi - Ürün {i+1}", 
            min_value=1, value=10, step=1, key=f"q{i}"
        )
        products.append({'t_i': t_i, 'q_i': q_i})  # Ürünü listeye ekle
    return products
