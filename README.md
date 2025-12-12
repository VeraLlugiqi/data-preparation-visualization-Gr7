# Përgatitja dhe Vizualizimi i të Dhënave - Projekt Gr7

Ky projekt përmban përgatitjen dhe pastrimin e të dhënave të renditjes së universiteteve nga dy burime: Times Higher Education (THE) dhe Center for World University Rankings (CWUR). Projekti është organizuar në 8 hapa kryesorë, secili me procesin e vet të transformimit të të dhënave.

---

## Përmbledhje e Procesit

Procesi fillon me bashkimin e dy datasetave (THE dhe CWUR), pastaj bëhet pastrimi i të dhënave, konvertimi i tipave, filtrim i viteve, imputim i vlerave munguese, kampionim, agregim dhe krijim i karakteristikave të reja deri në transformim dhe diskretizim final.

---

## Hapi 1: Bashkimi i të Dhënave (`1st_step-merging`)

### Përshkrim
Ky hap bashkon dy datasetat e renditjes së universiteteve: `timesData.csv` (Times Higher Education) dhe `cwurData.csv` (Center for World University Rankings) në një dataset të vetëm.

### Kolona të Krijuara

**Kolonat origjinale nga Times Data (14 kolona):**
- `world_rank` - Pozicioni në renditjen botërore (integer, më i ulët = më mirë)
- `university_name` - Emri i universitetit (string)
- `country` - Shteti i universitetit (string)
- `teaching` - Rezultati për mësimdhënie (0-100, më i lartë = më mirë)
- `international` - Rezultati për perspektivë ndërkombëtare (0-100, më i lartë = më mirë)
- `research` - Rezultati për kërkime (0-100, më i lartë = më mirë)
- `citations` - Rezultati për citime (0-100, më i lartë = më mirë)
- `income` - Rezultati për të ardhura industriale (0-100, më i lartë = më mirë)
- `total_score` - Rezultati total (0-100, më i lartë = më mirë)
- `num_students` - Numri i studentëve (integer)
- `student_staff_ratio` - Raporti student-staf (float, p.sh. 8.9)
- `international_students` - Përqindja e studentëve ndërkombëtarë (string, p.sh. "25%")
- `female_male_ratio` - Raporti meshkuj-femra (string, p.sh. "42:58:00")
- `year` - Viti i renditjes (2011-2016)

**Kolonat e shtuara nga CWUR Data (11 kolona):**
- `cwur_world_rank` - Pozicioni në renditjen botërore CWUR (integer, më i ulët = më mirë)
- `cwur_national_rank` - Pozicioni në renditjen kombëtare (integer)
- `cwur_quality_of_education` - Renditja për cilësinë e arsimit (integer)
- `cwur_alumni_employment` - Renditja për punësimin e alumni (integer)
- `cwur_quality_of_faculty` - Renditja për cilësinë e fakultetit (integer)
- `cwur_publications` - Renditja për publikimet (integer)
- `cwur_influence` - Renditja për influencën (integer)
- `cwur_citations` - Renditja për citimet (integer)
- `cwur_broad_impact` - Renditja për ndikimin e gjerë (integer)
- `cwur_patents` - Renditja për patentat (integer)
- `cwur_score` - Rezultati total CWUR (numeric)

**Formula e Bashkimit:**
Bashkimi bëhet duke përdorur outer join në:
- `year` (përputhje e saktë)
- `normalized_university_name` (emër i normalizuar për përputhje më të mirë)


---

## Hapi 2: Konvertimi i Tipave (`2nd_step-changing_types`)

### Përshkrim
Ky hap pastron dhe konverton kolonat e datasetit të bashkuar në formatet e duhura numerike për analizë.

### Proces
1. Konvertohen kolonat numerike nga string në int/float
2. Pastrohen vlerat (heqja e presjeve, përqindjeve, diapazoneve)
3. Transformohet `female_male_ratio` në `female_male_percent`
4. Vlerat e paparsueshme vendosen si NaN

### Kolona të Modifikuara

**`female_male_percent` (i krijuar nga `female_male_ratio`):**
- **Formula:** Nëse format është "X:Y", atëherë: `female_percent = (X / (X + Y)) * 100`
- Nëse format është "X%", atëherë: `female_percent = X`
- **Tip:** float (përqindje e studentëve femra)

**Kolonat numerike të konvertuara:**
- `world_rank`, `cwur_world_rank`, `cwur_national_rank` → int
- `teaching`, `international`, `research`, `citations`, `income`, `total_score` → float
- `num_students`, `student_staff_ratio`, `international_students` → float
- Të gjitha kolonat CWUR → int/float

