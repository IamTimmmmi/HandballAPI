from gid_extractor import get_spiel_links, get_gids_from_links
from pdf_download import download_pdf_by_gid
from pdf_parser import parse_pdf
from analysis import *
import pandas as pd
import glob
import os
import gc

team_name =  "SC Alstertal-Langenhorn" 
spielplan_url = "https://www.handball.net/mannschaften/handball4all.hamburg.1347116/spielplan?dateFrom=2025-07-01&dateTo=2026-06-30"
pdf_folder = r"C:/Users/tim-e/OneDrive/Desktop/HandballAPI/berichte"

spiel_links = get_spiel_links(spielplan_url)
gids = get_gids_from_links(spiel_links)

# PDFs herunterladen
for gid in gids:
    download_pdf_by_gid(gid, pdf_folder)

# PDFs auslesen
data = []
for pdf_file in glob.glob(f"{pdf_folder}/*.pdf"):
    data += parse_pdf(pdf_file, team_name)

df_all = pd.DataFrame(data)


eigene_spieler = df_all[df_all["Is_Own"] == 1]
gegner_mannschaft = df_all[df_all["Is_Own"] == 0]

print("Gesamt Tore eigene Mannschaft:", gesamt_tore(eigene_spieler))
print("7m Treffer / Chancen:", gesamt_7m(eigene_spieler))
print("Gesamt 2-Minuten-Strafen:", gesamt_zweitstrafe(eigene_spieler))
print("Disqualifikationen:", gesamt_disq(eigene_spieler))

print(ranking_gesamt(eigene_spieler))

gc.collect()