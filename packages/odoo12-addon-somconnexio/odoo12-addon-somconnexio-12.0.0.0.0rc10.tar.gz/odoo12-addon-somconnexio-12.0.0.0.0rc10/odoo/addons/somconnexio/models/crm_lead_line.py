from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CRMLeadLine(models.Model):
    _inherit = 'crm.lead.line'

    broadband_isp_info = fields.Many2one(
        'broadband.isp.info',
        string='Broadband ISP Info'
    )
    mobile_isp_info = fields.Many2one(
        'mobile.isp.info',
        string='Mobile ISP Info'
    )

    is_mobile = fields.Boolean(
        compute='_get_is_mobile',
    )

    @api.depends('product_id')
    def _get_is_mobile(self):
        for record in self:
            mobile = self.env.ref('somconnexio.mobile_service')
            record.is_mobile = (
                mobile.id == record.product_id.product_tmpl_id.categ_id.id
            )

    @api.constrains('is_mobile', 'broadband_isp_info', 'mobile_isp_info')
    def _check_isp_info(self):
        for record in self:
            if record.is_mobile:
                if not record.mobile_isp_info:
                    raise ValidationError(
                        'A mobile lead line needs a Mobile ISP Info instance related.'
                    )
            else:
                if not record.broadband_isp_info:
                    raise ValidationError(
                        'A broadband lead line needs a Broadband '
                        + 'ISP Info instance related.'
                    )