**Formula e Pastrimit:**
Për çdo kolonë numerike:
1. Heq presjet: "1,234" → 1234
2. Nxjerr numrin e parë nga diapazonet: "100-200" → 100
3. Konverton përqindje: "14%" → 14.0 (ose 0.14 për raporte)

**Rezultati:** Dataset i pastër me tipet e duhura për analizë

---

## Hapi 3: Filtrimi i Viteve (`3rd_step-filtering_years`)

### Përshkrim
Ky hap filtron datasetin për të mbajtur vetëm vitet 2012-2015, duke hequr 2011 dhe 2016 sepse ato nuk kanë të dhëna CWUR.

### Kolona e Modifikuar
- `year` - Filtruar për të përmbajtur vetëm [2012, 2013, 2014, 2015]


## Hapi 4: Pastrimi dhe Imputimi (`4th_step-data_cleaning`)

### Përshkrim
Ky hap kryen pastrim të avancuar të të dhënave, imputim të vlerave munguese dhe përmirësim të konsistencës.

### Proces
1. Normalizohen emrat e kolonave (lowercase, underscore)
2. Hiqen kolonat me mungesa të larta (>45-70%): `total_score`, `female_male_percent`, `income`
3. Plotësohen vlerat munguese në kolonat e renditjes (world_rank ↔ cwur_world_rank)
4. Imputimi me medianë për çdo universitet (bazuar në të dhënat historike)
5. Imputimi global me medianë për vlerat e mbetura
6. Konvertohen kolonat CWUR në integer
7. Hiqen rreshtat pa të dhëna renditjeje

### Formulat e Imputimit

**Imputimi për nivel universiteti:**
```
për çdo kolonë numerike:
  median_university = median(e të gjitha vlerat për këtë universitet nëpër vite)
  zëvendëso NaN me median_university
```

**Imputimi global:**
```
për çdo kolonë që ka ende NaN:
  median_global = median(e gjithë kolona)
  zëvendëso NaN me median_global
```

**Plotësimi i kolonave të renditjes:**
```
world_rank = fillna(cwur_world_rank)
cwur_world_rank = fillna(world_rank)
```

**Rezultati:** Dataset i pastër me mungesa minimale

---

## Hapi 5: Mostrimi

### Përshkrim
Ky hap krijon një kampion të stratifikuar (20% për vit) dhe krijon karakteristika të reja për analizë.

### Proces

#### A. Mostrimi (`sampling.py`)
1. Krijon kampion 20% të stratifikuar për vit (random_state=42)
2. Ruan `sampled_dataset.csv`

**Formula e kampionimit:**
```
për çdo vit:
  sample = df[df['year'] == year].sample(frac=0.2, random_state=42)
```

#### B. Inxhinieria e Karakteristikave (`feature_engineering.py`)

**Kolonat e Krijuara:**

1. **`rank_consistency_std`** - Devijimi standard i renditjes botërore për universitet
   - **Formula:** `std(world_rank për çdo universitet nëpër vite)`

2. **`consistency_score`** - Rezultati i konsistencës (invers i rank_consistency_std)
   - **Formula:** `1 / (1 + rank_consistency_std)`

3. **`research_index`** - Indeksi i kërkimeve
   - **Formula:** `mean(research, citations)`

4. **`teaching_index`** - Indeksi i mësimdhënies
   - **Formula:** `mean(teaching, international)`

5. **`global_index`** - Indeksi global
   - **Formula:** `mean(research_index, teaching_index)`

6. **`rank_change`** - Ndryshimi i renditjes vit pas viti
   - **Formula:** `world_rank[year] - world_rank[year-1]` (për çdo universitet)

7. **`trajectory`** - Kategoria e trajektores
   - **Formula:** 
     - Nëse `rank_change <= -10`: "rising"
     - Nëse `rank_change >= 10`: "declining"
     - Përndryshe: "stable"

8. **`region`** - Rajoni (bazuar në shtet)
   - **Formula:** Hartim nga shteti në rajon (USA/Canada → "North America", etj.)

9. **`diversity_index`** - Indeksi i diversitetit
   - **Formula:** `mean(international_students_normalized, inverted_student_staff_ratio)`
   - Ku `inverted_ratio = 1 - ((student_staff_ratio - min) / (max - min))`

10. **`research_index_z`** - Z-score i research_index
    - **Formula:** `(research_index - mean(research_index)) / std(research_index)`

11. **`teaching_index_z`** - Z-score i teaching_index
    - **Formula:** `(teaching_index - mean(teaching_index)) / std(teaching_index)`

