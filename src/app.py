import streamlit as st
import time
import psutil
import os
from input_data import load_default_products, get_manual_products
from create_blocks import create_production_blocks
from algorithms import algorithm_info
from reporting import (
    create_machine_summary, 
    create_machine_summary_avg,
    create_machine_detail, 
    plot_machine_usage, 
    plot_product_distribution, 
    plot_block_details
)

# --- Streamlit Ana Fonksiyonu ---

def main():

    start_time_code = time.time()

    st.title("Kapasite Planlama Simülatörü")

    # Girdi parametreleri
    w = st.number_input("Setup süresi (saniye)", min_value=0, value=0, step=1)
    C_days = st.number_input("Toplam çalışma süresi (gün)", min_value=1, value=1, step=1)
    usage_pct = st.slider("Kapasite kullanım limiti (%)", min_value=1, max_value=100, value=90)

    # Ürün verisi seçimi
    use_default = st.checkbox("Varsayılan ürün verisini kullan", value=False)
    if use_default:
        products = load_default_products()
        st.success(f"{len(products)} ürün varsayılan olarak yüklendi.")
    else:
        num_parts = st.number_input("Ürün sayısı", min_value=1, max_value=23, value=2, step=1)
        st.write("### Ürün Bilgileri")
        products = get_manual_products(num_parts)

    # Algoritma seçimi
    selected_algo = st.selectbox(
        "### Yerleştirme algoritmasını seçin",
        list(algorithm_info.keys()),
        index=0
    )
    
    # Simülasyonu başlatma
    if st.button("Simülasyonu Çalıştır"):
        if not products:
            st.error("Lütfen ürün verisi girin veya varsayılan veriyi seçin.")
            return

        # Üretim bloklarını oluşturma
        blocks, capacity_limit, total_work_sec = create_production_blocks(w, C_days, usage_pct, products)


        # Seçilen algoritmayı çalıştırma
        start_time = time.time()
        machines = algorithm_info[selected_algo]['func'](blocks, capacity_limit)
        end_time = time.time()
        elapsed = end_time - start_time

        st.success(f"Toplam makine sayısı: {len(machines)}")

        # --- Makine Özet Tablosu ---
        df_summary = create_machine_summary(machines, total_work_sec)
        st.write("### Makine Genel Özeti")
        st.dataframe(df_summary)
        st.download_button("Makine Genel Özeti CSV İndir", df_summary.to_csv(index=False).encode('utf-8'), "makine_genel_ozet.csv", "text/csv")

        # --- Makine Özet Tablosu Ortalmalar ---
        df_summary = create_machine_summary_avg(machines, total_work_sec)
        st.write("### Makine Genel Özeti Ortalama")
        st.dataframe(df_summary)
        st.download_button("Makine Genel Özeti Ortalama CSV İndir", df_summary.to_csv(index=False).encode('utf-8'), "makine_genel_ozet.csv", "text/csv")

        # --- Makine Detay Tablosu ---
        df_detail = create_machine_detail(machines)
        st.write("### Makine Blok Detayları")
        st.dataframe(df_detail)
        st.download_button("Blok Detayları CSV İndir", df_detail.to_csv(index=False).encode('utf-8'), "makine_blok_detay.csv", "text/csv")

        # --- Grafikler ---
        st.write("### Makine Bazlı Kapasite Kullanımı")
        fig_usage = plot_machine_usage(machines, total_work_sec)
        st.pyplot(fig_usage)

        st.write("### Makine Başına Ürün Dağılımı")
        fig_product = plot_product_distribution(machines)
        st.pyplot(fig_product)

        st.write("### Blok Bazlı Üretim Detayları")
        fig_block = plot_block_details(machines)
        st.pyplot(fig_block)

        # --- Algoritma Bilgisi ---
        st.write("### Seçilen Algoritma Bilgisi")
        st.markdown(f"**Açıklama:** {algorithm_info[selected_algo]['desc']}")
        st.markdown(f"**Zaman Karmaşıklığı:** {algorithm_info[selected_algo]['complexity']}")
        st.markdown(f"**Avantaj:** {algorithm_info[selected_algo]['advantages']}")
        st.markdown(f"**Desavantaj:** {algorithm_info[selected_algo]['disadvantages']}")
        st.markdown(f"**Algoritma Çalışma Süresi:** {elapsed:.6f} saniye")


        # --- Kod Çalışma Bilgisi ---
        end_time_code = time.time()
        execution_time = end_time_code - start_time_code

        # Bellek kullanımı
        process = psutil.Process(os.getpid())
        memory_usage_mb = process.memory_info().rss / (1024 * 1024)  # MB cinsinden

        st.write("### Kod Çalışma Bilgisi")
        st.markdown(f"**Çalışma süresi:** {execution_time:.2f} sn")
        st.markdown(f"**Bellek kullanımı:** {memory_usage_mb:.2f} MB")

if __name__ == "__main__":
    main()
