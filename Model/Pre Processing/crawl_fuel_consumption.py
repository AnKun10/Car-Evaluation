import time

import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

DELAY = 1


def convert_mpg_to_lkm(mpg):
    if not mpg:
        return 0
    return round(235.214583 / float(mpg), 1)


def select_by_tag_name(driver, val):
    search = Select(driver.find_element(By.TAG_NAME, 'select'))
    time.sleep(DELAY)
    search.select_by_visible_text(val)


def select_by_id(driver, element_id, val):
    search = Select(driver.find_element(By.ID, element_id))
    time.sleep(DELAY)
    search.select_by_value(val)


def click_by_class(driver, element_class):
    driver.find_element(By.ID, element_class).click()
    time.sleep(DELAY)


def click_by_id(driver, element_id):
    driver.find_element(By.ID, element_id).click()
    time.sleep(DELAY)


def click_by_link_text(driver, element_name):
    driver.find_element(By.LINK_TEXT, element_name).click()
    time.sleep(DELAY)


class Fuelly:
    def filter_data(self, data):
        # Filter 'year_of_manufacture'
        f = open("./dataset/year_produce.txt", 'r')
        tmp = 0
        for i, line in enumerate(f):
            if i % 2 == 0:
                tmp = int(line)
                continue
            data.loc[tmp, 'year_of_manufacture'] = np.float64(line)
        data['year_of_manufacture'] = np.array(data['year_of_manufacture'], dtype=np.int32)
        f.close()
        # Filter brand
        data['brand'] = data['brand'].astype(str)
        data['brand'] = data['brand'].str.replace('Mercedes Benz', 'Mercedes-Benz')
        data['brand'] = data['brand'].str.replace('Rolls Royce', 'Rolls-Royce')
        data['brand'] = data['brand'].str.replace('Aston Martin', 'Aston_Martin')
        # Filter grade
        data['grade'] = data['grade'].astype(str)
        data.loc[(data['grade'] == 'Super Carry Truck') | (data['grade'] == 'Super Carry Van'), 'grade'] = 'Super_Carry'
        data.loc[(data['grade'] == 'SantaFe'), 'grade'] = 'Santa_Fe'
        data.loc[(data['grade'] == 'CRV'), 'grade'] = 'CR-V'
        data.loc[(data['grade'] == 'HRV'), 'grade'] = 'HR-V'
        data.loc[(data['grade'] == 'CX3'), 'grade'] = 'CX-3'
        data.loc[(data['grade'] == 'CX5'), 'grade'] = 'CX-5'
        data.loc[(data['grade'] == 'CX7'), 'grade'] = 'CX-7'
        data.loc[(data['grade'] == 'CX8'), 'grade'] = 'CX-8'
        data.loc[(data['grade'] == 'CX9'), 'grade'] = 'CX-9'
        data.loc[(data['grade'] == 'CX30'), 'grade'] = 'CX-30'
        data.loc[(data['grade'] == 'Dmax'), 'grade'] = 'D-MAX'
        data.loc[(data['grade'] == 'X trail'), 'grade'] = 'X-Trail'

        for index, row in data.loc[(data['brand'] == 'Mercedes-Benz'), ['brand', 'grade', 'car_name']].iterrows():
            if row['grade'] not in ['AMG GT', 'CLA class', 'CLK class', 'CLS class', 'EQS', 'GL', 'GLA class', 'GLB',
                                    'GLC', 'GLE Class', 'GLS', 'MB', 'SL class', 'SLK class', 'Sprinter', 'Vito']:
                tmp = row['car_name'].split(' ' + row['grade'] + ' ')
                if len(tmp) <= 1:
                    continue
                data.loc[index, 'grade'] = row['car_name'].split(' ' + row['grade'] + ' ')[1].split()[0]
            if row['grade'] in ['CLA class', 'CLK class', 'CLS class', 'GL', 'GLA class', 'GLE Class', 'SLK class']:
                tmp = row['car_name'].split(' ' + row['grade'] + ' ')[1].split()
                data.loc[index, 'grade'] = tmp[0] + tmp[1]
            if row['grade'] in ['EQS', 'GLB', 'GLC', 'GLS']:
                data.loc[index, 'grade'] += row['car_name'].split(' ' + row['grade'] + ' ')[1].split()[0]

        for index, row in data.loc[(data['brand'] == 'Lexus'), ['brand', 'grade', 'car_name']].iterrows():
            if row['grade'] != 'IS':
                data.loc[index, 'grade'] += row['car_name'].split(' ' + row['grade'] + ' ')[1].split()[0]

        for index, row in data.loc[(data['brand'] == 'Porsche'), ['brand', 'grade', 'car_name']].iterrows():
            if row['grade'] == '718':
                data.loc[index, 'grade'] += ' ' + row['car_name'].split(' ' + row['grade'] + ' ')[1].split()[0]
        data['grade'] = data['grade'].str.replace(' ', '_')
        # Filter transmission
        data['transmission'] = data['transmission'].astype(str)
        data['transmission'] = data['transmission'].replace('-', np.nan)
        # Filter drive_type
        data['drive_type'] = data['drive_type'].astype(str)
        data['drive_type'] = data['drive_type'].replace('-', np.nan)
        # Filter engine & Create engine_capacity column
        data['engine'] = data['engine'].astype(str)
        data['engine'] = data['engine'].replace('-', np.nan)
        data[['engine', 'engine_capacity']] = data['engine'].str.split('\t').apply(pd.Series)
        # Filter num_of_doors
        data['num_of_doors'] = data['num_of_doors'].astype(str)
        data['num_of_doors'] = data['num_of_doors'].str.replace('-door', '')
        data['num_of_doors'] = data['num_of_doors'].replace('0', np.nan)
        # Filter seating_capacity
        data['seating_capacity'] = data['seating_capacity'].astype(str)
        data['seating_capacity'] = data['seating_capacity'].str.replace('-seat', '')
        data['seating_capacity'] = data['seating_capacity'].replace('0', np.nan)
        # Filter fuel_consumption
        data['fuel_consumption'] = data['fuel_consumption'].astype(str)
        data['fuel_consumption'] = data['fuel_consumption'].str.replace('.\tL/100Km', '')
        data['fuel_consumption'] = data['fuel_consumption'].str.replace(',\tL/100Km', '')
        data['fuel_consumption'] = data['fuel_consumption'].str.replace('\tL/100Km', '')
        data['fuel_consumption'] = data['fuel_consumption'].str.replace('l', '')
        data['fuel_consumption'] = data['fuel_consumption'].str.replace('L', '')
        data['fuel_consumption'] = data['fuel_consumption'].str.replace(' ', '')
        data.loc[(data['fuel_consumption'] == 'K0') | (data['fuel_consumption'] == '00') |
                 (data['fuel_consumption'] == '0') | (data['fuel_consumption'] == '') |
                 (data['fuel_consumption'] == '10000') | (data['fuel_consumption'] == '100000') |
                 (data['fuel_consumption'] == '200000') | (data['fuel_consumption'] == '65') |
                 (data['fuel_consumption'] == '66') | (data['fuel_consumption'] == '565') |
                 (data['fuel_consumption'] == '68') | (data['fuel_consumption'] == '100') |
                 (data['fuel_consumption'] == '55') | (data['fuel_consumption'] == '592') |
                 (data['fuel_consumption'] == '40') | (data['fuel_consumption'] == '89') |
                 (data['fuel_consumption'] == '83') | (data['fuel_consumption'] == '85') |
                 (data['fuel_consumption'] == '6500') | (data['fuel_consumption'] == '75') |
                 (data['fuel_consumption'] == '98') | (data['fuel_consumption'] == '225') |
                 (data['fuel_consumption'] == '4288') | (data['fuel_consumption'] == '111') |
                 (data['fuel_consumption'] == '58') | (data['fuel_consumption'] == '45') |
                 (data['fuel_consumption'] == '77') | (data['fuel_consumption'] == '42') |
                 (data['fuel_consumption'] == 'L/100Km') |
                 (data['fuel_consumption'] == '/100Km'), 'fuel_consumption'] = np.nan
        # Filter fuel_system
        data['fuel_system'] = np.nan
        return data

    def find_car_fuel_consumption(self, driver, brand, grade, year):
        driver.get("https://www.fuelly.com/car/" + brand.lower() + "/" + grade.lower())
        tables = driver.find_elements(By.CLASS_NAME, "model-year-summary")
        year_distance = 2000
        fuel_consumption = '0'
        for table in tables:
            tmp_distance = int(year) - int(table.find_element(By.CLASS_NAME, "summary-year").text)
            if abs(tmp_distance) <= abs(year_distance):
                year_distance = tmp_distance
                fuel_consumption = str(
                    convert_mpg_to_lkm(float(table.find_element(By.CLASS_NAME, "summary-avg-data").text)))
        return fuel_consumption


