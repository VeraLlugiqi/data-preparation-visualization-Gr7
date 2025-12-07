# Përgatitja dhe Vizualizimi i të Dhënave - Projekt Gr7

Ky projekt përmban përgatitjen, pastrimin dhe analizën eksploruese të të dhënave të renditjes së universiteteve nga dy burime: Times Higher Education (THE) dhe Center for World University Rankings (CWUR). Projekti është organizuar në 11 hapa kryesorë, secili me procesin e vet të transformimit dhe analizës së të dhënave.

---

## Përmbledhje e Procesit

Procesi fillon me bashkimin e dy datasetave (THE dhe CWUR), pastaj bëhet pastrimi i të dhënave, konvertimi i tipave, filtrimi i viteve, imputimi i vlerave munguese, kampionimi, agregimi dhe krijimi i karakteristikave të reja deri te transformimi, diskretizimi, detektimi dhe filtrimi i përjashtuesve, dhe në fund analiza eksploruese statistikore e datasetit final.

---

## Hapi 1: Bashkimi i të Dhënave (`1st_step-merging`)

### Përshkrim
Ky hap bashkon dy datasetat e renditjes së universiteteve: `timesData.csv` (Times Higher Education) dhe `cwurData.csv` (Center for World University Rankings) në një dataset të vetëm, duke përdorur outer join për të mbajtur të gjitha universitetet nga të dy burimet.

### Input
- **timesData.csv**: 2,603 rreshta (2011-2016), 14 kolona
- **cwurData.csv**: 2,200 rreshta (2012-2015), 13 kolona

### Procesi i Detajuar

#### 1. Normalizimi i Emrave
Për të përmirësuar përputhjen midis dy datasetave:
- **Heqja e karaktereve të padukshme**: Zero-width spaces, unicode dashes speciale
- **Fshirja e pjesëve në kllapa**: "University of Cambridge (UK)" → "university of cambridge"
- **Heqja e ndarjeve rajonale**: "University, California" → "university"
- **Unifikom variante**: 
  - "Pierre and Marie Curie University" ≈ "Pierre Marie Curie"
  - "Technion - Israel Institute of Technology" ≈ "Technion"
  - "Wageningen University and Research Center" ≈ "Wageningen University"
- **Lowercase dhe trim**: Të gjitha karakteret bëhen të vogla dhe hiqen hapësirat

#### 2. Bashkimi (Outer Join)
- **Kyçe bashkimi**: (`year`, `normalized_name`)
- **Tipi**: Outer join - mban të gjitha rreshtat nga të dyja datasetat
- **Plotësimi**: Nëse `university_name` ose `country` mungon nga THE, plotësohet nga CWUR

#### 3. Riemërtimi i Kolonave CWUR
Të gjitha kolonat nga CWUR marrin prefiksin `cwur_` për të shmangur konfliktet:
- `world_rank` → `cwur_world_rank`
- `citations` → `cwur_citations`
- etj.

#### 4. Pastrimi Final
- Heqja e duplikateve bazuar në (`year`, `university_name`)
- Vlerat munguese shënohen me "-"

### Kolona të Krijuara (Total: 25 kolona)

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

### Output

**Skedar:** `merged_university_data.csv`

**Dimensionet:**
- **Rreshta:** 3,895 (1 header + 3,894 rreshta të dhënash)
- **Kolona:** 25
- **Vite:** 2012-2015 (4 vite)
- **Universitete unike:** ~900-1000 universitete

**Struktura e Kolonave (25 total):**
```
1.  world_rank                    [THE - Pozicioni global]
2.  university_name                [Emri i universitetit]
3.  country                        [Shteti]
4.  teaching                       [THE - Rezultati mësimdhënie 0-100]
5.  international                  [THE - Perspektiva ndërkombëtare 0-100]
6.  research                       [THE - Rezultati kërkime 0-100]
7.  citations                      [THE - Rezultati citime 0-100]
8.  income                         [THE - Të ardhura industriale 0-100]
9.  total_score                    [THE - Rezultati total 0-100]
10. num_students                   [Numri i studentëve]
11. student_staff_ratio            [Raporti student-staf]
12. international_students         [% studentë ndërkombëtarë]
13. female_male_ratio              [Raporti femra:meshkuj]
14. year                           [Viti i renditjes]
15. cwur_world_rank                [CWUR - Pozicioni global]
16. cwur_national_rank             [CWUR - Pozicioni kombëtar]
17. cwur_quality_of_education      [CWUR - Renditja cilësia arsimit]
18. cwur_alumni_employment         [CWUR - Renditja punësimi alumni]
19. cwur_quality_of_faculty        [CWUR - Renditja cilësia fakulteti]
20. cwur_publications              [CWUR - Renditja publikime]
21. cwur_influence                 [CWUR - Renditja influenca]
22. cwur_citations                 [CWUR - Renditja citime]
23. cwur_broad_impact              [CWUR - Renditja ndikimi i gjerë]
24. cwur_patents                   [CWUR - Renditja patenta]
25. cwur_score                     [CWUR - Rezultati total]
```

