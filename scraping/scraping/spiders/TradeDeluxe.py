from scrapy.crawler import CrawlerProcess
import scrapy
import csv

class TradeDeluxe(scrapy.Spider):
    name = 'TradeDeluxe'
    start_urls = ['https://www.tradeluxe.at/collections/all?sort_by=created-descending']
    header = ['serial_no', 'ref', 'partner_id','url_key', 'product_type', 'group_sku', 'variation_type', 'product_sku', 'upc_ean', 'barcode', 'brand',
               'name_en', "original_price", 'strike_through_price', 'retail_price', 'whole_sale_price', 'description_en', 'gender',
               'main_category', 'category', 'sub_category', 'base_category', 'size', 'quantity', 'color', 'material', 'origin', 'size_slug',
               'description_plain_en', 'delivery_information', 'main_pic',
               "pic_1", "pic_2", "pic_3", "pic_4", "pic_5", "pic_6", "pic_7", "pic_8", "pic_9", "pic_10", "pic_11", "pic_12", "pic_13", "pic_14",
               "pic_15", "pic_16", "pic_17", "pic_18", "pic_19", "pic_20", "pic_21", "pic_22", "pic_23", "pic_24", "pic_25", "pic_26", "pic_27",
               "pic_28", "pic_29", "pic_30", "pic_31", "pic_32", "pic_33", "pic_34", "pic_35", "pic_36",
               "variant_1", "variant_1_stock", "variant_1_price",
                "variant_2", "variant_2_stock", "variant_2_price",
                "variant_3", "variant_3_stock", "variant_3_price",
                "variant_4", "variant_4_stock", "variant_4_price",
                "variant_5", "variant_5_stock", "variant_5_price",
                "variant_6", "variant_6_stock", "variant_6_price",
                "variant_7", "variant_7_stock", "variant_7_price",
                "variant_8", "variant_8_stock", "variant_8_price",
                "variant_9", "variant_9_stock", "variant_9_price",
                "variant_10", "variant_10_stock", "variant_10_price",
                "variant_11", "variant_11_stock", "variant_11_price",
                "variant_12", "variant_12_stock", "variant_12_price",
                "variant_13", "variant_13_stock", "variant_13_price",
                "variant_14", "variant_14_stock", "variant_14_price",
                "variant_15", "variant_15_stock", "variant_15_price",
                "variant_16", "variant_16_stock", "variant_16_price",
                "variant_17", "variant_17_stock", "variant_17_price",
                "variant_18", "variant_18_stock", "variant_18_price",
                "variant_19", "variant_19_stock", "variant_19_price",
                "variant_20", "variant_20_stock", "variant_20_price",
                "variant_21", "variant_21_stock", "variant_21_price",
                "variant_22", "variant_22_stock", "variant_22_price",
                "variant_23", "variant_23_stock", "variant_23_price",
                "variant_24", "variant_24_stock", "variant_24_price",
                "variant_25", "variant_25_stock", "variant_25_price",
                "variant_26", "variant_26_stock", "variant_26_price",
                "variant_27", "variant_27_stock", "variant_27_price",
                "variant_28", "variant_28_stock", "variant_28_price",
                "variant_29", "variant_29_stock", "variant_29_price",
                "variant_30", "variant_30_stock", "variant_30_price",
                "variant_31", "variant_31_stock", "variant_31_price",
                "variant_32", "variant_32_stock", "variant_32_price",
                "variant_33", "variant_33_stock", "variant_33_price",
                "variant_34", "variant_34_stock", "variant_34_price",
                "variant_35", "variant_35_stock", "variant_35_price",
                "variant_36", "variant_36_stock", "variant_36_price",
                "variant_37", "variant_37_stock", "variant_37_price",
                "variant_38", "variant_38_stock", "variant_38_price",
                "variant_39", "variant_39_stock", "variant_39_price",
                "variant_40", "variant_40_stock", "variant_40_price",
                "variant_41", "variant_41_stock", "variant_41_price",
                "variant_42", "variant_42_stock", "variant_42_price",
                "variant_43", "variant_43_stock", "variant_43_price",
                "variant_44", "variant_44_stock", "variant_44_price",
                "variant_45", "variant_45_stock", "variant_45_price",
                "variant_46", "variant_46_stock", "variant_46_price",
                "variant_47", "variant_47_stock", "variant_47_price",
                "variant_48", "variant_48_stock", "variant_48_price",
                "variant_49", "variant_49_stock", "variant_49_price",
                "variant_50", "variant_50_stock", "variant_50_price",
                "variant_51", "variant_51_stock", "variant_51_price",
                "variant_52", "variant_52_stock", "variant_52_price",
                "variant_53", "variant_53_stock", "variant_53_price",
                "variant_54", "variant_54_stock", "variant_54_price",
                "variant_55", "variant_55_stock", "variant_55_price",
                "variant_56", "variant_56_stock", "variant_56_price",
                "variant_57", "variant_57_stock", "variant_57_price",
                "variant_58", "variant_58_stock", "variant_58_price",
                "variant_59", "variant_59_stock", "variant_59_price",
                "variant_60", "variant_60_stock", "variant_60_price",
                "variant_61", "variant_61_stock", "variant_61_price",
                "variant_62", "variant_62_stock", "variant_62_price",
                "variant_63", "variant_63_stock", "variant_63_price",
                "variant_64", "variant_64_stock", "variant_64_price",
                "variant_65", "variant_65_stock", "variant_65_price",
                "variant_66", "variant_66_stock", "variant_66_price",
                "variant_67", "variant_67_stock", "variant_67_price",
                "variant_68", "variant_68_stock", "variant_68_price",
                "variant_69", "variant_69_stock", "variant_69_price",
                "variant_70", "variant_70_stock", "variant_70_price",
                "variant_71", "variant_71_stock", "variant_71_price",
                "variant_72", "variant_72_stock", "variant_72_price",
                "variant_73", "variant_73_stock", "variant_73_price",
                "variant_74", "variant_74_stock", "variant_74_price",
                "variant_75", "variant_75_stock", "variant_75_price",
                "variant_76", "variant_76_stock", "variant_76_price",
                "variant_77", "variant_77_stock", "variant_77_price",
                "variant_78", "variant_78_stock", "variant_78_price",
                "variant_79", "variant_79_stock", "variant_79_price",
                "variant_80", "variant_80_stock", "variant_80_price",
                "variant_81", "variant_81_stock", "variant_81_price",
                "variant_82", "variant_82_stock", "variant_82_price",
                "variant_83", "variant_83_stock", "variant_83_price",
                "variant_84", "variant_84_stock", "variant_84_price",
                "variant_85", "variant_85_stock", "variant_85_price",
                "variant_86", "variant_86_stock", "variant_86_price",
                "variant_87", "variant_87_stock", "variant_87_price",
                "variant_88", "variant_88_stock", "variant_88_price",
                "variant_89", "variant_89_stock", "variant_89_price",
                "variant_90", "variant_90_stock", "variant_90_price",
                "variant_91", "variant_91_stock", "variant_91_price",
                "variant_92", "variant_92_stock", "variant_92_price",
                "variant_93", "variant_93_stock", "variant_93_price",
                "variant_94", "variant_94_stock", "variant_94_price",
                "variant_95", "variant_95_stock", "variant_95_price",
                "variant_96", "variant_96_stock", "variant_96_price",
                "variant_97", "variant_97_stock", "variant_97_price",
                "variant_98", "variant_98_stock", "variant_98_price",
                "variant_99", "variant_99_stock", "variant_99_price",
                "variant_100", "variant_100_stock", "variant_100_price"
               ]
    file = open('TradeDeluxe.csv', 'w', newline='', encoding='utf-8')
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()


    def parse(self, response):
        for link in response.css('.col-lg-listt4 h3.product-title a::attr(href)').extract():
            yield scrapy.Request(url='https://www.tradeluxe.at/'+link.replace('/collections/all/',''), callback=self.scrapeData)
        try:
            next_page = [v.css('a::attr(href)').extract_first() for v in response.css('.pagination-page.page-numbers li') if v.css('a::attr(class)').extract_first() == 'next page-numbers'][0]
            yield scrapy.Request(url='https://www.tradeluxe.at'+next_page)
        except:
            pass

    def scrapeData(self, response):
        # try:
        item = dict()
        for res in response.css('.pr_short_des li'):
            if'Referenz:' in ''.join(res.css(' ::text').extract()):
                item['group_sku'] = ''.join(res.css(' ::text').extract()).strip().split(':')[-1].strip()
            if 'Zifferblatt:' in ''.join(res.css(' ::text').extract()):
                item['color'] = ''.join(res.css(' ::text').extract()).strip().split(':')[-1].strip()
        try:
            item['group_sku'] = item['group_sku'] +'-'+(item['color']).replace(' ','')
        except:
            pass
        item['url_key'] = response.url
        item['gender'] ='unisex'
        item['main_category'] ='unisex'
        item['category'] = 'watches'
        item['sub_category'] = 'watches'
        item['origin'] = 'website'
        item['size_slug'] = 'eu'
        item['delivery_information'] = '10 to 15 days'
        item['base_category'] = 'unisex/watches/watches'
        item['name_en'] = response.css('.product_title.entry-title::text').extract_first()
        item['original_price'] = int(float(response.css('#price_ppr::text').extract_first().replace('€', '').split(',')[0].replace('.','')))
        item['retail_price'] = int(float(response.css('#price_ppr::text').extract_first().replace('€', '').split(',')[0].replace('.','')))
        item['whole_sale_price'] = int(float(response.css('#price_ppr::text').extract_first().replace('€', '').split(',')[0].replace('.','')))
        try:
            item['brand'] = [v.css('.Apple-converted-space::text').extract_first() for v in response.css('.pr_short_des li') if v.css('b::text').extract_first() == 'Marke:' ][0].strip()
        except:
            try:
                item['brand'] = [v.css('span::text').extract()[1].strip() for v in response.css('.pr_short_des li') if v.css('strong span ::text').extract_first().strip() == 'Marke:' ][0]
            except:
                item['brand'] =  ''.join([v.css('li::text').extract() for v in response.css('.pr_short_des li') if v.css('strong::text').extract_first().strip() == 'Marke:'][0]).strip()
        # item['color'] = [v.css('.Apple-converted-space::text').extract_first() for v in response.css('.pr_short_des li') if v.css('b::text').extract_first() == 'Gehäuse:' ][0].strip()

        try:
            item['product_type'] = [v.css('.Apple-converted-space::text').extract_first() for v in response.css('.pr_short_des li') if v.css('b::text').extract_first() == 'Modell:' ][0].strip()
        except:
            try:
                item['product_type'] = [v.css('span::text').extract()[1].strip() for v in response.css('.pr_short_des li') if v.css('strong span ::text').extract_first().strip() == 'Modell:' ][0]
            except:
                try:
                    item['product_type'] = ''.join([v.css('li::text').extract() for v in response.css('.pr_short_des li') if v.css('strong::text').extract_first().strip() == 'Model:' or v.css('strong::text').extract_first().strip() == 'Modell:'][0]).strip()
                except:
                    pass
        item['main_pic'] = response.css('.img_ptw::attr(data-bgset)').extract()[0].replace('1x1', '1080x')
        for index, piclink in enumerate(response.css('.img_ptw::attr(data-bgset)').extract()[1:36]):
            item[f'pic_{index+1}'] = piclink.replace('1x1', '1080x')
        try:
            item['variant_1'] = [v.css('.Apple-converted-space::text').extract_first() for v in response.css('.pr_short_des li') if v.css('b::text').extract_first() == 'Größe:' ][0].strip()
        except:
            try:
                item['variant_1'] = [v.css('span::text').extract()[1].strip() for v in response.css('.pr_short_des li') if v.css('strong span ::text').extract_first().strip() == 'Größe:'][0]
            except:
                item['variant_1'] = ''.join([v.css('li::text').extract() for v in response.css('.pr_short_des li') if v.css('strong::text').extract_first().strip() == 'Größe:'][0]).strip()

        if response.css('.js_in_stock::text').extract()[0] == 'Auf Lager':
            item['variant_1_stock'] = 'Instock'
        else:
            item['variant_1_stock'] = 'out of stock'

        item['variant_1_price'] = item['retail_price']
        self.writer.writerow(item)
        self.file.flush()
        # except Exception as s:
        #     print(s)




        h=1


process = CrawlerProcess({})
process.crawl(TradeDeluxe)
process.start()