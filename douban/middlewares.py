# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import logging
import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


class RandomProxyMiddleware(object):
    logger = logging.getLogger(__name__)

    def process_request(self, request, spider):
        self.logger.debug("Using Proxy")
        request.meta['proxy'] = 'http://122.112.231.109:9999'
        return None

    def process_response(self, request, response, spider):
        response.status = 202
        return response


class RandomUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent_list):
        super().__init__()
        self.user_agent_list = user_agent_list

    @classmethod
    def from_crawler(cls, crawler):
        return cls(user_agent_list=crawler.settings.get('USER_AGENT_LIST'))

    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agent_list)
        if user_agent:
            request.headers['User-Agent'] = user_agent
        return None
