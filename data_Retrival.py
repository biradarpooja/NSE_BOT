from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import time
from datetime import datetime

# Step 1: Get today's date dynamically in the required format
today_date = datetime.now().strftime("%d-%b-%Y")  # Example: "18-Nov-2024"

# Step 2: Specify the base download folder
base_download_folder = r"C:\Users\birad\OneDrive\Desktop\NSE BOT\dow_nse_report"

# Step 3: Create a subfolder named with today's date
download_folder = os.path.join(base_download_folder, today_date)

if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# Step 4: Set up Chrome options with download preferences and user agent
chrome_options = Options()
prefs = {
    "download.default_directory": download_folder,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True,
}
chrome_options.add_experimental_option("prefs", prefs)

# Update user agent and add necessary options
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-infobars")

# Specify the path to the ChromeDriver executable
service = Service(executable_path=r"C:\Windows\chromedriver.exe")

# Step 5: Initialize WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Step 6: Navigate to the NSE URL
    url = "https://www.nseindia.com/all-reports"  # Replace with the correct URL
    driver.get(url)
    print(f"Searching for reports for the date: {today_date}")

    # Step 7: Locate the date element
    print("Waiting for the date element to be visible...")
    date_element = WebDriverWait(driver, 40).until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//span[contains(@id, 'cr_equity_currentDate') and contains(text(), '{today_date}')]")
        )
    )
    print("Date found successfully!")

    # Step 8: Locate the section containing the reports (checkboxes)
    print("Locating the section with checkboxes...")
    report_section = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'report-section')]"))  # Adjust as needed
    )

    # Step 9: Locate all checkboxes within the report section
    print("Locating checkboxes within the report section...")
    checkboxes = report_section.find_elements(By.XPATH, ".//span[contains(@class, 'checkmark')]")
    print(f"Checkboxes found: {len(checkboxes)}")

    if not checkboxes:
        raise Exception("No checkboxes found for today's reports.")

    # Step 10: Ensure all checkboxes are selected
    for checkbox in checkboxes:
        # Verify if the checkbox is already selected
        associated_input = checkbox.find_element(By.XPATH, "./preceding-sibling::input")
        if not associated_input.is_selected():
            driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(1)  # Brief delay between clicks

    # Step 11: Locate the "Download All" button
    print("Locating the download button...")
    download_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@class="link ms-3"]'))  # Adjust XPath
    )
    # Simulate pressing the download button
    driver.execute_script("arguments[0].click();", download_button)

    # Step 12: Wait for downloads to complete
    print("Waiting for downloads to complete...")
    time.sleep(30)

    # Step 13: Verify downloads (check if the files are in the folder)
    downloaded_files = [f for f in os.listdir(download_folder) if today_date in f]

    if not downloaded_files:
        raise Exception(f"No reports downloaded for the date {today_date}.")
    else:
        for file in downloaded_files:
            print(f"Downloaded: {file}")

except Exception as e:
    print("Error occurred:", str(e))

finally:
    # Step 14: Close the driver
    driver.quit()
