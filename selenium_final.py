from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# Initialize the WebDriver (Chrome)
driver = webdriver.Chrome()

try:
    # Open Google
    driver.get("https://www.google.com")
    wait = WebDriverWait(driver, 10)

    # Handle any pop-ups (like cookies or notifications)
    try:
        not_now_buttons = driver.find_elements(By.XPATH, "//button[contains(., 'Not now') or contains(., 'No')]")
        for button in not_now_buttons:
            button.click()
    except NoSuchElementException:
        print("No pop-up to dismiss.")

    # Find the search box, input query, and hit ENTER
    search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
    query = "Bowie State University"  # Search query
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # Allow results to load

    # Locate search result containers
    search_results = driver.find_elements(By.XPATH, "//div[@class='tF2Cxc']")

    # Ensure we fetch at least 10 results
    print("Top 10 Search Results (Titles and Links):")
    count = 0
    for result in search_results:
        try:
            title = result.find_element(By.TAG_NAME, "h3").text  # Extract title
            link = result.find_element(By.TAG_NAME, "a").get_attribute("href")  # Extract link
            print(f"{count+1}. {title}\n   {link}")
            count += 1
        except NoSuchElementException:
            continue
        if count >= 10:  # Stop after printing 10 results
            break

    if count < 10:
        print(f"Only found {count} results.")

except TimeoutException:
    print("Page took too long to load.")
except Exception as e:
    print("An error occurred:", e)

finally:
    # Close the browser
    driver.quit()
