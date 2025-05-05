from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time, datetime
import pandas as pd
from pathlib import Path

# url format of justjoin.it:
# https://justjoin.it/job-offers/location?keyword=position
# where location and position are variables

def setup_driver(headless=True):
    try:
        options = Options()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--incognito")
        options.add_argument("start-maximized")
        options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        options.add_experimental_option("useAutomationExtension", False)
        service = Service()
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(4)
        return driver
    except Exception as e:  
        print(f"Driver setup error: {e}")
        return None


def driver_setup_search(driver:webdriver.Chrome, location:str, position:str):
    try:
        
        base_url = "https://justjoin.it/job-offers"
        location_param = location.lower().replace(' ', '-')
        position_param = position.lower().replace(' ', '-')
        url = f"{base_url}/{location_param}?keyword={position_param}&with-salary=yes"
        driver.get(url)
        time.sleep(2)  # Attendre que la page se charge
        return driver
    except Exception as e:
        print(f"Error driver setup search: {e}")
        if driver:
            driver.quit()
        return None

def search_jobs(driver:webdriver.Chrome):
    try:
        current_url = driver.current_url
        if "justjoin.it" not in current_url:
            yield None, None

        jobs = driver.find_elements(By.CLASS_NAME, "MuiBox-root.css-7k63si")
        print(f"Found {len(jobs)} jobs")
        for job in jobs:
            try:
                parent_element = job.find_element(By.XPATH, "./..")
                job_url = parent_element.get_attribute('href')
                if not job_url:
                    anchor_element = job.find_element(By.XPATH, ".//a")
                    job_url = anchor_element.get_attribute('href')
                if job_url:
                    yield job_url, job
                else:
                    yield None, None
            except Exception as e:
                yield None, None    
                
                
    except Exception as e:
        print(f"Error in search_jobs: {e}")
        yield None, None
    finally:
        if driver:
            driver.quit()  # Fermer le driver seulement après avoir terminé la recherche

def apply_to_job(driver:webdriver.Chrome, job_url:str, job:str):
    driver.get(job_url)
    time.sleep(2)
    try: 
        # Handle cookie, because it's a popup
        try:
            cookie_dialog = driver.find_element(By.ID, "cookiescript_injected_wrapper")
            cookie_accept = cookie_dialog.find_element(By.ID, "cookiescript_accept")
            cookie_accept.click()
            time.sleep(1)  
        except Exception as e:
            print("Cookie dialog not found", e)
        try:
            apply_button = driver.find_element(By.CSS_SELECTOR, "button[name='floating_apply_button']")
            print("Apply button found 1")
        except:
            try:
                apply_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Apply')]")
                print("Apply button found 2")
            except:
                apply_button = driver.find_element(By.XPATH, "//button[contains(@class, 'MuiButton-solidPrimary')][.//div[contains(text(), 'Apply')]]")
                print("Apply button found 3")
        apply_button.click()
        print("Applied to job")
        yield True
    except Exception as e:
        print(f"Error applying to job: {e}")
        yield False
        
        
def create_csv(is_applied:bool, job:str, job_url:str) :
    new_row = pd.DataFrame({
        'job': [job.text],
        'date': [datetime.datetime.now().strftime('%Y-%m-%d')],
        'url': [job_url],
        'status': ['Not applied' if not is_applied else 'Applied']
    })
    
    if not Path('applied_jobs.csv').exists():
        new_row.to_csv('applied_jobs.csv', index=False)
    else:
        new_row.to_csv('applied_jobs.csv', mode='a', header=False, index=False)
