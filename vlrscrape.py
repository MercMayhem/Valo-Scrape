from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import pandas as pd
import traceback

def table_scrape(table, name, map):
    soup = BeautifulSoup(table.get_attribute('innerHTML'), 'html.parser')
    rows = soup.find_all('tr')
    table_data = []
    agents_col = []

    for row in rows:
        cells = row.find_all(['td', 'th'])
        row_data = tuple(cell.get_text().strip() for cell in cells)
        table_data.append(row_data)

        spans = row.find_all('span', class_='mod-agent')
        agent = [img['title'] for img in [span.find('img') for span in spans]]
        agents_col.append(agent[0] if len(agent) != 0 else " ")

    df = pd.DataFrame(table_data[1:])
    df.columns = list(table_data[0])

    # Cleaning
    df.iloc[:, 0] = df.iloc[:, 0].str.split('\n').str[0]
    
    column_names = list(df.columns)
    column_names[0] = 'Player'
    column_names[1] = 'Agent'
    column_names[7] = 'KD +/-'
    column_names[-1] = 'FKFD +/-'
    df.columns = column_names

    df.D = df.D.str[3:-3]
    for col in [col for col in column_names if col not in ['Player', 'Agent']]:
        df[col+'_all'] = df[col].str.split('\n').str[0]
        df[col+'_attack'] = df[col].str.split('\n').str[1]
        df[col+'_defend'] = df[col].str.split('\n').str[2]

    df['Team'] = name
    df['Map'] = map
    if map != 'All Maps':
        df['Agent'] = agents_col[1:]
    else:
        df['Agent'] = '-'

    return df

def vlrscrape(link):
    driver = webdriver.Chrome()

    try:
        driver.get(link)

        driver.implicitly_wait(0.5)

        # Date of Match
        date = driver.find_element(By.CLASS_NAME, value='moment-tz-convert').get_attribute('data-utc-ts')

        # Teams
        teams = driver.find_elements(By.CLASS_NAME, value='wf-title-med')
        teams = [team.text for team in teams]

        # Winner
        winner = driver.find_elements(By.CLASS_NAME, value='match-bet-item-team')[1].text

        # Scoreline & Series type (bo3 / bo5)
        score = driver.find_element(By.CLASS_NAME, value='match-header-vs-score-winner').text + ':' + driver.find_element(By.CLASS_NAME, value='match-header-vs-score-loser').text
        series_type = driver.find_elements(By.CLASS_NAME, value='match-header-vs-note')[1].text

        # Stats Box and Maps
        stats_box = driver.find_element(By.CLASS_NAME, value='vm-stats')
        map_box = stats_box.find_elements(By.CLASS_NAME, value='vm-stats-gamesnav-item', )

        disabled_maps = stats_box.find_elements(By.CLASS_NAME, value='mod-disabled')
        for map in disabled_maps:
            map_box.remove(map)

        df_global = []

        for map in map_box:
            map.click()
            
            # Current map
            curr_map = map.text
            div = driver.find_element(By.CSS_SELECTOR, "div[style*='display: block;']")
            tables = div.find_elements(By.CLASS_NAME, value='wf-table-inset')

            # Team 1
            team1_table = tables[0]
            team1_name = teams[0]

            df_global.append(table_scrape(team1_table, team1_name, curr_map))

            # Team 2 Stats Table & Name
            team2_table = tables[1]
            team2_name = teams[1]

            df_global.append(table_scrape(team2_table, team2_name, curr_map))

        df_global = pd.concat(df_global, ignore_index=True, axis=0)
        df_global['Date'] = date
        df_global['VS'] = f'{teams[0]}\n{teams[1]}'
        df_global['Winner'] = winner
        df_global['Scoreline'] = score
        df_global['Series Type'] = series_type

        cols = df_global.columns.tolist()
        cols = cols[-5:] + [cols[-6]] + cols[0:-6]
        df_global = df_global[cols]

    except Exception as e:
        traceback.print_exc()
       

    finally:
        driver.quit()
        return df_global
