from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as soup
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Scraper:
    def __init__(self, url):
        self.url = url
        self.chrome_options = Options()
        self.service = Service('D:/4thyear/Cd/chromedriver')  # Path to ChromeDriver executable
        self.browser = webdriver.Chrome(service=self.service, options=self.chrome_options)

    def __del__(self):
        self.browser.quit()

    def __scroll_to_middle(self, speed=8):
        # Scroll down to the center of 50% of the page height
        page_height = self.browser.execute_script("return document.body.scrollHeight")
        target_scroll_position = int(page_height * 0.8)
        current_scroll_position, new_height = 0, 1
        while current_scroll_position <= target_scroll_position:
            current_scroll_position += speed
            self.browser.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            if current_scroll_position >= target_scroll_position:
                time.sleep(5)  # Wait for the content to load at the center of the scroll

    def scrape(self):
        self.browser.get(self.url)
        time.sleep(0.1)
        self.__scroll_to_middle(speed=5)

        # Create empty lists to store the text reviews and their corresponding image reviews
        text_reviews = []
        image_reviews = []
        image2_urls = []

        # Extract text reviews and add them to the list
        page_soup = soup(self.browser.page_source, 'html.parser')
        reviews = page_soup.findAll('div', attrs={"class": "item-content"})
        for review in reviews:
            text = review.div.text.strip()
            text_reviews.append(text)

            review_image_div = review.find_next('div', attrs={"class": "review-image"})
            if review_image_div:
                img = review_image_div.find('img')
                if img:
                    image_url = img['src']
                    image_reviews.append(image_url)
                else:
                    image_reviews.append('No Image Review Found')
            else:
                image_reviews.append('No Image Review Found')

        # Extract merchant images and add them to the list
        merchant_images = page_soup.findAll('div', attrs={"class": "gallery-preview-panel__content"})
        for image in merchant_images:
            img = image.find('img')
            if img:
                image_url = img['src']
                image2_urls.append(image_url)

        # Save the merchant images to a separate text file
        merchant_filename = 'Merchant-product.txt'
        with open(merchant_filename, 'w', encoding='utf-8') as merchant_file:
            for image_url in image2_urls:
                merchant_file.write("Merchant Image: " + image_url + "\n\n")

        print("Merchant images saved to", merchant_filename)

        # Combine text reviews, their corresponding image reviews, and merchant images
        combined_elements = []
        for i in range(len(text_reviews)):
            combined_elements.append("text-review[" + text_reviews[i] + "]")
            combined_elements.append("image-review[" + image_reviews[i] + "]")
            combined_elements.append(" ")  # Empty line for separation

        # Save the combined elements to a text file
        filename = 'combined_elements.txt'
        with open(filename, 'w', encoding='utf-8') as file:
            for element in combined_elements:
                file.write(element + '\n')

        print("Data saved to", filename)


# Create an instance of the Scraper class
url = 'http://rb.gy/eig2o'
scraper = Scraper(url)

# Call the scrape method to start scraping the data
scraper.scrape()
