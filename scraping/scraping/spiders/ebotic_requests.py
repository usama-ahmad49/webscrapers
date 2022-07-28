try:
    import pkg_resources.py2_warn
except ImportError:
    pass

import json
from threading import Thread

import requests
import scrapy


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def scrape_products():
    count = 0
    links_file = open('data.txt', 'a')
    url = 'https://ebutik.pl/'
    resp1 = requests.get(url)
    response1 = scrapy.Selector(text=resp1.content.decode('utf-8'))
    for resp11 in response1.css('#menu_categories .navbar-collapse .navbar-subnav.active li .navbar-subsubnav a'):
        category_url = 'https://ebutik.pl' + resp11.css('::attr(href)').extract_first() if 'http' not in resp11.css(
            '::attr(href)').extract_first() else resp11.css('::attr(href)').extract_first()
        try:
            resp2 = requests.get(category_url)
        except:
            print('failed category: {}'.format(category_url))
            continue
        response2 = scrapy.Selector(text=resp2.content.decode('utf-8'))
        for resp22 in response2.css('#search .product_wrapper.col-12.col-md-3.col-sm-4'):
            link = 'https://ebutik.pl{}'.format(resp22.css('a.product-icon ::attr(href)').extract_first(''))
            links_file.write('{}\n'.format(link))
            links_file.flush()
            count += 1
            print(count)

    links_file.close()