12. **`rank_tier`** - Nivel i renditjes
    - **Formula:** Kategorizim në: "Top 100", "101–200", "201–500", "501+"

13. **`performance_category`** - Kategoria e performancës
    - **Formula:** Kategorizim i `teaching_index`: "Low" (<40), "Medium" (40-60), "High" (>60)

14. **`size_category`** - Kategoria e madhësisë
    - **Formula:** Kategorizim i `num_students` bazuar në quantiles: "Small", "Medium", "Large"

15. **`is_top_100`** - Flag për top 100
    - **Formula:** `world_rank <= 100` (boolean)

16. **`is_research_intensive`** - Flag për kërkim-intensiv
    - **Formula:** `research_index >= 70` (boolean)

17. **`is_rising`** - Flag për universitet në rritje
    - **Formula:** `trajectory == "rising"` (boolean)

**Rezultati:** Dataset me karakteristika të reja për analizë dhe një kampion prej 20%

---

## Hapi 6: Agregimi (`6th_step-aggregation`)

### Përshkrim
Ky hap agregon të dhënat sipas shtetit dhe vitit, duke llogaritur statistika për çdo kombinim shtet-vit.

### Proces
1. Normalizohen emrat e shteteve
2. Krijohen kolona të derizuara
3. Agregohen të dhënat me groupby(country, year)
4. Llogariten statistika (mesatare, medianë, minimum)

### Kolona të Krijuara

1. **`rank_gap`** - Diferenca midis renditjeve THE dhe CWUR
   - **Formula:** `world_rank - cwur_world_rank`
   - **Interpretim:** Negativ = THE rendit më mirë; Pozitiv = CWUR rendit më mirë

2. **`faculty_efficiency`** - Efikasiteti i fakultetit
   - **Formula:** `cwur_quality_of_faculty / student_staff_ratio`

3. **`global_influence_index`** - Indeksi i ndikimit global
   - **Formula:** `mean(citations_z, cwur_influence_z, cwur_citations_z)`
   - Ku z-scores llogariten për çdo vit: `z = (x - mean(x)) / std(x)`

### Statistikat e Agreguara

Për çdo kombinim (shtet, vit), llogariten:
- `world_rank_mean`, `world_rank_median`, `world_rank_min` (best_the_world_rank)
- `cwur_world_rank_mean`, `cwur_world_rank_median`, `cwur_world_rank_min` (best_cwur_world_rank)
- Mesataret për: `teaching`, `international`, `citations`, `cwur_score`
- Mesataret për të gjitha kolonat CWUR
- `rank_gap_mean`, `faculty_efficiency_mean`, `global_influence_index_mean`
- `total_students_covered` (sum i num_students)
- `avg_students_per_university` (mean i num_students)
- `avg_international_student_share` (mean i international_students)
- `student_staff_ratio_mean`

**Rezultati:** Dataset agreguar me statistika për çdo shtet dhe vit

---

## Hapi 7: Përzgjedhja dhe Krijimi i Karakteristikave (`7th_step-feature_selection_creation`)

### Përshkrim
Ky hap heq kolonat redundante dhe krijon karakteristika të reja më informative.

### Proces
1. Hiqen kolonat redundante: `cwur_national_rank`, `cwur_broad_impact`, `cwur_patents`
2. Krijohen karakteristika të reja të derizuara

### Kolona të Krijuara

1. **`rank_gap`** - Diferenca midis renditjeve
   - **Formula:** `world_rank - cwur_world_rank`

2. **`research_efficiency_per_1k`** - Efikasiteti i kërkimave për 1000 studentë
   - **Formula:** `(research / num_students) * 1000`
   - **Rrumbullakimi:** 3 shifra pas presjes

3. **`faculty_efficiency`** - Efikasiteti i fakultetit
   - **Formula:** `cwur_quality_of_faculty / student_staff_ratio`

4. **`global_influence_index`** - Indeksi i ndikimit global
   - **Formula:** `mean(citations, cwur_influence, cwur_citations)`

5. **`high_international_ratio`** - Flag për raport të lartë ndërkombëtar
   - **Formula:** `1 nëse international_students > 0.30, përndryshe 0`

**Rezultati:** Dataset me karakteristika optimizuar dhe të derizuara

---

## Hapi 8: Diskretizimi, Binarizimi dhe Transformimi (`8th-step-discret_binar_transform`)

### Përshkrim
Ky hap konverton vlerat e vazhdueshme në kategorike, krijon flage binare dhe transformon të dhënat për krahasim kontekstual.

### Proces

#### A. Diskretizimi

1. **`teaching_level`** - Niveli i mësimdhënies
   - **Formula:** Kategorizim në 3 grupe (quantile): "Low", "Medium", "High"

