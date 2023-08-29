print ("hello world")

import bs4
import requests

def scrape_data(url):
    """Scrape data from the specified URL."""

    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content, "html.parser")

    return soup

if __name__ == "__main__":
    url = "https://palermo.viper.comcast.net/#ccvs/1c70a435-c32c-45ec-876d-0363314a8036"
    data = scrape_data(url)

    print(data)

