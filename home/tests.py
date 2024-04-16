from django.test import TestCase, LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class MySeleniumTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get(f'{self.live_server_url}/admin/')
        username_input = self.selenium.find_element_by_name('username')
        username_input.send_keys('admin@acme.ie')
        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys('admin')
        password_input.send_keys(Keys.RETURN)

        # Check the returned page
        greeting = self.selenium.find_element_by_id('greeting')
        self.assertIn('Welcome, myuser!', greeting.text)


    class MySeleniumTests(LiveServerTestCase):
        @classmethod
        def setUpClass(cls):
            super().setUpClass()
            cls.selenium = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            cls.selenium.implicitly_wait(10)

        @classmethod
        def tearDownClass(cls):
            cls.selenium.quit()
            super().tearDownClass()

        def test_payment_form_submission(self):
            self.selenium.get(f'{self.live_server_url}/load-payment-form/')

            # Wait for the card number field to be visible
            card_number_input = WebDriverWait(self.selenium, 20).until(
                EC.visibility_of_element_located((By.ID, 'cardNumber'))
            )

            # Use JavaScript to set the value of the card number
            self.selenium.execute_script("arguments[0].value = '4111111111111111';", card_number_input)

            # Optionally, continue to fill out other fields or submit the form
            # Debug: Take a screenshot to confirm the input
            self.selenium.save_screenshot('after_input.png')

    # You can run this test from your terminal using the manage.py script
    # python manage.py test home.tests.MySeleniumTests.test_payment_form_submission
