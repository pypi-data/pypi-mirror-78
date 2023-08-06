from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MobileISPInfo(models.Model):
    _inherit = 'base.isp.info'

    _name = 'mobile.isp.info'
    _description = "Mobile ISP Info"
    _rec_name = 'phone_number'
    icc = fields.Char(string='ICC', required=True)
    previous_contract_type = fields.Selection([
                                              ('contract', 'Contract'),
                                              ('prepaid', 'Prepaid')],
                                              string='Previous Contract Type')

    @api.one
    @api.constrains('type', 'previous_contract_type')
    def _check_previous_provider_info(self):
        if self.type == 'new':
            return True
        if not self.previous_contract_type:
            raise ValidationError(
                'Previous contract type is required in a portability'
            )
