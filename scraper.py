from bs4 import BeautifulSoup
import pandas as pd
from playwright.sync_api import sync_playwright
import datetime
data = []

with sync_playwright() as p:
    url = "https://calendar.msjc.edu/?view=list&search=y"
    print("Opening browser...")
    browser = p.chromium.launch()
    page = browser.new_page()
    print("Going to URL...")
    page.goto(url)
    print("Attempting to get all events...")

    #Running this makes it select for the next 365 days
    #Too bad we have to click on the second page though
    page.evaluate("javascript:__doPostBack('ctl01$ctl00$ctl00$publicBody$siteBody$UCEventSearch$ViewBy$lbtnNext365','')")
    
    print("Waiting for events...")

    #Waits until events are on the page
    page.wait_for_selector(".adx-rendering section")
    """
    This is the same as selecting:

        <div class="adx-rendering">
            <section> </section>
        </div>

    """
    print("Getting content...")
    html = page.inner_html('#main-content')

    soup = BeautifulSoup(html, 'html.parser')
    
    #Get the index of all the events
    all_events = soup.find("div", class_="adx-rendering")

    print("Parsing data...")
    for event in all_events.children:
        #Each event is surrounded by a 'section' tag, we can identify each one by its class
        ImageSec = event.find("section", class_="list-event-image")
        PreviewSec = event.find("section", class_="list-event-preview")
        DateLocationSec = PreviewSec.find("section", class_="list-event-when-where")
        
        #May not have an end time
        DateSec = DateLocationSec.find("section","list-event-date")
        
        #May not have children
        LocaleSec = DateLocationSec.find("section","list-event-locale")

        
        item = {}

        ############# Preview Section #############

        item['Title'] = PreviewSec.find('a').text
        item['Link'] = PreviewSec.find('a').attrs['href']

        ############# Date and Location Section #############

        #If there is an end time present, the list length will be 2. If there is only a start time, it will have a length of 1
        timeInfo = DateSec.find_all("time")

        startTime = timeInfo[0]
        startDateTime = startTime["datetime"]
        
        #I hate this
        #Time is in ISO format
        startDateTime = datetime.datetime.fromisoformat(startDateTime.replace("Z", "+00:00"))

        #Convert to PST
        startDateTime = startDateTime.astimezone()

        #Format the time again
        correctStartTime = f"{startDateTime.year}-{startDateTime.month}-{startDateTime.day}T{startDateTime.hour}:{"0" + str(startDateTime.minute) if startDateTime.minute < 10 else startDateTime.minute}:{"0" + str(startDateTime.second) if startDateTime.second < 10 else startDateTime.second}"
        
        item['StartDateTime'] = correctStartTime

        #T seperates the date from the time
        temp = correctStartTime.split("T")
        item['StartDate'] = temp[0]
        item['StartTime'] = temp[1]

        if len(timeInfo) == 2:
            #Has end time
            #We do the same thing
            endTime = timeInfo[1]
            endDateTime = endTime["datetime"]

            endDateTime = datetime.datetime.fromisoformat(endDateTime.replace("Z", "+00:00")).astimezone()
            correctEndTime = f"{endDateTime.year}-{endDateTime.month}-{endDateTime.day}T{endDateTime.hour}:{"0" + str(endDateTime.minute) if endDateTime.minute < 10 else endDateTime.minute}:{"0" + str(endDateTime.second) if endDateTime.second < 10 else endDateTime.second}"


            item['EndDateTime'] = correctEndTime            
            temp = correctEndTime.split("T")
            item['EndDate'] = temp[0]
            item['EndTime'] = temp[1]
        else:
            item['EndDateTime'] = ""
            item['EndDate'] = ""
            item['EndTime'] = ""
        

        ############# Location Section #############

        #Checking if the event has a location
        #For some reason, there is an empty string as a child
        if len(list(LocaleSec.children)) != 1:
            CampusRoom = LocaleSec.find("a").text
            item["CampusRoom"] = CampusRoom
            
            #It could just say "multiple locations" or zoom
            if CampusRoom != "Multiple Locations" and CampusRoom != "Zoom":
                
                #There may not be one of these

                #Address
                try:
                    item["Address"] = LocaleSec.find("span", itemprop="addressLocality").text
                except:
                    item["Address"] = ""

                #Street Address
                try:
                    item["streetAddress"] = LocaleSec.find("span", itemprop="streetAddress").text
                except:
                    item["streetAddress"] = ""
                
                
                #Zipcode
                try:
                    item["Zipcode"] = LocaleSec.find("span", itemprop="postalCode").text
                except:
                    item["Zipcode"] = ""
            else:
                item["Address"] = ""
                item["Zipcode"] = ""
                item["streetAddress"] = ""

        else:
            item["CampusRoom"] = ""
            item["Address"] = ""
            item["Zipcode"] = ""
            item["streetAddress"] = ""

        ############# Image Section #############
        try:
            item["Image"] = ImageSec.find("img")["src"]
        except:
            item["Image"] = ""
        data.append(item)
        
    
    print("Closing browser...")


print("Writing to Excel...")

df = pd.DataFrame(data)
df.to_json('msjc_events.json')
df.to_excel('msjc_events.xlsx', index=False)
print("Done")