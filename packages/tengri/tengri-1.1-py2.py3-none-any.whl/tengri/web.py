# -*- coding: utf-8 -*-
"""
    tengri.web
    ----------

    Web specific constants. Weather pages, xpaths, user_agents.

    :copyright: (c) 2017 by Robert Durkaj.
    :license: MIT, see the LICENSE for more details.
"""
# User-Agents from "http://useragentstring.com"
USER_AGENTS = (
    ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/41.0.2227.1 Safari/537.36'),
    ('Mozilla/5.0 (Windows NT 6.1) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/41.0.2228.0 Safari/537.36'),
    ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) '
     'AppleWebKit/602.3.12 (KHTML, like Gecko) '
     'Version/10.0.2 Safari/602.3.12'),
    'Mozilla/5.0 (Windows NT 6.1; x64; rv:25.0) Gecko/20100101 Firefox/29.0',
    ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) '
     'Gecko/20100101 Firefox/33.0'),
    'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0',
)


def _meteoblue_page():
    site = 'meteoblue.com'
    div = './/div[@id="day2"]'
    lines = (
        ('',            './/div[@id="header"]/div/div[1]/h1'),
        ('',            './/div[@class="location_description"]'),
        ('',            div + '//div[@class="tab_day_long"]'),
        ('Max temp',    div + '//div[@class="tab_temp_max"]'),
        ('Min temp',    div + '//div[@class="tab_temp_min"]'),
        ('Wind',        div + '//div[@class="wind"]'),
        ('Precipation', div + '//div[@class="tab_precip"]'),
    )
    return locals()


def _mountain_page():
    site = 'mountain-forecast.com'
    table = './/div[@id="forecast-cont"]/table'
    lines = (
        ('',            './/title'),
        ('',            table + '/thead/tr[2]/td[2]/button/div'),
        ('Summary',     table + '/tbody/tr[3]/td[3]'),
        ('High temp',   table + '/tbody/tr[7]/td[3]/span/span'),
        ('Low temp',    table + '/tbody/tr[8]/td[3]/span/spa'),
        ('Wind',        table + '/tbody/tr[2]/td[3]/div/div/span'),
        ('Rain',        table + '/tbody/tr[5]/td[3]/span/span'),
        ('Snow',        table + '/tbody/tr[6]/td[3]/span/span'),
    )
    return locals()


def _yrno_page():
    site = 'yr.no'
    table = './/*[@id="ctl00_ctl00_contentBody"]/div[2]/div[2]/table[2]'
    lines = (
        ('', './/*[@id="ctl00_ctl00_contentBody"]/div[1]/h1/span'),
        ('',                    table + '/caption'),
        ('Temp (01:00-07:00)',  table + '/tbody/tr[1]/td[3]'),
        ('Temp (07:00-13:00)',  table + '/tbody/tr[2]/td[3]'),
        ('Wind',                table + '/tbody/tr[2]/td[5]'),
        ('Precipation',         table + '/tbody/tr[2]/td[4]'),
    )
    return locals()


def weather_pages():
    return _meteoblue_page(), _mountain_page(), _yrno_page()
