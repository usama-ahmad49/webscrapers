import datetime
import json
import re

import requests
import scrapy
from scrapy.crawler import CrawlerProcess

'''headers and cookies necessary for the scraper to work'''
cookies = {'PHPSESSID': 'idfhb84l6enp07b0dq8m4vrcg4', '_ga': 'GA1.3.1313228774.1659800930',
           '_gid': 'GA1.3.1472182247.1659800930', 'twk_idm_key': '6GsWd6hdPGm6gb43Bu6ei', 'TawkConnectionTime': '0', }

headers = {'Accept': 'application/json, text/javascript, */*; q=0.01', 'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
           'Connection': 'keep-alive',
           'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryR92UUwRbDuvoKA5r',
           # Requests sorts cookies= alphabetically
           # 'Cookie': 'PHPSESSID=idfhb84l6enp07b0dq8m4vrcg4; _ga=GA1.3.1313228774.1659800930; _gid=GA1.3.1472182247.1659800930; twk_idm_key=6GsWd6hdPGm6gb43Bu6ei; TawkConnectionTime=0',
           'DNT': '1', 'Origin': 'https://adison.stjsonora.gob.mx',
           'Referer': 'https://adison.stjsonora.gob.mx/Publicacion/ListaAcuerdos/', 'Sec-Fetch-Dest': 'empty',
           'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
           'X-Requested-With': 'XMLHttpRequest',
           'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"', 'sec-ch-ua-mobile': '?0',
           'sec-ch-ua-platform': '"Windows"', }

dateNow = datetime.datetime.now().isoformat()

OutPutList = []


def remove_accents(string):
    # if type(string) is not unicode:
    #     string = unicode(string, encoding='utf-8')

    string = re.sub(u"[àáâãäå]", 'a', string)
    string = re.sub(u"[èéêë]", 'e', string)
    string = re.sub(u"[ìíîï]", 'i', string)
    string = re.sub(u"[òóôõö]", 'o', string)
    string = re.sub(u"[ùúûü]", 'u', string)
    string = re.sub(u"[ýÿ]", 'y', string)

    string = re.sub(u"[ÀÁÂÃÄÅ]", 'A', string)
    string = re.sub(u"[ÈÉÊË]", 'E', string)
    string = re.sub(u"[ÌÍÎÏ]", 'I', string)
    string = re.sub(u"[ÒÓÔÕÖ]", 'O', string)
    string = re.sub(u"[ÙÚÛÜ]", 'U', string)
    string = re.sub(u"[ÝŸ]", 'Y', string)
    return string


