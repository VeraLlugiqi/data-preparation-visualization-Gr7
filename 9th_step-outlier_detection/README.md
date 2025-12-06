# Hapi 9: Detektimi i Përjashtuesve (Outlier Detection)

## Përshkrim

Ky hap implementon tre metoda të ndryshme për detektimin e përjashtuesve (outliers) në datasetin e universiteteve. Përjashtuesit janë pikë të dhënash që devijojnë në mënyrë të konsiderueshme nga të dhënat e tjera dhe mund të tregojnë anomali, gabime, ose karakteristika unike të vërteta.

## Input

- **Skedar:** `../final_dataset.csv`
- **Rreshta:** 2,895
- **Kolona:** 39 karakteristika (numerike dhe kategorike)
- **Vite:** 2012-2015

## Metodat e Implementuara

### 1. Metoda IQR (Interquartile Range)

**Script:** `outlier_detection_iqr.py`

**Përshkrim:**  
Metoda IQR është një teknikë statistikore univariate që përdor kuartilet për të identifikuar përjashtues.

**Formula:**
```
IQR = Q3 - Q1
Lower Bound = Q1 - 1.5 × IQR
Upper Bound = Q3 + 1.5 × IQR

Outlier nëse: value < Lower Bound OSE value > Upper Bound
```

**Karakteristikat e Analizuara:**
- Rezultate akademike: `teaching`, `international`, `research`, `citations`
- Metrika institucionale: `num_students`, `student_staff_ratio`, `international_students`
- Rezultate CWUR: `cwur_score`
- Metrika të derizuara: `rank_gap`, `research_efficiency_per_1k`, `faculty_efficiency`, `global_influence_index`
- Metrika relative: `relative_teaching`, `relative_citations`, `relative_cwur_score`
- Z-scores: `teaching_z`, `citations_z`, `num_students_z`, `relative_teaching_z`, `relative_citations_z`

**Output:**
- `outliers_iqr.csv` - Detaje të plota për çdo outlier (row index, university, feature, value, bounds)
- `outliers_iqr_summary.csv` - Përmbledhje e outliers për kolonë
- `outliers_iqr_boxplots.png` - Boxplots për 8 kolonat me më shumë outliers
- `outliers_iqr_counts.png` - Histogram i numrit të outliers për kolonë
- `outliers_iqr_top_universities.png` - Top 10 universitete me më shumë outlier features

**Avantazhet:**
- E thjeshtë dhe e kuptueshme
- Nuk varet nga supozimi i normalitetit
- Rezistent ndaj outliers ekstreme
- E mirë për distributime të pjerrëta (skewed)

**Disavantazhet:**
- Analizon vetëm një kolonë në një kohë (univariate)
- Mund të identifikojë shumë false positives në distributime jo-normale

---

### 2. Metoda Z-Score (Standard Score)

**Script:** `outlier_detection_zscore.py`

**Përshkrim:**  
Metoda Z-Score mat sa devijime standarde larg mesatares është një vlerë. Vlera me |Z-score| > 3 konsiderohen outliers (99.7% e të dhënave normale janë brenda ±3σ).

**Formula:**
```
Z = (X - μ) / σ

Ku:
- X = vlera e observuar
- μ = mesatarja
- σ = devijimi standard

Outlier nëse: |Z| > 3
```

**Threshold:** |Z-score| > 3 (99.7% confidence level për distribucion normal)

**Output:**
- `outliers_zscore.csv` - Detaje për çdo outlier (university, feature, value, z-score, mean, std)
- `outliers_zscore_summary.csv` - Përmbledhje e outliers për kolonë
- `outliers_zscore_counts.png` - Histogram i numrit të outliers për kolonë
- `outliers_zscore_distributions.png` - Distribucionet e Z-scores për 8 kolonat kryesore
- `outliers_zscore_top_universities.png` - Top 10 universitete me më shumë outlier features
- `outliers_zscore_heatmap.png` - Heatmap e Z-scores për top universities dhe features

**Avantazhet:**
- E lehtë për tu interpretuar (në njësi devijimesh standarde)
- Matje probabilistike (bazohet në distribucion normal)
- Threshold i qartë dhe i mirëkuptuar

**Disavantazhet:**
- Supozon distribucion normal
- Ndjeshëm ndaj outliers ekstreme (mean dhe std ndikohen)
- Univariate (një kolonë në një kohë)

---

### 3. Metoda Isolation Forest (Multivariate)

**Script:** `outlier_detection_isolation_forest.py`

**Përshkrim:**  
Isolation Forest është një algoritëm machine learning që identifikon outliers bazuar në parimin se outliers janë më të lehtë për t'u izoluar në një strukturë druri. Kjo metodë është multivariate - analizon shumë karakteristika së bashku për të identifikuar kombinime të pazakonta.

