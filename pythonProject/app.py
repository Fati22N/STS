from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
import time

# Load CSV file
csv_file = "STS Score - Armin Ghaderi Thesis Data - Table.csv"
data = pd.read_csv(csv_file)

# Set up Selenium WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Open the target website
driver.get("https://acsdriskcalc.research.sts.org/")

# Handle Terms of Service Modal
try:
    time.sleep(10)
    accept_button = WebDriverWait(driver, 90).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="Accept"]'))
    )
    accept_button.click()
    print("✅ Accepted Terms of Service.")
except Exception as e:
    print("⚠️ No modal found or issue clicking 'Accept':", e)

# Iterate through each row in the CSV
for index, row in data.iterrows():
    try:
        # time.sleep(50)
        print(f"\n🔹 Processing Row {index}...")

        # Wait for the form to be available
        div_elements = WebDriverWait(driver, 80).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'shinyjs-resettable'))
        )

        # Ensure at least two divs are found
        if len(div_elements) < 2:
            print("❌ Not enough div elements found.")
        else:
            print("✅ Found form containers.")

        # Select Surgery Type from the first div
        try:
            proc_dropdown = WebDriverWait(div_elements[0], 20).until(
                EC.presence_of_element_located((By.ID, 'Proc'))
            )
            surgery_dropdown = Select(proc_dropdown)
            surgery_dropdown.select_by_visible_text(str(row['Planned Surgery']))
            print(f"✅ Selected Surgery: {row['Planned Surgery']}")
        except Exception as e:
            print("❌ Error selecting Surgery:", str(e))

        # div_element = WebDriverWait(driver, 80).until(
        #     EC.presence_of_all_elements_located((By.ID, 'tab-2072-1'))
        # )
        # # Ensure at least two divs are found
        # if len(div_element) < 2:
        #     print("❌ Not enough div element found.")
        # else:
        #     print("✅ Found form containers.")
        #
        # pdf_link = WebDriverWait(div_element[2], 10).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, 'btn-capture-screenshot-pdf'))
        # )
        # print('PDF Clicked')

        div_element = WebDriverWait(driver, 80).until(
            EC.presence_of_all_elements_located((By.ID, 'shiny-panel-conditional'))
        )
        # Ensure at least two divs are found
        if len(div_element) < 2:
            print("❌ Not enough div element found.")
        else:
            print("✅ Found form containers.")

        pdf_link = WebDriverWait(div_element[20], 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'btn-capture-screenshot-pdf'))
        )
        print('PDF Clicked')


        pdf_url = pdf_link.get_attribute('href')

        # Download PDF
        response = requests.get(pdf_url)
        pdf_filename = f"result_{index}.pdf"
        with open(pdf_filename, 'wb') as f:
            f.write(response.content)
        print(f"📥 Downloaded: {pdf_filename}")

        # Go back to the form for the next entry
        driver.get("https://acsdriskcalc.research.sts.org/")
        print("🔄 Reloaded form for next entry.")

    except Exception as e:
        print(f"❌ Error processing row {index}: {e}")

    # Close browser after all rows are processed
    driver.quit()
    print("\n🎉 All rows processed! Browser closed.")
