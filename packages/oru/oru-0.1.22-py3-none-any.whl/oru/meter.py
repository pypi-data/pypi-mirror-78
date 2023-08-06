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
        _LOGGER.debug("New oru meter id = %s", self.meter_id)

    async def last_read(self):
        """Return the last meter read in WH"""
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

            _LOGGER.debug("val = %s %s", self.last_read_val, self.unit_of_measurement)

            return self.last_read_val
        except requests.exceptions.RequestException:
            raise MeterError("Error requesting meter data")

    async def browse(self):
        browser = await launch({"defaultViewport": {"width": 1920, "height": 1080}, "dumpio": True,
            # "executablePath": "/root/.local/share/pyppeteer/local-chromium/588429/chrome-linux/chrome",
            "args": ["--no-sandbox"]})
        page = await browser.newPage()

        await page.goto('https://www.oru.com/en/login')
        # await page.screenshot({'path': 'oru0.png'})

        await page.type("#form-login-email", self.email)
        await page.type("#form-login-password", self.password)
        await page.click("#form-login-remember-me")
        await page.click(".submit-button")
        # Wait for login to authenticate
        await page.waitFor(20000)
        # await page.screenshot({'path': 'oru1.png'})

        # Enter in 2 factor auth code (see README for details)
        await page.type("#form-login-mfa-code", self.mfa_answer)
        await page.screenshot({'path': 'oru2.png'})
        await page.click(".js-login-new-device-form .button")
        # Wait for authentication to complete
        await page.waitForNavigation()
        await page.waitFor(20000)
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
