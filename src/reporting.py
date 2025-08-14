
import pandas as pd
import matplotlib.pyplot as plt

# --- Raporlama Fonksiyonları ---

def create_machine_summary(machines, total_work_sec):
    """
    Makine bazlı özet tablo oluşturur.
    Her makinenin toplam kullanılan süresi (used), kapasite yüzdesi (usage_pct) ve yaklaşık çalışma günü (work_days) hesaplanır.
    """
    summary = []  
    for i, machine in enumerate(machines, 1): 
        used = machine['used_time']  # Makinede kullanılan toplam süre (saniye)
        usage_pct = used / total_work_sec * 100  # Kapasite kullanım yüzdesi / total_work_sec = work_days * 24 * 360
        work_days = used / (24 * 3600)  # Kullanılan süreyi gün cinsine çevir

        summary.append({
            'Makine': i,
            'Kullanılan Süre (sn)': round(used),
            'Kapasite Kullanımı (%)': round(usage_pct, 2),
            'Yaklaşık Çalışma Günü': round(work_days, 2)
        })
    return pd.DataFrame(summary)  


def create_machine_summary_avg(machines, total_work_sec):
    """
    Makine özetinden toplam ve ortalama değerleri döndürür.
    """
    df = create_machine_summary(machines, total_work_sec)
    
    summary_totals = {
        "Makine Sayısı": len(df),
        "Ortalama Kullanılan Süre (sn)": round(df["Kullanılan Süre (sn)"].mean(), 2),
        "Ortalama Kapasite Kullanımı (%)": round(df["Kapasite Kullanımı (%)"].mean(), 2),
        # "Toplam Çalışma Günü": round(df["Yaklaşık Çalışma Günü"].sum(), 2),
        "Ortalama Çalışma Günü": round(df["Yaklaşık Çalışma Günü"].mean(), 2)
    }
    
    return pd.DataFrame([summary_totals])

def create_machine_detail(machines):
    """
    Makine bazlı detay tablo oluşturur.
    Her makinedeki bloklar ve bu blokların içerikleri (ürün, adet, blok süresi) listelenir.
    Her blok bir satır olarak tabloya eklenir ve pandas DataFrame döner.
    """
    details = []  
    for i, machine in enumerate(machines, 1):  # Makine numarası 1'den başlar
        for block in machine['blocks']:  # Makinedeki her bloğu sırayla işler
            details.append({
                'Makine': i,
                'Ürün': block['product_id'],       # Bloğun hangi ürüne ait olduğu
                'Adet': block['qty'],              # Bloğun içindeki ürün adedi
                'Blok Süresi (sn)': round(block['block_time'])  # Bloğun toplam çalışma süresi
            })
    return pd.DataFrame(details)  

def plot_machine_usage(machines, total_work_sec):
    """
    Makine başına kapasite kullanımını bar grafiği olarak çizer.
    """
    machine_ids = list(range(1, len(machines)+1)) 
    usage_percents = [m['used_time']/total_work_sec*100 for m in machines]

    fig, ax = plt.subplots()  
    ax.bar(machine_ids, usage_percents, color='cornflowerblue')  
    ax.set_xlabel("Makine No")  
    ax.set_ylabel("Kapasite Kullanımı (%)")  
    ax.set_title("Makine Bazlı Kapasite Kullanımı")  
    ax.set_ylim(0, 100)  
    return fig  


def plot_product_distribution(machines):
    """
    Makine başına ürün dağılımını stacked bar chart ile gösterir.
    """
    data = {}
    for i, machine in enumerate(machines, 1):
        for block in machine['blocks']:
            product = f"Ürün {block['product_id']}"
            data.setdefault(product, []).append((i, block['qty']))

    machine_ids = range(1, len(machines)+1)
    product_names = sorted(data.keys())
    df = pd.DataFrame(0, index=machine_ids, columns=product_names)
    for product, entries in data.items():
        for m_id, qty in entries:
            df.at[m_id, product] += qty

    ax = df.plot(kind='bar', stacked=True, figsize=(10,6))
    ax.set_xlabel("Makine No")
    ax.set_ylabel("Ürün Adedi")
    ax.set_title("Makine Başına Ürün Dağılımı")
    return ax.get_figure()


def plot_block_details(machines):
    """
    Her blok için adet ve süreyi aynı grafikte gösterir (bar + line grafiği)
    """

    block_ids = []
    block_times = []
    block_qtys = []

    counter = 1
    for machine in machines:
        for block in machine['blocks']:
            block_ids.append(counter)
            block_times.append(block['block_time'])
            block_qtys.append(block['qty'])
            counter += 1

    fig, ax1 = plt.subplots(figsize=(10,6))
    ax2 = ax1.twinx()

    ax1.bar(block_ids, block_qtys, color='skyblue', label='Adet')
    ax2.plot(block_ids, block_times, color='orange', marker='o', label='Blok Süresi (sn)')

    ax1.set_xlabel("Blok ID")
    ax1.set_ylabel("Adet", color='skyblue')
    ax2.set_ylabel("Blok Süresi (sn)", color='orange')
    ax1.set_title("Blok Bazlı Üretim Detayları")
    
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    return fig