2. **`citations_level`** - Niveli i citimeve
   - **Formula:** Kategorizim në 3 grupe (quantile): "Low", "Medium", "High"

#### B. Binarizimi

1. **`top100_times`** - Flag për top 100 në THE
   - **Formula:** `1 nëse world_rank <= 100, përndryshe 0`

2. **`top100_cwur`** - Flag për top 100 në CWUR
   - **Formula:** `1 nëse cwur_world_rank <= 100, përndryshe 0`

3. **`high_international_ratio`** - (Ruhet nga hapi i mëparshëm)

#### C. Transformime Kontekstuale

1. **`country_year_teaching_mean`** - Mesatarja e mësimdhënies për shtet-vit
   - **Formula:** `mean(teaching) për çdo kombinim (country, year)`

2. **`country_year_citations_mean`** - Mesatarja e citimeve për shtet-vit
   - **Formula:** `mean(citations) për çdo kombinim (country, year)`

3. **`country_year_cwur_score_mean`** - Mesatarja e rezultatit CWUR për shtet-vit
   - **Formula:** `mean(cwur_score) për çdo kombinim (country, year)`

4. **`relative_teaching`** - Mësimdhënia relative ndaj mesatares kombëtare
   - **Formula:** `teaching / country_year_teaching_mean`

5. **`relative_citations`** - Citimet relative ndaj mesatares kombëtare
   - **Formula:** `citations / country_year_citations_mean`

6. **`relative_cwur_score`** - Rezultati CWUR relative
   - **Formula:** `cwur_score / country_year_cwur_score_mean`

#### D. Standardizimi (Z-score)

1. **`teaching_z`** - Z-score i mësimdhënies
   - **Formula:** `(teaching - mean(teaching)) / std(teaching)`

2. **`citations_z`** - Z-score i citimeve
   - **Formula:** `(citations - mean(citations)) / std(citations)`

3. **`num_students_z`** - Z-score i numrit të studentëve
   - **Formula:** `(num_students - mean(num_students)) / std(num_students)`

4. **`relative_teaching_z`** - Z-score i mësimdhënies relative
   - **Formula:** `(relative_teaching - mean(relative_teaching)) / std(relative_teaching)`

5. **`relative_citations_z`** - Z-score i citimeve relative
   - **Formula:** `(relative_citations - mean(relative_citations)) / std(relative_citations)`

**Rezultati:** Dataset final me karakteristika diskretizuara, binare dhe të standardizuara për analizë dhe vizualizim


---

## Faza 2

---

## Hapi 9: Detektimi i Përjashtuesve (`9th_step-outlier_detection`)

### Përshkrim

Ky hap implementon tre metoda të ndryshme për detektimin e përjashtuesve (outliers) në datasetin e universiteteve. Përjashtuesit janë pikë të dhënash që devijojnë në mënyrë të konsiderueshme nga të dhënat e tjera dhe mund të tregojnë anomali, gabime, ose karakteristika unike të vërteta.

### Input

- **Skedar:** `../final_dataset.csv`
- **Rreshta:** 2,895
- **Kolona:** 39 karakteristika (numerike dhe kategorike)
- **Vite:** 2012-2015

### Logjika e Implementimit

**Metoda 1: IQR (Interquartile Range)**
- Llogarit kuartilet Q1 dhe Q3 për çdo kolonë numerike
- Identifikon outliers si vlera jashtë intervalit [Q1 - 1.5×IQR, Q3 + 1.5×IQR]
- Analizon 18 kolona numerike kryesore: teaching, research, citations, num_students, student_staff_ratio, international_students, cwur_score, rank_gap, research_efficiency_per_1k, faculty_efficiency, global_influence_index, relative_teaching, relative_citations, relative_cwur_score, teaching_z, citations_z, num_students_z, relative_teaching_z, relative_citations_z

**Metoda 2: Z-Score**
- Llogarit z-score për çdo vlerë: z = (x - μ) / σ
- Identifikon outliers si vlera me |z-score| > 3 (99.7% confidence level)
- Supozon distribucion normal dhe analizon të njëjtat 18 kolona

**Metoda 3: Isolation Forest**
- Algoritëm machine learning multivariate që analizon shumë karakteristika së bashku
- Analizon 15 karakteristika së bashku për të identifikuar kombinime të pazakonta
- Përdor contamination=0.1 (pret 10% outliers), n_estimators=100, random_state=42
- Standardizim me StandardScaler para analizës

### Output

