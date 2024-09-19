from bs4 import BeautifulSoup
import pandas as pd
from playwright.sync_api import sync_playwright

data = []

with sync_playwright() as p:
    url = "https://calendar.msjc.edu/?view=list2&search=y"
    print("Opening browser...")
    browser = p.chromium.launch(headless=False, slow_mo=100)
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
        item['DateTime'] = event.find('p').text.strip()
        data.append(item)
        
    
    print("Closing browser...")


print("Writing to Excel...")

df = pd.DataFrame(data)
df.to_json('msjc_events.json')
df.to_excel('msjc_events.xlsx', index=False)
print("Done")