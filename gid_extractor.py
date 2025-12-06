import requests
from bs4 import BeautifulSoup
import re as re

def get_spiel_links(spielplan_url):
    response = requests.get(spielplan_url)
    soup = BeautifulSoup(response.text, "html.parser")

    spiel_links = []
    for a in soup.find_all("a", class_="contents", href=True):
        href = a['href']
        if "/spielbericht" in href:
            full_url = "https://www.handball.net" + href
            spiel_links.append(full_url)
    return spiel_links

def get_gids_from_links(spiel_links):
    gids = []
    for link in spiel_links:
        info_link = link.replace("/spielbericht", "/info")
        response = requests.get(info_link)
        soup = BeautifulSoup(response.text, "html.parser")
        a_tag = soup.find("a", href=re.compile(r"sboPublicReports\.php\?sGID=\d+"))
        if a_tag:
            match = re.search(r"sGID=(\d+)", a_tag['href'])
            if match:
                gids.append(match.group(1))
    return gids