def try_upload(link, done_links_file):
    headers1 = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'content-length': '88',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': '__IAI_AC2=5f9ea1acced792.01764181; RSSID=MzN3TXJtbmpkOHdNTHhjU3lnOW5zTTB3V3VMOHQ0U3JUSDJjL0pWam9NOD0%3D; mautic_focus_20=1604231641; client=8au7dhqua01uakbagvnu9gf8n5; basket_id=8au7dhqua01uakbagvnu9gf8n5; _gid=GA1.2.890452330.1605189878; activeSubMenu=22089; mtc_id=9004402; mtc_sid=qeet5rsiae37azfoybhhh7f; mautic_device_id=qeet5rsiae37azfoybhhh7f; page_counter=9; _ga_FYXDSGPK4F=GS1.1.1605189875.8.1.1605190792.60; _ga=GA1.1.703389114.1604231599',
        'origin': 'https://ebutik.pl',
        'referer': 'https://ebutik.pl/product-pol-336017-Morska-sukienka-Hazel.html',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    if not link.strip():
        return
    resp = requests.get(link)
    response = scrapy.Selector(text=resp.content.decode('utf-8'))
    images = response.css('#projector_slider a ::Attr(href)').extract()
    ids = ','.join(response.css('div[data-ver_id] ::attr(data-ver_id)').extract())
    title = response.css('.projector_navigation_sub h1 ::text').extract_first('')
    price = response.css('.projector_price_value ::text').extract_first('').replace(',', '.')
    sizes = response.css('.product_section.sizes a::text').extract()
    description = '{}<br>\n{}\n<br> {}'.format(response.css('.product_info_top').extract_first(),
                                               response.css('.projector_longdescription').extract_first(),
                                               response.css('#component_projector_sizes_cms_not ').extract_first()
                                               )
    description = description.replace('<p>&nbsp;</p>', '').replace('<p> </p>', '')
    description = description.replace('<p>', '<div>').replace('</p> </div>', '')

    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    category_title = response.css('.category.bc-item-1 ::Text').extract_first('')
    cat_url = "https://{}:{}@oxka.myshopify.com/admin/api/2020-10/custom_collections.json".format(API_KEY, PASSWORD)
    cat_r = requests.get(cat_url, headers=headers)
    cat_data = json.loads(cat_r.content.decode('utf-8'))
    categories = [v for v in cat_data['custom_collections'] if category_title.strip() == v['title']]
    if not categories:
        category = {
            "custom_collection": {
                "title": category_title.strip()
            }
        }
        cat_url = "https://{}:{}@oxka.myshopify.com/admin/api/2020-10/custom_collections.json".format(API_KEY, PASSWORD)
        cat_r = requests.post(cat_url, json=category, headers=headers)
        cat_id = json.loads(cat_r.content.decode('utf-8'))['custom_collection']['id']
    else:
        cat_id = [v for v in cat_data['custom_collections'] if category_title.strip() == v['title']][0]['id']
    sku = response.css('.product_info_top strong ::Text').extract_first('')
    if ids:
        data = {
            'request': json.dumps({"Product": {"format": "json", "params": {"products": ids}}}),
            'getAjax': 'true'
        }
        data_resp = requests.post('https://ebutik.pl/ajax/get.php', headers=headers1, data=data).content.decode('utf-8')
        data = json.loads(data_resp)
        variants = []
        images = []
        variant_images = {}
        sizes = []
        colors = []
        material = ''
        try:
            material = \
                [v for v in response.css('.projector_longdescription.cm.longdescription_small p::text').extract() if
                 'materiału:' in v][0]
            material = material[material.find(':') + 1:].strip()
        except:
            pass
        for index, product in enumerate(data['Product']['response']['product']):
            images.extend([v['attributes']['url'] for v in product['enclosures']['images']['enclosure']])
            price = product['price']['attributes']['price_formatted']
            price = float(''.join([v for v in price.replace(',', '.') if v.isdigit() or v == '.'])) * .37
            compared_price = float(''.join(
                [v for v in response.css('#projector_price_maxprice ::Text').extract_first('').replace(',', '.') if
                 v.isdigit() or v == '.'])) * .37
            for i in range(0, len(product['versions']['version'])):
                size_name = None
                try:
                    size_LENGTH = len([v['attributes']['name'] for v in product['sizes']['size']])
                except:
                    size_LENGTH = 1
                    size_name = 'One Size'
                for k in range(0, size_LENGTH):
                    try:
                        option_2 = product['versions']['version'][i]['attributes']['name']
                    except:
                        option_2 = '-'
                    variant = {
                        "sku": response.css('.product_info_top strong ::Text').extract_first(''),
                        "option1": size_name if size_name else
                        [v['attributes']['name'] for v in product['sizes']['size']][k],
                        "option2": option_2,
                        "option3": material if material.strip() else '-',
                        "images": [{'src': i} for i in images],
                        "price": price,
                        "currency_code": 'PLN',
                        "compare_at_price": compared_price,
                        "inventory_quantity": 100,
                        "inventory_policy": "continue",
                        "inventory_management": "shopify"

                    }
                    colors.append(product['versions']['version'][i]['attributes']['name'])
                    variants.append(variant)
            colors.append(product['versions']['version'][index]['attributes']['name'])
            try:
                sizes.extend([v['attributes']['name'] for v in product['sizes']['size']])
            except:
                pass
        variants_copy = []
        unique_keys = []
        for v in variants:
            if '{}${}'.format(v['option1'], v['option2']) not in unique_keys:
                variants_copy.append(v)
                unique_keys.append('{}${}'.format(v['option1'], v['option2']))
        tags = response.css('.product_info_top strong ::Text').extract()
        tags.extend(list(set(sizes)))
        tags.extend(list(set(colors)))
        tags.extend(material.split(','))

        payload = {
            "product": {
                "title": title,
                "body_html": description,
                "images": [{'src': i} for i in images],
                "variants": variants_copy[:100],
                "tags": tags,
                "product_type": response.css('.category.bc-active ::Text').extract_first(''),
                "options": [
                    {
                        "name": "Size"
                    },
                    {
                        "name": "Color"
                    },
                    {
                        'name': 'Material'
                    }
                ]
            }
        }
        r = requests.post("https://{}:{}@oxka.myshopify.com/admin/products.json".format(API_KEY, PASSWORD),
                          json=payload, headers=headers)
        data = json.loads(r.text)
        try:
            product_id = data['product']['id']
        except:
            if 'daily variant' in str(data.get('errors', {}).get('product')).lower():
                print(str(data.get('errors', {}).get('product')))
        payload2 = {
            "collect": {
                "product_id": product_id,
                "collection_id": cat_id
            }
        }
        cat_add_url = "https://{}:{}@oxka.myshopify.com/admin/api/2020-10/collects.json".format(API_KEY,
                                                                                                PASSWORD)
        cat_r = requests.post(cat_add_url, headers=headers, json=payload2)
        g = 1
    else:
        g = 1
        tags = response.css('.product_info_top strong ::Text').extract()
        tags.extend(list(set(sizes)))
        variants_copy = []
        material = ''
        try:
            material = \
                [v for v in response.css('.projector_longdescription p::text').extract() if
                 'materiału:' in v][0]
            material = material[material.find(':') + 1:].strip()
        except:
            pass
        tags.extend(material.split(','))
        compared_price = response.css('#projector_price_maxprice ::Text').extract_first('').strip()
        if compared_price:
            compared_price = float(''.join(
                [v for v in compared_price.replace(',', '.') if v.isdigit() or v == '.'])) * .37
        price = float(''.join(
            [v for v in price.replace(',', '.') if v.isdigit() or v == '.'])) * .37
        for size in sizes:
            variant = {
                "sku": response.css('.product_info_top strong ::Text').extract_first(''),
                "option1": size,
                "option2": material if material else '-',
                "images": [{'src': i} for i in images],
                "price": price,
                "currency_code": 'PLN',
                "inventory_quantity": 100,
                "inventory_policy": "continue",
                "inventory_management": "shopify"

            }
            if compared_price:
                variant['compare_at_price'] = compared_price
            variants_copy.append(variant)
        payload = {
            "product": {
                "title": title,
                "body_html": description,
                "images": [{'src': i} for i in images],
                "variants": variants_copy[:100],
                "tags": tags,
                "product_type": response.css('.category.bc-active ::Text').extract_first(''),
                "options": [
                    {
                        "name": "Size"
                    },
                    {
                        'name': 'Material'
                    }
                ]
            }
        }
        r = requests.post("https://{}:{}@oxka.myshopify.com/admin/products.json".format(API_KEY, PASSWORD),
                          json=payload, headers=headers)
        data = json.loads(r.text)
        try:
            product_id = data['product']['id']
        except:
            g = 1
        payload2 = {
            "collect": {
                "product_id": product_id,
                "collection_id": cat_id
            }
        }
        cat_add_url = "https://{}:{}@oxka.myshopify.com/admin/api/2020-10/collects.json".format(API_KEY,
                                                                                                PASSWORD)
        cat_r = requests.post(cat_add_url, headers=headers, json=payload2)
    done_links_file.write('{}\n'.format(link))
    done_links_file.flush()


