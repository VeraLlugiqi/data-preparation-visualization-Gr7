# Hapi 10: Mënjanimi i Zbulimeve Jo të Sakta

## Përshkrim

Ky hap kryen një pastrim final të datasetit duke hequr vlera të pasakta, të pamundura, dhe rreshta duplikatë. Ai siguron që të gjitha vlerat janë logjike, konsistente dhe të vlefshme për analizë.

## Objektivat

1. **Heqja e vlerave negative ose zero** në kolona ku këto nuk janë të vlefshme
2. **Kontrollimi i vlerave të pamundura** (p.sh., përqindje > 100%)
3. **Heqja e duplikateve** për të shmangur bias në analizë
4. **Pastrimi i vlerave munguese kritike**
5. **Validimi logjik** i vlerave (p.sh., renditje pozitive)

## Input

- **Skedar:** `../8th-step-discret_binar_transform/university_data_discretized_transformed.csv`
- **Rreshta:** ~2,895
- **Kolona:** 39

## Procesi i Detajuar

### 1. Kontrollimi i Vlerave Negative ose Zero

Kolonat e mëposhtme nuk mund të kenë vlera negative ose zero:
- `international` - Rezultati duhet të jetë pozitiv
- `research` - Rezultati duhet të jetë pozitiv
- `citations` - Rezultati duhet të jetë pozitiv
- `num_students` - Numri i studentëve duhet të jetë > 0
- `student_staff_ratio` - Raporti duhet të jetë pozitiv

**Aksion:** Hiqen të gjithë rreshtat ku këto kolona kanë vlera <= 0

### 2. Kontrollimi i Vlerave të Pamundura për International Students

`international_students` paraqet përqindjen e studentëve ndërkombëtarë dhe duhet të jetë në rangun [0, 1] (ose [0, 100] nëse është në përqindje).

**Aksion:** Hiqen rreshtat ku `international_students > 1` (nëse është në formatin 0-1)

### 3. Heqja e Rreshtave Duplikatë

Duplikatët mund të shkaktojnë:
- Bias në analiza statistikore
- Përmirësim të rreme të saktësisë së modeleve
- Interpretim të gabuar të rezultateve

**Aksion:** Hiqen të gjithë rreshtat e përsëritur plotësisht

### 4. Kontrollimi i Vlerave NULL (Mungesë)

Për kolonat kritike, vlerat munguese nuk janë të pranueshme:
- `university_name` - Emri duhet të ekzistojë
- `country` - Shteti duhet të ekzistojë
- `year` - Viti duhet të ekzistojë
- `world_rank` - Renditja duhet të ekzistojë
- `teaching`, `research` - Rezultatet kryesore duhet të ekzistojnë

**Aksion:** Hiqen rreshtat ku mungojnë këto të dhëna kritike

### 5. Kontrollimi i Vlerave Logjike

- Renditjet (`world_rank`, `cwur_world_rank`) duhet të jenë pozitive (> 0)
- Vlerat duhet të jenë konsistente me kuptimin e tyre

**Aksion:** Hiqen rreshtat me renditje <= 0

## Output

**Skedar:** `university_data_final_cleaned.csv`

**Dimensionet:**
- **Rreshta:** ~2,800-2,850 (varësisht nga sa vlera jo të sakta gjenden)
- **Kolona:** 39 (të njëjta si input)
- **Reduktimi:** Zakonisht < 5% e rreshtave hiqen

**Karakteristikat:**
- ✅ Pa vlera negative ose zero në kolonat e specifikuara
- ✅ Pa vlera të pamundura (> 1 për përqindje)
- ✅ Pa duplikatë
- ✅ Pa vlera munguese kritike
- ✅ Renditje pozitive dhe logjike

## Përdorimi

```bash
cd 10th_step-removal-incorr-findings
python removal_incorrect_findings.py
```

## Kërkesat

- pandas
- numpy
- pathlib

## Shënime të Rëndësishme

1. **Heqja e të Dhënave:** Ky skedar heq rreshta që nuk janë të vlefshëm, kështu që dataset final mund të jetë pak më i vogël
2. **Kolonat Kritike:** Lista e kolonave kritike mund të modifikohet sipas nevojës
3. **Kontrollimi Logjik:** Duhet të siguroheni që vlerat janë në formatin e pritur (p.sh., përqindje në [0,1] apo [0,100])

## Rezultati

Dataset final i pastër dhe i validuar, i gatshëm për:
- Analiza statistikore të besueshme
- Vizualizime pa artefakte
- Modele Machine Learning më të sakta
- Raporte dhe prezantime profesionale

