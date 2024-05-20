import unittest
import os
from appium import webdriver
from time import sleep
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy


PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

capabilities = {'platformName': 'Android',
                'deviceName': "Genymotion Cloud",
                'appium:automationName': 'uiautomator2',
                'app': PATH('ApiDemos-debug.apk'),
                'udid': 'localhost:10000',
                # port nalezy odczytac z adb devices jesli nie ustawiony jako staly
                'appPackage': 'io.appium.android.apis',
                'appActivity': 'io.appium.android.apis.ApiDemos'}

appium_server_url = 'http://localhost:4723'
capabilities_options = UiAutomator2Options().load_capabilities(capabilities)

class testAppiumWIFI(unittest.TestCase):
    def setUp(self):
        sleep(2)
        # polaczenie z Appium, port jest staly dla Appium
        self.driver = webdriver.Remote(command_executor=appium_server_url, options=capabilities_options)
        self.driver.implicitly_wait(3)

    def tearDown(self):
        sleep(1)
        self.driver.quit()

    def testWIFI(self):
        # with self.assertRaises(NoSuchElementException):
        self.driver.is_app_installed('io.appium.android.apis')
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Preference').click()
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, '3. Preference dependencies').click()
        checkboxes = self.driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().checkable(true)')
        for el in checkboxes:
            is_checked = self.driver.find_element(AppiumBy.CLASS_NAME, 'android.widget.CheckBox').get_attribute('checked')
        if is_checked == 'true':
            print('checkbox jest zaznaczony')
        else:
            el.click()
            sleep(2)
        passwordInput = '12345'
        sleep(5)
        self.driver.find_element(AppiumBy.XPATH,'//*[@text="WiFi settings"]').click()
        self.driver.find_element(AppiumBy.CLASS_NAME,'android.widget.EditText').send_keys(passwordInput)
        passwordCurrent = self.driver.find_element(AppiumBy.CLASS_NAME,'android.widget.EditText').get_attribute('text')
        sleep(3)
        # asercja
        self.assertEqual(passwordInput, passwordCurrent)

        # wartosc w nawiasie jest wzieta z resouce-id z uiautomatorviewer
        self.driver.find_element(AppiumBy.ID,'android:id/button1').click()

        # wyjscie back
        self.driver.back()
        self.driver.keyevent(4)
        sleep(3)
        if (len(self.driver.find_elements(AppiumBy.CLASS_NAME,'android.widget.EdiText'))>0):
            self.assertTrue(True)

        # asercja to funkcja sprawdzajaca czy test przechodzi(passed) czy nie (failed)

if __name__ == 'main':
    suite = unittest.TestLoader().loadTestsFromTestCase(testAppiumWIFI)