def upload_product(link, done_links_file):
    try:
        try_upload(link, done_links_file)
    except:
        pass


def upload_products():
    done_links = []
    try:
        done_links_file = open('done_links.txt', 'r')
        done_links = done_links_file.read().split('\n')
        done_links_file.close()
    except:
        pass
    done_links_file = open('done_links.txt', 'a')
    links_file = open('data.txt', 'r')
    all_links = links_file.read().split('\n')
    all_links = list(set(all_links))
    chunk_size = 1
    total = 0
    for links in chunks(all_links, chunk_size):
        total += chunk_size
        print(total)
        threads = []
        for link in links:
            if link not in done_links:
                t = Thread(target=upload_product, args=(link, done_links_file,))
                t.start()
                threads.append(t)
        for t in threads:
            t.join()


if __name__ == '__main__':
    start_ = open('from_start.txt', 'r')
    start_ = start_.read()
    if start_.strip() == '1':
        get_products = True
    else:
        get_products = False
    API_KEY = "1db1b32be18891082b702cf43ecb09d0"
    PASSWORD = "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"
    SHARED_SECRET = "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"
    api_version = '2020-10'
    shop_url = "https://%s:%s@oxka.myshopify.com/admin" % (API_KEY, PASSWORD)
    if get_products:
        scrape_products()
        upload_products()
    else:
        upload_products()
