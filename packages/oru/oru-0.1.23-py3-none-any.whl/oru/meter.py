"""Orange and Rockland Utility Smart Energy Meter"""
import requests
import logging
import asyncio
from pyppeteer import launch
import os
import json

_LOGGER = logging.getLogger(__name__)


class MeterError(Exception):
    pass


class Meter(object):
    """A smart energy meter of Orange and Rockland Utility.

    Attributes:
        email: A string representing the email address of the account
        password: A string representing the password of the account
        mfa_answer: A string representing the multiple factor authorization answer for the account
        account_id: A string representing the account's id
        meter_id: A string representing the meter's id
    """

    def __init__(self, email, password, mfa_answer, account_id, meter_id, loop=None):
        """Return a meter object whose meter id is *meter_id*"""
        self.email = email
        self.password = password
        self.mfa_answer = mfa_answer
        self.account_id = account_id
        self.meter_id = meter_id
        self.loop = loop
        # _LOGGER.debug("Oru email = %s", self.email.replace(self.email[:10], '*'))
        # _LOGGER.debug("Oru password = %s", self.password.replace(self.password[:9], '*'))
        # _LOGGER.debug("Oru mfa_answer = %s", self.mfa_answer.replace(self.mfa_answer[:8], '*'))
        # _LOGGER.debug("Oru account_id = %s", self.account_id.replace(self.account_id[:20], '*'))
        # _LOGGER.debug("Oru meter_id = %s", self.meter_id.replace(self.meter_id[:5], '*'))

    async def last_read(self):
        """Return the last meter read value and unit of measurement"""
        try:
            asyncio.set_event_loop(self.loop)
            asyncio.create_task(self.browse())
            await self.browse()

            # parse the return reads and extract the most recent one
            # (i.e. last not None)
            jsonResponse = json.loads(self.raw_data)
            lastRead = None
            for read in jsonResponse['reads']:
                if read['value'] is None:
                    break
                lastRead = read
            _LOGGER.debug("lastRead = %s", lastRead)

            self.last_read_val = lastRead['value']
            self.unit_of_measurement = jsonResponse['unit']

            _LOGGER.debug("last read = %s %s", self.last_read_val, self.unit_of_measurement)

            return self.last_read_val, self.unit_of_measurement
        except:
            raise MeterError("Error requesting meter data")

    async def browse(self):
        browser = await launch({
            "defaultViewport": {"width": 1920, "height": 1080},
            "dumpio": True,
            # "executablePath": "/root/.local/share/pyppeteer/local-chromium/588429/chrome-linux/chrome",
            "args": ["--no-sandbox"]})
        page = await browser.newPage()

        await page.goto('https://www.oru.com/en/login')
        sleep = 8000
        _LOGGER.debug("Waiting for = %s millis", sleep)
        await page.waitFor(sleep)
        # await page.screenshot({'path': 'oru0.png'})

        await page.type("#form-login-email", self.email)
        await page.type("#form-login-password", self.password)
        await page.click("#form-login-remember-me")
        await page.click(".submit-button")
        # Wait for login to authenticate
        sleep = 20000
        _LOGGER.debug("Waiting for = %s millis", sleep)
        await page.waitFor(sleep)
        # await page.screenshot({'path': 'oru1.png'})

        # Enter in 2 factor auth code (see README for details)
        await page.type("#form-login-mfa-code", self.mfa_answer)
        # await page.screenshot({'path': 'oru2.png'})
        await page.click(".js-login-new-device-form .button")
        # Wait for authentication to complete
        await page.waitForNavigation()
        sleep = 15000
        _LOGGER.debug("Waiting for = %s millis", sleep)
        await page.waitFor(sleep)
        # await page.screenshot({'path': 'oru2.1.png'})

        # Access the API using your newly acquired authentication cookies!
        api_page = await browser.newPage()
        api_url = 'https://oru.opower.com/ei/edge/apis/cws-real-time-ami-v1/cws/oru/accounts/' + self.account_id + '/meters/' + self.meter_id + '/usage'
        await api_page.goto(api_url)
        # await api_page.screenshot({'path': 'oru3.png'})

        data_elem = await api_page.querySelector('pre')
        self.raw_data = await api_page.evaluate('(el) => el.textContent', data_elem)
        _LOGGER.debug(self.raw_data)

        await browser.close()
