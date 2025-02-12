from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests

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
                incidenc_dropdown = WebDriverWait(div_elements[3], 20).until(
                    EC.presence_of_element_located((By.ID, 'incidenc'))
                )
                if incidenc_dropdown:
                    surgery_dropdown = Select(incidenc_dropdown)
                    surgery_dropdown.select_by_visible_text(str(row['Surgery Incidence']))
                    print(f"✅ Selected Incidence: {row['Surgery Incidence']}")
                else:
                    print("❌ No incidenc dropdown found.")
            except Exception as e:
                print("❌ Error selecting Surgery Incidence:", str(e))

            # Select Surgical Priority
            try:
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
            Alcohol_dropdown = WebDriverWait(div_elements[41], 20).until(
                lambda d: d.find_element(By.ID, 'alcohol')
            )
            if Alcohol_dropdown:
                alcohol_dropdown = Select(Alcohol_dropdown)
                alcohol_dropdown.select_by_visible_text(str(row['Alcohol Use']))
                print(f"✅ Selected Alcohol: {row['Alcohol Use']}")
            else:
                print("❌ No Alcohol Use dropdown found.")
        except Exception as e:
            print("❌ Error selecting Alcohol Use:", str(e))

        # Select Tobacco Use
        try:
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
            Heart_dropdown = WebDriverWait(div_elements[57], 20).until(
                lambda d: d.find_element(By.ID, 'heartfailtmg')
            )
            if Heart_dropdown:
                heart_dropdown = Select(Heart_dropdown)
                heart_dropdown.select_by_visible_text(str(row['Heart Failure']))
                print(f"✅ Selected Heart Failure: {row['Heart Failure']}")
            else:
                print("❌ No Heart Failure dropdown found.")
        except Exception as e:
            print("❌ Error selecting Heart Failure:", str(e))

        # Select NYHA Classification
        try:
            NYHA_dropdown = WebDriverWait(div_elements[59], 20).until(
                lambda d: d.find_element(By.ID, 'classnyh')
            )
            if NYHA_dropdown:
                NYHA_dropdown = Select(NYHA_dropdown)
                NYHA_dropdown.select_by_visible_text(str(row['NYHA Classification']))
                print(f"✅ Selected NYHA: {row['NYHA Classification']}")
            else:
                print("❌ No NYHA dropdown found.")
        except Exception as e:
            print("❌ Error selecting NYHA:", str(e))

        # Select PreOp Mech Circ Support
        try:
            PreOp_dropdown = WebDriverWait(div_elements[61], 20).until(
                lambda d: d.find_element(By.ID, 'mcs')
            )
            if PreOp_dropdown:
                PreOp_dropdown = Select(PreOp_dropdown)
                PreOp_dropdown.select_by_visible_text(str(row['PreOp Mech Circ Support']))
                print(f"✅ Selected PreOp: {row['PreOp Mech Circ Support']}")
            else:
                print("❌ No PreOp dropdown found.")
        except Exception as e:
            print("❌ Error selecting PreOp:", str(e))

        # Input Ejection Fraction (%)
        try:
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
            Aortic_dropdown = WebDriverWait(div_elements[77], 20).until(
                lambda d: d.find_element(By.ID, 'vdinsufa')
            )
            if Aortic_dropdown:
                aortic_dropdown = Select(Aortic_dropdown)
                aortic_dropdown.select_by_visible_text(str(row['Aortic Regurgitation']))
                print(f"✅ Selected Aortic: {row['Aortic Regurgitation']}")
            else:
                print("❌ No Aortic dropdown found.")
        except Exception as e:
            print("❌ Error selecting Aortic:", str(e))

        # Select Miteral Regurgitation
        try:
            Mitral_dropdown = WebDriverWait(div_elements[79], 20).until(
                lambda d: d.find_element(By.ID, 'vdinsufm')
            )
            if Mitral_dropdown:
                mitral_dropdown = Select(Mitral_dropdown)
                mitral_dropdown.select_by_visible_text(str(row['Mitral Regurgitation']))
                print(f"✅ Selected Mitral: {row['Mitral Regurgitation']}")
            else:
                print("❌ No Mitral dropdown found.")
        except Exception as e:
            print("❌ Error selecting Mitral:", str(e))

        # Select Tricuspid Regurgitation
        try:
            Tricuspid_dropdown = WebDriverWait(div_elements[81], 20).until(
                lambda d: d.find_element(By.ID, 'vdinsuft')
            )
            if Tricuspid_dropdown:
                tricuspid_dropdown = Select(Tricuspid_dropdown)
                tricuspid_dropdown.select_by_visible_text(str(row['Tricuspid Regurgitation']))
                print(f"✅ Selected Tricuspid: {row['Tricuspid Regurgitation']}")
            else:
                print("❌ No Tricuspid dropdown found.")
        except Exception as e:
            print("❌ Error selecting Tricuspid:", str(e))

        # Select Atrial Fibrillation
        try:
            Atrial_dropdown = WebDriverWait(div_elements[83], 20).until(
                lambda d: d.find_element(By.ID, 'arrhythatrfib')
            )
            if Atrial_dropdown:
                atrial_dropdown = Select(Atrial_dropdown)
                atrial_dropdown.select_by_visible_text(str(row['Atrial Fibrillation']))
                print(f"✅ Selected Atrial: {row['Atrial Fibrillation']}")
            else:
                print("❌ No Tricuspid dropdown found.")
        except Exception as e:
            print("❌ Error selecting Tricuspid:", str(e))

        # Select Atrial Flutter
        try:
            Flutter_dropdown = WebDriverWait(div_elements[87], 20).until(
                lambda d: d.find_element(By.ID, 'arrhythaflutter')
            )
            if Flutter_dropdown:
                atrial_dropdown = Select(Flutter_dropdown)
                atrial_dropdown.select_by_visible_text(str(row['Atrial Flutter']))
                print(f"✅ Selected Flutter: {row['Atrial Flutter']}")
            else:
                print("❌ No Flutter dropdown found.")
        except Exception as e:
            print("❌ Error selecting Flutter:", str(e))

        # Select V. Tach / V. Fib
        try:
            Tach_dropdown = WebDriverWait(div_elements[89], 20).until(
                lambda d: d.find_element(By.ID, 'arrhythvv')
            )
            if Tach_dropdown:
                tach_dropdown = Select(Tach_dropdown)
                tach_dropdown.select_by_visible_text(str(row['V. Tach / V. Fib']))
                print(f"✅ Selected Tach: {row['V. Tach / V. Fib']}")
            else:
                print("❌ No Flutter dropdown found.")
        except Exception as e:
            print("❌ Error selecting Flutter:", str(e))

        # Select Sick Sinus Syn.
        try:
            Sinus_dropdown = WebDriverWait(div_elements[91], 20).until(
                lambda d: d.find_element(By.ID, 'arrhythsss')
            )
            if Sinus_dropdown:
                sinus_dropdown = Select(Sinus_dropdown)
                sinus_dropdown.select_by_visible_text(str(row['Sick Sinus Syn.']))
                print(f"✅ Selected Sinus: {row['Sick Sinus Syn.']}")
            else:
                print("❌ No Sinus dropdown found.")
        except Exception as e:
            print("❌ Error selecting Sinus:", str(e))

        # Select 2ⁿᵈ Degree Block
        try:
            Block_dropdown = WebDriverWait(div_elements[93], 20).until(
                lambda d: d.find_element(By.ID, 'arrhythsecond')
            )
            if Block_dropdown:
                block_dropdown = Select(Block_dropdown)
                block_dropdown.select_by_visible_text(str(row['2ⁿᵈ Degree Block']))
                print(f"✅ Selected Block: {row['2ⁿᵈ Degree Block']}")
            else:
                print("❌ No Block dropdown found.")
        except Exception as e:
            print("❌ Error selecting Block:", str(e))

        # Select 3ʳᵈ Degree Block
        try:
            Degree_dropdown = WebDriverWait(div_elements[95], 20).until(
                lambda d: d.find_element(By.ID, 'arrhyththird')
            )
            if Degree_dropdown:
                degree_dropdown = Select(Degree_dropdown)
                degree_dropdown.select_by_visible_text(str(row['3ʳᵈ Degree Block']))
                print(f"✅ Selected Degree: {row['3ʳᵈ Degree Block']}")
            else:
                print("❌ No Degree dropdown found.")
        except Exception as e:
            print("❌ Error selecting Degree:", str(e))

        # ---- Handle Checkboxes ---- #
        checkboxes = {
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
            # ---- SHOULD BE FIGURED THEY SRE DIFFERENT ---- #
            # "CABG": ,
            # "Valve",
            # "PCI",
            # "Other",

        }

        for label, checkbox_id in checkboxes.items():
            try:
                checkbox = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, checkbox_id))
                )

                if str(row[label]).strip().upper() == "TRUE":
                    if not checkbox.is_selected():  # Ensure we don't double-check
                        checkbox.click()
                        print(f"✅ Checked {label}")
                else:
                    print(f"❌ {label} remains unchecked")

            except Exception as e:
                print(f"❌ Error selecting {label}: {e}")





        # Check Hypertension if applicable
        # if str(row['Hypertension']).strip().lower() == 'true':
        #     driver.find_element(By.NAME, 'hypertension').click()
        #     print("✅ Checked Hypertension.")
        #
        # # Submit the form
        # driver.find_element(By.ID, 'submit_button').click()
        # print("🚀 Form Submitted.")

        # Wait for PDF link
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
