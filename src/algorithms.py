from pulp import LpProblem, LpVariable, LpMinimize, lpSum, LpBinary, PULP_CBC_CMD
from pulp import LpStatus

# ---  Algoritmalar ---

def first_fit_decreasing(blocks, capacity_limit):

    """
    Amaç, üretim bloklarını makinelerde yerleştirerek, minimum sayıda makine kullanmayı hedefler.
    """
    sorted_blocks = sorted(blocks, key=lambda b: b['block_time'], reverse=True)
    
    # Makineleri tutacak liste, her makine {'used_time':..., 'blocks':[...]} şeklinde olacak
    machines = []

    # Her bloğu sırayla makinelere yerleştirme
    for block in sorted_blocks:
        placed = False  # Bu blok yerleşti mi kontrolü
        for machine in machines:
            # Eğer makinenin mevcut süresi + bu bloğun süresi kapasiteyi aşmıyorsa
            if machine['used_time'] + block['block_time'] <= capacity_limit:
                # Bloğu makineye ekle
                machine['blocks'].append(block)
                # Kullanılan süreyi güncelle
                machine['used_time'] += block['block_time']
                placed = True  # Blok yerleştirildi
                break  
        # Eğer hiç uygun makine yoksa yeni makine aç
        if not placed:
            machines.append({'used_time': block['block_time'], 'blocks': [block]})

    return machines


def best_fit(blocks, capacity_limit):
    """
    Amaç, üretim bloklarını makinelerde yerleştirerek, mümkün olan en az boş alan ile makine kullanımını optimize etmek ve minimum makine sayısına yaklaşmak.
    """

    # Blokları sürelerine göre büyükten küçüğe sırala
    sorted_blocks = sorted(blocks, key=lambda b: b['block_time'], reverse=True)
    machines = []  # Makineleri tutacak liste

    for block in sorted_blocks:
        best_machine = None
        min_space_left = float('inf')  # En az boş alanı takip etmek için

        # Mevcut makineleri kontrol et
        for machine in machines:
            space_left = capacity_limit - machine['used_time']  # Makinede kalan boş süre
            
            # Eğer blok bu makineye sığıyor ve kalan alan minimumsa, bu makineyi seç
            if block['block_time'] <= space_left < min_space_left:
                best_machine = machine
                min_space_left = space_left

        # Eğer uygun makine bulunduysa, bloğu ekle ve makine kullanımını güncelle
        if best_machine:
            best_machine['blocks'].append(block)
            best_machine['used_time'] += block['block_time']
        else:
            # Uygun makine yoksa yeni makine aç
            machines.append({'used_time': block['block_time'], 'blocks': [block]})

    return machines

def ilp_bin_packing(blocks, capacity_limit, time_limit=60):
    """
    Amaç ILP (Integer Linear Programming) ile üretim bloklarını makinelerde en az makine kullanacak şekilde yerleştirmek. 
    Kapasite sınırları korunur ve optimum veya optimuma yakın çözüm elde edilir. 
    Eğer çözüm süre dolarsa kısmi çözüm döner veya boş liste döner.
        - time_limit: çözücünün çalışabileceği maksimum süre (saniye)
    """

    n = len(blocks)
    max_bins = n
    model = LpProblem("BinPacking", LpMinimize)

    # Değişkenler
    x = [[LpVariable(f"x_{i}_{j}", cat=LpBinary) for j in range(max_bins)] for i in range(n)]
    y = [LpVariable(f"y_{j}", cat=LpBinary) for j in range(max_bins)]


    model += lpSum(y)

    # Kısıtlar
    for i in range(n):
        model += lpSum(x[i][j] for j in range(max_bins)) == 1

    for j in range(max_bins):
        model += lpSum(blocks[i]['block_time'] * x[i][j] for i in range(n)) <= capacity_limit * y[j]

    # PULP_CBC_CMD solver ile çöz, zaman limiti ekle
    solver = PULP_CBC_CMD(msg=0, timeLimit=time_limit)
    status = model.solve(solver)

    # Çözüm durumu kontrol
    if LpStatus[status] != 'Optimal' and LpStatus[status] != 'Integer Feasible':
        # Süre doldu veya çözüm bulunamadı
        print("ILP çözümü: süre doldu veya çözüm bulunamadı. Kısmi çözüm/boş liste döndürülüyor.")
        return []

    # Sonuçları machines listesine dönüştür
    machines = []
    for j in range(max_bins):
        if y[j].varValue == 1:
            assigned_blocks = []
            used_time = 0
            for i in range(n):
                if x[i][j].varValue == 1:
                    assigned_blocks.append(blocks[i])
                    used_time += blocks[i]['block_time']
            machines.append({'used_time': used_time, 'blocks': assigned_blocks})

    return machines