**Skedarë CSV:**
- `iqr/outliers_iqr.csv` - Detaje të plota për çdo outlier IQR (row_index, university_name, country, year, feature, value, lower_bound, upper_bound, Q1, Q3, IQR)
- `zscore/outliers_zscore.csv` - Detaje për çdo outlier Z-Score (row_index, university_name, country, year, feature, value, z_score, mean, std)
- `isolation_forest/outliers_isolation_forest.csv` - Universitete outliers me anomaly scores dhe të gjitha 15 features

**Vizualizime PNG:**
- Boxplots, histogramë, scatter plots, heatmaps për secilën metodë
- Krahasime midis metodave dhe top universiteteve me outliers

### Shembull Rreshtash

**outliers_zscore.csv:**
```
row_index,university_name,country,year,feature,value,z_score,mean,std
20,University of Chicago,United States of America,2012,teaching,89.4,3.90,36.15,13.64
24,University of Cambridge,United Kingdom,2012,teaching,90.5,3.98,36.15,13.64
```

**outliers_isolation_forest.csv:**
```
university_name,country,year,anomaly_score,teaching,research,citations,num_students,...
Alexandria University,Egypt,2012,0.65,15.2,12.1,28.5,45231,...
Australian National University,Australia,2013,0.58,42.3,38.7,65.2,18542,...
```

### Rezultati

Tre metoda identifikojnë outliers të ndryshëm:
- IQR: ~800-1000 raste unike (shumë detektues, por me false positives të mundshme)
- Z-Score: ~600-800 raste unike (më konservativ, por supozon normalitet)
- Isolation Forest: ~290 raste unike (10% e datasetit, multivariate approach)

Krahasimi i tre metodave tregon se disa outliers shfaqen në më shumë se një metodë, që tregon konsensus për outliers të vërtetë. Kjo logjikë përdoret në Hapin 10 për të identifikuar outliers të vërtetë që duhen hequr.

---

## Hapi 10: Mënjanimi i Zbulimeve Jo të Sakta (`10th_step-removal-incorr-findings`)

### Përshkrim

Ky hap përfaqëson fazën "Mënjanimi i zbulimeve jo të sakta", ku kombinohen rezultatet e tre metodave të detektimit të përjashtuesve (Z-Score, IQR, Isolation Forest) për të identifikuar vetëm outliers të vërtetë.

Qëllimi është të hiqen rreshtat që kanë devijime të forta dhe shfaqen si outliers në më shumë se një metodë, duke siguruar një dataset më të qëndrueshëm për analizat e mëtejshme. Kjo metodë garanton stabilitet statistikor duke shmangur heqjen e rasteve që janë devijime të vogla ose false positives.

### Input

- `9th_step-outlier_detection/zscore/outliers_zscore.csv` (nga Hapi 9)
- `9th_step-outlier_detection/iqr/outliers_iqr.csv` (nga Hapi 9)
- `9th_step-outlier_detection/isolation_forest/outliers_isolation_forest.csv` (nga Hapi 9)
- `final_dataset.csv` (dataset origjinal me 2,895 rreshta)

### Logjika e Heqjes

1. **Krijimi i ID unik:** Për çdo rresht krijohet një identifikues unik: `university_name | country | year`. Kjo lejon kombinimin e rezultateve nga tre metodat e ndryshme.

2. **Kombinimi i metodave:** Për çdo entitet (universitet+vend+vit) numërohet në sa metoda shfaqet si outlier. Krijon kolona flag: `in_zscore`, `in_iqr`, `in_isolation_forest`.

3. **Klasifikimi:**
   - **Outliers të vërtetë (konsensus):** Shfaqen në ≥ 2 metoda (`methods_flagged >= 2`)
   - **Outliers të pasaktë (false positives):** Shfaqen vetëm në 1 metodë (`methods_flagged == 1`)

4. **Heqja:** Vetëm outliers të vërtetë (konsensus) hiqen nga dataseti origjinal. Outliers të pasaktë ruhen për referencë por nuk hiqen.

### Output

**Skedarë CSV:**
- `outliers_all_methods_comparison.csv` - Kombinimi i të gjitha metodave me kolona flag për secilën metodë dhe `methods_flagged` (0-3)
- `outliers_consensus.csv` - Outliers të vërtetë (≥2 metoda) - për t'u hequr nga dataseti
- `outliers_false_detected.csv` - Outliers të pasaktë (1 metodë) - për referencë dhe auditim
- `final_dataset_with_outlier_flags.csv` - Dataset origjinal me kolonë shtesë `is_outlier_consensus` (0/1)
- `final_dataset_no_outliers.csv` - Dataset final pa outliers konsensus (2,358 rreshta)

### Shembull Rreshtash