def crawl_Fuelly(data):
    # Crawl data
    options = Options()
    options.page_load_strategy = 'eager'
    options.experimental_options['prefs'] = {
        'profile.managed_default_content_settings.images': 2,
        'profile.managed_default_content_settings.javascript': 2
    }
    driver = webdriver.Chrome(options=options)
    website = Fuelly()
    data = website.filter_data(data)
    for i in range(len(data)):
        print("Iter " + str(i) + " ------ OLD: " + str(data.loc[i, 'fuel_consumption']) + " || ", end="")
        if pd.isnull(data.loc[i, 'fuel_consumption']) and data.loc[i, 'brand'] not in ['VinFast', 'Dongben',
                                                                                       'Hino', 'Ssangyong',
                                                                                       'Thaco', 'Vinaxuki']:
            brand, grade, year = data.loc[i, 'brand'], data.loc[i, 'grade'], data.loc[i, 'year_of_manufacture']
            data.loc[(data['brand'] == brand) & (data['grade'] == grade) &
                     (data['year_of_manufacture'] == year), 'fuel_consumption'] = website.find_car_fuel_consumption(
                driver, brand, grade, year)
        print("NEW: " + str(data.loc[i, 'fuel_consumption']))
    driver.quit()
    # Fill missing engine values
    data = fill_missing_engine(data)
    data = fill_missing_fuel_consumption(data)
    data.to_csv("./dataset/new_car_detail_en.csv", index=False)


