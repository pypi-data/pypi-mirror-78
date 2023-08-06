from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BaseISPInfo(models.AbstractModel):
    _name = 'base.isp.info'
    phone_number = fields.Char(string='Phone Number', required=True)
    delivery_address = fields.Many2one('res.partner',
                                       required=True,
                                       string='Delivery Address')
    type = fields.Selection([('portability', 'Portability'), ('new', 'New')],
                            default='new',
                            string='Type')
    previous_provider = fields.Many2one('previous.provider',
                                        string='Previous Provider')
    previous_owner_vat_number = fields.Char(string='Previous Owner VatNumber')
    previous_owner_name = fields.Char(string='Previous Owner Name')
    previous_owner_firstname = fields.Char(string='Previous Owner Firstname')

    @api.one
    @api.constrains(
        'type', 'previous_provider', 'previous_owner_vat_number',
        'previous_owner_name', 'previous_owner_firsname')
    def _check_protability_info(self):
        if self.type == 'new':
            return True
        if not self.previous_provider:
            raise ValidationError(
                'Previous provider is required in a portability'
            )
        if (not self.previous_owner_vat_number or not self.previous_owner_firstname or
                not self.previous_owner_name):
            raise ValidationError(
                'Previous owner info is required in a portability'
            )
