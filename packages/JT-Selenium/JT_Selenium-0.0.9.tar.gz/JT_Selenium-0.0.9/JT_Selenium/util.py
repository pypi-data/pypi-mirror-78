import json
import os
import time
from io import BytesIO
from os.path import dirname, exists
from sys import platform
from urllib.parse import urlparse, parse_qs
from zipfile import ZipFile
from typing import Callable

import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from .chrome_urls import urls

import requests
from requests.exceptions import HTTPError

STATUS_CODES = {
    '400': "UNKOWN ERROR",
    '404': "RESULTS NOT FOUND",
    '410': "REMOVED",
    '100': "ALREADY DONE",
    '101': "DECIDED NOT TO",
    '500': "TIME OUT",
    '200': "OK",
}


# TODO: use packaging.version.parse instead
def VerNum(num: str, ignore=0):
    """
    Converts a string representing a version number to an integer that can be compared

    :param num:
    :param ignore:
    :return:
    """
    return sum([1000000 ** i * int(n) for i, n in enumerate(num.split('.')[::-1][ignore:])])


def CheckChrome():
    """
    Checks if there is a portable version of chrome and it's driver downloaded to the folder this package is in.

    :return: A tuple of booleans denoting what's downloaded - (chrome, chromedriver)
    """
    if platform == "win32":
        response = requests.get("https://omahaproxy.appspot.com/all?csv=1")
        response.raise_for_status()
        for row in response.content.decode().split('\n'):
            row = row.split(',')
            if row[0] == 'win' and row[1] == 'stable':
                latest_version = VerNum(row[2], 1)
                print(row)
                break
        else:
            raise Exception
        try:
            assert exists(f"{dirname(__file__)}/chrome-win")
            versions = map(
                lambda s: VerNum(s, 1),
                filter(
                    lambda _: "manifest" in _,
                    os.listdir(f"{dirname(__file__)}/chrome-win")
                )
            )
            assert max(versions) >= latest_version
            update = False
        except AssertionError:
            update = True

        return (
            not update,
            exists(f"{dirname(__file__)}/chromedriver_win32/chromedriver.exe")
        )
    elif platform == "linux":
        return (
            exists(f"{dirname(__file__)}/chrome-linux/chrome"),
            exists(f"{dirname(__file__)}/chromedriver_linux64/chromedriver")
        )
    elif platform == "darwin":
        return (
            exists(f"{dirname(__file__)}/chrome-mac/Chromium.app/Contents/MacOS/Chromium"),
            exists(f"{dirname(__file__)}/chromedriver_mac64/chromedriver")
        )


def RecChmod(path, mode):
    """
    Simple wrapper for os.chmod that runs it in recursive mode.

    :param path: File or directory to change the permissions for.
    :param mode: Permissions to set in octal form - eg. 0o777 (the 0o tells Python it's an octal number)
    :return:
    """
    os.chmod(path, mode)
    for dirpath, dirnames, filenames in os.walk(path):
        for dirname in dirnames:
            os.chmod("/".join([dirpath, dirname]), mode)
        for filename in filenames:
            os.chmod("/".join([dirpath, filename]), mode)


def DownloadExtractZip(url: str, path: str, chunk_size: int = None, progress_func: Callable = None):
    """
    Downloads a zip file and extracts it's contents to the specified path.

    :param url: Link to the file to download
    :param path: Location to extract the contents to
    :param chunk_size: If the file is to be downloaded in chunks
    :param progress_func: Function to call every iteration when downloading in chunks (primarily for progress bars)
                          Will be called using progress_func(total, downloaded) where the inputs are the number of bytes
    :return:
    """
    print(chunk_size)
    if chunk_size:
        file = BytesIO()
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            total = int(response.raw.info()['Content-Length'])
            downloaded = 0
            for chunk in response.iter_content(chunk_size=1024 * 16):
                file.write(chunk)
                downloaded += len(chunk)
                progress_func(total, downloaded)
        zip_file = ZipFile(BytesIO(response.content))

    else:
        response = requests.get(url)
        response.raise_for_status()
        zip_file = ZipFile(BytesIO(response.content))
    zip_file.extractall(path)


def InstallWin():
    """
    NOTE: Use this if you're using Windows
    Runs CheckChrome() and downloads a build of chromium and it's driver if needed.

    The location it downloads the software from is defined in chrome.json

    :return:
    """
    chrome, chromium = CheckChrome()

    if not chrome:
        print("Downloading Chrome")
        response = requests.get("https://omahaproxy.appspot.com/all?csv=1")
        response.raise_for_status()
        for row in response.content.decode().split('\n'):
            row = row.split(',')
            if row[0] == 'win' and row[1] == 'stable':
                num = int(row[7])
                print(row)
                break
        else:
            raise Exception
        i = 0
        while True:
            try:
                DownloadExtractZip(
                    f"https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Win_x64%2F{num}"
                    "%2Fchrome-win.zip?&alt=media",
                    f"{dirname(__file__)}"
                )
                DownloadExtractZip(
                    f"https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Win_x64%2F{num}"
                    "%2Fchromedriver_win32.zip?&alt=media",
                    f"{dirname(__file__)}"
                )
            except HTTPError:
                num += 1
                i += 1
                print(num)
                pass
            else:
                break
            if i > 100:
                raise Exception


