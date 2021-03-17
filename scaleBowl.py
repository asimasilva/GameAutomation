from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import unittest


class scaleBowl(unittest.TestCase):
    locators = {"bowlLabel": "//div[@class='game-board']//div[@class='status' and contains(., '%s bowl')]",
                "box": "//div[@class='board-row']//input[@id='%s_%s' and @data-side='%s']"}

    def __init__(self, browser, side="left"):
        super().__init__()
        self.browser = browser
        self.side = side
        self.label = f"{self.side} bowl"

    def enter_box_val(self, index, num):
        box = self.browser.find_element(By.XPATH, self.locators["box"] % (self.side, index, self.side))
        box.send_keys(num)

    def get_box_val(self, index):
        box = self.browser.find_element(By.XPATH, self.locators["box"] % (self.side, index, self.side))
        return box.text

    def clear_box_val(self, index):
        self.enter_box_val(index, "")

    def reset(self):
        for index in range(0, 8):
            self.clear_box_val(index)

    def assert_bowl_displayed_correctly(self):
        for index in range(0, 8):
            box = self.browser.find_element(By.XPATH, self.locators["box"] % (self.side, index, self.side))
            self.assertTrue(box)

    def assert_bowl_label(self, label=""):
        if label == "":
            label = self.label
        xpath = self.locators["bowlLabel"] % self.side
        label_element = self.browser.find_element(By.XPATH, xpath)
        act_label = label_element.text
        self.assertEqual(act_label, label, msg=f"Label on {self.side} is act: {act_label}. \n expected: {label}")
