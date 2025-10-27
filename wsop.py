#!/usr/bin/env python3
"""
Scrape a winners table from the World Series of Poker Wikipedia page
URL: https://en.wikipedia.org/wiki/World_Series_of_Poker

Requires: requests, beautifulsoup4
Install: pip install requests beautifulsoup4
"""
import requests
from bs4 import BeautifulSoup
import sys

URL = "https://en.wikipedia.org/wiki/World_Series_of_Poker"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def find_winners_table(soup):
    # Prefer tables with "Year" and "Winner" headers
    for table in soup.select("table.wikitable"):
        headers = [th.get_text(strip=True).lower() for th in table.select("th")]
        if "year" in headers and "winner" in headers:
            return table
    # fallback: look for table after headings mentioning "Main Event"
    for header in soup.select("h2, h3"):
        text = header.get_text(strip=True).lower()
        if "main event" in text or "champions" in text:
            tbl = header.find_next_sibling("table")
            if tbl and "wikitable" in (tbl.get("class") or []):
                return tbl
    return None

def parse_table(table):
    rows = table.find_all("tr")
    if not rows:
        return []
    header_cells = [th.get_text(strip=True).lower() for th in rows[0].find_all("th")]
    def idx(name):
        try:
            return header_cells.index(name)
        except ValueError:
            return None
    i_year = idx("year")
    i_winner = idx("winner")
    i_prize = None
    for candidate in ("first place prize", "first place", "prize", "winning prize"):
        i = idx(candidate)
        if i is not None:
            i_prize = i
            break

    parsed = []
    for tr in rows[1:]:
        cols = [cell.get_text(strip=True) for cell in tr.find_all(["td","th"])]
        if not cols:
            continue
        year = cols[i_year] if i_year is not None and i_year < len(cols) else ""
        winner = cols[i_winner] if i_winner is not None and i_winner < len(cols) else ""
        prize = cols[i_prize] if i_prize is not None and i_prize < len(cols) else ""
        parsed.append((year, winner, prize))
    return parsed

def scrape():
    try:
        resp = requests.get(URL, headers=HEADERS, timeout=20)
        resp.raise_for_status()
    except Exception as e:
        print(f"Request failed: {e}", file=sys.stderr)
        return

    soup = BeautifulSoup(resp.text, "html.parser")
    table = find_winners_table(soup)
    if table is None:
        print("Could not find a suitable winners table on the page.", file=sys.stderr)
        return

    data = parse_table(table)
    if not data:
        print("No rows parsed from the table.", file=sys.stderr)
        return

    for year, winner, prize in data:
        out = f"{year}  Winner: {winner}"
        if prize:
            out += f"  First prize: {prize}"
        print(out)

if __name__ == "__main__":
    scrape()
