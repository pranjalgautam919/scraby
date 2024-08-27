import tkinter as tk
from tkinter import ttk, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import logging
import threading
from time import sleep

# Set up logging
logging.basicConfig(filename='scraper.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to perform the scraping
def scrape_amazon():
    search_term = search_entry.get()  # Get search term from the input field
    if not search_term:
        messagebox.showerror("Input Error", "Please enter a search term.")
        return

    progress_bar.start()  # Start progress bar
    scrape_button.config(state=tk.DISABLED)  # Disable scrape button during operation
    for i in tree.get_children():  # Clear previous results from the table
        tree.delete(i)

    # Set up the WebDriver for Firefox
    options = webdriver.FirefoxOptions()
    options.headless = True  # Use headless mode
    options.add_argument("--disable-blink-features=AutomationControlled")  # Anti-bot detection measure
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")  # User-Agent spoofing

    driver = webdriver.Firefox(options=options)

    try:
        # Navigate to Amazon India
        driver.get('https://www.amazon.in')

        # Wait until the search box is present in the DOM
        search_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
        )

        # Enter search term and submit
        search_box.send_keys(search_term)
        search_box.submit()

        # Wait for the products to load
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.s-main-slot .s-result-item'))
        )

        products_scraped = 0  # Initialize counter for scraped products
        page_number = 1

        with open('report.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["No", "Product Title", "Price", "Rating", "Product URL", "Availability"])

            while True:
                # Ensure dynamic content is fully loaded
                sleep(2)  # Short sleep to allow content to load

                products = driver.find_elements(By.CSS_SELECTOR, '.s-main-slot .s-result-item')
                for i, product in enumerate(products, start=products_scraped + 1):
                    try:
                        title = product.find_element(By.CSS_SELECTOR, '.a-size-medium.a-color-base.a-text-normal').text
                        price = product.find_element(By.CSS_SELECTOR, '.a-price-whole').text
                        rating = product.find_element(By.CSS_SELECTOR, '.a-icon-alt').get_attribute('aria-label')
                        product_url = product.find_element(By.CSS_SELECTOR, 'a.a-link-normal').get_attribute('href')
                        availability = product.find_element(By.CSS_SELECTOR, '.a-color-success').text if product.find_elements(By.CSS_SELECTOR, '.a-color-success') else 'Unavailable'
                        
                        writer.writerow([i, title, price, rating, product_url, availability])
                        tree.insert("", "end", values=(i, title, price, rating, product_url, availability))
                        products_scraped += 1
                    except Exception as e:
                        logging.error(f"Error extracting product {i}: {e}")
                        writer.writerow([i, f"Error: {e}", "", "", "", ""])
                        tree.insert("", "end", values=(i, f"Error: {e}", "", "", "", ""))

                # Check if there is a next page, and navigate to it
                try:
                    next_page = driver.find_element(By.CSS_SELECTOR, 'li.a-last a')
                    next_page.click()
                    page_number += 1
                    sleep(5)  # Sleep to simulate human behavior
                except Exception:
                    break  # No more pages

    except Exception as e:
        logging.error(f"Error scraping Amazon: {e}")
        tree.insert("", "end", values=(0, f"An error occurred: {e}", "", "", "", ""))
        messagebox.showerror("Scraping Error", f"An error occurred: {e}")
    finally:
        # Close the browser
        driver.quit()
        progress_bar.stop()  # Stop progress bar
        scrape_button.config(state=tk.NORMAL)  # Re-enable scrape button

# Threaded version of the scrape function to keep GUI responsive
def threaded_scrape():
    threading.Thread(target=scrape_amazon).start()

# Create the main application window
app = tk.Tk()
app.title("Amazon India Web Scraper")

# Create input field for search term
tk.Label(app, text="Enter Search Term:").grid(row=0, column=0, padx=10, pady=10)
search_entry = tk.Entry(app, width=40)
search_entry.grid(row=0, column=1, padx=10, pady=10)

# Create a button to trigger scraping
scrape_button = tk.Button(app, text="Scrape Amazon", command=threaded_scrape)
scrape_button.grid(row=0, column=2, padx=10, pady=10)

# Create a progress bar
progress_bar = ttk.Progressbar(app, orient="horizontal", length=400, mode="indeterminate")
progress_bar.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

# Create a table (Treeview) to display results
columns = ("No", "Product Title", "Price", "Rating", "Product URL", "Availability")
tree = ttk.Treeview(app, columns=columns, show='headings')
tree.heading("No", text="No")
tree.heading("Product Title", text="Product Title")
tree.heading("Price", text="Price")
tree.heading("Rating", text="Rating")
tree.heading("Product URL", text="Product URL")
tree.heading("Availability", text="Availability")
tree.column("No", width=50)
tree.column("Product Title", width=300)
tree.column("Price", width=80)
tree.column("Rating", width=80)
tree.column("Product URL", width=300)
tree.column("Availability", width=100)
tree.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

# Run the application
app.mainloop()
