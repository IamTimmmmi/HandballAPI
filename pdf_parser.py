import camelot
import pandas as pd
import os
import re
import pdfplumber


def clean_name(raw):
    if raw is None:
        return ""
    # Klammerinhalt entfernen, Pfeile/-> etc.
    raw = re.sub(r'\(.*?\)', '', str(raw))
    # alles außer Buchstaben (inkl. deutsche Umlaute) und Leerzeichen entfernen
    raw = re.sub(r'[^A-Za-zÄÖÜäöüß\s]', ' ', raw)
    # mehrfach-Leerzeichen reduzieren
    raw = re.sub(r'\s+', ' ', raw)
    return raw.strip()


def parse_pdf(pdf_file, team_name):
    data = []
    if os.path.getsize(pdf_file) == 0:
        print(f"{pdf_file} ist leer, überspringe...")
        return data

    # Teamnamen aus dem PDF extrahieren (Heim/Gast)
    extracted_team_name = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            page = pdf.pages[1]  # Seite 2
            text = page.extract_text()
            for line in text.splitlines():
                if line.startswith("Heim:"):
                    home_team = line.replace("Heim:", "").strip()
                elif line.startswith("Gast:"):
                    guest_team = line.replace("Gast:", "").strip()
            # Prüfen welche Tabelle das eigene Team ist
            if team_name.lower() == home_team.lower():
                extracted_team_name = home_team
                own_table_index = 0
            elif team_name.lower() == guest_team.lower():
                extracted_team_name = guest_team
                own_table_index = 1
            else:
                extracted_team_name = ""
                own_table_index = -1
    except Exception as e:
        print(f"Fehler beim Auslesen der Teamnamen aus {pdf_file}: {e}")

    try:
        tables = camelot.read_pdf(pdf_file, pages="2", flavor="lattice")
    except Exception as e:
        print(f"Fehler beim Lesen von {pdf_file}: {e}")
        return data

    if not tables:
        print(f"Keine Tabellen gefunden in {pdf_file}")
        return data

    for i, table in enumerate(tables):
        df = table.df
        df.columns = df.iloc[0]
        df = df[1:]

        # Flag für eigene Mannschaft
        is_own_flag = 1 if i == own_table_index else 0

        for _, row in df.iterrows():
            nr = row.iloc[0].strip()
            if not nr.isdigit():
                continue

            raw_name = row.iloc[1].strip()

            name = clean_name(raw_name)

            try:
                tore = int(row.iloc[5].strip())
            except:
                tore = 0

            seven_m = row.iloc[6].strip()
            match = re.match(r'(\d+)/(\d+)', seven_m)
            if match:
                seven_chancen = int(match.group(1))
                seven_treffer = int(match.group(2))
            else:
                seven_chancen = 0
                seven_treffer = 0

            verwarnungen = row.iloc[7].strip()
            strafen = row.iloc[9].strip().split()
            strafe1 = strafen[1] if len(strafen) > 1 else row.iloc[8].strip()
            strafe2 = strafen[1] if len(strafen) > 1 else ''
            strafe3 = strafen[2] if len(strafen) > 2 else ''
            disq = strafen[3] if len(strafen) > 3 else ''

            data.append({
                "Nr": nr,
                "Name": name,
                "Tore": tore,
                "7m_Chancen": seven_chancen,
                "7m_Treffer": seven_treffer,
                "Verwarnungen": verwarnungen,
                "2min_1": strafe1,
                "2min_2": strafe2,
                "2min_3": strafe3,
                "Disqualifikation": disq,
                "Is_Own": is_own_flag
            })

    return data
