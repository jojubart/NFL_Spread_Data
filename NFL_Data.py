from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import html5lib

# DATA FOR ONE YEAR FOR ONE TEAM
# URL with HTML table
url = "http://www.pro-football-reference.com/teams/nwe/2016_lines.htm"

html = urlopen(url)

soup = BeautifulSoup(html, "html5lib")

column_headers = [th.getText() for th in
                  soup.findAll('tr', limit=2)[0].findAll('th')]
column_headers = column_headers[1:]

print(column_headers)
data_rows = soup.findAll('tr')[1:]

team_data = [[td.getText() for td in data_rows[i].findAll('td')]
             for i in range(len(data_rows))]

df = pd.DataFrame(team_data, columns=column_headers)
df.index += 1
print(df.head())  # print first three rows

df.to_csv("NFL_Data_Scraped.csv")

# SCRAPING DATA FOR MANY YEARS
# we now have to do the process above several times and
# combine them into a large DataFrame
url_template = "http://www.pro-football-reference.com/teams/{team}/{year}_lines.htm"

# create an empty Dataframe
Spread_df = pd.DataFrame()

team_names = ['nwe', 'crd', 'ram', 'sfo', 'car', 'sea', 'dal', 'buf',
              'tam', 'den', 'atl', 'rai', 'chi', 'kan', 'sdg', 'jax',
              'clt', 'nor', 'oti', 'cle', 'mia', 'htx', 'min', 'det',
              'gnb', 'cin', 'nyj', 'pit', 'was', 'rav', 'phi', 'nyg']
team_names.sort()
print(team_names)
print(len(team_names))

for i in range(1, len(team_names)):
    team = team_names[i]
    print("Scraped team is ")
    print(team_names[i - 1])
    i += 1

    for year in range(1985, 2017):
        url = url_template.format(team=team, year=year)

        html = urlopen(url)  # get the html
        soup = BeautifulSoup(html, 'html5lib')  # create our BS object

        # get the player data
        data_rows = soup.findAll('tr')[1:]
        team_data = [[td.getText() for td in data_rows[i].findAll('td')]
                     for i in range(len(data_rows))]

        # turn yearly data into a dataframe
        year_df = pd.DataFrame(team_data, columns=column_headers)
        # create and insert Draft_yr column
        year_df.insert(0, 'Season', year)
        year_df.insert(0, 'Team', team)

        # start index at 1
        year_df.index += 1

        # Append to the big dataframe
        Spread_df = Spread_df.append(year_df, ignore_index=False)

print(Spread_df.head())
print(Spread_df.tail())

Spread_df.to_csv("NFL_data_1985_to_2016.csv")


