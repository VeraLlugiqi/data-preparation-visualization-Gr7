# Hapi 11: Eksplorimi i të Dhënave (Statistika Përmbledhëse & Multivariante)

## Përshkrim

Ky hap realizon **eksplorimin eksplorues të të dhënave (EDA)** mbështetur në datasetin final **pa përjashtues (outliers)**.  
Qëllimi është të:

- **Shikohen statistikat përmbledhëse** për të gjitha kolonat numerike (mesatare, medianë, devijim standard, minimum, maksimum, etj.).
- **Analizohen marrëdhëniet multivariante** midis metrikeve kryesore (teaching, research, citations, cwur_score, metrikat relative dhe të efikasitetit).
- **Vizualizohen shpërndarjet** (histograme, boxplot-e) dhe **korrelacionet** (heatmap, pairplot).

Pas detektimit të përjashtuesve (Hapi 9) dhe mënjanimit të zbulimeve jo të sakta (Hapi 10), këtu bëhet **analiza e thelluar e të dhënave të pastruara**.

---

## Input

- **Skedar:** `../10th_step-removal-incorr-findings/final_dataset_no_outliers.csv`
- **Përmbajtja:** Dataseti final i universiteteve pas heqjes së outliers konsensus.
- **Përmasa:**
  - Rreshta: 2,358
  - Kolona: 39 (përfshin metrikat bazë + metrika të derizuara/relative/z-scores)

---

## Output

Ky hap gjeneron:

- **`summary_statistics_numeric.csv`**  
  - Statistika përmbledhëse për të gjitha kolonat numerike (count, mean, std, min, 25%, 50%, 75%, max).

- **`country_summary_after_outlier_removal.csv`**  
  - Statistika përmbledhëse sipas shtetit (mesatare, medianë, min, max, count) për:
    - `teaching`, `research`, `citations`, `cwur_score`
    - `num_students`, `international_students` (nëse janë të pranishme)

- **`hist_*.png`**  
  - Histogramë + KDE për metrikat kryesore:
    - `teaching`, `research`, `citations`, `cwur_score`
    - `num_students`, `student_staff_ratio` (nëse ekzistojnë në dataset)

- **`boxplot_*.png`**  
  - Boxplot-e për të njëjtat metrika (identifikim vizual i vlerave ekstreme edhe pas filtrimit).

- **`correlation_heatmap_core_features.png`**  
  - Heatmap i matricës së korrelacioneve mes variablave kryesore:
    - Nota të performancës (`teaching`, `research`, `citations`, `cwur_score`)
    - Metrika të efikasitetit (`rank_gap`, `research_efficiency_per_1k`, `faculty_efficiency`, `global_influence_index`)
    - Metrika relative (`relative_teaching`, `relative_citations`, `relative_cwur_score`)
    - Variabla strukturore (`num_students`, `student_staff_ratio`) – nëse janë në dataset.

- **`pairplot_core_metrics.png`**  
  - Pairplot (scatter + distribucione) për një grup metrikash kyçe:
    - `teaching`, `research`, `citations`, `cwur_score`
    - `relative_teaching`, `relative_citations`

---

## Skripti Kryesor

- **Emri:** `exploratory_analysis_summary_multivariate.py`
- **Funksioni kryesor:** `main()`

### Çfarë bën skripti?

1. **Lexon datasetin pa outliers**
   - Nga `../10th_step-removal-incorr-findings/final_dataset_no_outliers.csv`
   - Kontrollon nëse file ekziston dhe nëse dataseti nuk është bosh.

2. **Statistika përmbledhëse (univariate)**
   - Për të gjitha kolonat numerike:
     - `count`, `mean`, `std`, `min`, `25%`, `50%`, `75%`, `max`
   - Ruhet në: `summary_statistics_numeric.csv`

3. **Statistika sipas shtetit (country-level)**
   - Grupim: `groupby("country")`
   - Për metrikat kryesore (nëse ekzistojnë): `teaching`, `research`, `citations`, `cwur_score`, `num_students`, `international_students`
   - Llogarit: `mean`, `median`, `min`, `max`, `count`
   - Ruhet në: `country_summary_after_outlier_removal.csv`

4. **Vizualizime univariate**
   - Për çdo kolonë kryesore numerike (p.sh. `teaching`, `citations`, ...):
     - Histogram + KDE: `hist_<column>.png`
     - Boxplot: `boxplot_<column>.png`

5. **Analizë multivariante – Korrelacionet**
   - Përzgjedh një nëngrup variablesh numerike relevante:
     - `teaching`, `research`, `citations`, `cwur_score`
     - `rank_gap`, `research_efficiency_per_1k`, `faculty_efficiency`, `global_influence_index`
     - `relative_teaching`, `relative_citations`, `relative_cwur_score`
     - `num_students`, `student_staff_ratio`
   - Llogarit matricën e korrelacioneve Pearson.
   - Vizualizon heatmap me annotime (vlera numerike të korrelacionit).
   - Ruhet në: `correlation_heatmap_core_features.png`

6. **Analizë multivariante – Marrëdhënie grafike**
   - Krijon një `pairplot` për metrikat:
     - `teaching`, `research`, `citations`, `cwur_score`, `relative_teaching`, `relative_citations`
   - Lejon shikimin e lidhjeve jo-lineare, shpërndarjeve dhe strukturave të mundshme të grupeve.
   - Ruhet në: `pairplot_core_metrics.png`

---

## Si të Ekzekutosh

1. Sigurohu që ke të instaluara paketat e nevojshme:

```bash
pip install pandas numpy matplotlib seaborn
```

2. Nga directory i projektit, ekzekuto:

```bash
cd 11th_step-exploratory_analysis
python exploratory_analysis_summary_multivariate.py
```

3. Shiko rezultatet:

- **CSV**:
  - `summary_statistics_numeric.csv`
  - `country_summary_after_outlier_removal.csv`
- **Figura (PNG)**:
  - `hist_*.png`, `boxplot_*.png`
  - `correlation_heatmap_core_features.png`
  - `pairplot_core_metrics.png`

---

## Roli i këtij Hapi në Projekt

- **Pas Hapit 9 (Detektimi i përjashtuesve)** dhe **Hapit 10 (Mënjanimi i zbulimeve jo të sakta)**, ky hap:
  - Verifikon se si duket **distribucioni i metrikeve** pasi janë hequr outliers.
  - Analizon **lidhjet mes variablave kryesore** (p.sh. si lidhen research dhe citations me cwur_score).
  - Jep një **pamje statistike të qartë** të datasetit final që do të përdoret për interpretim dhe vizualizim në raportin përfundimtar.

Me këtë hap, pipeline-i i përgatitjes së të dhënave përfshin jo vetëm pastrimin dhe transformimin, por edhe **analizën eksploruese statistikore** të rezultatit final.




