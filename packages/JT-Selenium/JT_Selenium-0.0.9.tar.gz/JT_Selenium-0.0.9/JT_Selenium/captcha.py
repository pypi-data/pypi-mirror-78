import requests
import time
from urllib.parse import urlparse, parse_qs
from selenium.common.exceptions import NoSuchElementException


def SolveCaptcha(api_key, site_key, url):
    """
    Uses the 2Captcha service to solve Captcha's for you.

    Captcha's are held in iframes; to solve the captcha, you need a part of the url of the iframe. The iframe is usually
    inside a div with id=gRecaptcha. The part of the url we need is the query parameter k, this is called the site_key:

    www.google.com/recaptcha/api2/anchor?ar=1&k=6LcleDIUAAAAANqkex-vX88sMHw8FXuJQ3A4JKK9&co=aHR0cHM6Ly93d3cuZGljZS5jb206NDQz&hl=en&v=oqtdXEs9TE9ZUAIhXNz5JBt_&size=normal&cb=rpcg9w84syix
                                              k=6LcleDIUAAAAANqkex-vX88sMHw8FXuJQ3A4JKK9

    Here the site_key is 6LcleDIUAAAAANqkex-vX88sMHw8FXuJQ3A4JKK9

    You also need to supply the url of the current page you're on.

    This function will return a string with the response key from captcha validating the test. This needs to be inserted
    into an input field with the id=g-recaptcha-response.

    :param api_key: The 2Captcha API key.
    :param site_key: The site_key extracted from the Captcha iframe url
    :param url: url of the site you're on
    :return: The response from captcha validating the test
    """
    print("Solving Captcha...")
    print("Sending Request...")
    request_response = requests.get("https://2captcha.com/in.php?", params={
        "googlekey": site_key,
        "method": "userrecaptcha",
        "pageurl": url,
        "key": api_key,
        "json": 1,
        "invisible": 0,
    })
    request_response.raise_for_status()
    print("Waiting for Response...")
    time.sleep(30)
    answer_response_json = {'status': 0, 'request': 'CAPCHA_NOT_READY'}
    while answer_response_json['request'] == 'CAPCHA_NOT_READY':
        answer_response = requests.get("https://2captcha.com/res.php", params={
            "key": api_key,
            "action": "get",
            "id": request_response.json()['request'],
            "json": 1
        })
        answer_response_json = answer_response.json()
        print(answer_response_json)
        time.sleep(5)
    if answer_response_json['status'] == 1:
        print("Solved!")
        return answer_response_json['request']
    elif answer_response_json['request'] == 'ERROR_CAPTCHA_UNSOLVABLE':
        raise TimeoutError("ERROR_CAPTCHA_UNSOLVABLE")
    else:
        raise Exception(answer_response_json['request'])


def FindSolveCaptcha(api_key, driver, form):
    """
    Finds and solves Captchas using the 2Captcha service. When this function is done running, the captcha will be solved
    (not visibly), and you can submit the form.

    Handles errors if there is no captcha present.

    Captcha's are generally tied to a form, to solve the captcha, we need the form that it's inside.

    The webdriver is also required to finish solving the captcha.

    :param api_key: The 2Captcha API key.
    :param driver: The webdriver controlling the browser.
    :param form: The form that houses the captcha.
    :return:
    """
    try:
        captcha_div = form.find_element_by_id("gRecaptcha")
        assert captcha_div.is_displayed(), '102'
        captcha_iframe = captcha_div.find_element_by_tag_name("iframe")
        assert captcha_iframe.is_displayed(), '102'
        captcha_src = urlparse(captcha_iframe.get_attribute("src"))
        assert captcha_src, '102'
        captcha_query = parse_qs(captcha_src.query)
        assert captcha_query, '102'
        captcha_sitekey = captcha_query['k'][0]
    except NoSuchElementException:
        return '102'
    except AssertionError as x:
        return x.args[0]
    else:
        solution = SolveCaptcha(api_key, captcha_sitekey, driver.current_url)
        captcha_answer = captcha_div.find_element_by_id("g-recaptcha-response")
        driver.execute_script(f"arguments[0].innerText = '{solution}'", captcha_answer)