**outliers_consensus.csv:**
```
entity_id,in_zscore,in_iqr,in_isolation_forest,methods_flagged,university_name,country,year
Alexandria University | Egypt | 2012,1,1,1,3,Alexandria University,Egypt,2012
Aberystwyth University | United Kingdom | 2014,1,1,0,2,Aberystwyth University,United Kingdom,2014
Arizona State University | United States of America | 2013,1,0,1,2,Arizona State University,United States of America,2013
```

**final_dataset_no_outliers.csv:**
```
world_rank,university_name,country,teaching,international,research,citations,num_students,student_staff_ratio,international_students,year,cwur_world_rank,...
201,University of Gothenburg,Sweden,25.8,48.4,37.7,55.7,26420,16.4,0.12,2012,201,...
156,University of Exeter,United Kingdom,31.3,73.4,33.3,67.8,17755,18.8,0.28,2012,156,...
251,University of Graz,Austria,24.9,63.8,14.0,55.1,20584,26.8,0.12,2012,251,...
```

### Rezultati

- **Rreshta origjinalë:** 2,895
- **Outliers konsensus (≥2 metoda):** 537 raste unike (18.5% e datasetit)
- **Outliers false positives (1 metodë):** ~400-500 raste (nuk hiqen)
- **Rreshta të mbetur:** 2,358 (81.5% e datasetit origjinal)
- **Dataset i pastruar:** Pa outliers të vërtetë, i balancuar dhe gati për analizë statistikore dhe eksploruese

---

## Hapi 11: Eksplorimi i të Dhënave (`11th_step-exploratory_analysis`)

### Përshkrim

Ky hap realizon eksplorimin eksplorues të të dhënave (EDA) mbështetur në datasetin final pa përjashtues (outliers). Qëllimi është të shikohen statistikat përmbledhëse për të gjitha kolonat numerike dhe të analizohen marrëdhëniet multivariante midis metrikeve kryesore.

Pas detektimit të përjashtuesve (Hapi 9) dhe mënjanimit të zbulimeve jo të sakta (Hapi 10), këtu bëhet analiza e thelluar e të dhënave të pastruara për të kuptuar shpërndarjet, korrelacionet dhe strukturat e datasetit final.

### Input

- **Skedar:** `../10th_step-removal-incorr-findings/final_dataset_no_outliers.csv`
- **Rreshta:** 2,358
- **Kolona:** 39 (përfshin metrikat bazë + metrika të derizuara/relative/z-scores)
- **Vite:** 2012-2015

### Logjika e Analizës

**1. Statistika Përmbledhëse (Univariate)**
- Për çdo kolonë numerike: count, mean, std, min, 25%, 50% (median), 75%, max
- Identifikon shpërndarjen, tendencën qendrore dhe shpërndarjen e të dhënave
- Ruhet në: `summary_statistics_numeric.csv`

**2. Statistika Sipas Shtetit**
- Grupim: `groupby("country")`
- Për metrikat kryesore (nëse ekzistojnë): teaching, research, citations, cwur_score, num_students, international_students
- Llogarit: mean, median, min, max, count për çdo shtet
- Ruhet në: `country_summary_after_outlier_removal.csv`

**3. Vizualizime Univariate**
- Histogramë + KDE (Kernel Density Estimation) për metrikat kryesore: teaching, research, citations, cwur_score, num_students, student_staff_ratio
- Boxplot-e për identifikim vizual të vlerave ekstreme edhe pas filtrimit të outliers

**4. Analizë Multivariante - Korrelacione**
- Matrica e korrelacioneve Pearson për 13 metrika kryesore:
  - Nota të performancës: teaching, research, citations, cwur_score
  - Metrika të efikasitetit: rank_gap, research_efficiency_per_1k, faculty_efficiency, global_influence_index
  - Metrika relative: relative_teaching, relative_citations, relative_cwur_score
  - Variabla strukturore: num_students, student_staff_ratio
- Heatmap me annotime për vlera numerike të korrelacionit (-1 deri +1)
- Identifikon marrëdhënie lineare të forta midis variablave

**5. Analizë Multivariante - Pairplot**
- Scatter plots dhe distribucione për kombinime metrikash: teaching, research, citations, cwur_score, relative_teaching, relative_citations
- Identifikon marrëdhënie jo-lineare, shpërndarje dhe struktura të mundshme grupesh

### Output

**Skedarë CSV:**
- `summary_statistics_numeric.csv` - Statistika përmbledhëse për të gjitha kolonat numerike (39 kolona)
- `country_summary_after_outlier_removal.csv` - Statistika sipas shtetit për metrikat kryesore

