import requests
from scrapers.paths import data, eth_file, ksh_file

class WebScraper():
    def __init__(self):
        self.ksh_link = "https://www.centralbank.go.ke/bills-bonds/treasury-bills/"
        self.eth_link = "https://nbe.gov.et/treasury-bills/"
    
    def run(self):
        print("Installing Pages....")
        if eth_file.exists():
          print(f"File already exist at {eth_file}")
          print("-"*60)
          answer = input("Overwrite(y/N)?: ").strip().lower()
          if answer == "y":
            self.eth_scrape()
          else:
             print(f"Keeping existing {eth_file}")
        else:
          self.eth_scrape()
       
        if ksh_file.exists():
           print(f"File already exist at {ksh_file}")
           print("-"*60)
           answer = input("Overwrite(y/N)?: ").strip().lower()
           if answer == "y":
             self.ksh_scrape()
           else:
             print(f"Keeping existing {ksh_file}")
        else:
          self.ksh_scrape()



    def ksh_scrape(self):
        with open(ksh_file, "w") as file:
            response = requests.get(self.ksh_link, timeout=100)
            response.raise_for_status()
            file.write(response.text)
            print(f"Saved file to {ksh_file}")

    def eth_scrape(self):
        with open(eth_file, "w") as file:
            response = requests.get(self.eth_link, timeout=100)
            response.raise_for_status()
            file.write(response.text)
            print(f"Saved file to {eth_file}")



