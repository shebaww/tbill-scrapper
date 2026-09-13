from scrapers import web_scrapper, pdf_scrapper
from parsers import modules
import argparse

# Visual ASCII Art Banner
BANNER = r"""
 ____                             _               _____          _     _ _ _     
/ ___|  ___ _ __ __ _ _ __  _ __ (_)_ __   __ _  |_   _|        | |__ (_) | |___ 
\___ \ / __| '__/ _` | '_ \| '_ \| | '_ \ / _` |   | |  |-----| | '_ \| | | / __|
 ___) | (__| | | (_| | |_) | |_) | | | | | (_| |   | |  |-----| | |_) | | | \__ \
|____/ \___|_|  \__,_| .__/| .__/|_|_| |_|\__, |   |_|          |_.__/|_|_|_|___/
                     |_|   |_|            |___/                                                                                     
  East African Treasury Bill Data Scraper & Merger
======================================================================
"""


def main():
  print(BANNER)
  print("Tip: Run 'python project.py --help' to view available command options.\n")
  arger = argparse.ArgumentParser(description="Scrape and Merge East African Treasury Bill Data")
  arger.add_argument("--merge", action="store_true", help="Merge Kenya and Ethiopia CSV's")
  arger.add_argument("-r","--run", action="store_true", help="Scrape HTML files from Central Bank of Kenya and National Bank of Ethiopia")
  arger.add_argument("-p","--pdfs",action="store_true", help="Download Kenyan Treasury Bill PDF's")
  arger.add_argument("--ethiopia", action="store_true", help="Parse Ethiopian T-Bills" )
  arger.add_argument("--kenya",action="store_true", help="Parse Kenyan T-Bills" )
  arger.add_argument("--years", nargs="+", type=int, default=[2024, 2025, 2026],
                help="Which years to scrape/install (default: 2024 2025 2026) \n CAUTION: THIS OPTION ONLY INSTALLS FILES. IF YOU HAVE DIFFERENT YEAR PDF FILES IN 'data' THEY WILL BE USED AND PARSED. IF YOU DON'T WANT THEM USED DELETE EVERYTHING IN 'data' AND RE-INSTALL THE YEAR PDF FILES YOU ONLY WANT USED AND PARSED")

  global args
  args = arger.parse_args()
  years = args.years
  if args.run:
    run_webscraper()
  if args.ethiopia:
    run_ethiopia()
  if args.kenya or args.merge:
    run_merge(years)
  if args.kenya:
    run_kenya(years)
  if args.merge:
    run_merge(years)


WebScraper = web_scrapper.WebScraper()
Parser = modules.Parser()

def run_webscraper():
    WebScraper.run()

def run_ethiopia():
    Parser.ethiopia()

def run_kenya(years):
    PdfScraper = pdf_scrapper.PdfScraper(years=years)
    PdfScraper.run()
    Parser.kenya()

def run_merge(years):
    PdfScraper = pdf_scrapper.PdfScraper(years=years)
    PdfScraper.run()
    Parser.merge()
  
if __name__ == "__main__":
  main()