**Algoritmi:**
1. Krijon pemë të rastësishme (random trees)
2. Outliers izolohen me më pak splits (janë "më të lehta" për t'u ndarë)
3. Llogarit anomaly score për çdo pikë

**Parametra:**
- `contamination=0.1` - Pret që 10% e të dhënave të jenë outliers
- `n_estimators=100` - 100 pemë të rastësishme
- `random_state=42` - Për riprodhueshmëri

**Karakteristikat e Përdorura (15 total):**
```python
features = [
    'teaching', 'international', 'research', 'citations',
    'num_students', 'student_staff_ratio', 'international_students',
    'cwur_score', 'rank_gap', 'research_efficiency_per_1k',
    'faculty_efficiency', 'global_influence_index',
    'relative_teaching', 'relative_citations', 'relative_cwur_score'
]
```

**Preprocessing:**
- StandardScaler për të normalizuar të dhënat (mean=0, std=1)
- Heqje e NaN values

**Output:**
- `outliers_isolation_forest.csv` - Universitete outliers me anomaly scores dhe të gjitha features
- `outliers_isolation_forest_summary.csv` - Statistika përmbledhëse
- `outliers_isolation_forest_scores.png` - Distribucion i anomaly scores (outliers vs inliers)
- `outliers_isolation_forest_top20.png` - Top 20 universitete më anomale
- `outliers_isolation_forest_scatter.png` - Scatter plots për kombinime kryesore të features
- `outliers_isolation_forest_comparison.png` - Heatmap krahasues: outliers vs inliers
- `outliers_isolation_forest_by_country.png` - Outliers sipas shtetit

**Avantazhet:**
- Multivariate - kapton marrëdhënie komplekse midis features
- Nuk supozon distribucion specifik
- Efektiv për high-dimensional data
- Rezistent ndaj noise
- Më pak false positives për outliers "lokale"

**Disavantazhet:**
- Më pak i interpretuar se metodat tradicionale
- Kërkon tuning të parametrave (contamination)
- Computationally më intensiv

---

## Krahasimi i Metodave

| Aspekti | IQR | Z-Score | Isolation Forest |
|---------|-----|---------|------------------|
| **Tipi** | Univariate | Univariate | Multivariate |
| **Supozime** | Asnjë | Normalitet | Asnjë |
| **Interpretim** | I lehtë | I mesëm | I vështirë |
| **Sensitivitet** | I ulët | I lartë | I mesëm |
| **False Positives** | Të larta | Të mesme | Të ulëta |
| **Computational Cost** | I ulët | I ulët | I lartë |
| **Outliers Ekstreme** | I mirë | Problematik | I mirë |
| **Outliers Multivariate** | S'kapton | S'kapton | Kapton |

---

## Si të Ekzekutosh

### 1. Ekzekuto metodën IQR:
```bash
cd 9th-step-outlier-detection
python outlier_detection_iqr.py
```

### 2. Ekzekuto metodën Z-Score:
```bash
python outlier_detection_zscore.py
```

### 3. Ekzekuto metodën Isolation Forest:
```bash
python outlier_detection_isolation_forest.py
```

**Kohëzgjatja:** ~1-2 minuta për çdo script

---

## Output Files - Struktura

### CSV Files

**outliers_iqr.csv:**
```
row_index, university_name, country, year, feature, value, lower_bound, upper_bound, Q1, Q3, IQR
```

**outliers_zscore.csv:**
```
row_index, university_name, country, year, feature, value, z_score, mean, std
```

**outliers_isolation_forest.csv:**
```
university_name, country, year, anomaly_score, [15 feature columns]
```

### Vizualizime

Të gjitha vizualizimet ruhen si PNG files me rezolucion 300 DPI:
- Boxplots për distribucionet
- Bar charts për numërimin
- Scatter plots për marrëdhëniet
- Heatmaps për krahasimet
- Histograms për distribucionet

---

## Gjetje të Përgjithshme

### Outliers të Zakonshëm:
1. **Universitete shumë të mëdha** (num_students >> mean)
2. **Universitete shumë të vogla** specializuara
3. **Raporti i lartë studentë ndërkombëtarë** (qendra të specializuara)
4. **Research efficiency ekstreme** (universitete të vogla me output të lartë kërkimor)
5. **Faculty efficiency i pazakontë** (raporti i pazakontë staf-student)

### Outliers Legitimë:
- Top universitete (Harvard, MIT, Oxford) kanë vlera ekstreme **legjitime**
- Universitete të specializuara (medicale, teknologjike) kanë profile unike
- Universitete në vende të vogla mund të kenë metrika të pasonormale

---

## Hapat e Ardhshëm

Pas detektimit, outliers duhet:
1. **Validuar** - A janë gabime apo vlera legjitime?
2. **Analizuar** - Pse janë outliers?
3. **Trajtuar** - Mbajtur, hequr, apo transformuar?

Këto do të trajtohen në:
- **Hapi 10:** Shmangja e False Positives dhe Validimi Kontekstual
- **Hapi 11:** Data Mining dhe Analiza e Outliers në kontekstin e përgjithshëm

---

## Kërkesat (Dependencies)

```bash
pip install pandas numpy matplotlib seaborn scikit-learn scipy
```

**Versione të testuara:**
- pandas >= 1.3.0
- numpy >= 1.21.0
- matplotlib >= 3.4.0
- seaborn >= 0.11.0
- scikit-learn >= 0.24.0
- scipy >= 1.7.0

---

**Data:** 23.11.2024  
**Grupi:** 7  
**Hapi:** 9 - Outlier Detection