**Karakteristikat:**
- Përfshin universitete që janë **vetëm në THE**, **vetëm në CWUR**, ose në **të dyja**
- Vlerat munguese (kur një universitet s'ekziston në njërën prej burimeve) shënohen me "-"
- Dataset i plotë i pakonsoliduar, me të gjitha kolonat origjinale

**Shembull Rreshti:**
```
world_rank: 1
university_name: Harvard University  
country: USA
teaching: 99.7 | research: 99.5 | citations: 99.9
cwur_world_rank: 1 | cwur_score: 100.00
```

---

## Hapi 2: Konvertimi i Tipave (`2nd_step-changing_types`)

### Përshkrim
Ky hap transformon të dhënat e papastërt nga formati string në formate numerike të përshtatshme për analizë. Shumë kolona në datasetat origjinale janë string (p.sh. "1,234", "100-200", "14%") dhe duhet të konvertohen.

### Input
- **Skedar:** `merged_university_data.csv` (3,895 rreshta)
- **Problem:** Vlera të tilla si "401-500", "5,000", "23%", "42:58" nuk janë numerike

### Procesi i Detajuar

#### 1. Heqja e Formatimeve
- **Presjet**: "1,234" → 1234
- **Diapazonet**: "100-200" → 100 (merret vlera e parë)
- **Simbolet**: "23%" → 23 ose 0.23 (sipas kontekstit)

#### 2. Transformimi i `female_male_ratio`
Kjo kolonë ka formate të ndryshme dhe transformohet në `female_male_percent`:
- **Format "X:Y"**: "42:58" → 42/(42+58) * 100 = 42%
- **Format "X%"**: "45%" → 45
- **Format "X:Y:Z"**: "42:58:00" → 42/(42+58) * 100 = 42%

#### 3. Konvertimi në Tipe Numerike
- **Integer**: Kolonat e renditjes (world_rank, cwur_world_rank, etj.)
- **Float**: Rezultatet (teaching, research, citations), raportet, përqindjet

#### 4. Menaxhimi i Vlerave të Pavlefshme
- Vlerat që s'mund të konvertohen vendosen si `NaN`
- Ruhen për trajtim në hapin e pastrimit (Hapi 4)

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

### Output

**Skedar:** Output i përkohshëm (përdoret si input për Hapin 3)

**Ndryshimet:**
- **Kolona të hequra:** `female_male_ratio` 
- **Kolona të krijuara:** `female_male_percent` (përqindja e studentëve femra)
- **Kolona totale:** 25 (e njëjta, por `female_male_ratio` zëvendësohet)
- **Rreshta:** 3,895 (të pandryshuara)

**Tipet e Konvertuara:**
```
INTEGER kolonat:
- world_rank, cwur_world_rank, cwur_national_rank
- Të gjitha kolonat CWUR ranking (quality_of_education, alumni_employment, etj.)

FLOAT kolonat:  
- teaching, international, research, citations, income, total_score
- num_students, student_staff_ratio
- international_students (nga "23%" → 0.23)
- female_male_percent (e re)
- cwur_score
```

**Shembuj Transformimesh:**
```
Parë:    "1,234"       → Pas: 1234.0
Parë:    "100-200"     → Pas: 100
Parë:    "14%"         → Pas: 0.14
Parë:    "42:58"       → Pas: 42.0 (female_male_percent)
Parë:    "-"           → Pas: NaN
```

**Rezultati:** Dataset me tipe numerike të sakta, gati për filtrimin dhe pastrimin

---

## Hapi 3: Filtrimi i Viteve (`3rd_step-filtering_years`)

### Përshkrim
Ky hap filtron datasetin për të mbajtur vetëm vitet që kanë të dhëna nga të dy burimet (THE dhe CWUR), duke siguruar një dataset të balancuar për krahasim.

### Arsyeja e Filtrimit

**Disponueshmëria e të Dhënave:**
- **Times Higher Education (THE)**: 2011, 2012, 2013, 2014, 2015, 2016
- **Center for World University Rankings (CWUR)**: 2012, 2013, 2014, 2015

**Problemi:** 
- Viti 2011: Ka vetëm të dhëna THE (kolonat CWUR do të jenë të gjitha NaN)
- Viti 2016: Ka vetëm të dhëna THE (kolonat CWUR do të jenë të gjitha NaN)

**Zgjidhja:**
Mbajmë vetëm vitet 2012-2015 ku kemi coverage të plotë nga të dy sistemet e renditjes.

### Procesi

```python
df_filtered = df[df['year'].isin([2012, 2013, 2014, 2015])]
```

### Output

**Rreshta të hequra:**
- Viti 2011: ~500 rreshta (vetëm THE)
- Viti 2016: ~800 rreshta (vetëm THE)  
- **Total hequr:** ~1,300 rreshta

**Dataset i Filtruar:**
- **Rreshta:** ~2,595 (nga 3,895)
- **Kolona:** 25 (të pandryshuara)
- **Vite:** 4 (2012, 2013, 2014, 2015)
- **Shpërndarja për vit:** ~650 rreshta për çdo vit

**Përfitimi:** Dataset i balancuar me të dhëna nga të dy burimet për çdo universitet në çdo vit


## Hapi 4: Pastrimi dhe Imputimi (`4th_step-data_cleaning`)

### Përshkrim
Ky është hapi më kritik i përgatitjes së të dhënave, ku kryhet pastrimi intensiv, menaxhimi i vlerave munguese me teknika të sofistikuara imputimi, dhe standardizimi i strukturës së datasetit.

### Input
- **Rreshta:** ~2,595
- **Kolona:** 25
- **Problemi kryesor:** Mungesa të larta në disa kolona (>50%)

### Procesi i Detajuar

#### 1. Analiza e Mungesave
Identifikohen kolonat me mungesa të larta:
- `total_score`: >45% mungesë
- `income`: >60% mungesë  
- `female_male_percent`: >50% mungesë

**Vendimi:** Këto kolona hiqen sepse imputimi do të krijonte bias të madh

#### 2. Plotësimi i Kolonave të Renditjes
Nëse një universitet ka renditje në një sistem por jo në tjetrin, përdorim renditjen ekzistuese:
```python
world_rank = world_rank.fillna(cwur_world_rank)
cwur_world_rank = cwur_world_rank.fillna(world_rank)
```

#### 3. Imputimi Hierarkik (3 nivele)

**Niveli 1 - Imputimi për Universitet:**
Për çdo universitet, përdorim medianën e vlerave të tij historike (2012-2015):
```python
Për çdo universitet:
  për çdo kolonë numerike:
    median_vlera = median(vlerat e këtij universiteti në të gjitha vitet)
    zëvendëso NaN me median_vlera
```
*Shembull:* Nëse MIT ka `teaching` = [95, NaN, 96, 94], NaN-i plotësohet me median(95,96,94) = 95

**Niveli 2 - Imputimi për Shtet:**  
Nëse universiteti nuk ka të dhëna historike, përdorim medianën e shtetit:
```python
Për çdo shtet:
  për çdo kolonë numerike:
    median_vlera = median(të gjitha universitetet në këtë shtet)
    zëvendëso NaN me median_vlera
```

**Niveli 3 - Imputimi Global:**
Për vlerat e mbetura, përdorim medianën globale:
```python
Për çdo kolonë:
  median_global = median(e gjithë kolona)
  zëvendëso NaN të mbetura me median_global
```

#### 4. Konvertimi i Tipave
Kolonat CWUR konvertohen në integer (pas imputimit):
```python
cwur_world_rank → int
cwur_quality_of_education → int
...
```

#### 5. Heqja e Rreshtave të Pavlefshme
Hiqen rreshtat që ende nuk kanë as `world_rank` as `cwur_world_rank` (universitete pa asnjë renditje).

### Kolona të Hequra (3 kolona)
1. `total_score` - >45% mungesë
2. `income` - >60% mungesë
3. `female_male_percent` - >50% mungesë

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

### Output

**Skedar:** `cleaned_university_data.csv`

**Dimensionet:**
- **Rreshta:** 2,895 (1 header + 2,894 rreshta të dhënash)
- **Kolona:** 22 (nga 25, -3 të hequra)
- **Mungesa të mbetura:** <1% për shumicën e kolonave

**Struktura e Kolonave (22 total):**
```
1.  world_rank                    [int - Pozicioni THE]
2.  university_name                [string - Emri]
3.  country                        [string - Shteti]
4.  teaching                       [float - THE mësimdhënie 0-100]
5.  international                  [float - THE ndërkombëtar 0-100]
6.  research                       [float - THE kërkime 0-100]
7.  citations                      [float - THE citime 0-100]
8.  num_students                   [float - Numri studentëve]
9.  student_staff_ratio            [float - Raporti student-staf]
10. international_students         [float - % studentë ndërkombëtarë]
11. year                           [int - Viti 2012-2015]
12. cwur_world_rank                [int - Pozicioni CWUR]
13. cwur_national_rank             [int - Pozicioni kombëtar]
14. cwur_quality_of_education      [int - Renditja cilësia arsimit]
15. cwur_alumni_employment         [int - Renditja punësimi]
16. cwur_quality_of_faculty        [int - Renditja fakulteti]
17. cwur_publications              [int - Renditja publikime]
18. cwur_influence                 [int - Renditja influenca]
19. cwur_citations                 [int - Renditja citime]
20. cwur_broad_impact              [int - Renditja ndikimi]
21. cwur_patents                   [int - Renditja patenta]
22. cwur_score                     [float - Rezultati CWUR]
```

**Cilësia e të Dhënave:**
- Mungesa < 1% për kolonat kryesore (teaching, research, citations)
- Të gjitha universitetet kanë të paktën një renditje (THE ose CWUR)
- Tipet numerike të sakta dhe konsistente
- Dataset i balancuar për 4 vite (2012-2015)

**Rezultati:** Dataset i pastër, konsistent, dhe i gatshëm për analizë dhe modele statistikore

---

## Hapi 5: Mostrimi dhe Inxhinieria e Karakteristikave

### Përshkrim
Ky hap krijon një kampion të stratifikuar për vit (për efikasëri në analizë) dhe pasurohet me karakteristika të reja anal itike të derizuara nga të dhënat ekzistuese. Këto karakteristika të reja ofrojnë perspektiva të thelluara për performancën, konsistencën dhe trajektoren e universiteteve.

### Input
- **Skedar:** `cleaned_university_data.csv`
- **Rreshta:** 2,895
- **Kolona:** 22

### Procesi i Detajuar

#### A. Mostrimi i Stratifikuar (`sampling.py`)

**Objektivi:** Krijon një kampion 20% duke ruajtur shpërndarja proporcionale për çdo vit.

**Mëtoda:**
```python
sampled_df = full_df.groupby('year', group_keys=False)
                    .sample(frac=0.2, random_state=42)
```

**Arsyeja:**
- Redukton madhësinë e datasetit për shpejtuar analizën dhe vizualizimet
- Ruan përfaqësim proporcional për çdo vit (2012-2015)
- random_state=42 siguron riprodhueshmori (rezultate konsistente)

**Output i Kampionit:**
- **Skedar:** `sampled_dataset.csv`
- **Rreshta:** 579 (20% e 2,895)
- **Shpërndarja për vit:** ~145 rreshta për çdo vit
- **Kolona:** 22 (të pandryshuara)

#### B. Inxhinieria e Karakteristikave (`feature_engineering.py`)

**Objektivi:** Krijon 17 karakteristika të reja që kapin dimensione të nd ryshme të performancës universiteteve.

**Karakteristikat e Krijuara (17 të reja):**

**1. Metrika të Konsistencës:**

1. **`rank_consistency_std`** (float)
   - Devijimi standard i `world_rank` për çdo universitet nëpër 4 vite
   - **Formula:** `std(world_rank_2012, world_rank_2013, world_rank_2014, world_rank_2015)`
   - **Interpretim:** I ulët = konsistent, i lartë = i paqendëruëshëm
   - **Shembull:** MIT: std=2.5 (shumë konsistent), University X: std=45 (variabil)

2. **`consistency_score`** (float 0-1)
   - Rezultat i normalizuar i konsistencës  
   - **Formula:** `1 / (1 + rank_consistency_std)`
   - **Interpretim:** 1 = perfect konsistent, ~0 = shumë variabil
   - **Shembull:** 0.95 = shumë i qëndrueshëm, 0.30 = i paqendëruëshëm

**2. Indekse Kompozite:**

3. **`research_index`** (float 0-100)
   - Indeksi i kërkimeve dhe impact-it shkencor
   - **Formula:** `(research + citations) / 2`
   - **Komponentet:** THE research score + THE citations score

4. **`teaching_index`** (float 0-100)
   - Indeksi i cilësisë së mësimdhënies dhe hapës në globale
   - **Formula:** `(teaching + international) / 2`
   - **Komponentet:** THE teaching score + THE international outlook

5. **`global_index`** (float 0-100)
   - Indeksi total i performancës (kërkim + mësimdhënie)
   - **Formula:** `(research_index + teaching_index) / 2`
   - **Përdorimi:** Metrikë e përgjithshme për krahasim

**3. Analiza e Trajektores:**

6. **`rank_change`** (int)
   - Ndryshimi i renditjes nga viti i mëparshëm
   - **Formula:** `world_rank[year] - world_rank[year-1]`
   - **Interpretim:** Negativ = përmirësim (renditje më e mirë), Pozitiv = renie
   - **Shembull:** -15 = përmirësuar 15 vende, +20 = rene 20 vende

7. **`trajectory`** (string)
   - Klasifikimi i trendit të universitetit
   - **Formula:**
     ```python
     if rank_change <= -10: "rising"      # Përmirësim i konsideruëshëm
     elif rank_change >= 10: "declining"  # Renie e konsiderueshme
     else: "stable"                      # Pak ndryshim
     ```
   - **Vlerat:** "rising", "stable", "declining"

**4. Klasifikime Gjeografike:**

8. **`region`** (string)
   - Rajoni gjeografik i universitetit
   - **Mëtoda:** Mapping nga `country` në regjione
   - **Vlerat:** "North America", "Europe", "Asia", "Oceania", "Latin America", "Africa"
   - **Shembull:** USA/Canada → "North America", UK/Germany → "Europe"

**5. Indeksi i Diversitetit:**

9. **`diversity_index`** (float 0-1)
   - Matje e diversitetit ndërkombëtar dhe raporti student-staf
   - **Formula:** Mesatarja e `international_students` (normalized) dhe `inverted_student_staff_ratio`
   - **Interpretim:** I lartë = më ndërkombëtar dhe raport më i mirë staf-student

**6. Z-Scores (Standardizim):**

10. **`research_index_z`** (float)
    - Z-score i `research_index`
    - **Formula:** `(research_index - μ) / σ`
    - **Interpretim:** Sa devijime standarde larg mesatares

11. **`teaching_index_z`** (float)
    - Z-score i `teaching_index`
    - **Formula:** `(teaching_index - μ) / σ`

**7. Kategorizime (Binning):**

12. **`rank_tier`** (string)
    - Niveli i renditjes
    - **Vlerat:** "Top 100", "101-200", "201-500", "501+"

13. **`performance_category`** (string)
    - Kategoria e performancës në mësimdhënie
    - **Krit eret:** 
      - "Low": teaching_index < 40
      - "Medium": 40 ≤ teaching_index ≤ 60
      - "High": teaching_index > 60

14. **`size_category`** (string)
    - Kategoria e madhësisë bazuar në `num_students`
    - **Mëtoda:** Quantile-based (33%, 66%)
    - **Vlerat:** "Small", "Medium", "Large"

**8. Flamurë Binarë (Flags):**

15. **`is_top_100`** (int 0/1)
    - A është në top 100 botëror?
    - **Formula:** `1 if world_rank <= 100 else 0`

16. **`is_research_intensive`** (int 0/1)
    - A është universitet kërkim-intensiv?
    - **Formula:** `1 if research_index >= 70 else 0`

17. **`is_rising`** (int 0/1)
    - A është në trajektore rëritjeje?
    - **Formula:** `1 if trajectory == "rising" else 0`

### Output

**Skedar:** `university_data_engineered.csv`

**Dimensionet:**
- **Rreshta:** 2,895 (e gjithë dataseti, jo kampioni)
- **Kolona:** 39 (22 origjinale + 17 të reja)

**Struktura e Kolonave (39 total):**
```
KOLONA ORIGJINALE (22):
1-22: [Njësoj si Hapi 4]

KOLONA TË REJA (17):
23. rank_consistency_std        [float - Devijimi std i renditjes]
24. consistency_score            [float 0-1 - Rezultati konsistence]
25. research_index               [float 0-100 - Indeksi kërkimeve]
26. teaching_index               [float 0-100 - Indeksi mësimdhënies]
27. global_index                 [float 0-100 - Indeksi global]
28. rank_change                  [int - Ndryshimi vit-pas-viti]
29. trajectory                   [string - rising/stable/declining]
30. region                       [string - Rajoni gjeografik]
31. diversity_index              [float 0-1 - Indeksi diversitetit]
32. research_index_z             [float - Z-score research]
33. teaching_index_z             [float - Z-score teaching]
34. rank_tier                    [string - Top 100/101-200/etj.]
35. performance_category         [string - Low/Medium/High]
36. size_category                [string - Small/Medium/Large]
37. is_top_100                   [int 0/1 - Flamur top 100]
38. is_research_intensive        [int 0/1 - Flamur kërkim-intensiv]
39. is_rising                    [int 0/1 - Flamur në rritje]
```

**Shembuj Vlerash:**
```
Harvard University, 2015:
  research_index: 99.7 (ekselentë)
  teaching_index: 96.8 (ekselentë)
  consistency_score: 0.99 (shumë konsistent)
  trajectory: "stable" (gjithmonë në top)
  region: "North America"
  is_top_100: 1
  is_research_intensive: 1
```

**Rezultati:** Dataset i pasuruar me metrika analitike për studime të thelluara të performancës, trendeve dhe karakteristikave të universiteteve

---

## Hapi 6: Agregimi (`6th_step-aggregation`)

### Përshkrim
Ky hap transformon të dhënat nga nivel universiteti në nivel shtet-vit, duke agreguar statistika për të krahasuar performancën e shteteve në periudha kohore. Krijim metrika të reja të derizuara para agregimit për analizë më të thellë.

### Input
- **Skedar:** `cleaned_university_data.csv`
- **Granularitet:** Nivel universiteti (2,895 rreshta)
- **Kolona:** 22

### Procesi i Detajuar

#### 1. Normalizimi i Shteteve
Standardizon emrat e shteteve:
```python
"USA" → "United States of America"
```

#### 2. Krijimi i Karakteristikave të Derizuara

Para agregimit, krijohen 3 metrika të reja:

**a) `rank_gap`** - Diferenca midis renditjeve THE dhe CWUR
```python
rank_gap = world_rank - cwur_world_rank
```
- **Negativ**: THE rendit më mirë (rank më i ulët = më mirë)
- **Pozitiv**: CWUR rendit më mirë
- **Zero**: Renditje identike

