from odoo import models, fields


class BroadbandISPInfo(models.Model):
    _inherit = 'base.isp.info'

    _name = 'broadband.isp.info'
    _description = "Broadband ISP Info"
    _rec_name = 'phone_number'
    service_address = fields.Many2one('res.partner',
                                      required=True,
                                      string='Service Address')
