from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import unittest


class weighings(unittest.TestCase):
    locators = {"weighingsLabel": "//div[@class='game-info']/div[contains(text(), '%s')]",
                "weighedList": "//div[@class='game-info']/ol/li"}

    def __init__(self, browser):
        super().__init__()
        self.browser = browser


    def assert_weighing_label(self, label="Weighings"):
        xpath = self.locators["weighingsLabel"] % label
        label_element = self.browser.find_element(By.XPATH, xpath)
        act_label = label_element.text
        self.assertEqual(act_label, label, msg=f"Label is act: {act_label}. \n expected: {label}")

    def get_size_of_weighed_list(self):
        weighed_list = self.browser.find_elements(By.XPATH, self.locators["weighedList"])
        return len(weighed_list)

    def assert_text_in_weighted_list(self, list_num, text_val):
        item = self.browser.find_elements(By.XPATH, self.locators["weighedList"])[int(list_num)-1]
        self.assertEqual(item.text.replace(' ', ''), text_val.replace(' ', ''))

    def get_parsed_text_for_scale_in_weighted_list(self, list_num):
        items_list = self.browser.find_elements(By.XPATH, self.locators["weighedList"])
        left_group, sign, right_group = "", "", ""
        if len(items_list) > 0:
            item_text = (items_list[int(list_num)-1]).text
            left_group = item_text[item_text.index("["): item_text.index("]")+1]
            sign = item_text[item_text.index("]")+2: item_text.rindex("[")-1]
            right_group = item_text[item_text.rindex("["): item_text.rindex("]")+1]
        return left_group, sign, right_group

    def get_text_in_weighted_list(self, list_num):
        item = self.browser.find_elements(By.XPATH, self.locators["weighedList"])[int(list_num) - 1]
        return item.text

