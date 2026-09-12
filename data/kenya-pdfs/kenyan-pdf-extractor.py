import os
import csv
import pdfplumber
import re
from pypdf import PdfReader
import pandas as pd

MASTER_CSV = "kenyan-tbills.csv"

def main():
  pdf_files = [f for f in os.listdir('.') if f.lower().endswith('.pdf')]
# For tests
# pdf_files = ["backup/test.pdf", "backup/rtest.pdf"]
  for pdf_file in pdf_files:
    process_single_pdf(pdf_file)
  print(f"Yes bro i have completed")


def process_single_pdf(filepath):
  try:
    print(f"Processing: {filepath}")
    table = grab_tables(filepath)
    issue_no = grab_issue_number(filepath)
    issue_date = grab_issue_date(filepath)

    write_tocsv(table, issue_no, issue_date)
  except Exception as e:
          print(f"  -> Error processing {Willfixerrorgivemeerrornamefirst}: {e}")


def grab_issue_number(filepath):
  reader = PdfReader(filepath)
  page = reader.pages[0]
  text = page.extract_text()
  pattern = r"bills issues (\d{4}/\d{3})+, (\d{4}/\d{3})+ & (\d{4}/\d{3})+.*dated"
  issue_no = []
  if i := re.search(pattern, text, re.I):
    issue_no.append(i.group(1))
    issue_no.append(i.group(2))
    issue_no.append(i.group(3))
    return issue_no

def grab_issue_date(filepath):
  reader = PdfReader(filepath)
  page = reader.pages[0]
  text = page.extract_text()
  pattern = r"dated (\d{2}/\d{2}/\d{4})+"
  issue_no = []
  if issue_date := re.search(pattern, text, re.I):
    return issue_date.group(1)

def grab_tables(filepath):
  with pdfplumber.open(filepath) as file:
    i = file.pages[0]
    mega_list =[]
    table = i.extract_tables()
    outcome_table = table[0]
    for rows in outcome_table:
      csv_row = []
      if "ISIN" in rows:
        continue
      for values in rows:
        csv_row.append(values)
      mega_list.append(csv_row)
  return mega_list

def write_tocsv(table, issue_no, issue_date):
  df = pd.DataFrame(table[1:], columns=table[0])
  df.columns = df.columns.str.strip()
  metric_col = df.columns[0]
  if not metric_col:
    df = df.rename(columns={metric_col:"Tenor"})
    metric_col = "Tenor"
  df = df.set_index(metric_col)
  df = df.T
  df = df.reset_index()
  df = df.rename(columns={df.columns[0]: "Tenor"})
  tenor_suffix = df["Tenor"].str.extract(r"(\d+)")[0].str.zfill(3)  
  issue_map = {"091": issue_no[0], "182": issue_no[1], "364": issue_no[2]}
  df = df[df['Tenor'] != "TOTAL"]
  df.columns = df.iloc[0]
  df = df[1:]
  df = df.rename(columns={df.columns[0]: "Tenor"})
  df["Issue Date"] = issue_date
  df["Issue Number"] = tenor_suffix.map(issue_map)
  df["Country"] = "Kenya"
  df["Currency"] = "Kshs"
  df = df.drop(
    columns=[
        "Performance Rate (%)",
        "Rollover / Redemptions",
        "Market Weighted Average Interest\nRate",
        "New Borrowing/Net Repayment",
        "Of which: Competitive bids",
        ": Non-competitive bids",
        "Purpose / Application of Funds:",
        "Bid-to-Cover Ratio",
    ]
)
  df["Issue Date"] = pd.to_datetime(df["Issue Date"], dayfirst=True, errors='coerce').dt.strftime('%Y-%m-%d')
  if "Due Date" in df.columns:
        df["Due Date"] = pd.to_datetime(df["Due Date"], dayfirst=True, errors='coerce').dt.strftime('%Y-%m-%d')
  df.columns = df.columns.str.replace(r'\n', ' ', regex=True).str.strip()
  
  cols_to_drop = ["Purpose / Application of Funds"]
  df = df.drop(columns=[col for col in cols_to_drop if col in df.columns], errors="ignore")

  for col in df.columns:
    if col not in ["Tenor", "Due Date", "Issue Number", "Issue Date", "Country", "Currency", ""]:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(r"[^\d.-]", "", regex=True),
            errors="coerce"
        )
  df = df.rename(columns={
                      df.columns[1]: "Maturity Date",
                      df.columns[2]: "Amount Offered (Millions)",
                      df.columns[3]: "Bids Received (Millions)",
                      df.columns[4]: "Total Amount Accepted (Millions)",
                      df.columns[5]: "Weighted Average Yield (Annual in %)",
                      df.columns[6]: "Weighted Average Price (Per 100)",
    })
  df = df.rename(columns={df.columns[0]: "Tenor"})
  file_exists = os.path.exists(MASTER_CSV)
    
  df.to_csv(
      MASTER_CSV, 
      mode='a',            
      index=False,          
      header=not file_exists 
  )

if __name__ == "__main__":
  main()
