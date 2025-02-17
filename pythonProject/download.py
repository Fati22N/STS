from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pyperclip
import time
from fpdf import FPDF
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def setup_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": "/mnt/windows/Fatima/temp/MrArian/Copy",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def accept_terms(driver):
    try:
        WebDriverWait(driver, 80).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="Accept"]'))
        ).click()
        logging.info("✅ Accepted Terms of Service.")
    except Exception as e:
        logging.warning("⚠️ No modal found or issue clicking 'Accept': %s", e)

def fill_form(driver, row):
    # Define the filling process here, using helper functions for each section
    pass

def download_pdf(driver):
    try:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn-capture-screenshot-pdf"))
        ).click()
        logging.info("✅ PDF download initiated.")
    except Exception as e:
        logging.error("❌ Error clicking PDF button: %s", e)

def copy_to_clipboard(driver):
    try:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "copybuttonestimates"))
        ).click()
        logging.info("✅ Copy button clicked.")
        time.sleep(3)  # Wait for clipboard to update
        return pyperclip.paste()
    except Exception as e:
        logging.error("❌ Error clicking Copy button: %s", e)
        return None

def save_to_pdf(copied_text, index):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, copied_text)
    pdf_file_path = f"/mnt/windows/Fatima/temp/MrArian/Copy/copied_data_{index}.pdf"
    pdf.output(pdf_file_path)
    logging.info("📄 PDF saved: %s", pdf_file_path)

def main():


    driver.quit()
    logging.info("🎉 All rows processed! Browser closed.")


if __name__ == "__main__":
    main()