**b) `faculty_efficiency`** - Efikasiteti i fakultetit
```python
faculty_efficiency = cwur_quality_of_faculty / student_staff_ratio
```
- Sa cilësië fakulteti për çdo njësi raporti student-staf
- I lartë = fakultet cilësor me raport të mirë

**c) `global_influence_index`** - Indeksi i ndikimit global
Përdor z-scores për vit për të normalizuar:
```python
Për çdo vit:
  citations_z = (citations - mean) / std
  cwur_influence_z = (cwur_influence - mean) / std
  cwur_citations_z = (cwur_citations - mean) / std
  
global_influence_index = mean(citations_z, cwur_influence_z, cwur_citations_z)
```
- Kombinon impactin nga të dy sistemet e renditjes
- I standardizuar për krahasim fair në vite

#### 3. Agregimi sipas Shteti dhe Vitit

Grouping: `groupby(['country', 'year'])`

**Statistikat e Agreguara:**

**Renditjet (mean, median, min):**
- `world_rank` → `world_rank_mean`, `world_rank_median`, `the_best_world_rank` (min)
- `cwur_world_rank` → `cwur_world_rank_mean`, `cwur_world_rank_median`, `the_best_cwur_world_rank` (min)

**Rezultatet Akademike (mean):**
- `teaching`, `international`, `citations`, `cwur_score`
- Të gjitha kolonat CWUR (quality_of_education, alumni_employment, etj.)