**Vizualizime PNG (300 DPI):**
- `hist_teaching.png`, `hist_research.png`, `hist_citations.png`, `hist_cwur_score.png`, `hist_num_students.png`, `hist_student_staff_ratio.png` - Histogramë + KDE
- `boxplot_teaching.png`, `boxplot_research.png`, etj. - Boxplot-e
- `correlation_heatmap_core_features.png` - Heatmap i korrelacioneve (13x13 matrica)
- `pairplot_core_metrics.png` - Pairplot për 6 metrika kryesore

### Shembull Rreshtash

**summary_statistics_numeric.csv:**
```
,count,mean,std,min,25%,50%,75%,max
teaching,2358,36.15,13.64,5.2,26.8,34.5,44.2,99.7
research,2358,38.42,15.23,8.1,27.3,36.8,48.1,99.5
citations,2358,52.18,18.92,12.4,38.5,50.2,65.8,99.9
cwur_score,2358,46.85,2.34,42.1,45.2,46.8,48.1,51.2
num_students,2358,21543.5,12456.8,5234,12345,19876,28765,45231
```

**country_summary_after_outlier_removal.csv:**
```
country,teaching_mean,teaching_median,research_mean,research_median,citations_mean,...
United States of America,47.35,46.8,52.18,51.2,71.32,...
United Kingdom,35.15,34.2,42.67,41.8,60.59,...
Germany,37.07,36.5,38.24,37.9,59.34,...
```

### Rezultati

- **Statistika të plota** për të gjitha 39 kolonat numerike, duke treguar shpërndarjen dhe karakteristikat e secilës metrikë
- **Korrelacione të identifikuara** midis metrikave (p.sh. research dhe citations kanë korrelacion të lartë r>0.7, teaching dhe research kanë korrelacion mesatar r>0.5)
- **Vizualizime komplekse** për shpërndarje dhe marrëdhënie që ndihmojnë në interpretim
- **Dataset i analizuar** dhe i gatshëm për interpretim dhe raportim

Dataseti final me 2,358 rreshta dhe 39 kolona është i pastruar, i analizuar dhe i gatshëm për vizualizim në Power BI ose mjete të tjera. Struktura e të dhënave është e përshtatshme për dashboard interaktivë, raporte dhe analiza të mëtejshme.

---

## Përmbjedhje e Pipeline-it të Përgatitjes së Të Dhënave

### Transformimi i Të Dhënave Nëpër Hapa

| Hapi | Input | Output | Rreshta | Kolona | Transformimi Kryesor |
|------|-------|--------|---------|--------|----------------------|
| **0. Burimet** | timesData.csv + cwurData.csv | - | 2,603 + 2,200 | 14 + 13 | Të dhëna të papastërta |
| **1. Bashkimi** | 2 dataset | merged_university_data.csv | 3,895 | 25 | Outer join në (year, name) |
| **2. Konvertimi** | merged | output i përkoh shëm | 3,895 | 25 | String → numeric, female_male_ratio → percent |
| **3. Filtrimi** | converted | output i përkohshëm | 2,595 | 25 | Mbajtur vetëm 2012-2015 |
| **4. Pastrimi** | filtered | cleaned_university_data.csv | 2,895 | 22 | Imputim hierarkik, -3 kolona |
| **5A. Mostrimi** | cleaned | sampled_dataset.csv | 579 | 22 | 20% stratified sample |
| **5B. Engineering** | cleaned | university_data_engineered.csv | 2,895 | 39 | +17 karakteristika analitike |
| **6. Agregimi** | cleaned | country_year_summary.csv | ~280 | ~28 | Universitet → Shtet-Vit |
| **7. Seleksionimi** | cleaned | feature_selected_created.csv | 2,895 | 24 | -3 redundante, +5 të reja |
| **8. Transformimi** | selected | university_data_discretized.csv | 2,895 | 39 | +15 (diskrete/binare/relative/z-scores) |
| **9. Detektimi Outliers** | final_dataset | outliers_*.csv | - | - | 3 metoda: IQR, Z-Score, Isolation Forest |
| **10. Heqja Outliers** | final_dataset | final_dataset_no_outliers.csv | 2,358 | 39 | Konsensus >=2 metoda |
| **11. Eksplorimi** | no_outliers | summary_*.csv, vizualizime | 2,358 | 39 | Statistika + multivariante |

### Karakteristikat e Datasetit Final

**Skedari Kryesor:** `10th_step-removal-incorr-findings/final_dataset_no_outliers.csv`

