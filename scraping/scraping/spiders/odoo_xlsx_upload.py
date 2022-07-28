from odoo_csv_tools.lib import mapper
from odoo_csv_tools.lib.transform import Processor

if __name__ == '__main__':
   processor = Processor('client_file.csv', delimiter=';')
   res_partner_mapping = {
      'id': mapper.m2o_map('my_import_res_partner', mapper.concat('_', 'Firstname', 'Lastname', 'Birthdate')),
      'name': mapper.concat(' ','Firstname','Lastname'),
      'birthdate': mapper.val('Birthdate', postprocess=lambda x: datetime.strptime(x, "%d/%m/%y").strftime("%Y-%m-%d 00:00:00")),
   }
