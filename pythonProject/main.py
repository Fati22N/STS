from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pandas as pd
import pyperclip
import time
from fpdf import FPDF

# Load CSV file
csv_file = r"/mnt/windows/Fatima/temp/MrArian/pythonProject/CSV/STS - TVR.csv"
data = pd.read_csv(csv_file)

# Configure Chrome options
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": "/mnt/windows/Fatima/temp/MrArian/Copy",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

# Set up Selenium WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Open the target website
driver.get("https://acsdriskcalc.research.sts.org/")

# Handle Terms of Service Modal
try:
    time.sleep(6)
    accept_button = WebDriverWait(driver, 80).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="Accept"]'))
    )
    accept_button.click()
    print("✅ Accepted Terms of Service.")
except Exception as e:
    print("⚠️ No modal found or issue clicking 'Accept':", e)

# Iterate through each row in the CSV
for index, row in data.iterrows():
    try:
        print(f"\n🔹 Processing Row {index}...")

        # Wait for the form to be available
        div_elements = WebDriverWait(driver, 70).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'shinyjs-resettable'))
        )

        # Ensure at least two divs are found
        if len(div_elements) < 2:
            print("❌ Not enough div elements found.")
        else:
            print("✅ Found form containers.")

            # Select Surgery Type from the first div
            try:
                time.sleep(1)
                proc_dropdown = WebDriverWait(div_elements[0], 20).until(
                    EC.presence_of_element_located((By.ID, 'Proc'))
                )
                surgery_dropdown = Select(proc_dropdown)
                surgery_dropdown.select_by_visible_text(str(row['Planned Surgery']))
                print(f"✅ Selected Surgery: {row['Planned Surgery']}")
            except Exception as e:
                print("❌ Error selecting Surgery:", str(e))

            # Select Incidence
            try:
                time.sleep(1)
                incidenc_dropdown = WebDriverWait(div_elements[3], 20).until(
                    EC.presence_of_element_located((By.ID, 'incidenc'))
                )
                if incidenc_dropdown:
                    surgery_dropdown = Select(incidenc_dropdown)
                    # Print available options
                    options = [opt.text for opt in surgery_dropdown.options]
                    print("🔹 Available surgery options:", options)

                    incidenc_value = str(row['Surgery Incidence']).strip() if pd.notna(
                        row['Surgery Incidence']) else "Class I"

                    # Check if the value is in the options
                    if incidenc_value in options:
                        surgery_dropdown.select_by_visible_text(incidenc_value)
                        print(f"✅ Selected Surgery Incidence: {incidenc_value}")
                    else:
                        print(f"❌ surgery value '{incidenc_value}' not found in dropdown. Selecting default 'First CV surgery'")
                        surgery_dropdown.select_by_visible_text("First CV surgery")  # Use correct default
                else:
                #     surgery_dropdown.select_by_visible_text(str(row['Surgery Incidence']))
                #     print(f"✅ Selected Incidence: {row['Surgery Incidence']}")
                # else:
                    print("❌ No incidenc dropdown found.")
            except Exception as e:
                print("❌ Error selecting Surgery Incidence:", str(e))

            # Select Surgical Priority
            try:
                time.sleep(1)
                status_dropdown = WebDriverWait(div_elements[5], 20).until(
                    EC.presence_of_element_located((By.ID, 'status'))
                )
                if status_dropdown:
                    surgical_dropdown = Select(status_dropdown)
                    surgical_dropdown.select_by_visible_text(str(row['Surgical Priority']))
                    print(f"✅ Selected Priority: {row['Surgical Priority']}")
                else:
                    print("❌ No status dropdown found.")
            except Exception as e:
                print("❌ Error selecting Surgical Priority:", str(e))

            # Select Sex
            try:
                time.sleep(1)
                sex_dropdown = WebDriverWait(div_elements[7], 20).until(
                    EC.presence_of_element_located((By.ID, 'gender'))
                )
                if sex_dropdown:
                    sex_dropdown = Select(sex_dropdown)
                    sex_dropdown.select_by_visible_text(str(row['Sex']))
                    print(f"✅ Selected Sex: {row['Sex']}")
                else:
                    print("❌ No sex dropdown found.")
            except Exception as e:
                print("❌ Error selecting Sex:", str(e))

        # Input Age
        try:
            time.sleep(1)
            age_input = WebDriverWait(driver, 20).until(
                lambda d: d.find_element(By.ID, 'ageN')
            )
            if age_input:
                # age_input = driver.find_element(By.NAME, 'age')
                age_input.send_keys(str(row['Age (years)']))
                print(f"✅ Entered Age: {row['Age (years)']}")
            else:
                print("❌ No age input found.")
        except Exception as e:
            print("❌ Error selecting age:", str(e))

        # Input Weight
        try:
            time.sleep(1)
            height_input = WebDriverWait(driver, 20).until(
                lambda d: d.find_element(By.ID, 'heightN')
            )
            if height_input:
                height_input.send_keys(str(row['Height (cm)']))
                print(f"✅ Entered Height: {row['Height (cm)']}")
            else:
                print("❌ No height input found.")
        except Exception as e:
            print("❌ Error selecting Height:", str(e))

        # Input Weight
        try:
            time.sleep(1)
            weight_input = WebDriverWait(driver, 20).until(
                lambda d: d.find_element(By.ID, 'weightN')
            )
            if weight_input:
                weight_input.send_keys(str(row['Weight (kg)']))
                print(f"✅ Entered Weight: {row['Weight (kg)']}")
            else:
                print("❌ No weight input found.")
        except Exception as e:
            print("❌ Error selecting Weight:", str(e))

        # Select Race
        try:
            time.sleep(1)
            race_dropdown = WebDriverWait(div_elements[13], 20).until(
                lambda d: d.find_element(By.ID, 'racemulti')
            )
            if race_dropdown:
                race_dropdown = Select(race_dropdown)
                race_dropdown.select_by_visible_text(str(row['Race']))
                print(f"✅ Selected Race: {row['Race']}")
            else:
                print("❌ No weight race found.")
        except Exception as e:
            print("❌ Error selecting Race:", str(e))

        # Select Payor / Insurance
        try:
            time.sleep(1)
            payordata_dropdown = WebDriverWait(div_elements[15], 20).until(
                lambda d: d.find_element(By.ID, 'payordata')
            )
            if payordata_dropdown:
                Payor_dropdown = Select(payordata_dropdown)
                Payor_dropdown.select_by_visible_text(str(row['Payor / Insurance']))
                print(f"✅ Selected Payor: {row['Payor / Insurance']}")
            else:
                print("❌ No payor dropdown found.")
        except Exception as e:
            print("❌ Error selecting Payor:", str(e))

        # Input Creatinine
        try:
            time.sleep(1)
            creatinine_input = WebDriverWait(driver, 20).until(
                lambda d: d.find_element(By.ID, 'creatlstN')
            )
            if creatinine_input:
                creatinine_input.send_keys(str(row['Creatinine (mg/dL)']))
                print(f"✅ Entered Creatinine: {row['Creatinine (mg/dL)']}")
            else:
                print("❌ No creatinine input found.")
        except Exception as e:
            print("❌ Error selecting Creatinine:", str(e))

        # Input Creatinine
        try:
            time.sleep(1)
            hematocrit_input = WebDriverWait(driver, 20).until(
                lambda d: d.find_element(By.ID, 'hctN')
            )
            if hematocrit_input:
                hematocrit_input.send_keys(str(row['Hematocrit (%)']))
                print(f"✅ Entered Hematocrit: {row['Hematocrit (%)']}")
            else:
                print("❌ No hematocrit input found.")
        except Exception as e:
            print("❌ Error selecting Hematocrit:", str(e))

        # Input WBC Count
        try:
            time.sleep(1)
            WBC_input = WebDriverWait(driver, 20).until(
                lambda d: d.find_element(By.ID, 'wbcN')
            )
            if WBC_input:
                WBC_input.send_keys(str(row['WBC Count (10³/μL)']))
                print(f"✅ Entered WBC: {row['WBC Count (10³/μL)']}")
            else:
                print("❌ No WBC Count input found.")
        except Exception as e:
            print("❌ Error selecting WBC_Count :", str(e))

        # Input Platelet Count
        try:
            time.sleep(1)
            Platelet_input = WebDriverWait(driver, 20).until(
                lambda d: d.find_element(By.ID, 'plateletsN')
            )
            if Platelet_input:
                Platelet_input.send_keys(str(row['Platelet Count (cells/μL)']))
                print(f"✅ Entered Platelet: {row['Platelet Count (cells/μL)']}")
            else:
                print("❌ No Platelet Count input found.")
        except Exception as e:
            print("❌ Error selecting Platelet_Count :", str(e))

        # Select Diabetes
        try:
            time.sleep(1)
            Diabetes_dropdown = WebDriverWait(div_elements[27], 20).until(
                lambda d: d.find_element(By.ID, 'diabetes')
            )
            if Diabetes_dropdown:
                Diabetes_dropdown = Select(Diabetes_dropdown)
                Diabetes_dropdown.select_by_visible_text(str(row['Diabetes']))
                print(f"✅ Selected Diabetes: {row['Diabetes']}")
            else:
                print("❌ No Diabetes dropdown found.")
        except Exception as e:
            print("❌ Error selecting Diabetes:", str(e))

        # Select Endocarditis
        try:
            time.sleep(1)
            Endocarditis_dropdown = WebDriverWait(div_elements[38], 20).until(
                lambda d: d.find_element(By.ID, 'endocarditis')
            )
            if Endocarditis_dropdown:
                endocarditis_dropdown = Select(Endocarditis_dropdown)
                endocarditis_dropdown.select_by_visible_text(str(row['Endocarditis']))
                print(f"✅ Selected Endocarditis: {row['Endocarditis']}")
            else:
                print("❌ No Endocarditis dropdown found.")
        except Exception as e:
            print("❌ Error selecting Endocarditis:", str(e))

        # Select Illicit Drug Use
        try:
            time.sleep(1)
            Illicit_dropdown = WebDriverWait(div_elements[40], 20).until(
                lambda d: d.find_element(By.ID, 'ivdrugab')
            )
            if Illicit_dropdown:
                illicit_dropdown = Select(Illicit_dropdown)
                illicit_dropdown.select_by_visible_text(str(row['Illicit Drug Use']))
                print(f"✅ Selected Illicit Drug Use: {row['Illicit Drug Use']}")
            else:
                print("❌ No Illicit Drug Use dropdown found.")
        except Exception as e:
            print("❌ Error selecting Illicit Drug Use:", str(e))

        # Select Alcohol Use
        try:
            time.sleep(1)
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

        # Select Tobacco Use
        try:
            time.sleep(1)
            Tobacco_dropdown = WebDriverWait(div_elements[44], 20).until(
                lambda d: d.find_element(By.ID, 'tobaccouse')
            )
            if Tobacco_dropdown:
                tobacco_dropdown = Select(Tobacco_dropdown)
                tobacco_dropdown.select_by_visible_text(str(row['Tobacco Use']))
                print(f"✅ Selected Tobacco: {row['Tobacco Use']}")
            else:
                print("❌ No tobacco dropdown found.")
        except Exception as e:
            print("❌ Error selecting tobacco:", str(e))

        # Select Chronic Lung Disease
        try:
            time.sleep(1)
            Chronic_dropdown = WebDriverWait(div_elements[46], 20).until(
                lambda d: d.find_element(By.ID, 'chrlungd')
            )
            if Chronic_dropdown:
                chronic_dropdown = Select(Chronic_dropdown)
                chronic_dropdown.select_by_visible_text(str(row['Chronic Lung Disease']))
                print(f"✅ Selected Lung Disease: {row['Chronic Lung Disease']}")
            else:
                print("❌ No Chronic Lung Disease dropdown found.")
        except Exception as e:
            print("❌ Error selecting Chronic Lung Disease:", str(e))

        # Select Cerebrovascular Disease
        try:
            time.sleep(1)
            Cerebrovascular_dropdown = WebDriverWait(div_elements[51], 20).until(
                lambda d: d.find_element(By.ID, 'cvd')
            )
            if Cerebrovascular_dropdown:
                cerebrovascular_dropdown = Select(Cerebrovascular_dropdown)
                cerebrovascular_dropdown.select_by_visible_text(str(row['Cerebrovascular Disease']))
                print(f"✅ Selected Cerebrovascular: {row['Cerebrovascular Disease']}")
            else:
                print("❌ No Cerebrovascular Disease dropdown found.")
        except Exception as e:
            print("❌ Error selecting Cerebrovascular Disease:", str(e))

        # Select Heart Failure
        try:
            time.sleep(1)
            Heart_dropdown = WebDriverWait(div_elements[57], 20).until(
                lambda d: d.find_element(By.ID, 'heartfailtmg')
            )
            print('--- DROPDOWN CLICKED ---')

            if Heart_dropdown:
                heart_dropdown = Select(Heart_dropdown)
                if pd.notna(row['Heart Failure']) and row['Heart Failure'] not in [None, 'None', '']:
                    heart_dropdown.select_by_visible_text(str(row['Heart Failure']).strip())
                    print(f"✅ Selected Heart Failure: {row['Heart Failure']}")
                else:
                    heart_dropdown.select_by_visible_text("None")  # Ensure a valid selection
                    print("✅ Selected Heart Failure: None")

                print(f"✅ Selected Heart Failure: {row['Heart Failure']}")
            else:
                print("❌ No Heart Failure dropdown found.")
        except Exception as e:
            print("❌ Error selecting Heart Failure:", str(e))

        # Select NYHA Classification
        try:
            time.sleep(1)
            NYHA_dropdown = WebDriverWait(div_elements[59], 20).until(
                lambda d: d.find_element(By.ID, 'classnyh')
            )
            print('--- DROPDOWN CLICKED ---')

            if NYHA_dropdown:
                NYHA_dropdown = Select(NYHA_dropdown)

                # Print available options
                options = [opt.text for opt in NYHA_dropdown.options]
                print("🔹 Available NYHA options:", options)

                nyha_value = str(row['NYHA Classification']).strip() if pd.notna(
                    row['NYHA Classification']) else "Class I"

                # Check if the value is in the options
                if nyha_value in options:
                    NYHA_dropdown.select_by_visible_text(nyha_value)
                    print(f"✅ Selected NYHA Classification: {nyha_value}")
                else:
                    print(f"❌ NYHA value '{nyha_value}' not found in dropdown. Selecting default 'Class I'")
                    NYHA_dropdown.select_by_visible_text("Class I")  # Use correct default
            else:
                print("❌ No NYHA dropdown found.")
        except Exception as e:
            print("❌ Error selecting NYHA:", str(e))

        # Select PreOp Mech Circ Support
        # try:
        #     time.sleep(1)
        #     PreOp_dropdown = WebDriverWait(div_elements[61], 20).until(
        #         lambda d: d.find_element(By.ID, 'mcs')
        #     )
        #     if PreOp_dropdown:
        #         PreOp_dropdown = Select(PreOp_dropdown)
        #         PreOp_dropdown.select_by_visible_text(str(row['PreOp Mech Circ Support']))
        #         print(f"✅ Selected PreOp: {row['PreOp Mech Circ Support']}")
        #     else:
        #         print("❌ No PreOp dropdown found.")
        # except Exception as e:
        #     print("❌ Error selecting PreOp:", str(e))

        # Select PreOp Mech Circ Support
        try:
            time.sleep(1)
            PreOp_dropdown = WebDriverWait(div_elements[61], 20).until(
                lambda d: d.find_element(By.ID, 'mcs')
            )

            # Get the value from the CSV
            preop_value = str(row['PreOp Mech Circ Support']).strip()

            if preop_value == "Not Chosen":
                print("⏩ Skipping PreOp selection (Not Chosen).")
            else:
                PreOp_dropdown = Select(PreOp_dropdown)
                PreOp_dropdown.select_by_visible_text(preop_value)
                print(f"✅ Selected PreOp: {preop_value}")

        except Exception as e:
            print("❌ Error selecting PreOp:", str(e))

        # Input Ejection Fraction (%)
        try:
            time.sleep(1)
            ejection_input = WebDriverWait(driver, 20).until(
                lambda d: d.find_element(By.ID, 'hdef')
            )
            if ejection_input:
                ejection_input.send_keys(str(row['Ejection Fraction (%)']))
                print(f"✅ Entered Ejection Fraction: {row['Ejection Fraction (%)']}")
            else:
                print("❌ No Ejection Fraction input found.")
        except Exception as e:
            print("❌ Error selecting Ejection Fraction :", str(e))

        # Select Prim. Coronary Symptom
        try:
            time.sleep(1)
            Prim_dropdown = WebDriverWait(div_elements[66], 20).until(
                lambda d: d.find_element(By.ID, 'cardsymptimeofadm')
            )
            if Prim_dropdown:
                prim_dropdown = Select(Prim_dropdown)
                prim_dropdown.select_by_visible_text(str(row['Prim. Coronary Symptom']))
                print(f"✅ Selected Prim: {row['Prim. Coronary Symptom']}")
            else:
                print("❌ No Prim dropdown found.")
        except Exception as e:
            print("❌ Error selecting Prim:", str(e))

        # Select Myocardial Infarction-when
        try:
            time.sleep(1)
            Myocardial_dropdown = WebDriverWait(div_elements[68], 20).until(
                lambda d: d.find_element(By.ID, 'miwhen')
            )
            if Myocardial_dropdown:
                myocardial_dropdown = Select(Myocardial_dropdown)
                myocardial_dropdown.select_by_visible_text(str(row['Myocardial Infarction-when']))
                print(f"✅ Selected Myocardial: {row['Myocardial Infarction-when']}")
            else:
                print("❌ No Myocardial dropdown found.")
        except Exception as e:
            print("❌ Error selecting Myocardial:", str(e))

        # Select No. of Diseased Vessels
        try:
            time.sleep(1)
            Vessels_dropdown = WebDriverWait(div_elements[70], 20).until(
                lambda d: d.find_element(By.ID, 'numdisv')
            )
            if Vessels_dropdown:
                vessels_dropdown = Select(Vessels_dropdown)
                vessels_dropdown.select_by_visible_text(str(row['No. of Diseased Vessels']))
                print(f"✅ Selected Vessels: {row['No. of Diseased Vessels']}")
            else:
                print("❌ No Vessels dropdown found.")
        except Exception as e:
            print("❌ Error selecting Vessels:", str(e))

        # Select Aortic Regurgitation
        try:
            time.sleep(1)
            Aortic_dropdown = WebDriverWait(div_elements[77], 20).until(
                lambda d: d.find_element(By.ID, 'vdinsufa')
            )
            if Aortic_dropdown:
                aortic_dropdown = Select(Aortic_dropdown)

                # Print available options
                options = [opt.text for opt in aortic_dropdown.options]
                print("🔹 Available Aortic Regurgitation options:", options)

                aortic_value = str(row['Aortic Regurgitation']).strip() if pd.notna(
                    row['Aortic Regurgitation']) else "None"

                # Check if the value is in the options
                if aortic_value in options:
                    aortic_dropdown.select_by_visible_text(aortic_value)
                    print(f"✅ Selected Aortic Regurgitation: {aortic_value}")
                else:
                    print(f"❌ Aortic value '{aortic_value}' not found in dropdown. Selecting default 'None'")
                    aortic_dropdown.select_by_visible_text("None")  # Use correct default
            else:
                print("❌ No Aortic dropdown found.")
        except Exception as e:
            print("❌ Error selecting Aortic:", str(e))

        # Select Miteral Regurgitation
        try:
            time.sleep(1)
            Mitral_dropdown = WebDriverWait(div_elements[79], 20).until(
                lambda d: d.find_element(By.ID, 'vdinsufm')
            )
            if Mitral_dropdown:
                mitral_dropdown = Select(Mitral_dropdown)
                # mitral_dropdown.select_by_visible_text(str(row['Mitral Regurgitation']))
                # print(f"✅ Selected Mitral: {row['Mitral Regurgitation']}")
                # Print available options
                options = [opt.text for opt in mitral_dropdown.options]
                print("🔹 Available Mitral Regurgitation options:", options)

                mitral_value = str(row['Mitral Regurgitation']).strip() if pd.notna(
                    row['Mitral Regurgitation']) else "None"

                # Check if the value is in the options
                if mitral_value in options:
                    mitral_dropdown.select_by_visible_text(mitral_value)
                    print(f"✅ Selected Mitral Regurgitation: {mitral_value}")
                else:
                    print(f"❌ Mitral value '{mitral_value}' not found in dropdown. Selecting default 'None'")
                    mitral_dropdown.select_by_visible_text("None")  # Use correct default
            else:
                print("❌ No Mitral dropdown found.")
        except Exception as e:
            print("❌ Error selecting Mitral:", str(e))

        # Select Tricuspid Regurgitation
        try:
            time.sleep(1)
            Tricuspid_dropdown = WebDriverWait(div_elements[81], 20).until(
                lambda d: d.find_element(By.ID, 'vdinsuft')
            )
            if Tricuspid_dropdown:
                tricuspid_dropdown = Select(Tricuspid_dropdown)
                # tricuspid_dropdown.select_by_visible_text(str(row['Tricuspid Regurgitation']))
                # print(f"✅ Selected Tricuspid: {row['Tricuspid Regurgitation']}")
                options = [opt.text for opt in tricuspid_dropdown.options]
                print("🔹 Available Tricuspid Regurgitation options:", options)

                tricuspid_value = str(row['Tricuspid Regurgitation']).strip() if pd.notna(
                    row['Tricuspid Regurgitation']) else "None"

                # Check if the value is in the options
                if tricuspid_value in options:
                    tricuspid_dropdown.select_by_visible_text(tricuspid_value)
                    print(f"✅ Selected Tricuspid Regurgitation: {tricuspid_value}")
                else:
                    print(f"❌ Tricuspid value '{tricuspid_value}' not found in dropdown. Selecting default 'None'")
                    tricuspid_dropdown.select_by_visible_text("None")  # Use correct default
            else:
                print("❌ No Tricuspid dropdown found.")
        except Exception as e:
            print("❌ Error selecting Tricuspid:", str(e))

        # Select Atrial Fibrillation
        try:
            time.sleep(1)
            Atrial_dropdown = WebDriverWait(div_elements[83], 20).until(
                lambda d: d.find_element(By.ID, 'arrhythatrfib')
            )
            if Atrial_dropdown:
                atrial_dropdown = Select(Atrial_dropdown)
                # atrial_dropdown.select_by_visible_text(str(row['Atrial Fibrillation']))
                # print(f"✅ Selected Atrial: {row['Atrial Fibrillation']}")
                options = [opt.text for opt in atrial_dropdown.options]
                print("🔹 Available Atrial Regurgitation options:", options)

                atrial_value = str(row['Atrial Fibrillation']).strip() if pd.notna(
                    row['Atrial Fibrillation']) else "None"

                # Check if the value is in the options
                if atrial_value in options:
                    atrial_dropdown.select_by_visible_text(atrial_value)
                    print(f"✅ Selected Atrial Fibrillation: {atrial_value}")
                else:
                    print(f"❌ Atrial value '{atrial_value}' not found in dropdown. Selecting default 'None'")
                    atrial_dropdown.select_by_visible_text("None")  # Use correct default
            else:
                print("❌ No Atrial dropdown found.")
        except Exception as e:
            print("❌ Error selecting Atrial:", str(e))

        # Select Atrial Flutter
        try:
            time.sleep(1)
            Flutter_dropdown = WebDriverWait(div_elements[87], 20).until(
                lambda d: d.find_element(By.ID, 'arrhythaflutter')
            )
            if Flutter_dropdown:
                atrial_dropdown = Select(Flutter_dropdown)
                # atrial_dropdown.select_by_visible_text(str(row['Atrial Flutter']))
                # print(f"✅ Selected Flutter: {row['Atrial Flutter']}")
                options = [opt.text for opt in atrial_dropdown.options]
                print("🔹 Available Atrial Flutter options:", options)

                atrial_value = str(row['Atrial Flutter']).strip() if pd.notna(
                    row['Atrial Flutter']) else "None"

                # Check if the value is in the options
                if atrial_value in options:
                    atrial_dropdown.select_by_visible_text(atrial_value)
                    print(f"✅ Selected Atrial Flutter: {atrial_value}")
                else:
                    print(f"❌ Atrial value '{atrial_value}' not found in dropdown. Selecting default 'None'")
                    atrial_dropdown.select_by_visible_text("None")  # Use correct default
            else:
                print("❌ No Flutter dropdown found.")
        except Exception as e:
            print("❌ Error selecting Flutter:", str(e))

        # Select V. Tach / V. Fib
        try:
            time.sleep(1)
            Tach_dropdown = WebDriverWait(div_elements[89], 20).until(
                lambda d: d.find_element(By.ID, 'arrhythvv')
            )
            if Tach_dropdown:
                tach_dropdown = Select(Tach_dropdown)
                # tach_dropdown.select_by_visible_text(str(row['V. Tach / V. Fib']))
                # print(f"✅ Selected Tach: {row['V. Tach / V. Fib']}")
                options = [opt.text for opt in tach_dropdown.options]
                print("🔹 Available tach options:", options)

                tach_value = str(row['V. Tach / V. Fib']).strip() if pd.notna(
                    row['V. Tach / V. Fib']) else "None"

                # Check if the value is in the options
                if tach_value in options:
                    tach_dropdown.select_by_visible_text(tach_value)
                    print(f"✅ Selected tach: {tach_value}")
                else:
                    print(f"❌ tach value '{tach_value}' not found in dropdown. Selecting default 'None'")
                    tach_dropdown.select_by_visible_text("None")  # Use correct default
            else:
                print("❌ No tach dropdown found.")
        except Exception as e:
            print("❌ Error selecting tach:", str(e))

        # Select Sick Sinus Syn.
        try:
            time.sleep(1)
            Sinus_dropdown = WebDriverWait(div_elements[91], 20).until(
                lambda d: d.find_element(By.ID, 'arrhythsss')
            )
            if Sinus_dropdown:
                sinus_dropdown = Select(Sinus_dropdown)
                # sinus_dropdown.select_by_visible_text(str(row['Sick Sinus Syn.']))
                # print(f"✅ Selected Sinus: {row['Sick Sinus Syn.']}")

                options = [opt.text for opt in sinus_dropdown.options]
                print("🔹 Available Sick Sinus options:", options)

                sinus_value = str(row['Sick Sinus Syn.']).strip() if pd.notna(
                    row['Sick Sinus Syn.']) else "None"

                # Check if the value is in the options
                if sinus_value in options:
                    sinus_dropdown.select_by_visible_text(sinus_value)
                    print(f"✅ Selected Sick Sinus: {sinus_value}")
                else:
                    print(
                        f"❌ Sick Sinus Syn. value '{sinus_value}' not found in dropdown. Selecting default 'None'")
                    sinus_dropdown.select_by_visible_text("None")  # Use correct default
            else:
                print("❌ No Sinus dropdown found.")
        except Exception as e:
            print("❌ Error selecting Sinus:", str(e))

        # Select 2ⁿᵈ Degree Block
        try:
            time.sleep(1)
            Block_dropdown = WebDriverWait(div_elements[93], 20).until(
                lambda d: d.find_element(By.ID, 'arrhythsecond')
            )
            if Block_dropdown:
                block_dropdown = Select(Block_dropdown)
                # block_dropdown.select_by_visible_text(str(row['2ⁿᵈ Degree Block']))
                # print(f"✅ Selected Block: {row['2ⁿᵈ Degree Block']}")
                options = [opt.text for opt in block_dropdown.options]
                print("🔹 Available 2ⁿᵈ Degree Block options:", options)

                block_value = str(row['2ⁿᵈ Degree Block']).strip() if pd.notna(
                    row['2ⁿᵈ Degree Block']) else "None"

                # Check if the value is in the options
                if block_value in options:
                    block_dropdown.select_by_visible_text(block_value)
                    print(f"✅ Selected 2ⁿᵈ Degree Block: {block_value}")
                else:
                    print(
                        f"❌ 2ⁿᵈ Degree Block value '{block_value}' not found in dropdown. Selecting default 'None'")
                    block_dropdown.select_by_visible_text("None")  # Use correct default
            else:
                print("❌ No Block dropdown found.")
        except Exception as e:
            print("❌ Error selecting Block:", str(e))

        # Select 3ʳᵈ Degree Block
        try:
            time.sleep(1)
            Degree_dropdown = WebDriverWait(div_elements[95], 20).until(
                lambda d: d.find_element(By.ID, 'arrhyththird')
            )
            if Degree_dropdown:
                degree_dropdown = Select(Degree_dropdown)
                # degree_dropdown.select_by_visible_text(str(row['3ʳᵈ Degree Block']))
                # print(f"✅ Selected Degree: {row['3ʳᵈ Degree Block']}")
                options = [opt.text for opt in degree_dropdown.options]
                print("🔹 Available 3ʳᵈ Degree Block options:", options)

                degree_value = str(row['3ʳᵈ Degree Block']).strip() if pd.notna(
                    row['3ʳᵈ Degree Block']) else "None"

                # Check if the value is in the options
                if degree_value in options:
                    degree_dropdown.select_by_visible_text(degree_value)
                    print(f"✅ Selected 3ʳᵈ Degree Block: {degree_value}")
                else:
                    print(
                        f"❌ 3ʳᵈ Degree Block value '{degree_value}' not found in dropdown. Selecting default 'None'")
                    degree_dropdown.select_by_visible_text("None")  # Use correct default
            else:
                print("❌ No Degree dropdown found.")
        except Exception as e:
            print("❌ Error selecting Degree:", str(e))

        time.sleep(5)
        # ---- Handle Checkboxes ---- #
        check_boxes = {
            "ACE Inhibitors/ARBs ≤ 48 hrs": "medacei48",
            "GP IIb/IIIa Inhibitor ≤ 24 hrs": "medgp",
            "Inotropes ≤ 48 hrs": "medinotr",
            "Steroids ≤ 24 hrs": "medster",
            "ADP Inhibitors ≤ 5 days": "medadp5days",
            "Family Hx of CAD": "fhcad",
            "Hypertension": "hypertn",
            "Liver Disease": "liverdis",
            "Mediastinal Radiation": "mediastrad",
            "Unresponsive State": "unrespstat",
            "Dialysis": "dialysis",
            "Cancer ≤ 5 yrs": "cancer",
            "Syncope": "syncope",
            "Immunocompromised": "immsupp",
            "Recent Pneumonia": "pneumonia",
            "Sleep Apnea": "slpapn",
            "Home O₂": "hmo2",
            "Peripheral Artery Disease": "pvd",
            "Right Carotid Sten. ≥ 80%": "cvdstenrt",
            "Prior Carotid Surgery": "cvdpcarsurg",
            "Left Carotid Sten. ≥ 80%": "cvdstenlft",
            "Cardiogenic Shock": "carshock",
            "Resuscitation ≤ 1hr": "resusc",
            "Aortic Stenosis": "vdstena",
            "Mitral Stenosis": "vdstenm",
            "Aortic Root Abscess": "vdaoprimet",
        }

        # Handling standard checkboxes
        for label, checkbox_id in check_boxes.items():
            try:
                time.sleep(3)
                checkbox = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.ID, checkbox_id))
                )
                time.sleep(2)

                if str(row[label]).strip().upper() == "TRUE":
                    if not checkbox.is_selected():  # Ensure we don't double-check
                        checkbox.click()
                        print(f"✅ Checked {label}")
                else:
                    print(f"✅ {label} remains unchecked")

            except Exception as e:
                print(f"❌ Error selecting {label}: {e}")

        button_checkboxes = ["CABG", "Valve", "PCI", "Other"]  # List of button-style checkboxes

        for label in button_checkboxes:
            try:
                time.sleep(2)
                # Wait for the button that contains the checkbox
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"//button[contains(., '{label}')]"))
                )
                time.sleep(2)

                # Find the associated input (modify this based on the actual structure)
                checkbox_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"//button[contains(., '{label}')]/input"))
                )

                # Check if it needs to be selected
                if str(row[label]).strip().upper() == "TRUE":
                    if not checkbox_input.is_selected():
                        driver.execute_script("arguments[0].click();", button)  # Use JS click
                        print(f"✅ Checked {label}")
                else:
                    print(f"✅ {label} remains unchecked")

            except Exception as e:
                print(f"❌ Error selecting {label}: {e}")

        # Click PDF button
        try:
            time.sleep(7)
            pdf_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "btn-capture-screenshot-pdf"))
            )
            time.sleep(3)
            pdf_button.click()
            print("✅ PDF download initiated.")
        except Exception as e:
            print("❌ Error clicking PDF button:", str(e))

        # Click Copy button
        try:
            time.sleep(5)
            copy_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "copybuttonestimates"))
            )
            time.sleep(3)
            copy_button.click()
            print("✅ Copy button clicked.")
        except Exception as e:
            print("❌ Error clicking Copy button:", str(e))

        # Retrieve copied text
        time.sleep(3)  # Wait a bit for the clipboard to update
        copied_text = pyperclip.paste()
        print(f"📋 Copied Text:\n{copied_text}")

        try:
            time.sleep(2)
            reset_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'reset'))
            )
            time.sleep(5)
            reset_button.click()
            print('RESET clicked.')
        except Exception as e:
            print('❌ Error clicking Reset button:', str(e))

        # Handle Terms of Service Modal
        try:
            time.sleep(6)
            accept_button = WebDriverWait(driver, 80).until(
                EC.element_to_be_clickable((By.XPATH, '//button[text()="Accept"]'))
            )
            accept_button.click()
            print("✅ Accepted Terms of Service.")
        except Exception as e:
            print("⚠️ No modal found or issue clicking 'Accept':", e)

        # Save copied text to a PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, copied_text)
        pdf_file_path = f"/mnt/windows/Fatima/temp/MrArian/Copy/copied_data_{index}.pdf"
        pdf.output(pdf_file_path)
        print(f"📄 PDF saved: {pdf_file_path}")

    except Exception as e:
        print(f"❌ Error processing row {index}: {e}")

# Wait for downloads to complete
time.sleep(10)

# Close the browser
driver.quit()
print("\n🎉 All rows processed! Browser closed.")