**Karakteristikat:**
- **2,358 rreshta** - Universitete nga e gjithë bota (2012-2015), pa outliers konsensus (81.5% e datasetit origjinal)
- **39 kolona** - Karakteristika të ndryshme për analizë të thellë
- **Të dhëna të pastruara** - Mungesa <1%, pa duplikate, pa outliers të vërtetë
- **2 burime** - THE dhe CWUR të integruara
- **4 vite** - Timeline 2012-2015
- **Forma të shumta** - Numerike, kategorike, binare, relative, standardizuara

**Përshtatja për Power BI:**
Dataseti final me 2,358 rreshta dhe 39 kolona është optimal për Power BI:
- Madhësia e datasetit (2,358 rreshta) është e përshtatshme për performancë të shpejtë në Power BI
- 39 kolona ofrojnë fleksibilitet për krijimin e dashboard-eve komplekse me metrika të shumta
- Struktura e të dhënave (identifikues, metrika numerike, kategorike, binare) lejon filtrim, grupim dhe agregim të lehtë
- Të dhënat janë të pastruara dhe të konsistuara, pa nevojë për pastrim shtesë në Power BI
- Metrikat relative dhe z-scores lejojnë krahasime dhe analiza të avancuara
- Kolonat kategorike (teaching_level, citations_level) dhe binare (top100_times, top100_cwur) lejojnë filtrim dhe grupim të shpejtë

### Tipet e Karakteristikave

**1. Identifikues (3):**
- university_name, country, year

**2. Renditje & Rezultate (9):**
- world_rank, cwur_world_rank
- teaching, international, research, citations
- cwur_quality_of_education, cwur_alumni_employment, cwur_quality_of_faculty, etj.

**3. Statistika Institucionale (3):**
- num_students, student_staff_ratio, international_students

**4. Metrika të Derizuara (10):**
- rank_gap, research_efficiency_per_1k, faculty_efficiency
- global_influence_index, relative_teaching, relative_citations, etj.

**5. Indekse Kompozite (3):**
- research_index, teaching_index, global_index

**6. Kategorizime (2):**
- teaching_level, citations_level (Low/Medium/High)

**7. Flamurë Binarë (3):**
- top100_times, top100_cwur, high_international_ratio (0/1)

**8. Z-Scores (5):**
- teaching_z, citations_z, num_students_z, relative_teaching_z, relative_citations_z

### Përdorimet e Datasetit

**Analiza Eksploruese**
- Shpërndarja e renditjeve sipas shteteve/rajoneve
- Trendet kohore (2012-2015)
- Krahasimet midis THE dhe CWUR

**Analiza Statistikore**
- Korrelacione midis metrikave
- Regression për parashikim
- Clustering i universiteteve

**Vizualizime**
- Scatter plots, heatmaps, bar charts
- Time series analysis
- Geographic distributions

**Machine Learning**
- Classification (p.sh., top100 prediction)
- Ranking prediction
- Feature importance analysis

**Krahasime Kontekstuale**
- Performanca relative brenda shteteve
- Identifikimi i outlierëve
- Benchmark analysis

---

---

## Përmbledhje e Datasetit Final

### Statistikat e Datasetit Final

**Skedari:** `10th_step-removal-incorr-findings/final_dataset_no_outliers.csv`

- **Rreshta:** 2,358 (81.5% e datasetit origjinal pas heqjes së outliers konsensus)
- **Kolona:** 39 (identifikues, metrika numerike, kategorike, binare, relative, z-scores)
- **Vite:** 2012-2015 (4 vite)
- **Shtete:** ~70-80 shtete të ndryshme
- **Universitete unike:** ~600-700 universitete

### Si Duken Të Dhënat

**Shembull rreshtash nga dataseti final:**

```
world_rank,university_name,country,teaching,international,research,citations,num_students,student_staff_ratio,international_students,year,cwur_world_rank,...
201,University of Gothenburg,Sweden,25.8,48.4,37.7,55.7,26420,16.4,0.12,2012,201,...
156,University of Exeter,United Kingdom,31.3,73.4,33.3,67.8,17755,18.8,0.28,2012,156,...
251,University of Graz,Austria,24.9,63.8,14.0,55.1,20584,26.8,0.12,2012,251,...
```

**Karakteristikat kryesore:**
- Të gjitha vlerat numerike janë të pastruara dhe të konsistuara
- Kolonat kategorike (teaching_level, citations_level) ofrojnë grupim të lehtë
- Kolonat binare (top100_times, top100_cwur) lejojnë filtrim të shpejtë
- Metrikat relative lejojnë krahasime kontekstuale brenda shteteve
- Z-scores lejojnë standardizim dhe krahasime midis metrikave të ndryshme

---

**Grupi:**  7  
**Lënda:** Përgatitja dhe vizualizimi i të dhënave



