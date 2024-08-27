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
        # Navigate to Amazon India
        driver.get('https://www.amazon.in')

        # Wait until the search box is present in the DOM
        search_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
        )

        # Locate elements and extract information
        search_box.send_keys(search_term)
        search_box.submit()

        # Wait for the products to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.s-main-slot .s-result-item'))
        )

        # Extract dynamic content
        products = driver.find_elements(By.CSS_SELECTOR, '.s-main-slot .s-result-item')
        for i, product in enumerate(products, start=1):
            try:
                title = product.find_element(By.CSS_SELECTOR, 'h2 span').text
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
app.title("Amazon India Web Scraper")

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
