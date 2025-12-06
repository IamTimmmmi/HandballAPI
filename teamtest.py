

import pdfplumber
import camelot

pdf_file = "C:/Users/tim-e/OneDrive/Desktop/HandballAPI/berichte/spielbericht_3049286.pdf"
own_team_name = "SC Alstertal-Langenhorn"

# Seite 2 öffnen
with pdfplumber.open(pdf_file) as pdf:
    page = pdf.pages[1]
    text = page.extract_text()

# Teamname finden
lines = text.splitlines()
home_team = ""
guest_team = ""
for line in lines:
    if line.startswith("Heim:"):
        home_team = line.replace("Heim:", "").strip()
    elif line.startswith("Gast:"):
        guest_team = line.replace("Gast:", "").strip()

# Tabellen einlesen
tables = camelot.read_pdf(pdf_file, pages="2", flavor="lattice")

# Tabellen Heim/Gast zuordnen
table_flags = []
for i, table in enumerate(tables):
    if own_team_name.lower() == home_team.lower():
        table_flags.append(1 if i == 0 else 0)
    elif own_team_name.lower() == guest_team.lower():
        table_flags.append(1 if i == 1 else 0)
    else:
        table_flags.append(0)  # Fallback, Team nicht gefunden

print("Home Team:", home_team)
print("Guest Team:", guest_team)
print("Table flags (1=own team, 0=opponent):", table_flags)