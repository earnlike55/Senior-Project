from calendar import c
import os
import pandas as pd
from constants import PL_FILE, PL_FILE_SEASON, SCRAPER_TIMEOUT, SCRAPER_SLEEP, OVA_FILE_PATH
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import datetime


def scrape_premier_season(from_year, to_year, csv_path,target_path):

    
    now = datetime.datetime.now().date()
        
    
    if not os.path.exists(csv_path):
        os.makedirs(csv_path)

    # Start scraping.
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get("https://fixturedownload.com/results/epl-{year}".format(year = from_year))

    # try:
    #     WebDriverWait(browser, SCRAPER_TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//a[contains(@class, 'bp3-button bp3-minimal text dropdown-toggle')]")))
    # except TimeoutException:
    #     print("Timed out waiting for page to load")
    #     browser.quit()

    # Clicks
    for year in range(from_year, to_year + 1):
        try:
            filePath = "{}/{}-{}.csv".format(csv_path, year, year + 1)
            target = "{}/{}-{}.csv".format(target_path,year,year+1)
            if os.path.exists(filePath) and year < to_year - 1:
                # Skip if file already exists and does not need to be updated
                continue
            # fifa_version = str(format((year % 2000 + 1), '02d'))

            # show_list_button = browser.find_element_by_xpath("//a[contains(@class, 'bp3-button bp3-minimal text dropdown-toggle')]")
            # show_list_button.click()
            # time.sleep(SCRAPER_SLEEP)

            # fifa_year_button = browser.find_element_by_xpath("//a[contains(text(), 'FIFA " + fifa_version + "')]")
            # fifa_year_button.click()
            # time.sleep(SCRAPER_SLEEP)

            # Collect the data we need
            # name_elements = browser.find_elements_by_xpath("//tbody/tr/td[2]/a/div")
            

            round_elements = browser.find_elements_by_xpath("//tbody/tr/td[1]")  
            date_elements = browser.find_elements_by_xpath("//tbody/tr/td[2]")    
            home_elements = browser.find_elements_by_xpath("//tbody/tr/td[4]")
            away_elements = browser.find_elements_by_xpath("//tbody/tr/td[5]")
            score_elements = browser.find_elements_by_xpath("//tbody/tr/td[6]")
            
            
            # def_elements = browser.find_elements_by_xpath("//tbody/tr/td[6]/span")
            # titles = [x.text for x in name_elements[::2]]
            homes = [x.text for x in home_elements]
            aways = [x.text for x in away_elements]
            scores = [x.text for x in score_elements]
            dates = [x.text for x in date_elements]
            rounds = [x.text for x in round_elements]

            homess = []
            awayss = []
            times = []
            div = []
            matchdays = []

            now = ""
            round = 0
            now = datetime.datetime.now().date()
            print(len(dates))
            for dayy in range(len(dates)):
                datess = dates[dayy]
                d = datess.split("/")
                    
                days = int(d[0])
                months = int(d[1])
                y = d[2].split(" ")
                years = int(y[0])
                
                margin = datetime.timedelta(days = 6)
                check = now - margin <= datetime.date(years, months, days) <= now + margin
                if check == True:
                    round = rounds[dayy]
                    break
            print(round)

            for count in range(len(homes)):
                if rounds[count] == round:
                    if scores[count] == "-":
                        fixture = dates[count]
                        
                        d = fixture.split("/")
                    
                        days = int(d[0])
                        months = int(d[1])
                        y = d[2].split(" ")
                        years = int(y[0])
                        matchday = fixture.split(" ")
                        
                        homess.append(homes[count])
                        awayss.append(aways[count])
                        matchdays.append(matchday[0])
                        times.append(matchday[1])
                        div.append("E0")

            # homesss = [x.text for x in homess]
            # awaysss = [x.text for x in awayss]  
                 
                    
                    

                    
    
            print()
            print("Data for ", year)
            print("Titles    |     OVA    ")
            for title, OVA in zip( homess, awayss ):
                print(title, "   ", OVA, "   ")

            # Data to csv
            df = pd.DataFrame.from_records(zip(div,matchdays,times,homess,awayss), columns=["Div","Date","Time","Home", "Away"])
            df.set_index('Div', inplace=True)
            df.to_csv(filePath)
            df.to_csv(target,mode = 'a', header=False)
            print(f'Scraping OVA for year {year} completed')
        except Exception as e:
            print(f'Failed to scrape OVA for year {year}')
            print(e)


