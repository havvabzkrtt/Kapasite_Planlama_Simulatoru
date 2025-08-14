# Python 3.11 resmi imaj
FROM python:3.11-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Gereksinimleri kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Streamlit portu
EXPOSE 8501

# Streamlit uygulamasını başlat
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]