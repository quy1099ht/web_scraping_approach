# My Approach to the Assignment

## Timeline

1. My first approach was using BeautifulSoup for trying to get all the data loaded from the website.
2. By trying to get data from a few html tags such as ul, div to get things like currencies and the first exchange value.

```py
import requests
from bs4 import BeautifulSoup

url = "https://www.bullionstar.com/charts/gold-price-today"

response = requests.get(url)
if response.status_code == 200:
    html_content = response.text
else:
    print("Failed to fetch webpage")
soup = BeautifulSoup(html_content, 'html.parser')

ul_element = soup.find('ul', class_='currency-dropdown')

if ul_element and 'hide' in ul_element.get('class', []):
    print("Found hidden <ul> element with class 'currency-dropdown'")
else:
    print("Unable to find hidden <ul> element with class 'currency-dropdown'")
```

- This block of code up here was because I wanted to see was it possible for me to get the select box and click it.
- It was not possible since all the data in soup was kinda static.

3. So I changed my approach to Selenium.
4. Since it was possible to click butons and other things with Selenium already so I just wanted to find out how to get the chart data.
5. Once again it was not quite possible in my knowledges to know how to get the chart data because I need to locate the function that run render new chart data. I didn't know how.
6. In the end, I went back for the last solution. As a web developer, It's my instinct to look at the network and I realise I can just use the APIs instead.
7. That was the end of it. I wasn't sure which way of the excel or xml files should be presented so I did for both.

## Conclusion
- It took me a while to get a bit familiar with BeautifulSoup but I was also a bit sad that I could not use it alone to get the job done.
- Overral, The data set seem normal to me. Under the eyes of an engineer, I only see them as number and data that I can convert to csv. Nothing more nothing less.
- I'm pretty bad with economic stuffs so when I looked at the data and such. I had no idea what is going on.

## Installation
### Instal libraries
```sh
pip install requests pandas csv openpyxl
```

### Run the files
- Export CSV:
```sh
python .\scrape.py
```
- Export to Excels
```sh
python .\scrape_to_excels.py
```
