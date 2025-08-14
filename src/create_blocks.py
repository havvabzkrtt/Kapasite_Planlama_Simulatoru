# --- Blok Oluşturma --- 

def create_production_blocks(setup_time, work_days, usage_pct, products):

    # Toplam çalışma süresini saniyeye çevir
    total_work_sec = work_days * 24 * 3600

    # Kapasite kullanım limiti 
    capacity_limit = total_work_sec * usage_pct / 100 

    blocks = []
    # Her ürün için blokları oluştur
    for idx, product in enumerate(products):
        cycle_time = product['t_i'] + setup_time  # Bir ürün çevrim süresi + setup
        total_time = product['q_i'] * cycle_time  # Tüm adetlerin toplam süresi

        if total_time <= capacity_limit:
            blocks.append({
                'product_id': idx+1,
                'qty': product['q_i'],
                'block_time': total_time
            })
        else:
            # Eğer blok kapasiteyi aşarsa, blokları parçalara ayır
            max_qty_per_block = int(capacity_limit // cycle_time) 
            remaining_qty = product['q_i']
            while remaining_qty > 0:
                qty_block = min(remaining_qty, max_qty_per_block)  # Blok boyutu
                block_time = qty_block * cycle_time # Blok süresi = blok sayısı * çevrim süresi
                blocks.append({
                    'product_id': idx+1,
                    'qty': qty_block,
                    'block_time': block_time
                })
                remaining_qty -= qty_block  # Kalan adedi güncelle

    return blocks, capacity_limit, total_work_sec