**Statistikat e Studentëve:**
- `total_students_covered`: sum(num_students) - Total studentë të mbuluar
- `avg_students_per_university`: mean(num_students)
- `avg_international_student_share`: mean(international_students)
- `student_staff_ratio_mean`: mean(student_staff_ratio)

**Metrikat e Derizuara:**
- `rank_gap_mean`, `faculty_efficiency_mean`, `global_influence_index_mean`

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

### Output

**Skedar:** `country_year_summary.csv`

**Dimensionet:**
- **Granularitet:** Shtet-Vit (transformim nga nivel universiteti)
- **Rreshta:** ~280 kombinime unike (shtet, vit)
- **Kolona:** ~28 kolona statistikore
- **Periudha:** 2012-2015

**Struktura e Kolonave (~28 total):**
```
IDENTIFIKUES (2):
1. country                           [string - Shteti]
2. year                              [int - Viti]

RENDITJET THE (3):
3. world_rank_mean                   [float - Mesatarja e renditjes THE]
4. world_rank_median                 [float - Mediana e renditjes THE]
5. the_best_world_rank               [int - Renditja më e mirë THE]

RENDITJET CWUR (3):
6. cwur_world_rank_mean              [float - Mesatarja e renditjes CWUR]
7. cwur_world_rank_median            [float - Mediana e renditjes CWUR]
8. the_best_cwur_world_rank          [int - Renditja më e mirë CWUR]

RENDIMENTI AKADEMIK (4):
9. teaching_mean                     [float - Mesatarja e mësimdhënies]
10. international_mean               [float - Mesatarja e perspektivës ndërkombëtare]
11. citations_mean                   [float - Mesatarja e citimeve]
12. cwur_score_mean                  [float - Mesatarja e rezultatit CWUR]

METRIKA CWUR (8):
13. cwur_quality_of_education_mean   [float - Mes. cilësia arsimit]
14. cwur_alumni_employment_mean      [float - Mes. punësimi alumni]
15. cwur_quality_of_faculty_mean     [float - Mes. cilësia fakulteti]
16. cwur_publications_mean           [float - Mes. publikime]
17. cwur_influence_mean              [float - Mes. influenca]
18. cwur_citations_mean              [float - Mes. citime CWUR]
19. [cwur_broad_impact, cwur_patents] [Nëse të pranishme]

STATISTIKA STUDENTËVE (4):
20. total_students_covered           [int - Total studentë në shtet]
21. avg_students_per_university      [float - Mes. studentë për universitet]
22. avg_international_student_share  [float - Mes. % studentë ndërkombëtarë]
23. student_staff_ratio_mean         [float - Mes. raport student-staf]

METRIKA TË DERIZUARA (3):
24. rank_gap_mean                    [float - Mes. diferenca THE-CWUR]
25. faculty_efficiency_mean          [float - Mes. efikasiteti fakulteti]
26. global_influence_index_mean      [float - Mes. ndikimi global]
```

