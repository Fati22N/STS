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

        # Select Alcohol Use
        try:
            # Wait for the dropdown to be present in the DOM
            Alcohol_dropdown = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, 'alcohol'))
            )
            print('Alcohol dropdown Found!!!')

            # Click the Bootstrap select picker to open the dropdown
            alcohol_picker_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@data-id="alcohol"]'))
            )
            alcohol_picker_button.click()
            print('--- DROPDOWN CLICKED ---')
            time.sleep(1)  # Give time for dropdown to expand

            # Handle NaN values from CSV
            alcohol_value = str(row['Alcohol Use']).strip() if pd.notna(row['Alcohol Use']) else "None"
            print(f"Trying to select Alcohol Use: '{alcohol_value}'")

            # Select the option from the dropdown list
            alcohol_option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f'//li/a/span[text()="{alcohol_value}"]'))
            )
            alcohol_option.click()
            print(f"✅ Selected Alcohol: {alcohol_value}")

            # Trigger Bootstrap's internal update mechanism
            driver.execute_script("$('#alcohol').selectpicker('refresh');")
            time.sleep(1)

        except Exception as e:
            print("❌ Error selecting Alcohol Use:", str(e))

        # Select Heart Failure
        try:
            Heart_dropdown = WebDriverWait(driver, 20).until(
                lambda d: d.find_element(By.ID, 'heartfailtmg')
            )
            print('--- DROPDOWN CLICKED ---')

            if Heart_dropdown:
                heart_dropdown = Select(Heart_dropdown)
                heart_dropdown.select_by_visible_text(str(row['Heart Failure']))
                print(f"✅ Selected Heart Failure: {row['Heart Failure']}")
            else:
                print("❌ No Heart Failure dropdown found.")
        except Exception as e:
            print("❌ Error selecting Heart Failure:", str(e))

        # # Select NYHA Classification
        # try:
        #     NYHA_dropdown = WebDriverWait(div_elements[59], 20).until(
        #         lambda d: d.find_element(By.ID, 'classnyh')
        #     )
        #     if NYHA_dropdown:
        #         NYHA_dropdown = Select(NYHA_dropdown)
        #         NYHA_dropdown.select_by_visible_text(str(row['NYHA Classification']))
        #         print(f"✅ Selected NYHA: {row['NYHA Classification']}")
        #     else:
        #         print("❌ No NYHA dropdown found.")
        # except Exception as e:
        #     print("❌ Error selecting NYHA:", str(e))

        # # Select Aortic Regurgitation
        # try:
        #     Aortic_dropdown = WebDriverWait(div_elements[77], 20).until(
        #         lambda d: d.find_element(By.ID, 'vdinsufa')
        #     )
        #     if Aortic_dropdown:
        #         aortic_dropdown = Select(Aortic_dropdown)
        #         aortic_dropdown.select_by_visible_text(str(row['Aortic Regurgitation']))
        #         print(f"✅ Selected Aortic: {row['Aortic Regurgitation']}")
        #     else:
        #         print("❌ No Aortic dropdown found.")
        # except Exception as e:
        #     print("❌ Error selecting Aortic:", str(e))
        #
        # # Select Miteral Regurgitation
        # try:
        #     Mitral_dropdown = WebDriverWait(div_elements[79], 20).until(
        #         lambda d: d.find_element(By.ID, 'vdinsufm')
        #     )
        #     if Mitral_dropdown:
        #         mitral_dropdown = Select(Mitral_dropdown)
        #         mitral_dropdown.select_by_visible_text(str(row['Mitral Regurgitation']))
        #         print(f"✅ Selected Mitral: {row['Mitral Regurgitation']}")
        #     else:
        #         print("❌ No Mitral dropdown found.")
        # except Exception as e:
        #     print("❌ Error selecting Mitral:", str(e))
        #
        # # Select Tricuspid Regurgitation
        # try:
        #     Tricuspid_dropdown = WebDriverWait(div_elements[81], 20).until(
        #         lambda d: d.find_element(By.ID, 'vdinsuft')
        #     )
        #     if Tricuspid_dropdown:
        #         tricuspid_dropdown = Select(Tricuspid_dropdown)
        #         tricuspid_dropdown.select_by_visible_text(str(row['Tricuspid Regurgitation']))
        #         print(f"✅ Selected Tricuspid: {row['Tricuspid Regurgitation']}")
        #     else:
        #         print("❌ No Tricuspid dropdown found.")
        # except Exception as e:
        #     print("❌ Error selecting Tricuspid:", str(e))
        #
        # # Select Atrial Flutter
        # try:
        #     Flutter_dropdown = WebDriverWait(div_elements[87], 20).until(
        #         lambda d: d.find_element(By.ID, 'arrhythaflutter')
        #     )
        #     if Flutter_dropdown:
        #         atrial_dropdown = Select(Flutter_dropdown)
        #         atrial_dropdown.select_by_visible_text(str(row['Atrial Flutter']))
        #         print(f"✅ Selected Flutter: {row['Atrial Flutter']}")
        #     else:
        #         print("❌ No Flutter dropdown found.")
        # except Exception as e:
        #     print("❌ Error selecting Flutter:", str(e))
        #
        # # Select V. Tach / V. Fib
        # try:
        #     Tach_dropdown = WebDriverWait(div_elements[89], 20).until(
        #         lambda d: d.find_element(By.ID, 'arrhythvv')
        #     )
        #     if Tach_dropdown:
        #         tach_dropdown = Select(Tach_dropdown)
        #         tach_dropdown.select_by_visible_text(str(row['V. Tach / V. Fib']))
        #         print(f"✅ Selected Tach: {row['V. Tach / V. Fib']}")
        #     else:
        #         print("❌ No Flutter dropdown found.")
        # except Exception as e:
        #     print("❌ Error selecting Flutter:", str(e))
        #
        # # Select Sick Sinus Syn.
        # try:
        #     Sinus_dropdown = WebDriverWait(div_elements[91], 20).until(
        #         lambda d: d.find_element(By.ID, 'arrhythsss')
        #     )
        #     if Sinus_dropdown:
        #         sinus_dropdown = Select(Sinus_dropdown)
        #         sinus_dropdown.select_by_visible_text(str(row['Sick Sinus Syn.']))
        #         print(f"✅ Selected Sinus: {row['Sick Sinus Syn.']}")
        #     else:
        #         print("❌ No Sinus dropdown found.")
        # except Exception as e:
        #     print("❌ Error selecting Sinus:", str(e))
        #
        # # Select 2ⁿᵈ Degree Block
        # try:
        #     Block_dropdown = WebDriverWait(div_elements[93], 20).until(
        #         lambda d: d.find_element(By.ID, 'arrhythsecond')
        #     )
        #     if Block_dropdown:
        #         block_dropdown = Select(Block_dropdown)
        #         block_dropdown.select_by_visible_text(str(row['2ⁿᵈ Degree Block']))
        #         print(f"✅ Selected Block: {row['2ⁿᵈ Degree Block']}")
        #     else:
        #         print("❌ No Block dropdown found.")
        # except Exception as e:
        #     print("❌ Error selecting Block:", str(e))
        #
        # # Select 3ʳᵈ Degree Block
        # try:
        #     Degree_dropdown = WebDriverWait(div_elements[95], 20).until(
        #         lambda d: d.find_element(By.ID, 'arrhyththird')
        #     )
        #     if Degree_dropdown:
        #         degree_dropdown = Select(Degree_dropdown)
        #         degree_dropdown.select_by_visible_text(str(row['3ʳᵈ Degree Block']))
        #         print(f"✅ Selected Degree: {row['3ʳᵈ Degree Block']}")
        #     else:
        #         print("❌ No Degree dropdown found.")
        # except Exception as e:
        #     print("❌ Error selecting Degree:", str(e))

        pdf_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(@href, ".pdf")]'))
        )
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
