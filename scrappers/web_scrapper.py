import requests
from paths import data

class WebScraper():
    def __init__(self):
        self.ksh_file = data / "CBK.gov.html"
        self.eth_file = data / "NBE.gov.html"
        self.ksh_link = "https://www.centralbank.go.ke/bills-bonds/treasury-bills/"
        self.eth_link = "https://nbe.gov.et/treasury-bills/"
    
    def run(self):
        if self.eth_file.exists():
          print(f"File already exist at {self.eth_file}")
          print("==="*50)
          answer = input("Do you want to overwrite(y/N)?: ").strip().lower()
          if answer == "y":
            self.eth_scrape()
          else:
             print(f"Keeping existing {self.eth_file}")
        else:
          self.eth_scrape()
       
        if self.ksh_file.exists():
           print(f"File already exist at {self.ksh_file}")
           print("==="*50)
           answer = input("Do you want to overwrite(y/N)?: ").strip().lower()
           if answer == "y":
             self.ksh_scrape()
           else:
             print(f"Keeping existing {self.ksh_file}")
        else:
          self.ksh_scrape()



    def ksh_scrape(self):
        with open(self.ksh_file, "w") as file:
            response = requests.get(self.ksh_link, timeout=100)
            response.raise_for_status()
            file.write(response.text)
            print(f"Saved file to {self.ksh_file}")

    def eth_scrape(self):
        with open(self.eth_file, "w") as file:
            response = requests.get(self.eth_link, timeout=100)
            response.raise_for_status()
            file.write(response.text)
            print(f"Saved file to {self.eth_file}")



