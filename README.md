# East African Treasury Bill Data Scraper

A Python command line tool designed to automate the collection, installation and merging of Treasury Bill (T-Bill) data from the **Central Bank of Kenya (CBK)** and the **National Bank of Ethiopia (NBE)**

---

## Features

- Scrapes HTML Pages from both CBK and NBE
- Automatically Extracts and downloads targeted kenyan T-Bill PDF Files
- Parses Ethiopian and Kenyan Financial data
- Combines cleaned datasets into their own CSV files and a merged master.csv for research and analysis
- Built a CLI using 'argparse' for easy command line control

---

## Project Structure

- 'data': Directory used to store finished CSV files and scraped html files
- 'data/kenya-pdfs': Stores all the scraped kenya Tbill PDF files
- 'project.py': Main Script
- 'parsers/eth_methods': Holds majority of the classes for parsing html file
- 'parsers/ksh_methods': Holds majority of the classes for parsing pdf file
- 'parsers/modules.py': Holds the classes required to parse files
- 'requirements.txt': Holds all library used
- '\*/paths.py': Holds all the file paths needed
- 'scrapers/pdf_scrapper.py': 'Scrapes all PDF files'
- 'scrapers/web_scrapper.py': Scrapes all the HTML files necessary
- 'test_project.py': Unit test for project.py

---

## Installation and Setup

1. Clone the Repo:

```bash
git clone https://github.com/shebaww/tbill-scrapper.git

```

2. Create and Activate Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate # On windows use: .venv\Scripts\activate
```

3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Usage

Run the project script with python. To view all the option and built in commands use the help flag

```bash
python project.py --help
```

---

## Example Commands

- Scrape and parse Kenyan T-Bills for 2024:

```bash
python project.py --kenya --years 2024
```

Important Note on --years & Local Data

The --years option controls which files are filtered and processed. If you have older or different year PDF files stored in your data/ directory, they may still be referenced during parsing. If you want a clean run with only specific years, clear out the data/ directory before executing your command.

Note on AI assistance: I used an AI assistant to help with some pandas DataFrame manipulation and debugging. The project structure, scraping logic, and parsing code are my own.