def fill_missing_engine_capacity(data):
    tmp_cars = data.loc[
        (data['engine_capacity'].isnull()), ['engine', 'brand', 'grade', 'transmission', 'engine_capacity']]
    for index, car in tmp_cars.iterrows():
        group = data.loc[(data['brand'] == car['brand']) & (data['grade'] == car['grade']) &
                         (data['engine'] == car['engine']) & (data['engine_capacity'] != '0')
                         (data['transmission'] == car['transmission']), 'engine_capacity']
        if len(group):
            data.loc[index, 'engine_capacity'] = group.mode()[0]
    return data


def fill_missing_engine(data):
    tmp_cars = data.loc[(data['engine'].isnull()), ['engine', 'brand', 'grade']]
    for index, car in tmp_cars.iterrows():
        data.loc[index, 'engine'] = \
            data.loc[(data['brand'] == car['brand']) & (data['grade'] == car['grade']), 'engine'].mode()[0]
    return data


def fill_missing_fuel_consumption(data):
    tmp_cars = data.loc[(dataset['fuel_consumption'].isnull()) | (data['fuel_consumption'] == 0),
    ['fuel_consumption', 'engine', 'brand', 'grade']]
    for index, car in tmp_cars.iterrows():
        group = data.loc[(data['fuel_consumption'].notnull()) &
                         (data['fuel_consumption'] != 0) &
                         (data['brand'] == car['brand']) &
                         (data['grade'] == car['grade']), 'fuel_consumption']
        if len(group):
            data.loc[index, 'fuel_consumption'] = round(group.mean(axis=0), 1)
        return data


