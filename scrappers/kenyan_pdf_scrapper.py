from bs4 import BeautifulSoup
import time
import requests
import re


def main():
## Only call if you want re-install every pdf file of the kenyan treasury bills ok bro?
#   url364, url182, url91 = scrape()
#   install_pdfs(url364, url182, url91)



def scrape():
    with open("../data/CBK.gov.html") as file:
        content  = file.read()
        soup = BeautifulSoup(content, "lxml")
        
        links = soup.find_all("a", href=True)
        valid_links_364 = []
        valid_links_182 = []
        valid_links_91 = []
        for link in links:
          pattern_364 = r"^.*/364_day_historical_treasury_bill_results/.*(2024|2025|2026)+\.pdf"
          pattern_182 = r"^.*/182_day_historical_treasury_bill_results/.*(2024|2025|2026)+\.pdf"
          pattern_91 = r"^.*/91_day_historical_treasury_bill_results/.*(2024|2025|2026)+\.pdf"
          if link["href"].endswith(".pdf"):
            url = link["href"]
            if re.match(pattern_364, url, re.I):
              valid_links_364.append(url)

            if re.match(pattern_182, url, re.I):
              valid_links_182.append(url)

            if re.match(pattern_91, url, re.I):
              valid_links_91.append(url)

    return valid_links_364, valid_links_182, valid_links_91

def install_pdfs(url364, url182, url91):
    for link in url364:                      
      link_name = link.replace("/", "-")
      with open(f"../data/kenya-pdfs/364/{link_name}", "wb") as file:
         content = requests.get(f"https://www.centralbank.go.ke{link}")
         file.write(content.content)

    for link in url182:
      link_name = link.replace("/", "-")
      time.sleep(1)
      with open(f"../data/kenya-pdfs/182/{link_name}", "wb") as file:
         content = requests.get(f"https://www.centralbank.go.ke{link}")
         file.write(content.content)

    for link in url91:
      link_name = link.replace("/", "-")
      time.sleep(1)
      with open(f"../data/kenya-pdfs/91/{link_name}", "wb") as file:
         content = requests.get(f"https://www.centralbank.go.ke{link}")
         file.write(content.content)



    




if __name__ == "__main__":
  main()
