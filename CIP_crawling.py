# All imports. Use "pip install -r requirements.txt" if the required libraries are not installed.
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from bs4 import BeautifulSoup
from lxml import etree
import re
from tqdm.notebook import tqdm
import pandas as pd


def crawl_for_links(url = "https://www.galaxus.ch/en/s2/producttype/robot-vacuum-cleaners-174?take=204", print_i = True,
                    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"):
    """
    Opens a Galaxus product search link and iterates through all products,
    scraping their individual product URLs.

    Parameters:
        url (str): URL of the product search page on galaxus.ch
        print_i (bool): If True, prints the first 5 scraped product URLs

    Returns:
        list: A list of product URLs
    """
    # Start "undetectable" Chrome
    options = uc.ChromeOptions()
    options.add_argument("--no-first-run --no-service-autorun --password-store=basic")
    options.add_argument(f"user-agent={user_agent}")

    # To ensure we aren't detected as a bot
    driver = uc.Chrome(options=options, headless=False)

    driver.get(url)

    # Wait for the first page to load
    time.sleep(random.uniform(2, 3))

    # Scroll down to load lazy-loaded items
    scroll_height = 0
    scroll_step = 2000
    new_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Perform scrolling
        driver.execute_script(f"window.scrollTo({scroll_height}, {scroll_height + scroll_step});")
        time.sleep(random.uniform(0.2, 0.4))
        scroll_height += scroll_step
        new_height = driver.execute_script("return document.body.scrollHeight")
        # If we reach the bottom
        if new_height < scroll_height:
            try:
                # Select the button to click
                show_more = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "productListFooter_styled_StyledLoadMoreButton")]'))
                )
                # Scroll to the correct position to click the button
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", show_more)
                time.sleep(random.uniform(1, 2))
                show_more.click()
                print("Clicked button")
                time.sleep(random.uniform(0.5, 1))
                # Scroll back up to continue the process
                scroll_height -= 8000
                driver.execute_script(f"window.scrollTo({scroll_height}, {scroll_height - 8000});")
            except:
                # Exit the loop normally
                print("No more buttons found.")
                break

    # Save the HTML source for parsing
    soup = BeautifulSoup(driver.page_source, 'lxml')
    urls = []

    # Collect all product links into a list
    for a in soup.find_all("a", href=True):
        href = a["href"]
        # Only include product links
        if href.startswith("/en/s2/product/"):
            full_url = "https://www.galaxus.ch" + href
            if full_url not in urls:
                urls.append(full_url)

    if print_i:
        # For testing: print a few product URLs
        print(f"\nFound {len(urls)} product URLs.")
        for u in urls[:5]: print(u)

    driver.quit()
    return urls
    
    