**Shembull Rreshti:**
```
country: United States of America
year: 2015
world_rank_mean: 145.3
the_best_world_rank: 1 (Harvard)
cwur_world_rank_mean: 152.8
the_best_cwur_world_rank: 1 (Harvard)
teaching_mean: 68.4
citations_mean: 72.1
total_students_covered: 1,850,000
avg_students_per_university: 25,342
avg_international_student_share: 0.18 (18%)
rank_gap_mean: -7.5 (THE rendit mesatarisht më mirë)
faculty_efficiency_mean: 4.2
```

**Përdorimet:**
- Krahasimi i performancës së shteteve në kohë
- Identifikimi i shteteve me universitetet më të mira
- Analiza e trendeve kombetare (2012-2015)
- Vlerësimi i sistemeve arsimore kombetare

**Rezultati:** Dataset agreguar për analizë komparative në nivel kombëtar dhe temporal

---

## Hapi 7: Përzgjedhja dhe Krijimi i Karakteristikave (`7th_step-feature_selection_creation`)

### Përshkrim
Ky hap optimizon strukturen e datasetit duke hequr karakteristika me vlerë të ulët anal itike (redundante ose me pak informacion) dhe duke krijuar karakteristika të reja më të dobishme që kombinojnë informacion nga burime të ndryshme.

