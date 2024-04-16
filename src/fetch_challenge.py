import time
from selenium import webdriver
from src.challenge_page import ChallengePage

CHALLENGE_URL = 'http://sdetchallenge.fetch.com/'
driver = webdriver.Chrome()
driver.implicitly_wait(5)
driver.get(CHALLENGE_URL)
CHALLENGE_PAGE = ChallengePage(driver)

"""
Split the given list into two equal parts, if the list is not of even length remove the final entry of 
the original list as the odd_val_out

return three params - first half of list, second half, and the odd value removed if list is odd length
"""
def split_list(list_to_split):
    odd_val_out = None
    if (len(list_to_split) % 2) != 0:
        # if list is not evenly split chop off the last value that will be the fake if both sides are equal
        odd_val_out = list_to_split[-1]
        list_to_split.pop(-1)
    midpoint = len(list_to_split) // 2

    first_half = list_to_split[:midpoint]
    second_half = list_to_split[midpoint:]
    return first_half, second_half, odd_val_out


"""Recursively run tests in the UI until we determine which coin is fake"""
def run_test(option_list):
    left_list, right_list, odd_val_out = split_list(option_list)
    test_result = run_test_in_ui(left_list, right_list)
    fake_coin_found = find_fake_coin(left_list=left_list, right_list=right_list,
                                     test_result=test_result, odd_val_out=odd_val_out)
    if fake_coin_found:
        return fake_coin_found
    else:
        next_list = left_list if test_result == "<" else right_list
        return run_test(next_list)


"""
Find the fake coin from the given two lists, odd val out and the given result.  If a fake cannot be determined
return None
"""
def find_fake_coin(left_list, right_list, test_result, odd_val_out):
    if test_result not in ["=", ">", "<"]:
        raise ValueError(f"Test result {test_result} cannot be parsed.  Something went wrong.")
    if test_result == "=":
        return odd_val_out
    elif test_result == "<" and len(left_list) == 1:
        return left_list[0]
    elif test_result == ">" and len(right_list) == 1:
        return right_list[0]
    else:
        # No fake found yet
        return None


"""Enter a left and right list into the correct bowl and get the result"""
def run_test_in_ui(left_list, right_list):
    starting_weighing_len = len(CHALLENGE_PAGE.get_weighings())
    CHALLENGE_PAGE.reset_game()
    CHALLENGE_PAGE.enter_bowl(left_list, "left")
    CHALLENGE_PAGE.enter_bowl(right_list, 'right')
    CHALLENGE_PAGE.click_weigh()
    wait_for_weight_list_increase(starting_weighing_len)
    return CHALLENGE_PAGE.get_result()


"""Wait for the list of weighings to increase by one from the given starting length"""
def wait_for_weight_list_increase(starting_weighing_len, timeout=15):
    increased = False
    end_time = time.time() + timeout
    while time.time() < end_time and not increased:
        increased = len(CHALLENGE_PAGE.get_weighings()) > starting_weighing_len


"""Print out all the weightings done in this run"""
def output_weighing_attempts():
    weighings = CHALLENGE_PAGE.get_weighings()
    print(f"The following {len(weighings)} weighings were made:")
    for weighing in weighings:
        print(weighing.text)


"""Click the given coin number and print the alert text"""
def click_coin(coin_num):
    CHALLENGE_PAGE.click_coin(coin_num)
    alert = driver.switch_to.alert
    alert_text = alert.text
    print(f"Alert text is: {alert_text}")
    alert.accept()


if __name__ == '__main__':
    # Ideally we would read this list from the UI but hard coding for now since this is just a take home project.
    all_coins = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    fake_coin = run_test(all_coins)
    print(f"fake coin is: {fake_coin}")
    click_coin(fake_coin)
    output_weighing_attempts()

    driver.quit()
