# Proyek Analisis Data

Proyek ini bertujuan untuk melakukan analisis data menggunakan **Google Colab (Jupyter Notebook)** sebagai media eksplorasi dan pemrosesan data, serta menyajikan hasil analisis dalam bentuk **dashboard interaktif menggunakan Streamlit** yang dijalankan melalui **Visual Studio Code**.

## Struktur Proyek

```
submission/
├── dashboard/
│   ├── all_bike_data.csv        
│   └── dashboard.py        
├── data/
│   ├── day.csv          
│   └── hour.csv           
├── notebook.ipynb           
├── README.md                
├── requirements.txt         
└── url.txt            
```

## Analisis Data (Google Colab)

Notebook digunakan untuk:

* Data loading dan data cleaning
* Exploratory Data Analysis (EDA)
* Visualisasi
* Insight
  
### Cara Menjalankan Notebook di Google Colab

1. Buka **Google Colab**: [https://colab.research.google.com/](https://colab.research.google.com/)
2. Upload file `notebook.ipynb` atau hubungkan dengan repository GitHub
3. Jalankan seluruh cell secara berurutan

### Library yang Digunakan

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
```

Jika dataset berada di Google Drive:

```python
from google.colab import drive
drive.mount('/content/drive')
```

## Dashboard Interaktif (Streamlit + VS Code)

Dashboard dibuat menggunakan **Streamlit** untuk menampilkan hasil analisis secara interaktif.

### Setup Environment (Visual Studio Code)

Disarankan menggunakan **Conda Environment**.

```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install numpy pandas scipy matplotlib seaborn jupyter streamlit
```

### Menjalankan Dashboard

Masuk ke folder dashboard, lalu jalankan:

```bash
streamlit run dashboard.py
```

Dashboard akan terbuka otomatis di browser