class Fueleconomy:
    def filter_data(self, data):
        # Filter 'year_of_manufacture'
        f = open("./dataset/year_produce.txt", 'r')
        tmp = 0
        for i, line in enumerate(f):
            if i % 2 == 0:
                tmp = int(line)
                continue
            data.loc[tmp, 'year_of_manufacture'] = np.float64(line)
        data['year_of_manufacture'] = np.array(data['year_of_manufacture'], dtype=np.int32)
        f.close()
        # Filter brand
        data['brand'] = data['brand'].astype(str)
        data['brand'] = data['brand'].str.replace('Mercedes Benz', 'Mercedes-Benz')
        data['brand'] = data['brand'].str.replace('Rolls Royce', 'Rolls-Royce')
        data['brand'] = data['brand'].str.replace('Aston Martin', 'Aston_Martin')
        # Filter grade
        data['grade'] = data['grade'].astype(str)
        data.loc[
            (data['grade'] == 'Super Carry Truck') | (data['grade'] == 'Super Carry Van'), 'grade'] = 'Super_Carry'
        data.loc[(data['grade'] == 'SantaFe'), 'grade'] = 'Santa_Fe'
        data.loc[(data['grade'] == 'CRV'), 'grade'] = 'CR-V'
        data.loc[(data['grade'] == 'HRV'), 'grade'] = 'HR-V'
        data.loc[(data['grade'] == 'CX3'), 'grade'] = 'CX-3'
        data.loc[(data['grade'] == 'CX5'), 'grade'] = 'CX-5'
        data.loc[(data['grade'] == 'CX7'), 'grade'] = 'CX-7'
        data.loc[(data['grade'] == 'CX8'), 'grade'] = 'CX-8'
        data.loc[(data['grade'] == 'CX9'), 'grade'] = 'CX-9'
        data.loc[(data['grade'] == 'CX30'), 'grade'] = 'CX-30'
        data.loc[(data['grade'] == 'Dmax'), 'grade'] = 'D-MAX'
        data.loc[(data['grade'] == 'X trail'), 'grade'] = 'X-Trail'

        for index, row in data.loc[(data['brand'] == 'Mercedes-Benz'), ['brand', 'grade', 'car_name']].iterrows():
            if row['grade'] not in ['AMG GT', 'CLA class', 'CLK class', 'CLS class', 'EQS', 'GL', 'GLA class',
                                    'GLB',
                                    'GLC', 'GLE Class', 'GLS', 'MB', 'SL class', 'SLK class', 'Sprinter', 'Vito']:
                tmp = row['car_name'].split(' ' + row['grade'] + ' ')
                if len(tmp) <= 1:
                    continue
                data.loc[index, 'grade'] = row['car_name'].split(' ' + row['grade'] + ' ')[1].split()[0]
            if row['grade'] in ['CLA class', 'CLK class', 'CLS class', 'GL', 'GLA class', 'GLE Class', 'SLK class']:
                tmp = row['car_name'].split(' ' + row['grade'] + ' ')[1].split()
                data.loc[index, 'grade'] = tmp[0] + tmp[1]
            if row['grade'] in ['EQS', 'GLB', 'GLC', 'GLS']:
                data.loc[index, 'grade'] += row['car_name'].split(' ' + row['grade'] + ' ')[1].split()[0]

        for index, row in data.loc[(data['brand'] == 'Lexus'), ['brand', 'grade', 'car_name']].iterrows():
            if row['grade'] != 'IS':
                data.loc[index, 'grade'] += row['car_name'].split(' ' + row['grade'] + ' ')[1].split()[0]

        for index, row in data.loc[(data['brand'] == 'Porsche'), ['brand', 'grade', 'car_name']].iterrows():
            if row['grade'] == '718':
                data.loc[index, 'grade'] += ' ' + row['car_name'].split(' ' + row['grade'] + ' ')[1].split()[0]
        data['grade'] = data['grade'].str.replace(' ', '_')
        # Filter transmission
        data['transmission'] = data['transmission'].astype(str)
        data['transmission'] = data['transmission'].replace('-', np.nan)
        # Filter drive_type
        data['drive_type'] = data['drive_type'].astype(str)
        data['drive_type'] = data['drive_type'].replace('-', np.nan)
        # Filter engine & Create engine_capacity column
        data['engine'] = data['engine'].astype(str)
        data['engine'] = data['engine'].replace('-', np.nan)
        data[['engine', 'engine_capacity']] = data['engine'].str.split('\t').apply(pd.Series)
        # Filter num_of_doors
        data['num_of_doors'] = data['num_of_doors'].astype(str)
        data['num_of_doors'] = data['num_of_doors'].str.replace('-door', '')
        data['num_of_doors'] = data['num_of_doors'].replace('0', np.nan)
        # Filter seating_capacity
        data['seating_capacity'] = data['seating_capacity'].astype(str)
        data['seating_capacity'] = data['seating_capacity'].str.replace('-seat', '')
        data['seating_capacity'] = data['seating_capacity'].replace('0', np.nan)
        # Filter fuel_consumption
        data['fuel_consumption'] = data['fuel_consumption'].astype(str)
        data['fuel_consumption'] = data['fuel_consumption'].str.replace('.\tL/100Km', '')
        data['fuel_consumption'] = data['fuel_consumption'].str.replace(',\tL/100Km', '')
        data['fuel_consumption'] = data['fuel_consumption'].str.replace('\tL/100Km', '')
        data['fuel_consumption'] = data['fuel_consumption'].str.replace('l', '')
        data['fuel_consumption'] = data['fuel_consumption'].str.replace('L', '')
        data['fuel_consumption'] = data['fuel_consumption'].str.replace(' ', '')
        data.loc[(data['fuel_consumption'] == 'K0') | (data['fuel_consumption'] == '00') |
                 (data['fuel_consumption'] == '0') | (data['fuel_consumption'] == '') |
                 (data['fuel_consumption'] == '10000') | (data['fuel_consumption'] == '100000') |
                 (data['fuel_consumption'] == '200000') | (data['fuel_consumption'] == '65') |
                 (data['fuel_consumption'] == '66') | (data['fuel_consumption'] == '565') |
                 (data['fuel_consumption'] == '68') | (data['fuel_consumption'] == '100') |
                 (data['fuel_consumption'] == '55') | (data['fuel_consumption'] == '592') |
                 (data['fuel_consumption'] == '40') | (data['fuel_consumption'] == '89') |
                 (data['fuel_consumption'] == '83') | (data['fuel_consumption'] == '85') |
                 (data['fuel_consumption'] == '6500') | (data['fuel_consumption'] == '75') |
                 (data['fuel_consumption'] == '98') | (data['fuel_consumption'] == '225') |
                 (data['fuel_consumption'] == '4288') | (data['fuel_consumption'] == '111') |
                 (data['fuel_consumption'] == '58') | (data['fuel_consumption'] == '45') |
                 (data['fuel_consumption'] == '77') | (data['fuel_consumption'] == '42') |
                 (data['fuel_consumption'] == 'L/100Km') |
                 (data['fuel_consumption'] == '/100Km'), 'fuel_consumption'] = np.nan
        # Filter fuel_system
        data['fuel_system'] = np.nan
        return data

    def find_car_engine_capacity_fuel_consumption(self, driver, year, brand, grade, engine, transmission,
                                                  engine_capacity, fuel_consumption, margin_error=0):
        # Go to website
        driver.get("https://fueleconomy.gov/feg/findacar.shtml")
        time.sleep(DELAY)
        # Select year (1984 - 2025)
        select_by_id(driver, "mnuYear1", "1984")
        select_by_id(driver, "mnuYear2", "2025")
        # if int(year) - margin_error < 1984:
        #     select_by_id(driver, "mnuYear1", "1984")
        #     select_by_id(driver, "mnuYear2", f"{int(year) + margin_error}")
        # elif int(year) + margin_error > 2025:
        #     select_by_id(driver, "mnuYear1", f"{int(year) - margin_error}")
        #     select_by_id(driver, "mnuYear2", "2025")
        # else:
        #     select_by_id(driver, "mnuYear1", f"{int(year) - margin_error}")
        #     select_by_id(driver, "mnuYear2", f"{int(year) + margin_error}")
        time.sleep(DELAY)
        # Select brand
        try:
            select_by_id(driver, "mnuMake", brand)
        except NoSuchElementException:
            if pd.isnull(engine_capacity) and pd.isnull(fuel_consumption):
                return '0', 0
            elif pd.isnull(engine_capacity):
                return '0', fuel_consumption
            elif pd.isnull(fuel_consumption):
                return engine_capacity, 0
        time.sleep(DELAY)
        # Select grade
        try:
            select_by_id(driver, "mnuModel", grade)
        except NoSuchElementException:
            if pd.isnull(engine_capacity) and pd.isnull(fuel_consumption):
                return '0', 0
            elif pd.isnull(engine_capacity):
                return '0', fuel_consumption
            elif pd.isnull(fuel_consumption):
                return engine_capacity, 0
        time.sleep(DELAY)
        driver.find_element(By.ID, "btnYmm").click()
        # Find car by engine, transmission
        if pd.isnull(engine_capacity) and pd.isnull(fuel_consumption):
            return self.get_info(driver, engine, transmission)
        elif pd.isnull(engine_capacity):
            return self.get_info(driver, engine, transmission, fuel_consumption=fuel_consumption)
        elif pd.isnull(fuel_consumption):
            return self.get_info(driver, engine, transmission, engine_capacity=engine_capacity)

    def get_info(self, driver, engine, transmission, engine_capacity='0', fuel_consumption=0):
        if "PowerSearch" in driver.current_url:
            cars = driver.find_elements(By.CLASS_NAME, "ymm-row")
            time.sleep(DELAY)
            fuels = driver.find_elements(By.CLASS_NAME, "mpg-comb")
            time.sleep(DELAY)
            for i in range(len(cars)):
                found = True
                info = cars[i].find_element(By.TAG_NAME, "span").text
                time.sleep(DELAY)
                engine_dict = {'Petrol': 'Gasoline', 'Diesel': 'Diesel', 'Hybrid': '', 'Electric': 'Electricity'}
                if engine_dict[engine] not in info or transmission not in info:
                    found = False
                if found:
                    if engine_capacity == '0':
                        engine_capacity = info.split(", ")[0]
                    if fuel_consumption == 0:
                        fuel_consumption = convert_mpg_to_lkm(fuels[i].text)
                    break
        else:
            if engine_capacity == '0':
                tmp = driver.find_element(By.CLASS_NAME, "specs")
                time.sleep(DELAY)
                info = tmp.find_elements(By.CLASS_NAME, "sbsCellData")[1].text
                time.sleep(DELAY)
                engine_capacity = info.split(", ")[0]
            if fuel_consumption == 0:
                fuel_consumption = convert_mpg_to_lkm(driver.find_element(By.CLASS_NAME, "combinedMPG").text)
                time.sleep(DELAY)
        return engine_capacity, fuel_consumption


