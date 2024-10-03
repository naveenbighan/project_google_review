
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as BS
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

url = "https://www.google.com/search?q=microsoft&sca_esv=76e0d290b07efa55&sca_upv=1&biw=1440&bih=778&tbm=lcl&sxsrf=ADLYWIJ6ka1A564FIGrAYZngF0Vwr08X6A%3A1727790669434&ei=Tf77Ztr3GYeZ4-EPrqP4yAI&ved=0ahUKEwia0uPoqe2IAxWHzDgGHa4RHikQ4dUDCAk&uact=5&oq=microsoft&gs_lp=Eg1nd3Mtd2l6LWxvY2FsGgIYAyIJbWljcm9zb2Z0MgQQIxgnMhAQABiABBixAxhDGPQFGIoFMg0QABiABBixAxhDGIoFMhAQABiABBixAxhDGIMBGIoFMg0QABiABBixAxhDGIoFMgoQABiABBhDGIoFMg0QABiABBixAxhDGIoFMgoQABiABBhDGIoFMhEQABiABBixAxiDARj0BRiLAzIOEAAYgAQYsQMY8wUYiwNI7akEUNvXA1iqhwRwAngAkAEAmAGXAqAB0g-qAQUwLjkuM7gBA8gBAPgBAZgCDqACrBCoAgrCAgUQABiABMICCxAAGIAEGLEDGIMBwgIIEAAYgAQYsQPCAgcQIxgnGOoCwgIREAAYgAQYsQMYgwEY8wUYiwPCAg4QABiABBixAxiDARiLA8ICCxAAGIAEGPQFGIsDwgIUEAAYgAQYsQMYgwEY8wUYigUYiwPCAg0QABiABBhDGIoFGIsDwgILEAAYgAQY8wUYiwPCAhMQABiABBixAxhDGPQFGIoFGIsDwgIWEAAYgAQYsQMYQxiDARjzBRiKBRiLA8ICExAAGIAEGLEDGEMY8wUYigUYiwPCAhMQABiABBixAxhDGIMBGIoFGIsDmAMEiAYBkgcFMi45LjOgB7FY&sclient=gws-wiz-local#lkt=LocalPoiReviews&rlfi=hd:;si:10230897090469711344,l,CgltaWNyb3NvZnQiA4gBAUibu5qX7qqAgAhaDxAAGAAiCW1pY3Jvc29mdJIBEGNvcnBvcmF0ZV9vZmZpY2WqAUwKCi9tLzBxdDE3OHEQASoNIgltaWNyb3NvZnQoADIeEAEiGlZelj03UsnupJDoA5Sevz3rOlj3uMMXbaLsMg0QAiIJbWljcm9zb2Z0;mv:[[13.094729,77.7142424],[12.9037635,77.5240872]]"

driver.get(url)

time.sleep(5)

try:
    scrollable_div = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.ifM9O'))
    )
    print("Scrollable div found, attempting to scroll...")
except Exception as e:
    print(f"Error: {e}")
    driver.quit()
    exit()

def scroll_specific_div(driver, scrollable_div, scrolls=500, scroll_pause_time=2):
    reviews_data = []  
    overall_rating = None

    for i in range(scrolls):
        driver.execute_script("arguments[0].scrollBy(0, 1000);", scrollable_div)
        time.sleep(scroll_pause_time)

        html = driver.page_source
        soup = BS(html, 'html.parser')

        divs = soup.find_all("div", class_="OA1nbd")
        names = soup.find_all("div", class_="Vpc5Fe") 
        for div, name in zip(divs, names):
            review_text = div.get_text().strip()
            name_text = name.get_text().strip()
            if review_text and name_text:
                reviews_data.append({"Name": name_text, "Review": review_text})

        if not overall_rating:
            rating_div = soup.find("div", class_="PLxO5 VDgVie")
            if rating_div:
                rating_span = rating_div.find("span", class_="fzTgPe Aq14fc")
                if rating_span:
                    overall_rating = rating_span.get_text().strip()

        print(f"Scroll {i + 1} done")
    
    return reviews_data, overall_rating

all_reviews, overall_rating = scroll_specific_div(driver, scrollable_div, scrolls=50)

driver.quit()

df = pd.DataFrame(all_reviews)

df['Overall Company Rating'] = overall_rating
dduplicate=df.drop_duplicates()

df.to_csv("Microsoft2.csv", index=False)

print(f"CSV file 'reviews_and_ratings.csv' created successfully with {len(df)} reviews.")