def crawl_for_product_data(urls,
                           user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"):
    """
    Takes a list of Galaxus product URLs and scrapes each product page individually.
    For each product, the following information is extracted:
    - Name
    - Price
    - Rating
    - Rating count
    - All specifications from the product details table

    Parameters:
        urls (list): A list of product URLs from galaxus.ch

    Returns:
        dict: A dictionary containing the scraped data for each product
    """
    data = dict()
    # Start "undetectable" Chrome
    options = uc.ChromeOptions()
    options.add_argument("--no-first-run --no-service-autorun --password-store=basic")
    options.add_argument(f"user-agent={user_agent}")

    # To ensure we aren't detected as a bot
    driver = uc.Chrome(options=options, headless=False)

    # Test URLs (optional)
    # urls = ["https://www.galaxus.ch/en/s2/product/roborock-s8-maxv-ultra-vacuum-mopping-robot-robot-vacuum-cleaners-43695849", "https://www.galaxus.ch/en/s2/product/dreame-x50-ultra-complete-vacuum-mopping-robot-robot-vacuum-cleaners-53898301"]

    for i, url in tqdm(enumerate(urls), total=len(urls)):
        try:
            driver.get(url)
            time.sleep(random.uniform(3, 4))

            soup = BeautifulSoup(driver.page_source, 'lxml')
            dom = etree.HTML(str(soup))

            # Here we tried using XPath. Maybe it would have been better to stick with BeautifulSoup,
            # because we ended up handling many exceptions.
            # We assumed base product info would always be in the same place—which turned out to be incorrect.

            name_element = dom.xpath('//*[@id="pageContent"]/div/div[1]/div/div/div[2]/div/div[1]/div/h1')
            name = name_element[0].xpath("string()")



            # extracting the price
            try:
                price_element = dom.xpath('//*[@id="pageContent"]/div/div[1]/div/div/div[2]/div/div[1]/span/strong/button/text()')
                price_float = float(re.sub(r"[^\d]", "", price_element[0]))
            except:
                # This block handles cases where the product is a returned item
                price_element = dom.xpath('//*[@id="pageContent"]/div/div[1]/div[1]/div/div[2]/div/div[1]/span/strong/text()')
                price_float = float(re.sub(r"[^\d]", "", price_element[0]))
            
            
            if data.get(str(name)) is None:
                data[str(name)] = dict()
            else:
                # If only the color changes, we overwrite the previous entry since the data is similar.
                # We rename the old entry to preserve both.
                data[name + "_" + str(data.get(name).get("price"))] = data.get(name)
                data.pop(name)
                # create the new one
                name = name + "_" + str(price_float)
                data[name] = dict()
                
            data.get(name).update({"price" : price_float})

            # extracting the rating
            try:
                rating_element = dom.xpath('//*[@id="pageContent"]/div/div[1]/div/div/div[2]/div/div[2]/div[1]/a/span[3]')                   
                rating_float = float(rating_element[0].get("aria-label").split()[0])
            except:
                try:
                    # Just a small variation—likely when there's an additional price reduction window
                    rating_element = dom.xpath('//*[@id="pageContent"]/div/div[1]/div/div/div[2]/div/div[3]/div[1]/a/span[3]')
                    rating_float = float(rating_element[0].get("aria-label").split()[0])
                except:
                    # Happens if there is no rating available
                    rating_float = None
            data.get(name).update({"rating" : rating_float})

            # extracting the rating
            try:
                rating_count_element = dom.xpath('//*[@id="pageContent"]/div/div[1]/div/div/div[2]/div/div[2]/div[1]/a/span[1]')
                rating_count_int = int(rating_count_element[0].xpath("string()"))
            except:
                try:
                    # only a small change, I thing it happens when there is an additional price reduction window
                    rating_count_element = dom.xpath('//*[@id="pageContent"]/div/div[1]/div/div/div[2]/div/div[3]/div[1]/a/span[1]')
                    rating_count_int = int(rating_count_element[0].xpath("string()"))
                except:
                    # happens if there is no rating
                    rating_float = None
            data.get(name).update({"rating_count" : rating_count_int})

            # Here we used only BeautifulSoup
            # Use partial class matching for tables
            for table in soup.find_all("table"):
                # Optionally filter only those with captions you care about
                caption_tag = table.find("caption")
                if not caption_tag:
                    continue
                table_name = caption_tag.get_text(strip=True)
                for row in table.find_all("tr"):
                    cells = row.find_all("td")
                    if len(cells) != 2:
                        continue
                    key = cells[0].get_text(separator=" ", strip=True)
                    value_spans = cells[1].find_all("span")
                    if not value_spans:
                        value = cells[1].get_text(" ", strip=True)
                    else:
                        value = ", ".join([v.get_text(" ", strip=True) for v in value_spans])
                    value = value.replace("\xa0", " ")
                    data.get(name).update({table_name + "  " + key : value})
            # Clear cookies after each iteration
            driver.delete_all_cookies()
        except:
            # If something goes wrong or the site couldn't load for some reason
            # Not the cleanest way to handle it, but the last run didn’t report any issues
            print(f"There was a Problem with: {i} {url}")
            pass

    driver.quit()
    return data



def data_to_csv(data, save = True):
    """
    Converts the data from a dictionary to a pandas DataFrame
    and saves the DataFrame as a .csv file.

    Parameters:
        data (dict): A dictionary containing the scraped data for each product
        save (bool): If True, saves the DataFrame as a CSV file

    Returns:
        pandas.DataFrame: The resulting DataFrame created from the dictionary
    """
    # Convert the dictionary to a DataFrame and move the product name into a column
    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.reset_index().rename(columns={"index": "product_name"})
    print(df.shape)
    # Save as a CSV file
    if save:
        df.to_csv("robot_vacuums.csv", index=False)
    return df