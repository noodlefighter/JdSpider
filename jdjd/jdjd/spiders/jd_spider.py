# -*- coding: utf-8 -*-

import scrapy
import json
from jdjd.items import JDItem

class JDSpider(scrapy.Spider):    
    # 爬虫名字
    name = 'jdspider'
    
    allowed_domains = ['jd.com', 'p.3.cn']
    
    # 类目 当cat=670,677,688时，category为688
    category = 688
        
    # 初始页
    page = 1
    
    # 列表页地址(category, page)
    list_url = 'https://list.jd.com/list.html?cat=%d&page=%d'
    
    # 商品价格查询地址(id)
    price_url = 'https://p.3.cn/prices/mgets?skuIds=J_%s'

    def start_requests(self):
        # 请求 商品列表页的第1页
        yield scrapy.Request(url=self.list_url%(self.category, self.page), callback=self.parse)

    def parse(self, response):
        # 商品列表页gl-item列表
        gl_items = response.css('.gl-item')
        for gl_item in gl_items:

            # 每一个gl_item都对应着一个商品，即对应着我们的采集项，所以这里建立jdItem
            item = JDItem()
            item['id'] = ''
            item['title'] = ''
            item['url'] = ''
            item['price'] = 0.0
            item['brand'] = ''
            item['model'] = ''
            item['color'] = ''
            item['ratio'] = ''
            item['resolution'] = ''
            item['refresh_rate'] = ''
            item['luminance'] = ''
            
            # 获取详情页地址, 如果地址以//开头, 转换成 https://
            url = gl_item.css('.gl-i-wrap .p-name a::attr(href)').extract_first()
            if url.startswith('//'):
                url = ''.join(['https:', url])
            item['url'] = url

            # 获取价格 先拿到商品id 再访问取价格的URL
            item['id'] = gl_item.css('.gl-item div::attr(data-sku)').extract_first()
            yield scrapy.Request(url=self.price_url%(item['id']), callback=self.parsePrice, meta={'item':item})
           
        if self.page < 100:
            self.page += 1

            # 下一页
            yield scrapy.Request(url=self.list_url%(self.category, self.page), callback=self.parse)

    
    def parsePrice(self, response): 
        item = response.meta['item']

        # json例 [{"cbf":"1","id":"J_5375281","m":"1499.00","op":"1399.00","p":"1149.00"}]
        dict = json.loads(response.text)
        price = float(dict[0]['p'])

        # 把price存到item里
        item['price'] = price

        # 处理详情页，通过meta参数传递已经采好的一些数据
        yield scrapy.Request(url=item['url'], callback=self.parseDetail, meta={'item':item})

    def parseDetail(self, response):
        item = response.meta['item']

        # 商品标题
        item['title'] = response.css('#spec-img::attr(alt)').extract_first('')

        # 参数列表
        ptable = response.css('.Ptable .clearfix')
        for p in ptable:
            pitem = p.css('dt::text').extract_first()
            pval  = p.css('dd::text').extract_first()

            # pitem到item参数的转换表
            pitem_map = {
                '品牌': 'brand', 
                '型号': 'model',
                '颜色': 'color',
                '屏幕比例': 'ratio',
                '最佳分辨率': 'resolution',
                '刷新率': 'refresh_rate',
                '亮度': 'luminance',
            }
            
            # 如果是我们想采集的参数，则保存
            if pitem in pitem_map:
                item[pitem_map[pitem]] = pval

        # 提交这个item            
        yield item
            