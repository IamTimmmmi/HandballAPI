import os
import requests

def download_pdf_by_gid(gid, pdf_folder):
    os.makedirs(pdf_folder, exist_ok=True)
    pdf_name = f"spielbericht_{gid}.pdf"
    pdf_path = os.path.join(pdf_folder, pdf_name)

    if os.path.exists(pdf_path):
        print(f"{pdf_name} existiert bereits. Download übersprungen.")
        return pdf_path

    pdf_url = f"https://spo.handball4all.de/misc/sboPublicReports.php?sGID={gid}"
    response = requests.get(pdf_url)
    if response.status_code == 200:
        with open(pdf_path, "wb") as f:
            f.write(response.content)
        print(f"{pdf_name} erfolgreich heruntergeladen.")
        return pdf_path
    else:
        print(f"Fehler beim Download: Status {response.status_code}")
        return None
