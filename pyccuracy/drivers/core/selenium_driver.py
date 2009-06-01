#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Bernardo Heynemann <heynemann@gmail.com>
# Copyright (C) 2009 Gabriel Falcão <gabriel@nacaolivre.org>
#
# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.opensource.org/licenses/osl-3.0.php
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from traceback import format_exc

from selenium import *

from pyccuracy.drivers import BaseDriver, DriverError
from selenium_element_selector import *

class SeleniumDriver(BaseDriver):
    backend = 'selenium'
    
    def __init__(self, context, selenium=None):
        self.context = context
        self.selenium = selenium

    def start_test(self, url=None):
        host = self.context.settings.extra_args.get("selenium.server", "localhost")
        port = self.context.settings.extra_args.get("selenium.port", 4444)
        browser_to_run = self.context.settings.browser_to_run

        if not self.selenium:
            self.selenium = selenium(host, port, browser_to_run, url)

        try:
            self.selenium.start()
        except Exception, e:
            raise DriverError("Error when starting selenium. Is it running?\n\n\n Error: %s\n" % format_exc(e))

    def stop_test(self):
        self.selenium.stop()

    def resolve_element_key(self, context, element_type, element_key):
        if not context: 
            return element_key
        return SeleniumElementSelector.element(element_type, element_key)

    def page_open(self, url):
        self.selenium.open(url)

    def wait_for_page(self, timeout=10000):
        self.selenium.wait_for_page_to_load(timeout)

    def click_element(self, element_selector):
        self.selenium.click(element_selector)

    def get_title(self):
        return self.selenium.get_title()