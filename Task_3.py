# https://books.toscrape.com/

from playwright.sync_api import sync_playwright
import pandas as pd

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  
    page = browser.new_page()
    page.goto("https://books.toscrape.com/")
    page.wait_for_timeout(4000)

    book_data = []
    articles = page.query_selector_all('article.product_pod')

    for article in articles:
        title = article.query_selector('h3 > a').get_attribute('title')
        price = article.query_selector('.price_color').inner_text().replace('£', '')
        rating_class = article.query_selector('.star-rating').get_attribute('class')

        rating = {
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'Five': 5
        }.get(rating_class.split()[-1], 0)

        book_data.append({
            'Title': title,
            'Price (£)': price,
            'Rating (1-5)': rating
        })

    df = pd.DataFrame(book_data)
    df.to_csv('books.csv', index=False)
    print(df)

    browser.close()