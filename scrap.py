# import asyncio
# from playwright.async_api import async_playwright

# async def run(playwright):
#     browser = await playwright.chromium.launch()
#     page = await browser.new_page()
#     await page.goto('https://www.amazon.com')
#     await page.fill('#twotabsearchtextbox', 'laptop')
#     await page.press('#twotabsearchtextbox', 'Enter')
#     await page.wait_for_function('document.querySelectorAll(".s-main-slot .s-result-item h2.a-size-medium.a-color-base.a-text-normal").length > 0')
#     products = await page.query_selector_all('.s-main-slot .s-result-item h2.a-size-medium.a-color-base.a-text-normal')
#     print(f"Found {len(products)} products")
#     for product in products:
#         title = await product.text_content()
#         print(title)

#     await browser.close()

# async def main():
#     async with async_playwright() as p:
#         await run(p)

# asyncio.run(main())
# # asyncio.run(run(async_playwright()))


# import scrapy
# from scrapy_splash import SplashRequest

# class MySpider(scrapy.Spider):
#     name = 'my_spider'

#     def start_requests(self):
#         yield SplashRequest(url="https://dynamic-website.com", callback=self.parse)

#     def parse(self, response):
#         data = []
#         for item in response.css('div.item'):
#             title = item.css('h2.title::text').get().strip()
#             price = item.css('span.price::text').get().strip()
#             data.append({'title': title, 'price': price})

#         yield {
#             'data': data
#         }


# import tkinter as tk
# from tkinter import scrolledtext
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # Function to perform the scraping
# def scrape_amazon():
#     search_term = search_entry.get()  # Get search term from the input field
#     results_textbox.delete(1.0, tk.END)  # Clear the results textbox

#     # Set up the WebDriver
#     driver = webdriver.Chrome()

#     try:
#         # Navigate to Amazon
#         driver.get('https://www.amazon.com')

#         # Wait until the search box is present in the DOM
#         search_box = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
#         )

#         # Locate elements and extract information
#         search_box.send_keys(search_term)
#         search_box.submit()

#         # Wait for the products to load
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, '.s-main-slot .s-result-item'))
#         )

#         # Extract dynamic content
#         products = driver.find_elements(By.CSS_SELECTOR, '.s-main-slot .s-result-item')
#         for product in products:
#             try:
#                 title = product.find_element(By.TAG_NAME, 'h2').text
#                 results_textbox.insert(tk.END, title + '\n')
#             except Exception as e:
#                 results_textbox.insert(tk.END, f"Error: {e}\n")
#     except Exception as e:
#         results_textbox.insert(tk.END, f"An error occurred: {e}\n")
#     finally:
#         # Close the browser
#         driver.quit()

# # Create the main application window
# app = tk.Tk()
# app.title("Amazon Web Scraper")

# # Create input field for search term
# tk.Label(app, text="Enter Search Term:").grid(row=0, column=0, padx=10, pady=10)
# search_entry = tk.Entry(app, width=40)
# search_entry.grid(row=0, column=1, padx=10, pady=10)

# # Create a button to trigger scraping
# scrape_button = tk.Button(app, text="Scrape Amazon", command=scrape_amazon)
# scrape_button.grid(row=0, column=2, padx=10, pady=10)

# # Create a scrolled text box to display results
# results_textbox = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=60, height=20)
# results_textbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

# # Run the application
# app.mainloop()

import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to perform the scraping
def scrape_amazon():
    search_term = search_entry.get()  # Get search term from the input field
    for i in tree.get_children():  # Clear previous results from the table
        tree.delete(i)

    # Set up the WebDriver for Firefox
    driver = webdriver.Firefox()

    try:
        # Navigate to Amazon
        driver.get('https://www.amazon.in')

        # Wait until the search box is present in the DOM
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
        )

        # Locate elements and extract information
        search_box.send_keys(search_term)
        search_box.submit()

        # Wait for the products to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.s-main-slot .s-result-item'))
        )

        # Extract dynamic content
        products = driver.find_elements(By.CSS_SELECTOR, '.s-main-slot .s-result-item')
        for i, product in enumerate(products, start=1):
            try:
                title = product.find_element(By.TAG_NAME, 'h2').text
                tree.insert("", "end", values=(i, title))
            except Exception as e:
                tree.insert("", "end", values=(i, f"Error: {e}"))
    except Exception as e:
        tree.insert("", "end", values=(0, f"An error occurred: {e}"))
    finally:
        # Close the browser
        driver.quit()

# Create the main application window
app = tk.Tk()
app.title("Amazon Web Scraper")

# Create input field for search term
tk.Label(app, text="Enter Search Term:").grid(row=0, column=0, padx=10, pady=10)
search_entry = tk.Entry(app, width=40)
search_entry.grid(row=0, column=1, padx=10, pady=10)

# Create a button to trigger scraping
scrape_button = tk.Button(app, text="Scrape Amazon", command=scrape_amazon)
scrape_button.grid(row=0, column=2, padx=10, pady=10)

# Create a table (Treeview) to display results
columns = ("No", "Product Title")
tree = ttk.Treeview(app, columns=columns, show='headings')
tree.heading("No", text="No")
tree.heading("Product Title", text="Product Title")
tree.column("No", width=50)
tree.column("Product Title", width=500)
tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

# Run the application
app.mainloop()
