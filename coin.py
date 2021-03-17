from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest


class coin(unittest.TestCase):
    locators = {"coinBtn": "//button[@id='coin_%s']"}

    def __init__(self, browser, index):
        super().__init__()
        self.browser = browser
        self.val = index
        self.xpath = self.locators["coinBtn"] % self.val

    def assert_coin_val(self, exp_val):
        a_coin = self.browser.find_element(By.XPATH, self.xpath)
        act_val = a_coin.text
        self.assertEqual(act_val, exp_val, msg=f"Coin value act: {act_val}. \n expected: {exp_val}")

    def click_it(self):
        act_coin = self.browser.find_element(By.XPATH, self.xpath)
        act_coin.click()
