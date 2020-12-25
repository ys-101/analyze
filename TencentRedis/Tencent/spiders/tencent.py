# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
import json
from ..items import TencentItem

class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['careers.tencent.com']
    one_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=11111&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword={}&pageIndex={}&pageSize=10&language=zh-cn&area=cn'
    two_url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=111111&postId={}&language=zh-cn'
    keyword = input('请输入职位类别:')
    keyword = parse.quote(keyword)
    # start_urls: 一级页面第1页的URL地址
    def start_requests(self):
        first_url = self.one_url.format( self.keyword, 1)
        yield scrapy.Request(url=first_url,callback=self.parse, dont_filter=True)


    def parse(self, response):
        """生成所有一级页面的url地址,交给调度器入队列"""
        # 获取总页数
        html = json.loads(response.text)
        count = html['Data']['Count']
        total = count//10 if count%10==0 else count//10 + 1
        # 生成所有页的URL地址
        for index in range(1, total + 1):
            page_url = self.one_url.format(

                self.keyword,
                index
            )
            # 调度器入队列
            yield scrapy.Request(
                url=page_url,
                callback=self.detail_page,
                dont_filter=True,
            )

    def detail_page(self, response):
        """一级页面:提取每个职位的postid的值"""
        html = json.loads(response.text)
        for one_job_dict in html['Data']['Posts']:
            item = TencentItem()
            item['job_id'] = one_job_dict['PostId']
            # 生成详情页的URL地址,交给调度器入队列
            url = self.two_url.format(

                item['job_id']
            )
            # meta参数:在不同的解析函数之间传递数据
            # meta字典先到调度器,再到下载器,meta会做为
            # response的一个属性,传递给下个解析函数
            yield scrapy.Request(
                url=url,
                meta={'item':item},
                callback=self.get_job_info
            )

    def get_job_info(self, response):
        """二级页面:提取每个职位的信息"""
        html = json.loads(response.text)
        # 获取item对象,利用response的meta属性
        item = response.meta['item']
        item['job_name'] = html['Data']['RecruitPostName']
        item['job_type'] = html['Data']['CategoryName']
        item['job_city'] = html['Data']['LocationName']
        item['job_time'] = html['Data']['LastUpdateTime']
        item['job_require'] = html['Data']['Requirement']
        item['job_duty'] = html['Data']['Responsibility']

        # 至此,一条完整的数据提取完成,交给管道文件处理
        yield item









