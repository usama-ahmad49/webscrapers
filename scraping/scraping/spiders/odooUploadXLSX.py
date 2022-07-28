import base64
import logging
import os
import xmlrpc.client
import xlsxwriter
import xlrd
import pandas as pd
import io
import json
# import openerp




logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

cwd = os.getcwd()


# def import_journal_entry(self):
#     try:
#         book = xlrd.open_workbook(filename=self.file_name)
#     except FileNotFoundError:
#         raise UserError('No such file or directory found. \n%s.' % self.file_name)
#     except xlrd.biffh.XLRDError:
#         raise UserError('Only excel files are supported.')
#     for sheet in book.sheets():
#         try:
#             line_vals = []
#             if sheet.name == 'Sheet1':
#                 for row in range(sheet.nrows):
#                     if row >= 1:
#                         row_values = sheet.row_values(row)
#                         vals = self._create_journal_entry(row_values)
#                         line_vals.append((0, 0, vals))
#             if line_vals:
#                 date = self.date
#                 ref = self.jv_ref
#                 self.env['account.move'].create({
#                     'date': date,
#                     'ref': ref,
#                     'journal_id': self.jv_journal_id.id,
#                     'line_ids': line_vals
#                 })
#         except IndexError:
#             pass
#
# def _create_journal_entry(self, record):
#     code = int(record[0])
#     account_id = self.env['account.account'].search([('code', '=', code)], limit=1)
#     if not account_id:
#         raise UserError(_("There is no account with code %s.") % code)
#     partner_id = self.env['res.partner'].search([('name', '=', record[2])], limit=1)
#     if not partner_id:
#         partner_id = self.env['res.partner'].create({
#             'name': record[1],
#             'customer': True,
#         })
#     line_ids = {
#         'account_id': account_id.id,
#         'partner_id': partner_id.id,
#         'name': record[1],
#         'debit': record[4],
#         'credit': record[5],
#     }
#     return line_ids
#
row_value = []
def open_target_file(target_path):
    try:
        book = xlrd.open_workbook(filename=target_path)
    except FileNotFoundError:
        raise UserError('No such file or directory found. \n%s.' % self.file_name)
    except xlrd.biffh.XLRDError:
        raise UserError('Only excel files are supported.')
    for sheet in book.sheets():
        if sheet.name == 'Sheet1':
            for row in range(sheet.nrows):
                if row >= 1:
                    row_value.append(sheet.row_values(row))
    return row_value

    # with open(target_path, "rb") as excel_file:
    #     return output.read(excel_file)
        # return io.BytesIO(excel_file.read())


def encode_file(excel_file):
    json_encoded_list = json.dumps(excel_file)
    return json_encoded_list
    # return base64.b64encode(json_encoded_list)


def csvtoxlsx(csvfile):
    read_file = pd.read_csv(f'{cwd}/{csvfile}')
    read_file.to_excel(f'{cwd}/{csvfile.split(".csv")[0] + ".xlsx"}', index=None, header=True)


# class odooClient:
def insert_records(file, id):
    csvtoxlsx(file)
    path = f'{cwd}/{file.split(".csv")[0] + ".xlsx"}'
    url = 'https://odoo-dev.brandrange.com'
    db = 'BrandRange'
    username = 'scrapper@oc.com'
    password = '123#'
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    excel_file = open_target_file(path)
    encoded_excel = encode_file(excel_file)
    # encoded = base64.b64decode(excel_file)

    test = models.execute_kw(db, uid, password, 'api.configuration', 'create', [{'partner_id': id, 'import_mechanism': 'file', 'file_operation_type': 'update_sp', 'upload_sheet': f'value({excel_file})'}])
    print(test)
    logger.info(f'file sent to odoo')

if __name__ == '__main__':
    # insert_records('linoricci_pricelist_odoo_delta.csv', 34)
    filename = 'linoricci_pricelist_odoo_delta.csv'
    insert_records(filename, 34)
