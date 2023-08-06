"""Main module."""

import logging
import requests

from lxml import html
from collections import namedtuple
from datetime import datetime

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

XP_USAGE_SINCE = '//*[@id="main"]/div/section/' \
                 'div[2]/section[1]/div/h2/text()'
XP_USAGE_TOTAL = '//*[@id="main"]/div/section/' \
                 'div[2]/section[1]/div/div/div/strong/text()'
XP_ACCOUNT_BALANCE = '//*[@id="main"]/div/section/' \
                     'div[1]/section[1]/div/span/text()'
XP_BUNDLE_NAME = '//*[@id="main"]/div/section/' \
                 'div[2]/section[2]/div/div[1]/div[1]/ul[1]/li/text()'

# 'My Usage' page:
XP_USAGE_TOTAL_DATA_USED = '//*[@id="main"]/div[1]/' \
                           'section/div[2]/dl/dd[4]/strong/text()'
XP_USAGE_DATA_UPLOADED = '//*[@id="main"]/div[1]/' \
                         'section/div[2]/dl/dd[3]/text()'
XP_USAGE_DATA_DOWNLOADED = '//*[@id="main"]/div[1]/' \
                           'section/div[2]/dl/dd[2]/text()'
XP_TIME_SPENT_ONLINE = '//*[@id="main"]/div[1]/' \
                       'section/div[2]/dl/dd[1]/text()'
XP_USAGE_UPDATED = '//*[@id="main"]/div[1]/' \
                   'section/div[2]/p/text()'

# 'My Usage' page 'Your Broadband Logins' table
XP_LOGINS_TABLE_BASE = '//*[@id="main"]/div[1]/' \
                       'section/div[3]/table/tbody/tr[1]/'

XP_USAGE_DATA_DOWNLOADED_TODAY_SO_FAR = '{}td[6]/text()'.format(
    XP_LOGINS_TABLE_BASE)
XP_USAGE_DATA_UPLOADED_TODAY_SO_FAR = '{}td[5]/text()'.format(
    XP_LOGINS_TABLE_BASE)
XP_USAGE_ONLINE_TIME_TODAY = '{}td[4]/text()'.format(XP_LOGINS_TABLE_BASE)
XP_USAGE_IP_ADDRESS_TODAY = '{}td[3]/text()'.format(XP_LOGINS_TABLE_BASE)
XP_USAGE_ENDED_TIME_TODAY = '{}td[2]/text()'.format(XP_LOGINS_TABLE_BASE)
XP_USAGE_STARTED_TIME_TODAY = '{}td[1]/text()'.format(XP_LOGINS_TABLE_BASE)

# Bill period dropdown
XP_USAGE_PERIOD_CURRENT = '//*[@id="billing-period"]/option[1]/text()'

DEFAULT_FAIR_USAGE_LIMIT_GB = 1024
DATA_KILOBYTES = "kB"
DATA_MEGABYTES = "MB"
DATA_GIGABYTES = "GB"
DATA_TERABYTES = "TB"

UNKNOWN_VALUE = ""


