from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from time import sleep
import quickstart

while(True):
    try:
        parcel_num_book = "503"
        parcel_num_map = "51"
        parcel_num_item = "079"
        parcel_num_split = "A"

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")

        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        driver.get("https://treasurer.maricopa.gov/Parcel/Summary.aspx")

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[id=\"txtParcelNumBook\"]")))
        parcel_num_book_input = driver.find_element(By.CSS_SELECTOR, "input[id=\"txtParcelNumBook\"]")
        parcel_num_book_input.send_keys(parcel_num_book)
        parcel_num_map_input = driver.find_element(By.CSS_SELECTOR, "input[id=\"txtParcelNumMap\"]")
        parcel_num_map_input.send_keys(parcel_num_map)
        parcel_num_item_input = driver.find_element(By.CSS_SELECTOR, "input[id=\"txtParcelNumItem\"]")
        parcel_num_item_input.send_keys(parcel_num_item)
        parcel_num_split_input = driver.find_element(By.CSS_SELECTOR, "input[id=\"txtParcelNumSplit\"]")
        parcel_num_split_input.send_keys(parcel_num_split)

        search_button = driver.find_element(By.CSS_SELECTOR, "div[id=\"btnGo\"]")
        search_button.click()
        sleep(3)

        quickstart.main()
        apn_list = quickstart.getAPNList()
        last_index = quickstart.getLastIndex()
        if len(apn_list) == last_index:
            break
        index = last_index - 1
        while(len(apn_list) > index):
            split_string = apn_list[index].split('-')
            parcel_num_book = split_string[0]
            parcel_num_map = split_string[1]
            parcel_num_item = split_string[2]
            try:
                parcel_num_split = split_string[3]
            except:
                parcel_num_split = ""

            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[id=\"txtParcelNumBook\"]")))
            parcel_num_book_input = driver.find_element(By.CSS_SELECTOR, "input[id=\"txtParcelNumBook\"]")
            parcel_num_book_input.send_keys(parcel_num_book)
            parcel_num_map_input = driver.find_element(By.CSS_SELECTOR, "input[id=\"txtParcelNumMap\"]")
            parcel_num_map_input.send_keys(parcel_num_map)
            parcel_num_item_input = driver.find_element(By.CSS_SELECTOR, "input[id=\"txtParcelNumItem\"]")
            parcel_num_item_input.send_keys(parcel_num_item)
            parcel_num_split_input = driver.find_element(By.CSS_SELECTOR, "input[id=\"txtParcelNumSplit\"]")
            parcel_num_split_input.send_keys(parcel_num_split)

            search_button = driver.find_element(By.CSS_SELECTOR, "input[id=\"btnGo\"]")
            search_button.click()
            sleep(3)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[id=\"cphMainContent_cphRightColumn_divViewAdditionalYears\"]")))
            view_addtional_tax_years_button = driver.find_element(By.CSS_SELECTOR, "div[id=\"cphMainContent_cphRightColumn_divViewAdditionalYears\"]").find_element(By.TAG_NAME, "a")
            view_addtional_tax_years_button.click()
            sleep(3)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[title=\"Click for a Tax Stub printout\"]")))
            # tax_elements = driver.find_elements(By.CSS_SELECTOR, "a[title=\"Click for a Tax Stub printout\"]")
            total_tax_due = driver.find_element(By.CSS_SELECTOR, "span[class=\"text-bold text-black \"]").text
            tax_due_2023 = "0"
            tax_due_2022 = "0"
            tax_due_2021 = "0"
            
            tax_rows = driver.find_elements(By.CSS_SELECTOR, "tr[class=\"gridviewRow\"]")
            for tax_row in tax_rows:
                try:
                    if "2023" in tax_row.find_element(By.CSS_SELECTOR, "a[title=\"Click to view Tax Details\"]").text:
                        try:
                            tax_due_2023 = tax_row.find_element(By.CSS_SELECTOR, "a[title=\"Click for a Tax Stub printout\"]").text
                        except:
                            tax_due_2023 = tax_row.find_element(By.CSS_SELECTOR, "a[class=\"text-red\"]").text
                    if "2022" in tax_row.find_element(By.CSS_SELECTOR, "a[title=\"Click to view Tax Details\"]").text:
                        try:
                            tax_due_2022 = tax_row.find_element(By.CSS_SELECTOR, "a[title=\"Click for a Tax Stub printout\"]").text
                        except:
                            tax_due_2022 = tax_row.find_element(By.CSS_SELECTOR, "a[class=\"text-red\"]").text
                    if "2021" in tax_row.find_element(By.CSS_SELECTOR, "a[title=\"Click to view Tax Details\"]").text:
                        try:
                            tax_due_2021 = tax_row.find_element(By.CSS_SELECTOR, "a[title=\"Click for a Tax Stub printout\"]").text
                        except:
                            tax_due_2021 = tax_row.find_element(By.CSS_SELECTOR, "a[class=\"text-red\"]").text
                except:
                    pass
            print(total_tax_due)
            print(tax_due_2023)
            print(tax_due_2022)
            print(tax_due_2021)

            data = []
            data.append(tax_due_2023)
            data.append(tax_due_2022)
            data.append(tax_due_2021)
            data.append(total_tax_due)

            RANGE_NAME_INDEX = f'Sheet1!C{index + 2}:F'
            quickstart.insert_data(RANGE_NAME_INDEX, data)
            index += 1

    except:
        pass

