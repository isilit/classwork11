import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pd

targetUrl = "https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&offer_type=flat&region=1&room1=1&room2=1"

requestHeaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
}

serverResponse = req.get(targetUrl, headers=requestHeaders)
print("Response status:", serverResponse.status_code)

def extractApartmentsData(htmlContent):
    parsedHtml = bs(htmlContent, 'html.parser')
    resultSet = []
    
    cardNodes = parsedHtml.find_all('article', {'data-name': 'CardComponent'})
    
    for node in cardNodes[:10]:
        try:
            titleNode = node.find('span', {'data-mark': 'OfferTitle'})
            flatTitle = titleNode.get_text(strip=True) if titleNode else "Apartment"
            
            addressNode = node.find('a', {'data-name': 'GeoLabel'})
            fullAddress = addressNode.get_text(strip=True) if addressNode else "No address"
            
            priceNode = node.find('span', {'data-mark': 'MainPrice'})
            rentPrice = priceNode.get_text(strip=True) if priceNode else "0"
            
            areaNode = node.find('span', string=lambda txt: txt and 'м²' in txt)
            squareMeters = areaNode.get_text(strip=True) if areaNode else "0 m²"
            
            resultSet.append({
                'PropertyType': flatTitle,
                'Location': fullAddress,
                'MonthlyRent': rentPrice,
                'TotalArea': squareMeters
            })
        except Exception:
            continue
    
    return resultSet

if serverResponse.status_code == 200:
    scrapedData = extractApartmentsData(serverResponse.text)
    
    if scrapedData:
        dataFrame = pd.DataFrame(scrapedData)
        print("\n" + "="*50)
        print(dataFrame)
        print("="*50)
    else:
        print("[!] Warning: No apartment data extracted")
else:
    print(f"[!] Request failed with code: {serverResponse.status_code}")