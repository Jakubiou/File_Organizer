# File Organizer
Jakub Šrámek

Program pro automatické přesouvání souborů do složek podle typu.

---

## Popis

Tento projekt umožňuje:

- organizovat soubory v zadané složce (`input_folder`) do podsložek podle typu (např. obrázky, dokumenty, archivy),
- používat více vláken pro rychlejší přesun souborů,
- měnit konfiguraci pomocí `dist/config.json`.

Projekt je připraven jako **Python projekt + hotový EXE v `dist/`**.

---

## Konfigurace (`dist/config.json`)

Tento soubor určuje, odkud se mají soubory brát a kam se mají přesouvat.  
Stačí upravit hodnoty podle potřeby.

input_folder -> cesta ke složce, ze které se soubory přesouvají

num_threads -> počet vláken pro rychlejší přesun souborů

output_folders -> mapování cílových složek na typy souborů