def InstallMac():
    """
    NOTE: Use this if you're using MacOS
    Runs CheckChrome() and downloads a build of chromium and it's driver if needed.

    The location it downloads the software from is defined in chrome.json

    :return:
    """
    chrome, chromium = CheckChrome()
    if not chrome:
        print("Downloading Chrome")
        DownloadExtractZip(urls["mac"]["chrome"], f"{dirname(__file__)}")
        RecChmod(f"{dirname(__file__)}/chrome-mac/Chromium.app/Contents/MacOS/Chromium", 0o777)
    if not chromium:
        print("Downloading ChromeDriver")
        DownloadExtractZip(urls["mac"]["chromedriver"], f"{dirname(__file__)}")
        RecChmod(f"{dirname(__file__)}/chromedriver_mac64/chromedriver", 0o777)


def InstallLinux():
    """
    NOTE: Use this if you're using Linux
    Runs CheckChrome() and downloads a build of chromium and it's driver if needed.

    The location it downloads the software from is defined in chrome.json

    :return:
    """
    chrome, chromium = CheckChrome()
    if not chrome:
        print("Downloading Chrome")
        DownloadExtractZip(urls["linux"]["chrome"], f"{dirname(__file__)}")
        RecChmod(f"{dirname(__file__)}/chrome-linux/chrome", 0o777)
    if not chromium:
        print("Downloading ChromeDriver")
        DownloadExtractZip(urls["linux"]["chromedriver"], f"{dirname(__file__)}")
        try:
            RecChmod(f"{dirname(__file__)}/chromedriver_linux64/chromedriver", 0o777)
        except:
            pass


def Install():
    """
    Runs CheckChrome() and downloads a build of chromium and it's driver if needed.

    The location it downloads the software from is defined in chrome.json

    :return:
    """
    if platform == "win32":
        InstallWin()
    elif platform == "linux":
        InstallLinux()
    elif platform == "darwin":
        InstallLinux()


def OpenBrowser(options: selenium.webdriver.chrome.options.Options = None, cookie_path=None):
    """
    Opens a Selenium connected browser with the designated options and path to the cookies.

    Makes a check and downloads chrome if necessary.

    :param options:
    :param cookie_path:
    :return:
    """
    if options is None:
        options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-logging')
    if cookie_path:
        os.makedirs(cookie_path, exist_ok=True)
        options.add_argument(f'--user-data-dir={cookie_path}')

    if platform == "win32":
        InstallWin()
        options.binary_location = f"{dirname(__file__)}/chrome-win/chrome.exe"
        chromedriver = f"{dirname(__file__)}/chromedriver_win32/chromedriver.exe"
    elif platform == "linux":
        InstallLinux()
        options.binary_location = f"{dirname(__file__)}/chrome-linux/chrome"
        chromedriver = f"{dirname(__file__)}/chromedriver_linux64/chromedriver"
    elif platform == "darwin":
        InstallMac()
        options.binary_location = f"{dirname(__file__)}/chrome-mac/Chromium.app/Contents/MacOS/Chromium"
        chromedriver = f"{dirname(__file__)}/chromedriver_mac64/chromedriver"
    else:
        raise RuntimeError("Unknown platform")
    driver = webdriver.Chrome(chromedriver, options=options)
    driver.set_page_load_timeout(15)
    return driver


def WaitForLoad(element, timeout=5.):
    """
    Waits until an element has been fully loaded (both enabled and displayed).

    :param element: Element to wait for
    :param timeout: How long to wait before raising an error
    :return:
    """
    start = time.time()
    try:
        while not element.is_displayed() or not element.is_enabled():
            assert (time.time() - start) < timeout
    except AssertionError:
        raise TimeoutError


def WaitForFind(source, by, value, timeout=5.):
    """
    Looks for an element using the source.find_element(by, value) method.

    Waits until it actually finds an element

    :param source: Element or driver to look into
    :param by: How to look for it (see the documentation for selenium's webdriver.find_element())
    :param value: The value of the thing you want to find
    :param timeout: How long to wait before raising an error
    :return: The element it finds
    """
    start = time.time()
    while True:
        try:
            assert (time.time() - start) < timeout
            return source.find_element(by, value)
        except NoSuchElementException:
            pass
        except AssertionError:
            raise TimeoutError


def WaitForFindLoad(source, by, value, timeout=5.):
    """
    Combines WaitForLoad() and WaitForFind() to one function.

    Looks for an element using the source.find_element(by, value) method.
    Then
    Waits until that element has been fully loaded (both enabled and displayed).

    :param source: Element or driver to look into
    :param by: How to look for it (see the documentation for selenium's webdriver.find_element())
    :param value: The value of the thing you want to find
    :param timeout: How long to wait before raising an error
    :return: The element it finds
    """
    start = time.time()
    while True:
        try:
            assert (time.time() - start) < timeout, "500"
            element = source.find_element(by, value)
            break
        except NoSuchElementException:
            pass
        except AssertionError:
            raise TimeoutError
    WaitForLoad(element, timeout + start - time.time())
    return element


def CloseOtherTabs(driver, keep_tab=0):
    """
    Closes all tabs but the specified tab (default 0)

    :param keep_tab: The index of the tab to keep (default 0)
    :param driver: The selenium driver
    :return:
    """
    for tab in driver.window_handles[:keep_tab] + driver.window_handles[(keep_tab + 1):]:
        driver.switch_to.window(tab)
        driver.close()
    driver.switch_to.window(driver.window_handles[0])


def QueryEncode(q: dict):
    """

    :param q:
    :return:
    """
    return "?" + "&".join(["=".join(entry) for entry in q.items()])
