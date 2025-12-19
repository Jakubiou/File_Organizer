# File Organizer  
Jakub Šrámek

Program pro automatickou organizaci souborů pomocí grafického uživatelského rozhraní.

---

## Popis

Tento projekt slouží k organizaci souborů ve zvolené složce.  
Uživatel si vše nastavuje přímo v grafickém rozhraní, není potřeba upravovat žádné konfigurační soubory.

Program umožňuje:

- vybrat vstupní složku pomocí UI,
- organizovat soubory podle:
  - typu souboru (přípona),
  - data vytvoření,
  - velikosti souboru,
- zvolit počet procesů pro rychlejší zpracování,
- sledovat průběh pomocí progress baru,
- zobrazit průběh a výsledky v logu aplikace.

Projekt je vytvořen v Pythonu a používá `multiprocessing` pro paralelní zpracování souborů.

---

## Použití programu

### 1. Spuštění aplikace

Program se spouští spuštěním exe souboru v dist s nazvem FileOrganizer.exe.  
Po spuštění se otevře grafické okno **File Organizer UI**.

---

### 2. Výběr vstupní složky

- Klikni na tlačítko **Vybrat složku**
- Vyber složku, ve které chceš organizovat soubory

---

### 3. Nastavení počtu procesů

- Pomocí posuvníku nastav počet procesů
- Vyšší počet procesů znamená rychlejší zpracování (záleží na výkonu počítače)

---

### 4. Volba způsobu organizace

#### Podle typu souboru

- Soubory se přesouvají podle přípony
- Mapování cílových složek a přípon se nastavuje v textovém poli **Output složky**

Příklad:


Images:jpg,jpeg,png
Docs:txt,pdf,docx
Archives:zip,rar


---

#### Podle data

- Přesune soubory vytvořené v zadaném časovém intervalu
- Datum se zadává ve formátu:


YYYY-MM-DD


---

#### Podle velikosti souboru

- Přesune soubory menší nebo rovné zadané velikosti
- Velikost se zadává v MB

---

### 5. Spuštění organizace

- Klikni na tlačítko **Start**
- Program začne zpracovávat soubory

---

## Průběh a výstup

- **Progress bar** zobrazuje průběh zpracování
- **Log** zobrazuje:
  - přesunuté soubory,
  - přeskočené soubory,
  - chybové hlášky,
  - konečný výsledek