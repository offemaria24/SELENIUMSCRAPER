import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

class MyAutomation:
    def __init__(self):
        self.browser = webdriver.Chrome()

    def __del__(self):
        self.browser.quit()

    def __scroll_to_middle(self, speed=4):
        # Scroll down to the center of 50% of the page height
        page_height = self.browser.execute_script("return document.body.scrollHeight")
        target_scroll_position = int(page_height * 1)
        current_scroll_position, new_height = 0, 1
        while current_scroll_position <= target_scroll_position:
            current_scroll_position += speed
            self.browser.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            if current_scroll_position >= target_scroll_position:
                time.sleep(5)  # Wait for the content to load at the center of the scroll

    def automate_click_elements(self):
        # Navigate to the desired webpage
        self.browser.get('http://rb.gy/eig2o')  # Replace with your target URL

        # Find all elements with the attribute 'data-spm-anchor-id'
        elements = self.browser.find_elements(By.CSS_SELECTOR, '[data-spm-anchor-id]')

        # Store the clicked elements
        clicked_elements = []

        # Scroll to the middle of the page
        self.__scroll_to_middle()

        # Click on each element and store the clicked elements
        for element in elements:
            try:
                element.click()
            except ElementClickInterceptedException:
                # Wait for the overlaying element to disappear
                wait = WebDriverWait(self.browser, 10)
                wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'lzd-logo-bar')))
                
                # Scroll the element into view
                self.browser.execute_script("arguments[0].scrollIntoView();", element)
                
                # Click on the desired element using JavaScript
                self.browser.execute_script("arguments[0].click();", element)

            clicked_elements.append(element.get_attribute('data-spm-anchor-id'))

        # Print the clicked elements
        print("Clicked elements:")
        for clicked_element in clicked_elements:
            print(clicked_element)

automation = MyAutomation()
automation.automate_click_elements()
