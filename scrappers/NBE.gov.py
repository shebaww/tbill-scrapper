from bs4 import BeautifulSoup
import time
import csv
import requests



def main():
## Only call if you want current HTML file to be re-written okay bro? 
   # scrape()



def scrape():
    with open("../data/NBE.gov.html", "w") as file:
        response = requests.get("https://nbe.gov.et/treasury-bills/")
        file.write(response.text)
        soup = BeautifulSoup(response.text, "lxml")



if __name__ == "__main__":
  main()
