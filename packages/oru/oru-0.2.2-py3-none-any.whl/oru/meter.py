"""Orange and Rockland Utility Smart Energy Meter"""
import requests
import logging
import asyncio
from pyppeteer import launch
import os
import json
import pyotp

_LOGGER = logging.getLogger(__name__)


class MeterError(Exception):
    pass


class Meter(object):
    """A smart energy meter of Orange and Rockland Utility.

    Attributes:
        email: A string representing the email address of the account
        password: A string representing the password of the account
        mfa_type: Meter.MFA_TYPE_SECURITY_QUESTION or Meter.MFA_TYPE_TOTP
        mfa_secret: A string representing the multiple factor authorization secret
        account_id: A string representing the account's id
        meter_id: A string representing the meter's id
    """

    MFA_TYPE_SECURITY_QUESTION = 'SECURITY_QUESTION'
    MFA_TYPE_TOTP = 'TOTP'

    def __init__(self, email, password, mfa_type, mfa_secret, account_id, meter_id, loop=None):
        """Return a meter object whose meter id is *meter_id*"""
        self.email = email
        if self.email is None:
            raise MeterError("Error initializing meter Oru data - email is missing")
        # _LOGGER.debug("Oru email = %s", self.email.replace(self.email[:10], '*'))

        self.password = password
        if self.password is None:
            raise MeterError("Error initializing Oru meter data - password is missing")
        #_LOGGER.debug("Oru password = %s", self.password.replace(self.password[:9], '*'))

        self.mfa_type = mfa_type
        if self.mfa_type is None:
            raise MeterError("Error initializing Oru meter data - mfa_type is missing")
        _LOGGER.debug("Oru mfa_type = %s", self.mfa_type)
        if self.mfa_type not in [Meter.MFA_TYPE_SECURITY_QUESTION, Meter.MFA_TYPE_TOTP]:
            raise MeterError("Error initializing Oru meter data - unsupported mfa_type %s", self.mfa_type)

        self.mfa_secret = mfa_secret
        if self.mfa_secret is None:
            raise MeterError("Error initializing Oru meter data - mfa_secret is missing")
        #_LOGGER.debug("Oru mfa_secret = %s", self.mfa_secret.replace(self.mfa_secret[:8], '*'))

        self.account_id = account_id
        if self.account_id is None:
            raise MeterError("Error initializing  Orumeter data - account_id is missing")
        #_LOGGER.debug("Oru account_id = %s", self.account_id.replace(self.account_id[:20], '*'))

        self.meter_id = meter_id
        if self.meter_id is None:
            raise MeterError("Error initializing  Orumeter data - meter_id is missing")
        #_LOGGER.debug("Oru meter_id = %s", self.meter_id.replace(self.meter_id[:5], '*'))

        self.loop = loop

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
        mfa_code = self.mfa_secret
        if self.mfa_type == self.MFA_TYPE_TOTP:
            mfa_code = pyotp.TOTP(self.mfa_secret).now()
        #_LOGGER.debug("mfa_code = %s", mfa_code)
        await page.type("#form-login-mfa-code", mfa_code)
        await page.screenshot({'path': 'oru2.png'})
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
