# -*- coding: utf-8 -*-
import scrapy
import json
from zhihu.items import ZhihuItem
import re
import time

class ZhihuuserSpider(scrapy.Spider):
    name = 'zhihuuser'
    allowed_domains = ['www.zhihu.com']
    user_include ='locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,included_answers_count,included_articles_count,included_text,message_thread_token,account_status,is_active,is_bind_phone,is_force_renamed,is_bind_sina,is_privacy_protected,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,is_org_createpin_white_user,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'
    user_url ='https://www.zhihu.com/api/v4/members/{user}?include={include}'
    follow_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit=20'
    follow_include ='data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit=20'
    follows_include = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def parse_user(self, response):
        result = json.loads(response.text)
        item = ZhihuItem()
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        if 'business' in item.keys():
            item['business'] = item['business']['name']
        if 'locations' in item.keys() :
            if not item['locations'] == []:
                item['locations'] = item['locations'][0]['name']
        if 'educations' in result.keys():
            if 'major' in str(result['educations']):
                item['major'] = result['educations'][0]['major']['name']
            if 'school' in str(result['educations']):
                item['school'] = result['educations'][0]['school']['name']
        yield item
        yield scrapy.Request(
            self.follow_url.format(user = result.get('url_token'), include = self.follow_include, offset=0),
            self.parse_follow)
        yield scrapy.Request(
            self.follows_url.format(user = result.get('url_token'), include = self.follows_include, offset = 0),
            self.parse_follows
        )

    def parse_follow(self,response):
        result = json.loads(response.text)
        if 'data' in result.keys():
            datas = result.get('data')
            for data in datas:
                url_token = data['url_token']
                yield scrapy.Request(self.user_url.format(user = url_token,include = self.user_include),callback=self.parse_user)
        if 'paging' in result.keys() and result.get('paging')['is_end'] == False:
            next_page = result.get('paging')['next']
            yield scrapy.Request(next_page,callback=self.parse_follow)


    def parse_follows(self,response):
        result = json.loads(response.text)
        if 'data' in result.keys():
            datas = result.get('data')
            for data in datas:
                url_token = data['url_token']
                yield scrapy.Request(self.user_url.format(user = url_token,include = self.user_include),callback=self.parse_user)
        if 'paging' in result.keys() and result.get('paging')['is_end'] == False:
            next_page = result.get('paging')['next']
            yield scrapy.Request(next_page,callback=self.parse_follows)

    def start_requests(self):
        yield scrapy.Request(self.user_url.format(user='excited-vczh', include=self.user_include),
                      self.parse_user)
        yield scrapy.Request(self.follow_url.format(user='excited-vczh', include=self.follow_include, offset=0),
                      self.parse_follow)
        yield scrapy.Request(self.follows_url.format(user='excited-vczh', include=self.follows_include, offset=0,),
                      self.parse_follows)

