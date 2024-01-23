from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By


# define the website to scrape and path where the chromediver is located
web = "https://www.audible.in/adblbestsellers"
# define 'driver' variable
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
driver.get(web)

# The first website has 5 pages while the second has 60. Test the code with any of them
driver.maximize_window()

# Pagination 1
pagination = driver.find_element(by='xpath', value='//ul[contains(@class, "pagingElements")]')
pages = pagination.find_elements(By.TAG_NAME ,'li')
last_page = int(pages[-2].text)  # getting the last page with negative indexing (starts from where the array ends)

book_title = []
book_author = []
book_length = []

# Pagination 2
current_page = 1   # this is the page the bot starts scraping

# The while loop below will work until the the bot reaches the last page of the website, then it will break
while current_page <= last_page:
    time.sleep(2)  # let the page render correctly
    container = driver.find_element(By.CLASS_NAME, 'adbl-impression-container ')
    products = container.find_elements(By.XPATH, './/li[contains(@class, "productListItem")]')


    for product in products:
        book_title.append(product.find_element(By.XPATH, './/h3[contains(@class, "bc-heading")]').text)
        book_author.append(product.find_element(By.XPATH, './/li[contains(@class, "authorLabel")]').text)
        book_length.append(product.find_element(By.XPATH, './/li[contains(@class, "runtimeLabel")]').text)

    current_page = current_page + 1  # increment the current_page by 1 after the data is extracted
    # Locating the next_page button and clicking on it. If the element isn't on the website, pass to the next iteration
    try:

        next_page = driver.find_element(By.XPATH, './/span[contains(@class , "nextButton")]')
        next_page.click()
    except:
        pass

driver.quit()

df_books = pd.DataFrame({'title': book_title, 'author': book_author, 'length': book_length})
df_books.to_csv('books_pagination.csv', index=False)
