from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest
from pageObjects.scaleBowl import scaleBowl
from pageObjects.weighings import weighings
from pageObjects.coin import coin
from selenium.common.exceptions import NoAlertPresentException


class scaleGameBoard(unittest.TestCase):

    def __init__(self, browser):
        super().__init__()
        self.browser = browser
        self.leftScaleBowl = scaleBowl(self.browser, "left")
        self.rightScaleBowl = scaleBowl(self.browser, "right")
        self.weighings = weighings(self.browser)
        self.num_weighings = 0
        self.coinList = []
        for i in range(9):
            self.coinList.append(coin(self.browser, i))

    locators = {"resetBtn": "reset",
                "weightBth": "weigh",
                "resultLabel": "//div[@class='result']/div[contains(.,'Result')]",
                "resultBtn": "//div[@class='result']/button[@id='reset']",
                "resetBtn": "//button[@id='reset' and contains(., 'Reset')]",
                "weighBtn": "//button[@id='weigh']"
                }

    def assert_result_label(self, label):
        label_element = self.browser.find_element(By.XPATH, self.locators["resultLabel"])
        act_label = label_element.text
        self.assertEqual(act_label, label, msg=f"Label is act: {act_label}. \n expected: {label}")

    def assert_result_button(self, val):
        result_btn = self.browser.find_element(By.XPATH, self.locators["resultBtn"])
        act_val = result_btn.text
        self.assertEqual(act_val, val, msg=f"Label is act: {act_val}. \n expected: {val}")

    def get_result(self):
        result_btn = self.browser.find_element(By.XPATH, self.locators["resultBtn"])
        result_btn.click()
        return result_btn.text

    def click_reset(self):
        reset_btn = self.browser.find_element(By.XPATH, self.locators['resetBtn'])
        reset_btn.click()

    def click_weigh(self):
        weigh_btn = self.browser.find_element(By.XPATH, self.locators['weighBtn'])
        weigh_btn.click()
        try:
            alert = self.browser.switch_to.alert
            print("Unexpected alert")
            return
        except NoAlertPresentException as e:
            self.num_weighings += 1
            act_text = self.weighings.get_text_in_weighted_list(self.num_weighings)
            print(act_text)

    def click_coin(self, val):
        coin_item = self.coinList[val]
        coin_item.click_it()

    def print_list(self):
        for a_coin in self.coinList:
            print(str(a_coin.val))

    def assert_all_coins_displayed(self):
        for i, a_coin in enumerate(self.coinList, 0):
            a_coin.assert_coin_val(str(i))
            print(str(a_coin.val))

    def assert_and_accept_alert(self, txt):
        alert = self.browser.switch_to.alert
        print(alert.text)
        self.assertEqual(alert.text, txt)
        alert.accept()

    def find_fake_bar(self, start=0, end=8):
        """ Approach: binary. Split the coinlist in two sections. And weigh each section to find the
        section with the less weight, and repeat process until the fake bar is found.
        Can find bar in <= 4 steps.
        """
        self.click_reset()
        is_mid = (end - start + 1) % 2
        first_half = mid_index = int((end - start) / 2) + start
        second_half = mid_index + 1

        # If there is a odd/center bar or only two bars
        if is_mid == 1 or start + 1 == end:
            mid_val = self.coinList[mid_index].val
            self.leftScaleBowl.enter_box_val(mid_val, mid_val)
            end_val = self.coinList[end].val
            self.rightScaleBowl.enter_box_val(end_val, end_val)
            self.click_weigh()
            sign = self.get_result()
            if sign == "<":
                self.coinList[mid_val].click_it()
                self.assert_and_accept_alert('Yay! You find it!')
                return mid_val
            if sign == ">":
                self.coinList[end_val].click_it()
                self.assert_and_accept_alert('Yay! You find it!')
                return end_val
            # Proceed with the odd number of bars left
            self.click_reset()
            first_half = mid_index - 1

        # Populate both sides of the scale and weight it
        left_group, right_group = [], []
        for i in range(start, first_half + 1):
            self.leftScaleBowl.enter_box_val(i, i)
            left_group.append(i)
        for i in range(second_half, end + 1):
            self.rightScaleBowl.enter_box_val(i, i)
            right_group.append(i)
        self.click_weigh()
        sign = self.get_result()
        self.weighings.assert_text_in_weighted_list(self.weighings.get_size_of_weighed_list(),
                                                    f"{left_group} {sign} {right_group}")
        if sign == "<":
            return self.find_fake_bar(start, first_half)
        if sign == ">":
            return self.find_fake_bar(second_half, end)

    def find_fake_bar2(self, start=0, end=8):
        """ Approach: Three buckets. PUt the coins into three buckets. Weigh first and last bucket, and whichever
        is less, weigh it against the second bucket, repeat process until the fake bar is found.
        Can find bar in 2 steps.
        """
        self.click_reset()
        thirds = int(len(self.coinList) / 3)
        first_third, second_third, last_third = [], [], []
        for i in range(0, thirds):
            first_third.append(self.coinList[i].val)
        for i in range(thirds, thirds*2):
            second_third.append(self.coinList[i].val)
        for i in range(thirds*2, len(self.coinList)):
            last_third.append(self.coinList[i].val)

        for i in first_third:
            self.leftScaleBowl.enter_box_val(i, i)
        for i in last_third:
            self.rightScaleBowl.enter_box_val(i, i)
        self.click_weigh()
        sign = self.get_result()
        self.weighings.assert_text_in_weighted_list(self.weighings.get_size_of_weighed_list(),
                                                    f"{first_third} {sign} {last_third}")
        self.click_reset()

        # If its equal
        final_third = second_third
        if sign == "<":
            final_third = first_third
        if sign == ">":
            final_third = last_third
        self.leftScaleBowl.enter_box_val(final_third[0], final_third[0])
        self.rightScaleBowl.enter_box_val(final_third[2], final_third[2])
        self.click_weigh()
        sign = self.get_result()

        fake_coin = final_third[1]
        if sign == "<":
            fake_coin = final_third[0]
        if sign == ">":
            fake_coin = final_third[2]

        return fake_coin

    def find_fake_bar3(self):
        """ Approach: Three buckets. Same approach as above, but less repetitive code.
        Can find bar in 2 steps.
        """
        return self.find_less_third(self.coinList)

    def find_less_third(self, section):
        third_index = int(len(section) / 3)
        first_third, second_third, last_third = [], [], []
        for i in range(0, int(third_index)):
            first_third.append(i)
        for i in range(int(third_index), int(third_index)*2):
            second_third.append(i)
        for i in range(int(third_index)*2, len(section)):
            last_third.append(i)

        for i in first_third:
            self.leftScaleBowl.enter_box_val(i, i)
        for i in last_third:
            self.rightScaleBowl.enter_box_val(i, i)
        self.click_weigh()
        sign = self.get_result()
        self.weighings.assert_text_in_weighted_list(self.weighings.get_size_of_weighed_list(),
                                                    f"{first_third} {sign} {last_third}")

        # If its equal
        final_third = second_third
        if sign == "<":
            final_third = first_third
        if sign == ">":
            final_third = last_third
        self.click_reset()
        if len(final_third) == 1:
            return final_third[0]
        return self.find_less_third(final_third)


