# Removal of Incorrect Findings (Outlier Consensus Filtering)

Ky hap përfaqëson fazën “Mënjanimi i zbulimeve jo të sakta”, ku kombinohen rezultatet e tre metodave të detektimit të përjashtuesve (Z-Score, IQR, Isolation Forest) për të identifikuar vetëm outliers e vërtetë.

Qëllimi është të hiqen rreshtat që kanë devijime të forta dhe shfaqen si outliers në më shumë se një metodë, duke siguruar një dataset më të qëndrueshëm për analizat e mëtejshme.

---

## 1. Përmbledhje

Ky hap kryen:

- Leximin e outliers nga:
  - `outliers_zscore.csv`
  - `outliers_iqr.csv`
  - `outliers_isolation_forest.csv`
  - datasetin origjinal `final_dataset.csv`
- Ndërtimin e një identifikuesi unik për çdo rresht (university_name | country | year)
- Kombinimin e rezultateve të tre metodave
- Klasifikimin e outliers në:
  - outliers të vërtetë (shfaqen në ≥ 2 metoda)
  - outliers të pasaktë (shfaqen vetëm në 1 metodë)
- Heqjen e outliers të vërtetë nga dataset-i origjinal
- Gjenerimin e dataset-it final pa outliers

---

## 2. Input Files

Ky hap përdor këto fajlla:

- `outliers_zscore.csv`
- `outliers_iqr.csv`
- `outliers_isolation_forest.csv`
- `final_dataset.csv` (dataset origjinal)

---

## 3. Output Files

### 3.1 outliers_all_methods_comparison.csv  
Përmban kombinimin e tre metodave për çdo universitet/vend/vit, si dhe numrin e metodave që e kanë etiketuar si outlier (`methods_flagged`).

### 3.2 outliers_consensus.csv  
Përfshin outliers të vërtetë, pra ato raste që janë detektuar nga dy ose tre metoda (`methods_flagged ≥ 2`).  
Këta rreshta hiqen nga dataset-i final.

### 3.3 outliers_false_detected.csv  
Përfshin rastet që janë detektuar si outlier vetëm nga një metodë.  
Këta konsiderohen zbulime të pasakta dhe nuk hiqen nga dataset-i.

### 3.4 final_dataset_with_outlier_flags.csv  
Dataset-i origjinal i zgjeruar me një kolonë shtesë:


Përdoret për verifikim dhe auditim.

### 3.5 final_dataset_no_outliers.csv  
Dataset-i final i pastër pa outliers të vërtetë.  
Ky file përdoret për analizat e mëtejshme të projektit.

---

## 4. Logjika e Heqjes së Outliers

- Një rresht konsiderohet outlier i vërtetë nëse është shënuar si outlier në 2 ose 3 metoda.
- Një rresht që del si outlier vetëm në 1 metodë klasifikohet si "false detection".
- Vetëm outliers e vërtetë hiqen nga dataset-i.
- Metoda garanton stabilitet statistikor duke shmangur heqjen e rasteve që janë devijime të vogla.

---

## 5. Shembuj të Outliers Konsensus

Disa universitete të detektuara si outliers të vërtetë në këtë hap:

- Alexandria University  
- Australian National University  
- Aberystwyth University  
- Arizona State University  
- Bielefeld University  
- Aston University  

Këto institucione shfaqin devijime të forta në një ose më shumë nga dimensionet:

- numër studentësh jashtëzakonisht i lartë ose i ulët
- vlera të pazakonta të research dhe citations
- student-staff ratio jashtë intervalit normal
- variacione të mëdha nga viti në vit

---

## 6. Rezultati Final

| File | Përmbajtja | Qëllimi |
|------|-------------|---------|
| outliers_consensus.csv | Outliers të vërtetë | Për t'u hequr |
| final_dataset_no_outliers.csv | Dataset final pa outliers | Përdoret për analizat e tjera |
| outliers_false_detected.csv | Outliers të pasaktë | Vetëm raportim |

Dataset-i final është më i balancuar, pa ekstremitete dhe gati për fazat e tjera të analizës statistikore dhe modelimit.

---