def scrape_premier_entire_season(from_year, to_year, csv_path,target_path):

    
    now = datetime.datetime.now().date()
        
    
    if not os.path.exists(csv_path):
        os.makedirs(csv_path)

    # Start scraping.
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get("https://fixturedownload.com/results/epl-{year}".format(year = from_year))

    # try:
    #     WebDriverWait(browser, SCRAPER_TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//a[contains(@class, 'bp3-button bp3-minimal text dropdown-toggle')]")))
    # except TimeoutException:
    #     print("Timed out waiting for page to load")
    #     browser.quit()

    # Clicks
    for year in range(from_year, to_year + 1):
        try:
            filePath = "{}/{}-{}.csv".format(csv_path, year, year + 1)
            target = "{}/{}-{}.csv".format(target_path,year,year+1)
            if os.path.exists(filePath) and year < to_year - 1:
                # Skip if file already exists and does not need to be updated
                continue
            # fifa_version = str(format((year % 2000 + 1), '02d'))

            # show_list_button = browser.find_element_by_xpath("//a[contains(@class, 'bp3-button bp3-minimal text dropdown-toggle')]")
            # show_list_button.click()
            # time.sleep(SCRAPER_SLEEP)

            # fifa_year_button = browser.find_element_by_xpath("//a[contains(text(), 'FIFA " + fifa_version + "')]")
            # fifa_year_button.click()
            # time.sleep(SCRAPER_SLEEP)

            # Collect the data we need
            # name_elements = browser.find_elements_by_xpath("//tbody/tr/td[2]/a/div")
            

            round_elements = browser.find_elements_by_xpath("//tbody/tr/td[1]")  
            date_elements = browser.find_elements_by_xpath("//tbody/tr/td[2]")    
            home_elements = browser.find_elements_by_xpath("//tbody/tr/td[4]")
            away_elements = browser.find_elements_by_xpath("//tbody/tr/td[5]")
            score_elements = browser.find_elements_by_xpath("//tbody/tr/td[6]")
            
            
            # def_elements = browser.find_elements_by_xpath("//tbody/tr/td[6]/span")
            # titles = [x.text for x in name_elements[::2]]
            homes = [x.text for x in home_elements]
            aways = [x.text for x in away_elements]
            scores = [x.text for x in score_elements]
            dates = [x.text for x in date_elements]
            rounds = [x.text for x in round_elements]

            homess = []
            awayss = []
            times = []
            div = []
            matchdays = []

            now = ""
            round = 0
            now = datetime.datetime.now().date()
            print(len(dates))
            for dayy in range(len(dates)):
                datess = dates[dayy]
                d = datess.split("/")
                    
                days = int(d[0])
                months = int(d[1])
                y = d[2].split(" ")
                years = int(y[0])
                
                margin = datetime.timedelta(days = 6)
                check = now - margin <= datetime.date(years, months, days) <= now + margin
                if check == True:
                    round = rounds[dayy]
                    break
            print(round)

            for count in range(len(homes)):
                if rounds[count] >= round:
                    if scores[count] == "-":
                        
                        fixture = dates[count]
                        
                        d = fixture.split("/")
                    
                        days = d[0]
                        months = d[1]
                        y = d[2].split(" ")
                        years = y[0]
                        myTuple = (months,days,years)
                        # matchh = months+"/"+days+"/"+years
                        matchh = "/".join(myTuple)
                        matchday = fixture.split(" ")
                        if (homes[count] == "Man Utd") and (aways[count] == "Spurs"):
                            homess.append("Man United")
                            awayss.append("Tottenham")
                            matchdays.append(matchday[0])
                            times.append(matchday[1])
                            div.append("E0")
                        elif (homes[count] == "Spurs") and (aways[count] == "Man Utd"):
                            homess.append("Tottenham")
                            awayss.append("Man United")
                            matchdays.append(matchday[0])
                            times.append(matchday[1])
                            div.append("E0")
                        elif homes[count]  == "Man Utd":
                            homess.append("Man United")
                            awayss.append(aways[count])
                            matchdays.append(matchday[0])
                            times.append(matchday[1])
                            div.append("E0")
                        elif aways[count] == "Man Utd":
                            homess.append(homes[count])
                            awayss.append("Man United")
                            matchdays.append(matchday[0])
                            times.append(matchday[1])
                            div.append("E0")
                        elif aways[count] == "Spurs":
                            homess.append(homes[count])
                            awayss.append("Tottenham")
                            matchdays.append(matchday[0])
                            times.append(matchday[1])
                            div.append("E0")
                        elif homes[count] == "Spurs":
                            awayss.append(aways[count])
                            homess.append("Tottenham")
                            matchdays.append(matchday[0])
                            times.append(matchday[1])
                            div.append("E0")
                        else:    
                            homess.append(homes[count])
                            awayss.append(aways[count])
                            matchdays.append(matchday[0])
                            times.append(matchday[1])
                            div.append("E0")
                        

            # homesss = [x.text for x in homess]
            # awaysss = [x.text for x in awayss]  
                 
                    
                    

                    
    
            print()
            print("Data for ", year)
            print("Titles    |     OVA    ")
            for title, OVA in zip( homess, awayss ):
                print(title, "   ", OVA, "   ")

            # Data to csv
            df = pd.DataFrame.from_records(zip(div,matchdays,times,homess,awayss), columns=["Div","Date","Time","Home", "Away"])
            df.set_index('Div', inplace=True)
            df.to_csv(filePath)
            df.to_csv(target,mode = 'a', header=False)
            print(f'Scraping OVA for year {year} completed')
        except Exception as e:
            print(f'Failed to scrape OVA for year {year}')
            print(e)

def convert_team_name(name):
    name_list = ['Man Utd']
    name_change_map = {
        'Bournemouth': 'AFC Bournemouth',
        'Birmingham': 'Birmingham City',
        'Blackburn': 'Blackburn Rovers',
        'Bolton': 'Bolton Wanderers',
        'Brighton': 'Brighton & Hove Albion',
        'Cardiff': 'Cardiff City',
        'Charlton': 'Charlton Athletic',
        'Derby': 'Derby County',
        'Huddersfield': 'Huddersfield Town',
        'Hull': 'Hull City',
        'Leeds': 'Leeds United',
        'Leicester': 'Leicester City',
        'Man City': 'Manchester City',
        'Man United': 'Manchester United',
        'Newcastle': 'Newcastle United',
        'Norwich': 'Norwich City',
        'QPR': 'Queens Park Rangers',
        'Stoke': 'Stoke City',
        'Swansea': 'Swansea City',
        'Tottenham': 'Tottenham Hotspur',
        'West Brom': 'West Bromwich Albion',
        'West Ham': 'West Ham United',
        'Wigan': 'Wigan Athletic',
        'Wolves': 'Wolverhampton Wanderers'
    }
    return name_change_map[name] if name in name_change_map else name

if __name__ == "__main__":
    scrape_premier_entire_season(2021, 2021,PL_FILE_SEASON)