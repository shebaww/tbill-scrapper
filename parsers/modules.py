import pandas as pd
import pdfplumber
import os
import sys; from pathlib import Path
from parsers.paths import current_dir, root, data, parsers, kenya_pdfs, ETH_CSV, KSH_CSV, MASTER_CSV
from parsers import ksh_methods
from parsers import eth_methods


class Parser():
    def __init__(self):
        self.pdf_files = len([f for f in os.listdir(kenya_pdfs) if f.lower().endswith('.pdf')])
        self.Write = Write_tocsv()
        # For tests
        # self.pdf_files = ["backup/test.pdf", "backup/rtest.pdf"]

    def kenya(self):
        KPM = ksh_methods.KenyanParserMethods()
        KSH_CSV.unlink(missing_ok=True)
        print(f"Automatically Re-populating {KSH_CSV}")
        print("==="*20)
        for _ in range(self.pdf_files):
          df = KPM.process_single_pdf()
          self.Write.pdf(df)
        print(f"Completed Parsing and Writing Kenyan PDF Files")
        


    def ethiopia(self):
        EPM = eth_methods.EthiopianParserMethods()
        ETH_CSV.unlink(missing_ok=True)
        print(f"Automatically Re-populating {ETH_CSV}")
        print("==="*20)
        self.Write.html(EPM.scrape())
   
    def merge(self):
        if not os.path.exists(KSH_CSV):
            print(f"Missing {KSH_CSV}")
            answer = input("Would you want to repopulate it?(y/N): ").strip().lower()
            if answer == "y":
                self.kenya()
            else:
                raise FileNotFoundError(f"Please repopulate {KSH_CSV}")
        if not os.path.exists(ETH_CSV):
            print(f"Missing {ETH_CSV}")
            answer = input("Would you want to repopulate it?(y/N): ").strip().lower()
            if answer == "y":
                self.ethiopia()
            else:
                raise FileNotFoundError(f"Please repopulate {ETH_CSV}")
        df_eth = pd.read_csv(ETH_CSV)
        df_ksh = pd.read_csv(KSH_CSV)
        combined_df = pd.concat([df_eth, df_ksh], ignore_index=True)
        combined_df.to_csv(MASTER_CSV, index=False)
        print(f"Merged Files\nSaved to{MASTER_CSV}")

class Write_tocsv():
    def html(self, clean_table):
        eth_exists = os.path.exists(ETH_CSV)
        for df in clean_table:
          df.to_csv(
                    ETH_CSV,
                    index=False,
                    mode="a",
                    header=not eth_exists,
                    )
          eth_exists = True

    
    def pdf(self, df):
        ksh_exists = os.path.exists(KSH_CSV)
        df = pd.DataFrame(df)
        if df is None or df.empty:
          return
        df.to_csv(
            KSH_CSV, 
            mode='a',    
            index=False,    
            header=not ksh_exists 
        ) 
    