# ---  Algoritma Bilgileri ---

algorithm_info = {
    'First Fit Decreasing (FFD)': {
        'func': first_fit_decreasing,
        'desc': (
            "First Fit Decreasing (FFD) algoritması, üretim bloklarını makinelerde yerleştirirken minimum makine sayısına yaklaşmayı hedefleyen "
            "hızlı ve sezgisel bir yöntemdir. Bloklar sürelerine göre büyükten küçüğe sıralanır ve her blok mevcut makinelerin ilk uygununa yerleştirilir; "
            "uygun makine yoksa yeni bir makine açılır. Basit ve anlaşılır yapısı sayesinde küçük ve orta ölçekli veri setlerinde etkin bir şekilde kullanılabilir, "
            "ancak kesin minimum makine sayısını garanti etmez ve çok büyük veri setlerinde optimal çözüme kıyasla sapma gösterebilir."
        ),
        'complexity': "Bloklar büyükten küçüğe sıralanır (O(N log N)) ve makinelerde yerleştirilir (O(N×M)). Makine sayısı blok sayısına yakınsa, toplam karmaşıklık O(N²) olarak alınabilir.",
        'advantages': "Hızlı ve uygulanması kolay, küçük/orta veri setlerinde iyi sonuç verir.",
        'disadvantages': "Optimal çözüm garanti edilmez, makine kullanım dengesi diğer yöntemlere göre daha düşük olabilir."
    },
    'Best Fit (BF)': {
        'func': best_fit,
        'desc': (
            "Best Fit (BF) algoritması, üretim bloklarını makinelerde mümkün olan en az boş alan kalacak şekilde yerleştirerek makine kullanımını optimize etmeyi hedefleyen bir sezgisel yöntemdir. "
            "Bloklar sürelerine göre büyükten küçüğe sıralanır ve her blok, mevcut makineler arasında en az boş kapasiteye sahip makineye yerleştirilir; uygun makine yoksa yeni makine açılır. "
            "Bu yaklaşım, blokların makineler arasında dengeli dağılımını sağlar ve küçük-orta ölçekli veri setlerinde hızlı ve etkili bir yaklaşık çözüm sunar."
        ),
        'complexity': "Bloklar sıralanır (O(N log N)) ve makinelerde yerleştirilir (O(N×M)). Makine sayısı blok sayısına yakınsa, toplam karmaşıklık O(N²)’dir.",
        'advantages': "Makineler arası dengeli dağılım sağlar, yaklaşık optimum sonuç verir.",
        'disadvantages': "Optimal çözüm garanti edilmez, büyük veri setlerinde hesaplama süresi artabilir."
    },
    'ILP/MIP Kesin Çözüm (pulp)': {
        'func': ilp_bin_packing,
        'desc': (
            "ILP/MIP Kesin Çözüm algoritması (pulp), üretim bloklarını makinelerde en az makine kullanacak şekilde yerleştirirken kapasite sınırlarını koruyarak optimum veya optimuma yakın çözüm elde etmeyi hedefler. "
            "Her blok yalnızca bir makineye atanabilir ve makine kapasitesi aşılmaz; amaç fonksiyonu ise toplam kullanılan makine sayısını minimize etmektir. "
            "Problem, Integer veya Mixed Integer Linear Programming formülasyonu ile modellenir ve çözücü (ör. PULP) kullanılarak çözülür. "
            "Bu yöntem, küçük ve orta ölçekli veri setlerinde doğru sonuç verir ve yaklaşık heuristik yöntemlerin yeterli olmadığı durumlarda tercih edilir."
        ),
        'complexity': "NP-Hard problem olduğundan veri büyüdükçe çözüm süresi üssel artar. Değişken ve kısıt sayısı O(N²), ILP’nin en kötü durumu O(2^(N²)), sonuç işleme O(N²) (ihmal edilebilir).",
        'advantages': "Kesin minimum makine sayısına veya optimuma çok yakın sonuç verir.",
        'disadvantages': "Büyük veri setlerinde çözüm süresi uzun ve hesaplama kaynakları yüksek olabilir."
    }
}
