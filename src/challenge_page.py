import time

from selenium.webdriver.common.by import By


class ChallengePage:
    def __init__(self, driver):
        self.driver = driver

    def reset_game(self):
        # There is a disabled reset button for reasons unknown :)
        self.driver.find_elements(By.ID, "reset")[1].click()
        time.sleep(1)

    def click_weigh(self):
        self.driver.find_element(By.ID, "weigh").click()

    def click_coin(self, coin_num):
        self.driver.find_element(By.ID, f"coin_{str(coin_num)}").click()

    def enter_bowl(self, numbers, bowl_side):
        assert bowl_side.lower() in ["left", "right"], "Only left and right bowl currently supported"
        for i in range(len(numbers)):
            bowl_entry_id = bowl_side.lower() + "_" + str(i)
            self.driver.find_element(By.ID, bowl_entry_id).send_keys(numbers[i])

    def get_result(self):
        result_div = self.driver.find_element(By.XPATH, "//div[@class='result']")
        # Find the first button element within the result div, this is our result
        return result_div.find_element(By.XPATH, ".//button").text

    def get_weighings(self):
        game_info_div = self.driver.find_element(By.CLASS_NAME, "game-info")

        # Find all child <li> elements under the game_info_div
        return game_info_div.find_elements(By.XPATH, ".//li")