### Input
- **Skedar:** `cleaned_university_data.csv`
- **Rreshta:** 2,895
- **Kolona:** 22

### Procesi i Detajuar

#### 1. Analiza dhe Heqja e Karakteristikave

**Kolonat e Hequra (3):**

1. **`cwur_national_rank`** - Redundante
   - **Arsyeja:** Varet nga `country` dhe `cwur_world_rank`
   - Nuk ofron informacion shtese për analiza globale

2. **`cwur_broad_impact`** - Korrelacion i lartë
   - **Arsyeja:** I korreluar fort me `cwur_influence` dhe `cwur_citations`
   - Redundant në pranincë të metrikave të tjera të impactit

3. **`cwur_patents`** - Mungesa të larta
   - **Arsyeja:** Shumë universitete nuk kanë të dhëna patentash
   - Jo përfaqësuese për të gjitha llojet e universiteteve

#### 2. Krijimi i Karakteristikave të Reja

**Karakteristikat e Krijuara (5):**

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

5. **`high_international_ratio`** - Flag për raport të lartë ndërkombëtar (int 0/1)
   - **Formula:** `1 nëse international_students > 0.30, përndryshe 0`
   - **Interpretim:** Identifikon universitete me >30% studentë ndërkombëtarë
   - **Përdorimi:** Filtrim i shpejtë për universitete të diversifikuara

### Output

**Skedar:** `feature_selected_created_university_data.csv`

**Dimensionet:**
- **Rreshta:** 2,895 (të pandryshuara)
- **Kolona:** 24 (22 - 3 + 5)
- **Ndryshimi:** -3 redundante, +5 të reja

