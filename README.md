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




**Grupi:**  7  
**Data:** 02.11.2025  
**Lënda:** Përgatitja dhe vizualizimi i të dhënave