class Account:
    """
    Represents a VF Account.
    """

    def __init__(self, username, password, token1, token2,
                 fair_usage_limit=DEFAULT_FAIR_USAGE_LIMIT_GB):
        """
        Defines an vf account.

        :param username: VF Broadband username (email)
        :param password: VF Broadband password
        :param token1: Token 1
        :param token2: Token 2
        :param fair_usage_limit: If your fair usage is
        not 1000 GB, specify it here.
        """
        log.debug("Initialising new VF Account")

        if "@" not in username:
            log.warning("Vodafone Broadband username "
                        "should be an email address.")
        self.logged_in = False
        self.overview_data = None
        self.data = None

        self.username = username
        self.password = password

        self.verification_token1 = token1
        self.verification_token2 = token2
        self.fair_usage_limit = fair_usage_limit

    def init_login(self):
        """ Do the account overview request and return account tuple """
        self._session = requests.Session()
        self._session.get('https://n.vodafone'
                          '.ie/en.html')

        data = '{"userName":"' + self.username + '"}'

        self._session.post('https://n.vodafone.ie/'
                           'bin/mvc.do/credential/check/mml',
                           data=data)

        params = (
            ('t', '1'),
        )

        log.debug(f"self.username {self.username}")
        log.debug(f"self.verification_token1 {self.verification_token1}")
        log.debug(f"self.verification_token2 {self.verification_token2}")

        data = {
            '__RequestVerificationToken': self.verification_token2,
            'emailAddress': self.username,
            'password': self.password
        }

        response = self._session.post('https://broadband.'
                                      'vodafone.ie/myaccount/session/login',
                                      headers=self.get_headers(),
                                      cookies=self.get_cookies(),
                                      params=params,
                                      data=data
                                      )

        # usage since date
        # e.g. ['Since 15 Apr 2020']
        usage_since = self.get_xpath_value(response, XP_USAGE_SINCE)
        # data usage. e.g. ['397.35 GB']
        usage_value_raw = self.get_xpath_value(response, XP_USAGE_TOTAL)
        usage_value, usage_value_unit, usage_percent, usage_value_mb = \
            self.get_usage_values(usage_value_raw)

        # account due fee. e.g. €60
        account_balance = self.get_xpath_value(response, XP_ACCOUNT_BALANCE)
        # Bundles
        # Gigabit Broadband 300 (eir)
        bundle_name = self.get_xpath_value(response, XP_BUNDLE_NAME)

        if usage_value_raw == UNKNOWN_VALUE:
            log.warning("Unable to get usage data.")
            # log.warning(response.content)
        else:
            AccountDetails = namedtuple("AccountDetails",
                                        ["usage_since",
                                         "usage_value",
                                         "usage_value_raw",
                                         "usage_value_unit",
                                         "usage_percent",
                                         "last_updated",
                                         "account_balance",
                                         "bundle_name"])
            account_details = AccountDetails(usage_since,
                                             usage_value,
                                             usage_value_raw,
                                             usage_value_unit,
                                             usage_percent,
                                             datetime.now(),
                                             account_balance,
                                             bundle_name)
            log.debug(account_details)
            self.logged_in = True
            self.overview_data = account_details
            return account_details

        return None

    # flake8: noqa: E501
    def get_account_usage_request(self):
        """ Do the account usage request and return account tuple """

        self.init_login()
        response = self._session.get('https://broadband.vodafone.'
                                     'ie/myaccount/usage',
                                     headers=self.get_headers(),
                                     cookies=self.get_cookies()
                                     )

        log.info("'Your Broadband Usage' in result? {}".format(
            "Your Broadband Usage" in response.text))

        if "Error Occurred" in response.text:
            log.error("‼️ 'Error Occurred' in response.")
        if "Your Broadband Usage" in response.text:
            log.info("✅ Looking good. 'Your Broadband Usage' in result.")
            bill_period = self.get_xpath_value(
                response, XP_USAGE_PERIOD_CURRENT)
            total_used_value, total_used_unit, total_used_percent, total_used_value_mb = self.get_usage_values(
                self.get_xpath_value(response, XP_USAGE_TOTAL_DATA_USED))
            total_uploaded_value, total_uploaded_used_unit, total_uploaded_used_percent, total_uploaded_value_mb = \
                self.get_usage_values(
                    self.get_xpath_value(response, XP_USAGE_DATA_UPLOADED))
            total_downloaded_value, total_downloaded_used_unit, total_downloaded_used_percent, total_downloaded_value_mb = \
                self.get_usage_values(
                    self.get_xpath_value(response, XP_USAGE_DATA_DOWNLOADED))
            total_time_spent_online = self.get_xpath_value(
                response, XP_TIME_SPENT_ONLINE)
            total_updated_time = self.get_xpath_value(
                response, XP_USAGE_UPDATED)

            today_downloaded_value, today_downloaded_used_unit, today_downloaded_used_percent, today_downloaded_value_mb = \
                self.get_usage_values(
                    self.get_xpath_value(response, XP_USAGE_DATA_DOWNLOADED_TODAY_SO_FAR))
            today_uploaded_value, today_uploaded_used_unit, today_uploaded_used_percent, today_uploaded_value_mb = \
                self.get_usage_values(
                    self.get_xpath_value(response, XP_USAGE_DATA_UPLOADED_TODAY_SO_FAR))
            today_ip_address = self.get_xpath_value(
                response, XP_USAGE_IP_ADDRESS_TODAY)
            today_online_time = self.get_xpath_value(
                response, XP_USAGE_ONLINE_TIME_TODAY)

            AccountUsageDetails = namedtuple("AccountUsageDetails",
                                             ["bill_period",
                                              "total_time_spent_online",
                                              "total_used_value",
                                              "total_used_value_mb",
                                              "total_used_unit",
                                              "total_used_percent",
                                              "last_updated",
                                              "total_uploaded_value",
                                              "total_uploaded_value_mb",
                                              "total_uploaded_used_unit",
                                              "total_downloaded_value",
                                              "total_downloaded_value_mb",
                                              "total_downloaded_used_unit",
                                              "total_updated_time",
                                              "today_downloaded_value",
                                              "today_downloaded_value_mb",
                                              "today_downloaded_used_unit",
                                              "today_uploaded_value",
                                              "today_uploaded_value_mb",
                                              "today_uploaded_used_unit",
                                              "today_ip_address",
                                              "today_online_time"
                                              ])
            account_usage_details = AccountUsageDetails(bill_period,
                                                        total_time_spent_online,
                                                        total_used_value,
                                                        total_used_value_mb,
                                                        total_used_unit,
                                                        total_used_percent,
                                                        datetime.now(),
                                                        total_uploaded_value,
                                                        total_uploaded_value_mb,
                                                        total_uploaded_used_unit,
                                                        total_downloaded_value,
                                                        total_downloaded_value_mb,
                                                        total_downloaded_used_unit,
                                                        total_updated_time,
                                                        today_downloaded_value,
                                                        today_downloaded_value_mb,
                                                        today_downloaded_used_unit,
                                                        today_uploaded_value,
                                                        today_uploaded_value_mb,
                                                        today_uploaded_used_unit,
                                                        today_ip_address,
                                                        today_online_time)
            log.debug(account_usage_details)
            self.logged_in = True
            self.data = account_usage_details
            return account_usage_details

        return None

    def get_cookies(self):
        cookies = self._session.cookies
        # log.debug("cookies now: {}".format(self._session.cookies))
        cookies['__RequestVerificationToken'] = self.verification_token1

        return cookies

    def get_headers(self):
        return {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Origin': 'https://broadband.vodafone.ie',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Macintosh; '
                          'Intel Mac OS X 10_15_4) '
                          'AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome/81.0.4044.129 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml'
                      ',application/xml;q=0.9,image/webp,'
                      'image/apng,*/*;q=0.8,application/'
                      'signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://broadband.vodafone.ie'
                       '/myaccount/session/login?t=1',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

    def get_xpath_value(self, response, path):
        """ Returns first result of xpath
        match, or UNKNOWN_VALUE if not found. """
        tree = html.fromstring(response.content)
        try:
            result = tree.xpath(path)
            if len(result) == 0:
                log.warning(f"xpath not found: {path}")
                return UNKNOWN_VALUE
            return result[0]
        except ValueError:
            log.warning(f"xpath not found: {path}")

        return UNKNOWN_VALUE

    def is_logged_in(self):
        """Returns true if a successful login has happened"""
        return self.logged_in

    def get_usage_values(self, usage_value_raw):
        """ Get usage values. """
        try:
            usage_value = usage_value_raw.replace(',', '').split(' ')[0]
            usage_value_unit = self.get_unit(usage_value_raw.split(' ')[1])
            usage_percent = int((float(usage_value) /
                                 self.fair_usage_limit) * 100)

            if usage_value_unit == DATA_MEGABYTES:
                usage_value_mb = usage_value
            elif usage_value_unit == DATA_GIGABYTES:
                usage_value_mb = float(usage_value) * 1024
            elif usage_value_unit == DATA_TERABYTES:
                usage_value_mb = float(usage_value) * 1024 * 1024
            else:
                log.warning(f"Unable to determine usage_value_mb. usage_value_unit: {usage_value_unit}")
                usage_value_mb = None

            return usage_value, usage_value_unit, usage_percent, usage_value_mb
        except Exception:
            log.error(
                "Unable to calculate usage. usage_value_raw: {}".format(usage_value_raw))

        return None, None, None, None

    def get_unit(self, unit_string):
        value = unit_string.upper()
        if value == "KB":
            return DATA_KILOBYTES
        if value == "MB":
            return DATA_MEGABYTES
        if value == "GB":
            return DATA_GIGABYTES
        if value == "TB":
            return DATA_TERABYTES
