import requests 
from bs4 import BeautifulSoup
import pandas as pd

url='https://www.soccerstats.com/homeaway.asp?league=ecuador'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

print(soup)