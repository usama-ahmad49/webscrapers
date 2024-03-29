try:
    from pkg_resources import get_distribution
    import pkg_resources.py2_warn
except ImportError:
    pass

import datetime
import json
import re

import requests
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import defer
from twisted.internet import reactor

# from under_conn import Mongoconexion

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
    string = re.sub(u"[ñ]", 'n', string)

    string = re.sub(u"[ÀÁÂÃÄÅ]", 'A', string)
    string = re.sub(u"[ÈÉÊË]", 'E', string)
    string = re.sub(u"[ÌÍÎÏ]", 'I', string)
    string = re.sub(u"[ÒÓÔÕÖ]", 'O', string)
    string = re.sub(u"[ÙÚÛÜ]", 'U', string)
    string = re.sub(u"[ÝŸ]", 'Y', string)
    string = re.sub(u"[Ñ]", 'N', string)

    string = re.sub(u"[()~!@#$%^&*=-]",'',string)
    string = re.sub(u"[\t\n\r]", "", string)

    string = re.sub(u"[-]", "", string)
    return string


class JudicialSonoraSpider(scrapy.Spider):
    name = "judicial_sonora"

    def __init__(self, date, **kwargs):
        super().__init__(**kwargs)
        self.date = date

    def start_requests(self):
        fecha = self.date
        # fecha = '2017/01/04'
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

        for uuid in IDs[-1:]:
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
                if ' VS ' in data['Partes'] or 'VS.' in data['Partes']or 'VS-' in data['Partes']:
                    actor = data['Partes'].split('VS')[0]
                    demandado = data['Partes'].split('VS')[-1]
                    if '.-' in actor:
                        item['actor'] = remove_accents(actor.split('.-')[-1].strip()).upper()
                    elif '-' in actor:
                        item['actor'] = remove_accents(actor.split('-')[-1].strip()).upper()
                    elif '.' in actor:
                        item['actor'] = remove_accents(actor.split('.')[-1].strip()).upper()
                    elif 'PROMOVIDO POR' in actor:
                        item['actor'] = remove_accents(actor.split('PROMOVIDO POR')[-1].strip()).upper()
                    elif 'PROMOVIDO PRO' in actor:
                        item['actor'] = remove_accents(actor.split('PROMOVIDO PRO')[-1].strip()).upper()
                    elif ')' in actor:
                        item['actor'] = remove_accents(actor.split(')')[-1].strip()).upper()
                    else:
                        item['actor'] = remove_accents(actor.strip()).upper()
                    item['demandado'] = remove_accents(demandado.strip()).upper()
                elif '.-' in data['Partes']:
                    try:
                        if 'PRESENTADO POR' in data['Partes']:
                            item['actor'] = remove_accents(
                                data['Partes'].split('PRESENTADO POR')[-1].split('DERIVADO')[0]).upper()
                            item['demandado'] = ''
                        elif 'PROMOVIDO A FAVOR DE' in data['Partes']:
                            item['actor'] = remove_accents(
                                data['Partes'].split('PROMOVIDO A FAVOR DE')[-1]).upper()
                            item['demandado'] = ''
                        elif 'INTERPUESTO POR' in data['Partes']:
                            item['actor'] = remove_accents(data['Partes'].split('INTERPUESTO POR')[-1]).upper()
                            item['demandado'] = ''
                        elif 'PROM. POR' in data['Partes']:
                            if 'EN CONTRA DE' in data['Partes']:
                                item['actor'] = remove_accents(
                                    data['Partes'].split('PROM. POR')[-1].split('EN CONTRA DE')[0]).upper()
                                item['demandado'] = remove_accents(data['Partes'].split('EN CONTRA DE')[-1]).upper()
                            elif 'EN CONTRA DE' not in data['Partes']:
                                item['actor'] = remove_accents(data['Partes'].split('PROM. POR')[-1]).upper()
                                item['demandado'] = ''


                        elif 'PROMOVIDO POR' in data['Partes'] and 'VS' in data['Partes']:
                            item['actor'] = remove_accents(
                                data['Partes'].split('PROMOVIDO POR')[-1].split('VS')[0].strip()).upper()
                            item['demandado'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1].split('VS')[1]).upper()
                        elif 'PROMOVIDO POR' in data['Partes'] and 'EN CONTRA DE' in data['Partes']:
                            item['actor'] = remove_accents(
                                data['Partes'].split('PROMOVIDO POR')[-1].split('EN CONTRA DE')[0]).upper()
                            item['demandado'] = remove_accents(
                                data['Partes'].split('PROMOVIDO POR')[-1].split('EN CONTRA DE')[-1]).upper()
                        elif 'PROMOVIDO POR' in data['Partes'] and 'EN CONTRA DE' not in data['Partes']:
                            item['actor'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1]).upper()
                            item['demandado'] = ''
                        elif 'PROMOVIDO POR' not in data['Partes'] and 'EN CONTRA DE' in data['Partes']:
                            item['actor'] = ''
                            item['demandado'] = remove_accents(data['Partes'].split('EN CONTRA DE')[-1]).upper()

                        elif 'VS.-' in data['Partes']:
                            item['actor'] = remove_accents([v for v in data['Partes'].split('VS.-')[0].split('.-') if v!=' ' if v != ''][-1].strip()).upper()
                            item['demandado'] = remove_accents([v for v in data['Partes'].split('VS.-')[-1].split('.-') if v!=' ' if v != ''][-1].strip()).upper()


                        elif len([v for v in data['Partes'].split('.-') if v != '' if v != ' '][1].split('VS')) == 2:
                            item['actor'] = remove_accents(
                                [v for v in data['Partes'].split('.-') if v != '' if v != ' '][1].split('VS')[
                                    0].strip()).upper()
                            item['demandado'] = \
                                remove_accents(
                                    [v for v in data['Partes'].split('.-') if v != '' if v != ' '][1].split('VS')[
                                        -1].strip()).upper()
                        else:
                            item['actor'] = remove_accents(
                                ' '.join([v for v in data['Partes'].split('.-') if v != '' if v != ' '][1:]).split('VS')[
                                    0].strip().upper().replace('-', '').strip()).upper()
                            item['demandado'] = ''
                    except:
                        item['actor'] = ''
                        item['demandado'] = ''
                elif '.' in data['Partes'] and '.-' not in data['Partes']:
                    try:
                        if 'PRESENTADO POR' in data['Partes']:
                            item['actor'] = remove_accents(
                                data['Partes'].split('PRESENTADO POR')[-1].split('DERIVADO')[0]).upper()
                            item['demandado'] = ''
                        elif 'PROMOVIDO A FAVOR DE' in data['Partes']:
                            item['actor'] = remove_accents(
                                data['Partes'].split('PROMOVIDO A FAVOR DE')[-1]).upper()
                            item['demandado'] = ''
                        elif 'INTERPUESTO POR' in data['Partes']:
                            item['actor'] = remove_accents(data['Partes'].split('INTERPUESTO POR')[-1]).upper()
                            item['demandado'] = ''
                        elif 'PROM. POR' in data['Partes']:
                            if 'EN CONTRA DE' in data['Partes']:
                                item['actor'] = remove_accents(
                                    data['Partes'].split('PROM. POR')[-1].split('EN CONTRA DE')[0]).upper()
                                item['demandado'] = remove_accents(data['Partes'].split('EN CONTRA DE')[-1]).upper()
                            elif 'EN CONTRA DE' not in data['Partes']:
                                item['actor'] = remove_accents(data['Partes'].split('PROM. POR')[-1]).upper()
                                item['demandado'] = ''
                        elif 'PROMOVIDO POR' in data['Partes'] and 'VS' in data['Partes']:
                            item['actor'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1].split('VS')[0]).upper()
                            item['demandado'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1].split('VS')[1]).upper()
                        elif 'PROMOVIDO POR' in data['Partes'] and 'EN CONTRA DE' in data['Partes']:
                            item['actor'] = remove_accents(
                                data['Partes'].split('PROMOVIDO POR')[-1].split('EN CONTRA DE')[0]).upper()
                            item['demandado'] = remove_accents(
                                data['Partes'].split('PROMOVIDO POR')[-1].split('EN CONTRA DE')[-1]).upper()
                        elif 'PROMOVIDO POR' in data['Partes'] and 'EN CONTRA DE' not in data['Partes']:
                            item['actor'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1]).upper()
                            item['demandado'] = ''
                        elif 'PROMOVIDO POR' not in data['Partes'] and 'EN CONTRA DE' in data['Partes']:
                            item['actor'] = ''
                            item['demandado'] = remove_accents(data['Partes'].split('EN CONTRA DE')[-1]).upper()

                        # elif 'VS.' in data['Partes']:
                        #     item['actor'] = remove_accents(data['Partes'].split('VS.')[0].split('.')[-1].strip().upper())
                        #     item['demandado'] = remove_accents(data['Partes'].split('VS.')[-1].split('.')[-1].strip().upper())

                        elif len([v for v in data['Partes'].split('.') if v != '' if v != ' '][1].split('VS')) == 2:
                            item['actor'] = remove_accents(
                                [v for v in data['Partes'].split('.') if v != '' if v != ' '][1].split('VS')[
                                    0].strip().upper()).upper()
                            item['demandado'] = \
                                remove_accents(
                                    [v for v in data['Partes'].split('.') if v != '' if v != ' '][1].split('VS')[
                                        -1].strip().upper()).upper()
                        else:
                            item['actor'] = remove_accents(
                                ' '.join([v for v in data['Partes'].split('.') if v != '' if v != ' '][1:]).split('VS')[0].strip().upper()).upper()
                            item['demandado'] = ''
                    except:
                        item['actor'] = ''
                        item['demandado'] = ''
                else:
                    try:
                        if 'PRESENTADO POR' in data['Partes']:
                            item['actor'] = remove_accents(
                                data['Partes'].split('PRESENTADO POR')[-1].split('DERIVADO')[0]).upper()
                            item['demandado'] = ''
                        elif 'PROMOVIDO A FAVOR DE' in data['Partes']:
                            item['actor'] = remove_accents(
                                data['Partes'].split('PROMOVIDO A FAVOR DE')[-1]).upper()
                            item['demandado'] = ''
                        elif 'INTERPUESTO POR' in data['Partes']:
                            item['actor'] = remove_accents(data['Partes'].split('INTERPUESTO POR')[-1]).upper()
                            item['demandado'] = ''
                        elif 'PROM. POR' in data['Partes']:
                            if 'EN CONTRA DE' in data['Partes']:
                                item['actor'] = remove_accents(
                                    data['Partes'].split('PROM. POR')[-1].split('EN CONTRA DE')[0]).upper()
                                item['demandado'] = remove_accents(data['Partes'].split('EN CONTRA DE')[-1]).upper()
                            elif 'EN CONTRA DE' not in data['Partes']:
                                item['actor'] = remove_accents(data['Partes'].split('PROM. POR')[-1]).upper()
                                item['demandado'] = ''
                        elif 'PROMOVIDO POR' in data['Partes'] and 'VS' in data['Partes']:
                            item['actor'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1].split('VS')[0]).upper()
                            item['demandado'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1].split('VS')[1]).upper()
                        elif 'PROMOVIDO POR' in data['Partes'] and 'EN CONTRA DE' in data['Partes']:
                            item['actor'] = remove_accents(
                                data['Partes'].split('PROMOVIDO POR')[-1].split('EN CONTRA DE')[0]).upper()
                            item['demandado'] = remove_accents(
                                data['Partes'].split('PROMOVIDO POR')[-1].split('EN CONTRA DE')[-1]).upper()
                        elif 'PROMOVIDO POR' in data['Partes'] and 'EN CONTRA DE' not in data['Partes']:
                            item['actor'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1]).upper()
                            item['demandado'] = ''
                        elif 'PROMOVIDO POR' not in data['Partes'] and 'EN CONTRA DE' in data['Partes']:
                            item['actor'] = ''
                            item['demandado'] = remove_accents(data['Partes'].split('EN CONTRA DE')[-1]).upper()


                        elif len([v for v in data['Partes'].split('-') if v != '' if v != ' '][1].split('VS')) == 2:
                            item['actor'] = remove_accents(
                                [v for v in data['Partes'].split('-') if v != '' if v != ' '][1].split('VS')[
                                    0].strip().upper()).upper()
                            item['demandado'] = \
                                remove_accents(
                                    [v for v in data['Partes'].split('-') if v != '' if v != ' '][1].split('VS')[
                                        -1].strip().upper()).upper()

                        else:
                            item['actor'] = remove_accents(
                                ' '.join([v for v in data['Partes'].split('-') if v != '' if v != ' '][1:]).split('VS')[
                                    0].strip().upper()).upper()
                            item['demandado'] = ''
                    except:
                        item['actor'] = ''
                        item['demandado'] = ''
            except:
                try:
                    if 'PRESENTADO POR' in data['Partes']:
                        item['actor'] = remove_accents(data['Partes'].split('PRESENTADO POR')[-1].split('DERIVADO')[0]).upper()
                        item['demandado'] = ''
                    elif 'PROMOVIDO A FAVOR DE' in data['Partes']:
                        item['actor'] = remove_accents(
                            data['Partes'].split('PROMOVIDO A FAVOR DE')[-1]).upper()
                        item['demandado'] = ''
                    elif 'INTERPUESTO POR' in data['Partes']:
                        item['actor'] = remove_accents(data['Partes'].split('INTERPUESTO POR')[-1]).upper()
                        item['demandado'] = ''
                    elif 'PROM. POR' in data['Partes']:
                        if 'EN CONTRA DE' in data['Partes']:
                            item['actor'] = remove_accents(
                                data['Partes'].split('PROM. POR')[-1].split('EN CONTRA DE')[0]).upper()
                            item['demandado'] = remove_accents(data['Partes'].split('EN CONTRA DE')[-1]).upper()
                        elif 'EN CONTRA DE' not in data['Partes']:
                            item['actor'] = remove_accents(data['Partes'].split('PROM. POR')[-1]).upper()
                            item['demandado'] = ''

                    elif 'PROMOVIDO POR' in data['Partes'] and 'VS' in data['Partes']:
                        item['actor'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1].split('VS')[0]).upper()
                        item['demandado'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1].split('VS')[1]).upper()
                    elif 'PROMOVIDO POR' in data['Partes'] and 'EN CONTRA DE' in data['Partes']:
                        item['actor'] = remove_accents(
                            data['Partes'].split('PROMOVIDO POR')[-1].split('EN CONTRA DE')[0]).upper()
                        item['demandado'] = remove_accents(
                            data['Partes'].split('PROMOVIDO POR')[-1].split('EN CONTRA DE')[-1]).upper()
                    elif 'PROMOVIDO POR' in data['Partes'] and 'EN CONTRA DE' not in data['Partes']:
                        item['actor'] = remove_accents(data['Partes'].split('PROMOVIDO POR')[-1]).upper()
                        item['demandado'] = ''
                    elif 'PROMOVIDO POR' not in data['Partes'] and 'EN CONTRA DE' in data['Partes']:
                        item['actor'] = ''
                        item['demandado'] = remove_accents(data['Partes'].split('EN CONTRA DE')[-1]).upper()
                    elif len([v for v in data['Partes'].split('-') if v != '' if v != ' '][1].split('VS')) == 2:
                        item['actor'] = remove_accents(
                            [v for v in data['Partes'].split('-') if v != '' if v != ' '][1].split('VS')[
                                0].strip().upper()).upper()
                        item['demandado'] = \
                            remove_accents(
                                [v for v in data['Partes'].split('-') if v != '' if v != ' '][1].split('VS')[
                                    -1].strip().upper()).upper()
                    else:
                        item['actor'] = remove_accents(
                            ' '.join([v for v in data['Partes'].split('-') if v != '' if v != ' '][1:]).split('VS')[
                                0].strip().upper().replace('-', '').strip()).upper()
                        item['demandado'] = ''
                except:
                    item['actor'] = ''
                    item['demandado'] = ''

            if 'Penales'.lower() in data['Secretaria'].lower():
                if item['demandado'] == '':
                    try:
                        item['demandado'] = remove_accents(data['Partes'].split('.-')[-2]).upper()
                    except:
                        try:
                            item['demandado'] = remove_accents(data['Partes'].split('.-')[0]).upper()
                        except:
                            item['demandado'] = ''

            elif 'Acuerdos Mesa Penal'.lower() in data['Secretaria'].lower():
                if item['demandado'] == '':
                    try:
                        item['demandado'] = remove_accents(data['Partes'].split('.')[-2]).upper()
                    except:
                        try:
                            item['demandado'] = remove_accents(data['Partes'].split('.')[0]).upper()
                        except:
                            item['demandado'] = ''
            elif 'Primera Secretaría (Penal)'.lower() in data['Secretaria'].lower():
                if item['demandado'] == '':
                    try:
                        item['demandado'] = remove_accents(data['Partes'].split('.')[-2]).upper()
                    except:
                        try:
                            item['demandado'] = remove_accents(data['Partes'].split('.')[0]).upper()
                        except:
                            item['demandado'] = ''


            item['entidad'] = remove_accents(response.meta['entidad'].upper()).upper()
            try:
                tipoAsunto = data['TipoAsunto'] or ''
                asunto = data['Asunto'] or ''
                anio = data['Anio'] or ''
                item['expediente'] = remove_accents((tipoAsunto+' '+asunto+'/'+anio).upper().strip()).upper()
            except:
                item['expediente'] = ''
            item['fecha'] = remove_accents(response.meta['fecha'].upper()).upper()
            item['fuero'] = 'COMUN'
            item['juzgado'] = remove_accents(response.meta['juzgado'].upper()).upper()
            try:
                if '.-' in data['Partes']:
                    item['tipo'] = remove_accents(data['Partes'].split('.-')[0].upper()).upper()
                elif '-' in data['Partes'] and '.-' not in data['Partes']:
                    item['tipo'] = remove_accents(data['Partes'].split('-')[0].upper()).upper()
                else:
                    item['tipo'] = remove_accents(data['Partes'].split('.')[0].upper()).upper()
            except:
                item['tipo'] = ''
            try:
                item['acuerdos'] = remove_accents(data['Sintesis'].replace('@', '').upper()).upper()
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
                    item['expediente_origen'] = data['Partes'].split('DERIVADO DEL EXPEDIENTE')[-1].upper()
                else:
                    item['expediente_origen'] = ''
            except:
                item['expediente_origen'] = ''
            materia = ''
            try:
                if '(Penal)'.lower() in data['Secretaria'].lower():
                    materia = 'PENAL'
                elif 'FAMILIAR'.lower() in data['Partes'].lower() or 'FAMILIAR'.lower() in data[
                    'Secretaria'].lower() or 'FAMILIAR'.lower() in response.meta[
                    'juzgado'].lower():
                    if 'FAMILIAR'.lower() in data['Partes'].lower():
                        materia = 'FAMILIAR'
                    elif 'CIVIL'.lower() in data['Partes'].lower():
                        materia = 'CIVIL'
                    elif 'PENAL'.lower() in data['Partes'].lower():
                        materia = 'PENAL'
                    else:
                        materia = 'FAMILIAR'
                elif 'CIVIL'.lower() in data['Partes'].lower() or 'CIVIL'.lower() in data[
                    'Secretaria'].lower() or 'CIVIL'.lower() in response.meta[
                    'juzgado'].lower() or 'Civiles'.lower() in response.meta['juzgado'].lower() or 'Civiles'.lower() in \
                        data['Secretaria'].lower():
                    if 'FAMILIAR'.lower() in data['Partes'].lower():
                        materia = 'FAMILIAR'
                    elif 'CIVIL'.lower() in data['Partes'].lower():
                        materia = 'CIVIL'
                    elif 'PENAL'.lower() in data['Partes'].lower():
                        materia = 'PENAL'
                    else:
                        materia = 'CIVIL'
                elif 'PENAL'.lower() in data['Partes'].lower() or 'PENAL'.lower() in data[
                    'Secretaria'].lower() or 'PENAL'.lower() in response.meta['juzgado'].lower() or 'Penales'.lower() in \
                        data['Secretaria'].lower():
                    if 'FAMILIAR'.lower() in data['Partes'].lower():
                        materia = 'FAMILIAR'
                    elif 'CIVIL'.lower() in data['Partes'].lower():
                        materia = 'CIVIL'
                    elif 'PENAL'.lower() in data['Partes'].lower():
                        materia = 'PENAL'
                    else:
                        materia = 'PENAL'
                elif 'MIXTO'.lower() in data['Partes'].lower() or 'MIXTO'.lower() in data[
                    'Secretaria'].lower() or 'MIXTO'.lower() in response.meta['juzgado'].lower():
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
                elif item[
                    'juzgado'] == 'PRIMER UNITARIO REGIONAL DEL CIRCUITO ESPECIALIZADO PARA ADOLESCENTES EN HERMOSILLO':
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
            item['fecha_insercion'] = datetime.datetime.now()#.isoformat()
            item['fecha_tecnica'] = datetime.datetime.strptime(item['fecha'], '%Y/%m/%d')#.isoformat()
            OutPutList.append(item)

    def close(spider, reason):
        # MyClient = Mongoconexion('Crudo')
        # client = MyClient[0]
        # db = client['Crudo']
        # collection = db['Judicial_Sonora']
        global OutPutList
        with open('testdata.json', 'a+') as f:
            json.dump(OutPutList, f)
        OutPutList = []
        # try:
        #     collection.insert_many(OutPutList)
        # except:
        #     collection.insert_one(OutPutList)
        OutPutList = []


if __name__ == '__main__':
    configure_logging()
    runner = CrawlerRunner()


    @defer.inlineCallbacks
    def crawl():
        with open('dateofnextrun.txt','r',encoding='utf-8') as readdate:
            date = readdate.read()
        while True:
            dateobj = datetime.datetime.strptime(date, '%Y/%m/%d').date()
            dateToday = datetime.datetime.today().date()
            if dateobj < dateToday:
                yield runner.crawl(JudicialSonoraSpider, date)
                nextdateobj = dateobj + datetime.timedelta(days=1)
                date = nextdateobj.strftime('%Y/%m/%d')
                with open('dateofnextrun.txt','w',encoding='utf-8') as writedate:
                    writedate.write(date)

            else:
                break

        reactor.stop()


    crawl()
    reactor.run()