**Struktura e Kolonave (24 total):**
```
KOLONA ORIGJINALE TË MBETURA (19):
1.  world_rank
2.  university_name
3.  country
4.  teaching
5.  international
6.  research
7.  citations
8.  num_students
9.  student_staff_ratio
10. international_students
11. year
12. cwur_world_rank
13. cwur_quality_of_education
14. cwur_alumni_employment
15. cwur_quality_of_faculty
16. cwur_publications
17. cwur_influence
18. cwur_citations
19. cwur_score

KOLONA TË REJA (5):
20. rank_gap                     [int - Diferenca THE-CWUR]
21. research_efficiency_per_1k   [float - Efikasiteti për 1000 studentë]
22. faculty_efficiency           [float - Efikasiteti fakulteti]
23. global_influence_index       [float - Indeksi i ndikimit global]
24. high_international_ratio     [int 0/1 - >30% studentë ndërkombëtarë]
```

**Përfitimet:**
- Dataset më i kompakt (heqje redundancash)
- Metrika më informative (karakteristika të derizuara)
- Kombinim informacioni nga THE dhe CWUR
- Efikasië më e lartë për modele ML

**Rezultati:** Dataset i optimizuar me karakteristika të zgjedhura dhe të pasurura

---

## Hapi 8: Diskretizimi, Binarizimi dhe Transformimi (`8th-step-discret_binar_transform`)

### Përshkrim
Ky është hapi final i përgatitjes së të dhënave, ku krijohen forma të ndryshme të karakteristikave ekzistuese për të mbeshetur analiza të nd ryshme: diskretizim (për kategorizim), binarizim (për flamurë), transformime relative (për krahasime kontekstuale), dhe standardizim (për modele ML).

### Input
- **Skedar:** `feature_selected_created_university_data.csv`
- **Rreshta:** 2,895
- **Kolona:** 24

### Procesi i Detajuar

#### A. Diskretizimi (Binning)

**Objektivi:** Konverton vlera të vazhdueshme numerike në kategori diskrete për analiza kategorike dhe vizualizime.

**Mëtoda:** Quantile-based binning (ndarje në 3 grupe me numër të barabartë elementesh)

**Karakteristikat e Diskretizuara (2):**

1. **`teaching_level`** (string)
   - Kategorizimi i rezultatit THE teaching
   - **Formula:** 
     ```python
     quantiles = teaching.quantile([0.33, 0.67])
     if teaching < quantiles[0.33]: "Low"
     elif teaching < quantiles[0.67]: "Medium"
     else: "High"
     ```
   - **Vlerat:** "Low", "Medium", "High"
   - **Shpërndarja:** ~33% në çdo kategori
   - **Shembull:** teaching=45 → "Low", teaching=68 → "Medium", teaching=89 → "High"

2. **`citations_level`** (string)
   - Kategorizimi i rezultatit THE citations
   - **Formula:** Njësoj si `teaching_level`, por për kolonan `citations`
   - **Vlerat:** "Low", "Medium", "High"
   - **Përdorimi:** Identifikon universitete me impact të ulët/mesatar/të lartë shkencor

#### B. Binarizimi (Flamurë)

**Objektivi:** Krijon flamurë binarë (0/1) për identifikim të shpejtë të karakteristikave bin are.

**Karakteristikat Binare (3):**

1. **`top100_times`** (int 0/1)
   - A është në top 100 sipas THE?
   - **Formula:** `1 if world_rank <= 100 else 0`
   - **Përdorimi:** Filtrim i universiteteve elite sipas THE

2. **`top100_cwur`** (int 0/1)
   - A është në top 100 sipas CWUR?
   - **Formula:** `1 if cwur_world_rank <= 100 else 0`
   - **Përdorimi:** Filtrim i universiteteve elite sipas CWUR
   - **Krahasim:** Disa universitete mund të jenë top 100 në njërin sistem por jo në tjetrin

3. **`high_international_ratio`** (int 0/1)
   - Ruhet nga Hapi 7
   - Identifikon universitete me >30% studentë ndërkombëtarë

#### C. Transformime Kontekstuale (Relative)

**Objektivi:** Krijon metrika relative që krahasojnë çdo universitet me mesataren e shtetit të tij në atë vit.

**Arsyeja:** Lejon krahasime fair - p.sh., një universitet me teaching=70 në USA (ku mesatarja është 75) mund të jetë nën standard, por në vend tjetër (ku mesatarja është 50) do të jetë ekselent.

**Hapat:**

**1. Llogaritja e Mesatareve Kontekstuale (3 kolona auxiliare):**

1. **`country_year_teaching_mean`** (float)
   - Mesatarja e `teaching` për çdo kombinim (country, year)
   - **Formula:** `groupby(['country', 'year'])['teaching'].transform('mean')`

2. **`country_year_citations_mean`** (float)
   - Mesatarja e `citations` për çdo kombinim (country, year)
   - **Formula:** `groupby(['country', 'year'])['citations'].transform('mean')`

3. **`country_year_cwur_score_mean`** (float)
   - Mesatarja e `cwur_score` për çdo kombinim (country, year)
   - **Formula:** `groupby(['country', 'year'])['cwur_score'].transform('mean')`

**2. Llogaritja e Vlerave Relative (3 kolona):**

4. **`relative_teaching`** (float)
   - Mësimdhënia relative ndaj mesatares kombëtare-vjetore
   - **Formula:** `teaching / country_year_teaching_mean`
   - **Interpretim:**
     - 1.0 = në mesatare
     - 1.2 = 20% mbi mesataren kombëtare
     - 0.8 = 20% nën mesataren kombëtare

