import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from pageObjects.scaleGameBoard import scaleGameBoard


class scaleBowlTest(unittest.TestCase):

    @classmethod
    def setUp(self):
        # create a new chrome session
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        # navigate to the application home page
        self.driver.get("http://ec2-54-208-152-154.compute-1.amazonaws.com/")
        global gameBoard
        gameBoard = scaleGameBoard(self.driver)

    @classmethod
    def tearDown(self):
        self.driver.quit()

    def test_001_assert_game_board_display(self):
        # assert all elements on the page
        gameBoard.leftScaleBowl.assert_bowl_label("left bowl")
        gameBoard.rightScaleBowl.assert_bowl_label("right bowl")
        gameBoard.leftScaleBowl.assert_bowl_displayed_correctly()
        gameBoard.rightScaleBowl.assert_bowl_displayed_correctly()
        gameBoard.assert_result_label("Result")
        gameBoard.assert_result_button("?")
        gameBoard.assertEqual("?", gameBoard.get_result())
        gameBoard.browser.find_element(By.XPATH, gameBoard.locators["resetBtn"]).is_displayed()
        gameBoard.browser.find_element(By.XPATH, gameBoard.locators["weighBtn"]).is_displayed()
        gameBoard.weighings.assert_weighing_label("Weighings")
        gameBoard.assertEqual(gameBoard.weighings.get_size_of_weighed_list(), 0)
        gameBoard.assertEqual(len(gameBoard.coinList), 9)
        gameBoard.assert_all_coins_displayed()

    def test_002_neg_enter_non_numeric_chars(self):
        gameBoard.leftScaleBowl.enter_box_val(0, -1)
        gameBoard.assertEqual("", gameBoard.leftScaleBowl.get_box_val(0))
        gameBoard.leftScaleBowl.enter_box_val(0, "a")
        gameBoard.assertEqual("", gameBoard.leftScaleBowl.get_box_val(0))
        gameBoard.leftScaleBowl.enter_box_val(0, 10)
        gameBoard.assertEqual("", gameBoard.leftScaleBowl.get_box_val(0))

    def test_003_with_only_one_val(self):
        gameBoard.leftScaleBowl.enter_box_val(0, 4)
        gameBoard.click_weigh()
        left_group, sign, right_group = gameBoard.weighings.get_parsed_text_for_scale_in_weighted_list(1)
        print(left_group, sign, right_group)
        gameBoard.weighings.assert_text_in_weighted_list(1, "[4] "+sign+" []")

    def test_004_with_same_coin_on_both_scales(self):
        gameBoard.leftScaleBowl.enter_box_val(0, 4)
        gameBoard.rightScaleBowl.enter_box_val(0, 4)
        gameBoard.click_weigh()
        gameBoard.assert_and_accept_alert("Inputs are invalid: Both sides have coin(s): 4")

    def test_005_find_fake_bar(self):
        """ Approach: binary. Split the coinlist in two sections. And weigh each section to find the
        section with the less weight, and repeat process until the fake bar is found.
        Can find bar in <= 4 steps.
        """
        bar_num = gameBoard.find_fake_bar()
        print("Fake bar is: " + str(bar_num))
        print(f"Num of tries taken: {gameBoard.weighings.get_size_of_weighed_list()}")

    def test_006_selecting_not_fake_bar(self):
        def test_find_fake_bar(self):
            bar_num = gameBoard.find_fake_bar()
            print("Fake bar is: " + str(bar_num))
            print(f"Num of tries taken: {gameBoard.weighings.get_size_of_weighed_list()}")
            # Test clicking the wrong answer
            wrong_num = 5
            if bar_num == 5:
                wrong_num = 4
            gameBoard.coinList[wrong_num].click_it()
            self.assert_and_accept_alert('Oops! Try Again!')

    def test_007_find_fake_bar2(self):
        """ Approach: Three buckets. PUt the coins into three buckets. Weigh first and last bucket, and whichever
        is less, weigh it against the second bucket, repeat process until the fake bar is found.
        Can find bar in <= 2 steps.
        """
        bar_num = gameBoard.find_fake_bar2()
        print("Fake bar is: " + str(bar_num))
        print(f"Num of tries taken: {gameBoard.weighings.get_size_of_weighed_list()}")

    def test_008_find_fake_bar3(self):
        """ Approach: Three buckets. Same approach as above, but less repetitive code.
        Can find bar in <= 2 steps.
        """
        bar_num = gameBoard.find_fake_bar3()
        print("Fake bar is: " + str(bar_num))
        print(f"Num of tries taken: {gameBoard.weighings.get_size_of_weighed_list()}")


if __name__ == '__main__':
    unittest.main()
