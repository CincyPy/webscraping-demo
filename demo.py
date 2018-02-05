"""
demo.py - a web scraping demo using Beautiful Soup and Requests
by Brian Sauer for CincyPy
"""

import requests
from bs4 import BeautifulSoup
import datetime

class KenoDrawing(object):
    """KenoDrawing: a class to hold a specific Keno drawings"""
    def __init__(self, date, ID, numbers, booster):
        """
        KenoDrawing.__init__(): sets values representing a Keno Drawing
        Params:
        - date (datetime) : a datetime representing the time of the drawing
        - ID (string) : the Keno drawing number
        - numbers (list) : a list of ints for the keno draw
        - booster (int) : the Keno booster value
        Returns:
        - Nothing
        """
        self.date = date
        self.ID = ID
        self.numbers = numbers
        self.booster = booster

    def __str__(self):
        """
        KenoDrawing.__str__(): returns a string representation of a KenoDrawing class
        Params:
        - Nothing
        Returns: 
        - (string) : the string representation of this object
        """
        return "{} ==> {} : {}".format(self.ID, self.numbers, self.booster)


def get_html(url):
    """
    get_html() : fetches HTML from a URL using the requests library
    Params:
    - url (string) : url to pull from
    Returns:
    - (string) : the HTML from the page
    """
    response = requests.get(url)
    return response.text

def get_drawings(year, month, day):
    """
    get_drawings() : scrapes paginated tables to get a day's Keno drawings
    Params:
    - year (int) : the year for the drawing
    - month (int) : the month for the drawing
    - day (int) : the day for the drawing
    Returns:
    - (list) : a list of KenoDrawing objects
    """
    drawings = []
    id_set = set()
    page = 1
    done = False
    while not done:
        #fetch HTML
        html = get_html("https://www.ohiolottery.com/WinningNumbers/KenoDrawings/KenoDrawingsArchive?date={}/{}/{}&page={}".format(month, day, year, page))
        #get a soup object for the HTML
        soup = BeautifulSoup(html, "html.parser")
        #find a table with a css class of keno_drawings
        table_soup = soup.find("table", class_="keno_drawings")
        #from the table, look for all of the tr elements inside the child tbody tag
        trs = table_soup.tbody.find_all("tr")
        for tr in trs:
            #for each row, find all the td tags in that row
            tds = tr.find_all("td")
            #if the row doesn't have 22 td's, its a header row, so skip
            if len(tds) != 22:
                print("Skipping: row has only " + str(len(tr.contents)) + " children.")
            else:
                #build a KenoDrawing object and store
                date = datetime.datetime(year,month,day)
                ID = tds[0].string
                numbers = [tds[x].string for x in range(1,21)]
                booster = tds[21].string
                #have we seen this drawing ID before? if not, add, otherwise break
                if ID not in id_set:
                    id_set.add(ID)
                    drawings.append(KenoDrawing(date, ID, numbers, booster))
                else:
                    print("ID {} already set, breaking on page {}.".format(ID,page))
                    done = True #set while loop to break next go around
                    break #break for loop
        page+=1
        
    return drawings
                
if __name__ == "__main__":
    drawings = get_drawings(2018,2,1)
    print("Successfully scraped {} drawings.".format(len(drawings)))
    print("Done")
