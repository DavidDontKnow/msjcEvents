from bs4 import BeautifulSoup
import pandas as pd
from playwright.sync_api import sync_playwright

data = []

with sync_playwright() as p:
    url = "https://calendar.msjc.edu/?view=list2&search=y"
    print("Opening browser...")
    browser = p.chromium.launch()
    page = browser.new_page()
    print("Going to URL...")
    page.goto(url)
    print("Getting content...")
    page.is_visible('article.list-event')
    page.wait_for_timeout(5000)
    html = page.inner_html('#main-content')

    soup = BeautifulSoup(html, 'html.parser')
    
    all_events = soup.find_all("article", class_="list-event")

    for event in all_events:
        item = {}
        item['Title'] = event.find('a').text
        item['Link'] = event.find('a').attrs['href']
        dateTime = event.find('p').text.strip()
        ## remove all white spaces
        dateTime = " ".join(dateTime.split())
        item['DateTime'] = dateTime
        item['Date'] = dateTime.split(" ")[0]
        item['Time'] = dateTime.split(" ")[1:3]

        try:
            item['Image'] = event.find('img').attrs['src']
        except:
            item['Image'] = ""

        data.append(item)
        
    
    print("Closing browser...")


print("Writing to Excel...")

df = pd.DataFrame(data)
df.to_json('msjc_events.json')
df.to_excel('msjc_events.xlsx', index=False)
print("Done")