class JudicialSonoraSpider(scrapy.Spider):
    name = "judicial_sonora"

    def start_requests(self):
        fecha = '2022/08/24'
        categoryList = []
        response = scrapy.Selector(text=requests.get('https://adison.stjsonora.gob.mx/Publicacion/ListaAcuerdos/').text)
        IDs = []
        for k in response.css('#IdCatMunicipio option'):
            if k.css('::attr(value)').extract_first() == '':
                continue
            categoryList.append(k.css('::attr(value)').extract_first() + '*' + k.css('::text').extract_first())
        for v in response.css('#IdUnidad option'):
            IDs.append((v.css('::attr(value)').extract_first(), v.css('::attr(data-value)').extract_first(),
                        v.css('::text').extract_first()))

        for uuid in IDs:
            if uuid[0] == '':
                continue
            # data is the body of the request
            # data is variable for different options in the request
            data = f'------WebKitFormBoundaryR92UUwRbDuvoKA5r\r\nContent-Disposition: form-data; name="Accion"\r\n\r\nPublicacion|ListaAcuerdosController|BuscarByFecha\r\n------WebKitFormBoundaryR92UUwRbDuvoKA5r\r\nContent-Disposition: form-data; name="IdUnidad"\r\n\r\n{uuid[0]}\r\n------WebKitFormBoundaryR92UUwRbDuvoKA5r\r\nContent-Disposition: form-data; name="Fecha"\r\n\r\n{fecha}\r\n------WebKitFormBoundaryR92UUwRbDuvoKA5r--\r\n'
            url = 'https://adison.stjsonora.gob.mx/Controller/ActionController.php'  # url of the request; is constant for all requests
            try:
                entidad = [v for v in categoryList if v.split('*')[0] == uuid[1]][0].split('*')[-1]
                yield scrapy.Request(url=url, method='POST', dont_filter=True, cookies=cookies, headers=headers,
                                     body=data, meta={'entidad': entidad, 'juzgado': uuid[2], 'fecha': fecha},
                                     callback=self.parse)  # yield is used to send the request to the spider
            except:
                pass

    def parse(self, response, **kwargs):
        Jdata = json.loads(response.text)
        for data in Jdata['Resultado']:
            item = dict()
            try:
                if '.-' in data['Partes']:
                    try:
                        if 'PRESENTADO POR' in data['Partes']:
                            item['actor'] = remove_accents(data['Partes'].split('PRESENTADO POR')[-1].split('DERIVADO')[0])
                            item['demandado'] = ''
                        elif 'INTERPUESTO POR' in data['Partes']:
                            item['actor'] = remove_accents(data['Partes'].split('INTERPUESTO POR')[-1])
                            item['demandado'] = ''
                        elif 'PROM. POR' in data['Partes']:
                            if 'EN CONTRA DE' in data['Partes']:
                                item['actor'] = remove_accents(
                                    data['Partes'].split('PROM. POR')[-1].split('EN CONTRA DE')[0])
                                item['demandado'] = remove_accents(data['Partes'].split('EN CONTRA DE')[-1])
                            elif 'EN CONTRA DE' not in data['Partes']:
                                item['actor'] = remove_accents(data['Partes'].split('PROM. POR')[-1])
                                item['demandado'] = ''

                        elif 'PROMOVIDO POR' in data['Partes'] and 'VS' in data['Partes']:
                            item['actor'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1].split('VS')[0].strip())
                            item['demandado'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1].split('VS')[1])
                        elif 'PROMOVIDO POR' in data['Partes'] and 'EN CONTRA DE' in data['Partes']:
                            item['actor'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1].split('EN CONTRA DE')[0])
                            item['demandado'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1].split('EN CONTRA DE')[-1])
                        elif 'PROMOVIDO POR' in data['Partes'] and 'EN CONTRA DE' not in data['Partes']:
                            item['actor'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1])
                            item['demandado'] = ''
                        elif 'PROMOVIDO POR' not in data['Partes'] and 'EN CONTRA DE' in data['Partes']:
                            item['actor'] = ''
                            item['demandado'] = remove_accents(data['Partes'].split('EN CONTRA DE')[-1])

                        elif len([v for v in data['Partes'].split('.-') if v != '' if v != ' '][1].split('VS')) == 2:
                            item['actor'] = remove_accents([v for v in data['Partes'].split('.-') if v != '' if v != ' '][1].split('VS')[
                                                               0].strip().upper())
                            item['demandado'] = \
                                remove_accents(
                                    [v for v in data['Partes'].split('.-') if v != '' if v != ' '][1].split('VS')[
                                        -1].strip().upper())
                        else:
                            item['actor'] = remove_accents([v for v in data['Partes'].split('.-') if v != '' if v != ' '][1].split('VS')[
                                                               0].strip().upper().replace('-', '').strip())
                            item['demandado'] = ''
                    except:
                        item['actor'] = ''
                        item['demandado'] = ''
                elif '.' in data['Partes'] and '.-' not in data['Partes']:
                    try:
                        if 'PRESENTADO POR' in data['Partes']:
                            item['actor'] = remove_accents(data['Partes'].split('PRESENTADO POR')[-1].split('DERIVADO')[0])
                            item['demandado'] = ''
                        elif 'INTERPUESTO POR' in data['Partes']:
                            item['actor'] = remove_accents(data['Partes'].split('INTERPUESTO POR')[-1])
                            item['demandado'] = ''
                        elif 'PROM. POR' in data['Partes']:
                            if 'EN CONTRA DE' in data['Partes']:
                                item['actor'] = remove_accents(
                                    data['Partes'].split('PROM. POR')[-1].split('EN CONTRA DE')[0])
                                item['demandado'] = remove_accents(data['Partes'].split('EN CONTRA DE')[-1])
                            elif 'EN CONTRA DE' not in data['Partes']:
                                item['actor'] = remove_accents(data['Partes'].split('PROM. POR')[-1])
                                item['demandado'] = ''
                        elif 'PROMOVIDO POR' in data['Partes'] and 'VS' in data['Partes']:
                            item['actor'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1].split('VS')[0])
                            item['demandado'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1].split('VS')[1])
                        elif 'PROMOVIDO POR' in data['Partes'] and 'EN CONTRA DE' in data['Partes']:
                            item['actor'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1].split('EN CONTRA DE')[0])
                            item['demandado'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1].split('EN CONTRA DE')[-1])
                        elif 'PROMOVIDO POR' in data['Partes'] and 'EN CONTRA DE' not in data['Partes']:
                            item['actor'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1])
                            item['demandado'] = ''
                        elif 'PROMOVIDO POR' not in data['Partes'] and 'EN CONTRA DE' in data['Partes']:
                            item['actor'] = ''
                            item['demandado'] = remove_accents(data['Partes'].split('EN CONTRA DE')[-1])
                        elif len([v for v in data['Partes'].split('.') if v != '' if v != ' '][1].split('VS')) == 2:
                            item['actor'] = remove_accents([v for v in data['Partes'].split('.') if v != '' if v != ' '][1].split('VS')[
                                                               0].strip().upper())
                            item['demandado'] = \
                                remove_accents(
                                    [v for v in data['Partes'].split('.') if v != '' if v != ' '][1].split('VS')[
                                        -1].strip().upper())
                        else:
                            item['actor'] = remove_accents([v for v in data['Partes'].split('.') if v != '' if v != ' '][1].split('VS')[
                                                               0].strip().upper())
                            item['demandado'] = ''
                    except:
                        item['actor'] = ''
                        item['demandado'] = ''
                else:
                    try:
                        if 'PRESENTADO POR' in data['Partes']:
                            item['actor'] = remove_accents(data['Partes'].split('PRESENTADO POR')[-1].split('DERIVADO')[0])
                            item['demandado'] = ''
                        elif 'INTERPUESTO POR' in data['Partes']:
                            item['actor'] = remove_accents(data['Partes'].split('INTERPUESTO POR')[-1])
                            item['demandado'] = ''
                        elif 'PROM. POR' in data['Partes']:
                            if 'EN CONTRA DE' in data['Partes']:
                                item['actor'] = remove_accents(
                                    data['Partes'].split('PROM. POR')[-1].split('EN CONTRA DE')[0])
                                item['demandado'] = remove_accents(data['Partes'].split('EN CONTRA DE')[-1])
                            elif 'EN CONTRA DE' not in data['Partes']:
                                item['actor'] = remove_accents(data['Partes'].split('PROM. POR')[-1])
                                item['demandado'] = ''
                        elif 'PROMOVIDO POR' in data['Partes'] and 'VS' in data['Partes']:
                            item['actor'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1].split('VS')[0])
                            item['demandado'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1].split('VS')[1])
                        elif 'PROMOVIDO POR' in data['Partes'] and 'EN CONTRA DE' in data['Partes']:
                            item['actor'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1].split('EN CONTRA DE')[0])
                            item['demandado'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1].split('EN CONTRA DE')[-1])
                        elif 'PROMOVIDO POR' in data['Partes'] and 'EN CONTRA DE' not in data['Partes']:
                            item['actor'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1])
                            item['demandado'] = ''
                        elif 'PROMOVIDO POR' not in data['Partes'] and 'EN CONTRA DE' in data['Partes']:
                            item['actor'] = ''
                            item['demandado'] = remove_accents(data['Partes'].split('EN CONTRA DE')[-1])
                        elif len([v for v in data['Partes'].split('-') if v != '' if v != ' '][1].split('VS')) == 2:
                            item['actor'] = remove_accents([v for v in data['Partes'].split('-') if v != '' if v != ' '][1].split('VS')[
                                                               0].strip().upper())
                            item['demandado'] = \
                                remove_accents(
                                    [v for v in data['Partes'].split('-') if v != '' if v != ' '][1].split('VS')[
                                        -1].strip().upper())
                        else:
                            item['actor'] = remove_accents([v for v in data['Partes'].split('-') if v != '' if v != ' '][1].split('VS')[
                                                               0].strip().upper().replace('-', '').strip())
                            item['demandado'] = ''
                    except:
                        item['actor'] = ''
                        item['demandado'] = ''
            except:
                try:
                    if 'PRESENTADO POR' in data['Partes']:
                        item['actor'] = remove_accents(data['Partes'].split('PRESENTADO POR')[-1].split('DERIVADO')[0])
                        item['demandado'] = ''
                    elif 'INTERPUESTO POR' in data['Partes']:
                        item['actor'] = remove_accents(data['Partes'].split('INTERPUESTO POR')[-1])
                        item['demandado'] = ''
                    elif 'PROM. POR' in data['Partes']:
                        if 'EN CONTRA DE' in data['Partes']:
                            item['actor'] = remove_accents(
                                data['Partes'].split('PROM. POR')[-1].split('EN CONTRA DE')[0])
                            item['demandado'] = remove_accents(data['Partes'].split('EN CONTRA DE')[-1])
                        elif 'EN CONTRA DE' not in data['Partes']:
                            item['actor'] = remove_accents(data['Partes'].split('PROM. POR')[-1])
                            item['demandado'] = ''

                    elif 'PROMOVIDO POR' in data['Partes'] and 'VS' in data['Partes']:
                        item['actor'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1].split('VS')[0])
                        item['demandado'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1].split('VS')[1])
                    elif 'PROMOVIDO POR' in data['Partes'] and 'EN CONTRA DE' in data['Partes']:
                        item['actor'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1].split('EN CONTRA DE')[0])
                        item['demandado'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1].split('EN CONTRA DE')[-1])
                    elif 'PROMOVIDO POR' in data['Partes'] and 'EN CONTRA DE' not in data['Partes']:
                        item['actor'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1])
                        item['demandado'] = ''
                    elif 'PROMOVIDO POR' not in data['Partes'] and 'EN CONTRA DE' in data['Partes']:
                        item['actor'] = ''
                        item['demandado'] = remove_accents(data['Partes'].split('EN CONTRA DE')[-1])
                    elif len([v for v in data['Partes'].split('-') if v != '' if v != ' '][1].split('VS')) == 2:
                        item['actor'] = remove_accents([v for v in data['Partes'].split('-') if v != '' if v != ' '][1].split('VS')[
                                                           0].strip().upper())
                        item['demandado'] = \
                            remove_accents(
                                [v for v in data['Partes'].split('-') if v != '' if v != ' '][1].split('VS')[
                                    -1].strip().upper())
                    else:
                        item['actor'] = remove_accents([v for v in data['Partes'].split('-') if v != '' if v != ' '][1].split('VS')[
                                                           0].strip().upper().replace('-', '').strip())
                        item['demandado'] = ''
                except:
                    item['actor'] = ''
                    item['demandado'] = ''

            if 'Penales'.lower() in data['Secretaria'].lower():
                if item['demandado'] == '':
                    try:
                        item['demandado'] = remove_accents(data['Partes'].split('.-')[-2])
                    except:
                        try:
                            item['demandado'] = remove_accents(data['Partes'].split('.-')[0])
                        except:
                            item['demandado'] = ''
            elif 'Acuerdos Mesa Penal'.lower() in data['Secretaria'].lower():
                if item['demandado'] == '':
                    try:
                        item['demandado'] = remove_accents(data['Partes'].split('.')[-2])
                    except:
                        try:
                            item['demandado'] = remove_accents(data['Partes'].split('.')[0])
                        except:
                            item['demandado'] = ''
            elif 'Primera Secretaría (Penal)'.lower() in data['Secretaria'].lower():
                if item['demandado'] == '':
                    try:
                        item['demandado'] = remove_accents(data['Partes'].split('.')[-2])
                    except:
                        try:
                            item['demandado'] = remove_accents(data['Partes'].split('.')[0])
                        except:
                            item['demandado'] = ''

            item['entidad'] = remove_accents(response.meta['entidad'].upper())
            try:
                item['expediente'] = remove_accents(data['TipoAsunto'] + ' ' + data['Asunto'] + '/' + data['Anio'].upper())
            except:
                item['expediente'] = ''
            item['fecha'] = remove_accents(response.meta['fecha'].upper())
            item['fuero'] = 'COMUN'
            item['juzgado'] = remove_accents(response.meta['juzgado'].upper())
            try:
                if '.-' in data['Partes']:
                    item['tipo'] = remove_accents(data['Partes'].split('.-')[0].upper())
                elif '-' in data['Partes'] and '.-' not in data['Partes']:
                    item['tipo'] = remove_accents(data['Partes'].split('-')[0].upper())
                else:
                    item['tipo'] = remove_accents(data['Partes'].split('.')[0].upper())
            except:
                item['tipo'] = ''
            try:
                item['acuerdos'] = remove_accents(data['Sintesis'].replace('@','').upper())
            except:
                item['acuerdos'] = ''
            item['monto'] = ''
            item['fecha_presentacion'] = ''
            item['actos_reclamados'] = ''
            item['actos_reclamados_especificos'] = ''
            item['Naturaleza_procedimiento'] = ''
            item['Prestación_demandada'] = ''
            item['Organo_jurisdiccional_origen'] = ''
            try:
                if 'DERIVADO DEL EXPEDIENTE' in data['Partes']:
                    item['expediente_origen'] = data['Partes'].split('DERIVADO DEL EXPEDIENTE')[-1]
                else:
                    item['expediente_origen'] = ''
            except:
                item['expediente_origen'] = ''
            materia = ''
            try:
                if '(Penal)'.lower() in data['Secretaria'].lower():
                    materia = 'PENAL'
                elif 'FAMILIAR'.lower() in data['Partes'].lower() or 'FAMILIAR'.lower() in data['Secretaria'].lower() or 'FAMILIAR'.lower() in response.meta[
                    'juzgado'].lower():
                    if 'FAMILIAR'.lower() in data['Partes'].lower():
                        materia = 'FAMILIAR'
                    elif 'CIVIL'.lower() in data['Partes'].lower():
                        materia = 'CIVIL'
                    elif 'PENAL'.lower() in data['Partes'].lower():
                        materia = 'PENAL'
                    else:
                        materia = 'FAMILIAR'
                elif 'CIVIL'.lower() in data['Partes'].lower() or 'CIVIL'.lower() in data['Secretaria'].lower() or 'CIVIL'.lower() in response.meta[
                    'juzgado'].lower() or 'Civiles'.lower() in response.meta['juzgado'].lower() or 'Civiles'.lower() in data['Secretaria'].lower():
                    if 'FAMILIAR'.lower() in data['Partes'].lower():
                        materia = 'FAMILIAR'
                    elif 'CIVIL'.lower() in data['Partes'].lower():
                        materia = 'CIVIL'
                    elif 'PENAL'.lower() in data['Partes'].lower():
                        materia = 'PENAL'
                    else:
                        materia = 'CIVIL'
                elif 'PENAL'.lower() in data['Partes'].lower() or 'PENAL'.lower() in data['Secretaria'].lower() or 'PENAL'.lower() in response.meta['juzgado'].lower() or 'Penales'.lower() in data['Secretaria'].lower():
                    if 'FAMILIAR'.lower() in data['Partes'].lower():
                        materia = 'FAMILIAR'
                    elif 'CIVIL'.lower() in data['Partes'].lower():
                        materia = 'CIVIL'
                    elif 'PENAL'.lower() in data['Partes'].lower():
                        materia = 'PENAL'
                    else:
                        materia = 'PENAL'
                elif 'MIXTO'.lower() in data['Partes'].lower() or 'MIXTO'.lower() in data['Secretaria'].lower() or 'MIXTO'.lower() in response.meta['juzgado'].lower():
                    materia = 'CIVIL'
            except:
                materia = ''
            if materia != '':
                item['materia'] = materia
            else:
                if item['juzgado'] == 'JUZGADO PRIMERO DE EJECUCION DE SANCIONES DE HERMOSILLO':
                    item['materia'] = 'PENAL'
                elif item['juzgado'] == 'JUZGADO PRIMERO ESPECIALIZADO EN JUSTICIA PARA ADOLESCENTES DE HERMOSILLO':
                    item['materia'] = 'PENAL'
                elif item['juzgado'] == 'JUZGADO PRIMERO DE EJECUCION DE SANCIONES DE HERMOSILLO':
                    item['materia'] = 'PENAL'
                elif item['juzgado'] == 'PRIMER UNITARIO REGIONAL DEL CIRCUITO ESPECIALIZADO PARA ADOLESCENTES EN HERMOSILLO':
                    item['materia'] = 'PENAL'
                elif item['juzgado'] == 'SECRETARIA GENERAL DE ACUERDOS':
                    item['materia'] = 'CIVIL'
                elif item['juzgado'] == 'DIRECCION GENERAL DE SERVICIOS DE COMPUTO':
                    item['materia'] = 'CIVIL'
                else:
                    item['materia'] = ''
            if item['materia'] == '':
                item['materia'] = 'CIVIL'
            item['submateria'] = ''
            item['fecha_sentencia'] = ''
            item['sentido_sentencia'] = ''
            item['resoluciones'] = ''
            item['origen'] = 'PODER JUDICIAL DEL ESTADO DE SONORA'
            item['fecha_insercion'] = dateNow
            item['fecha_tecnica'] = datetime.datetime.strptime(item['fecha'], '%Y/%m/%d').isoformat()
            OutPutList.append(item)

    def close(spider, reason):
        global OutPutList
        with open('sample.json', 'w') as f:
            json.dump(OutPutList, f)
            OutPutList = []


if __name__ == '__main__':
    process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    process.crawl(JudicialSonoraSpider)
    process.start()  # the script will block here until the crawling is finished
