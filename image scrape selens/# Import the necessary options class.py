from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

# Initialize the options
options = Options()
options.add_argument('--headless')

# Initialize the web driver with the options
driver = webdriver.Chrome(options=options)

# Navigate to the Lazada product page
product_url = 'http://rb.gy/eig2o'  # Replace with the actual product URL
driver.get(product_url)

# Wait for the review section to be visible
wait = WebDriverWait(driver, 20)  # Increase the timeout value if necessary
review_section = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.item')))

# Scroll down the review section
driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", review_section)

# Wait for the page to load completely
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.review-image')))

# Find all image elements within the review section
image_elements = driver.find_elements(By.CSS_SELECTOR, '.review-image')

# Open the text file in write mode
with open('product_images.txt', 'w') as file:
    # Extract image URLs or download the images
    for i, element in enumerate(image_elements):
        image_url = element.get_attribute('src')
        # Download the image
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            # Save the image to a file
            image_path = f'product_image_{i}.jpg'  # Generate a unique image filename
            with open(image_path, 'wb') as image_file:
                for chunk in response.iter_content(1024):
                    image_file.write(chunk)
            # Write the image filename to the text file
            file.write(image_path + '\n')

# Close the browser driver
driver.quit()