def crawl_Fueleconomy(data):
    driver = webdriver.Chrome()
    website = Fueleconomy()
    for i, car in dataset[(data['fuel_consumption'].isnull()) | (data['engine_capacity'].isnull())].iterrows():
        if not pd.isnull(data.loc[i, 'fuel_consumption']) and not pd.isnull(data.loc[i, 'engine_capacity']):
            continue
        print(
            f"Iter {i} ------ OLD: (Fuel) {str(car['fuel_consumption'])}; (Engine) {str(car['engine_capacity'])} || ",
            end="")
        brand, grade, year, engine, transmission, fuel_consumption, engine_capacity = car['brand'], car['grade'], \
            car[
                'year_of_manufacture'], car['engine'], car['transmission'], car['fuel_consumption'], car[
            'engine_capacity']
        engine_capacity, fuel_consumption = website.find_car_engine_capacity_fuel_consumption(driver, year, brand,
                                                                                              grade, engine,
                                                                                              transmission,
                                                                                              engine_capacity,
                                                                                              fuel_consumption, 2)
        data.loc[(data['brand'] == brand) & (data['grade'] == grade) &
                 (data['transmission'] == transmission) & (data['engine'] == engine) &
                 (data['engine_capacity'].isnull()), 'engine_capacity'] = engine_capacity
        data.loc[(data['brand'] == brand) & (data['grade'] == grade) &
                 (data['year_of_manufacture'] == year) &
                 (data['fuel_consumption'].isnull()), 'fuel_consumption'] = fuel_consumption
        print(f"NEW: (Fuel) {str(data.loc[i, 'fuel_consumption'])}; (Engine) {str(data.loc[i, 'engine_capacity'])}")
    driver.quit()
    data.to_csv("./new_car_detail_en.csv", index=False)


# Import dataset
dataset = pd.read_csv("./new_car_detail_en.csv")

# Properties: (search on) 0-year,1-brand,2-grade,3-car_model,4-transmission,5-drive,6-engine
#             (crawl only) 7-num_of_doors, 8-seating_capacity, 9-fuel_consumption, 10-fuel_system
# Crawl:      (NULL) 4-transmission,5-drive,6-engine,7-num_of_doors,8-seating_capacity,9-fuel_consumption,
#                    10-fuel_system,11-engine_capacity