5. **`relative_citations`** (float)
   - Citimet relative ndaj mesatares kombëtare-vjetore
   - **Formula:** `citations / country_year_citations_mean`
   - **Shembull:** 1.5 = 50% më shumë citime se mesatarja e shtetit

6. **`relative_cwur_score`** (float)
   - Rezultati CWUR relative
   - **Formula:** `cwur_score / country_year_cwur_score_mean`
   - **Përdorimi:** Identifikon leaderë brenda çdo shteti

#### D. Standardizimi (Z-Scores)

**Objektivi:** Standardizon vlerat për të lejuar krahasime direkte midis karakteristikave me shkallë të ndryshme dhe për algoritme ML.

**Formula Gjenerike:** `z = (x - μ) / σ`
- μ = mesatarja e popullatrs
- σ = devijimi standard
- **Interpretim:** Sa devijime standarde larg mesatares
  - z=0: në mesatare
  - z=1: 1 devijim standard mbi mesataren
  - z=-2: 2 devijime standarde nën mesataren

**Karakteristikat e Standardizuara (5):**

1. **`teaching_z`** (float)
   - Z-score i `teaching`
   - **Formula:** `(teaching - mean(teaching)) / std(teaching)`
   - **Përdorimi:** Krahasim i teaching scores në shkallë të standardizuar

2. **`citations_z`** (float)
   - Z-score i `citations`
   - **Formula:** `(citations - mean(citations)) / std(citations)`
   - **Shembull:** z=2.5 tregon impact jashtezakonisht të lartë

3. **`num_students_z`** (float)
   - Z-score i `num_students`
   - **Formula:** `(num_students - mean(num_students)) / std(num_students)`
   - **Përdorimi:** Identifikon universitete jashtëzakonisht të mëdha ose të vogla

4. **`relative_teaching_z`** (float)
   - Z-score i `relative_teaching`
   - **Formula:** `(relative_teaching - mean(relative_teaching)) / std(relative_teaching)`
   - **Dallimi:** Standardizon performancën relative (jo absolute)

5. **`relative_citations_z`** (float)
   - Z-score i `relative_citations`
   - **Formula:** `(relative_citations - mean(relative_citations)) / std(relative_citations)`
   - **Përdorimi:** Identifikon outlierë brenda kontekstit kombëtar

### Output Final

**Skedar:** `university_data_discretized_transformed.csv`

**Dimensionet:**
- **Rreshta:** 2,895 (të pandryshuara)
- **Kolona:** 39 (24 nga Hapi 7 + 15 të reja)
- **Periudha:** 2012-2015

**Struktura e Kolonave (39 total):**
```
KOLONA ORIGJINALE (19):
1-19: [Si në Hapin 7 - kolona bazike]

KARAKTERISTIKA NGA HAPI 7 (5):
20. rank_gap
21. research_efficiency_per_1k
22. faculty_efficiency
23. global_influence_index
24. high_international_ratio

KARAKTERISTIKA TË REJA - HAPI 8 (15):

DISKRETIZUARA (2):
25. teaching_level               [string - Low/Medium/High]
26. citations_level              [string - Low/Medium/High]

BINARE (2):
27. top100_times                 [int 0/1 - Top 100 THE]
28. top100_cwur                  [int 0/1 - Top 100 CWUR]

KONTEKSTUALE - MESATARE (3):
29. country_year_teaching_mean   [float - Mesatarja kombëtare teaching]
30. country_year_citations_mean  [float - Mesatarja kombëtare citations]
31. country_year_cwur_score_mean [float - Mesatarja kombëtare cwur_score]

RELATIVE (3):
32. relative_teaching            [float - Raport ndaj mesatares kombëtare]
33. relative_citations           [float - Raport ndaj mesatares kombëtare]
34. relative_cwur_score          [float - Raport ndaj mesatares kombëtare]

Z-SCORES (5):
35. teaching_z                   [float - Z-score teaching]
36. citations_z                  [float - Z-score citations]
37. num_students_z               [float - Z-score numëri studentëve]
38. relative_teaching_z          [float - Z-score relative teaching]
39. relative_citations_z         [float - Z-score relative citations]
```

**Shembull Rreshti - Harvard University 2015:**
```
Kolona Bazike:
  world_rank: 1
  teaching: 99.7 | citations: 99.9
  
Diskretizuara:
  teaching_level: "High" | citations_level: "High"
  
Binare:
  top100_times: 1 | top100_cwur: 1
  
Kontekstuale:
  country_year_teaching_mean: 68.5 (mesatarja USA 2015)
  
Relative:
  relative_teaching: 1.45 (45% mbi mesataren USA)
  relative_citations: 1.38 (38% mbi mesataren USA)
  
Z-Scores:
  teaching_z: 2.89 (2.89 std mbi mesataren globale)
  citations_z: 3.15 (performancë ekselente)
  relative_teaching_z: 1.92 (leader kombëtar)
```

**Rezultati Final:** Dataset i plotë dhe i transformuar me:
- 39 karakteristika (bazike + të derizuara + të transformuara)
- Forma të ndryshme (numerike, kategorike, binare, relative, standardizuara)
- Gati për analiza të avancuara, vizualizime komplekse, dhe Machine Learning
- Mbeshtet krahasime absolute, relative, dhe kontekstuale
- Të dhënat e pastruara, konsistente dhe të standardizuara

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



