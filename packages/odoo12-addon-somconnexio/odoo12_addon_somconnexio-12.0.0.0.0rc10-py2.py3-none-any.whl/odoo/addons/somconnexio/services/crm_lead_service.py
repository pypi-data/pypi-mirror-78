import logging

from werkzeug.exceptions import BadRequest

from odoo import _

from odoo.addons.base_rest.http import wrapJsonException
from odoo.addons.component.core import Component

from . import schemas

_logger = logging.getLogger(__name__)


class CRMLeadService(Component):
    _inherit = "base.rest.service"
    _name = "crm.lead.services"
    _usage = "crm-lead"
    _collection = "emc.services"
    _description = """
        CRMLead requests
    """

    def create(self, **params):
        params = self._prepare_create(params)
        # tracking_disable=True in context is needed
        # to avoid to send a mail in CRMLead creation
        sr = self.env["crm.lead"].with_context(tracking_disable=True).create(params)
        return self._to_dict(sr)

    def _validator_create(self):
        return schemas.S_CRM_LEAD_CREATE

    def _validator_return_create(self):
        return schemas.S_CRM_LEAD_RETURN_CREATE

    @staticmethod
    def _to_dict(crm_lead):
        return {
            "id": crm_lead.id
        }

    def _get_country(self, code):
        country = self.env["res.country"].search([("code", "=", code)])
        if country:
            return country
        else:
            raise wrapJsonException(
                BadRequest(_("No country for isocode %s") % code)
            )

    def _get_state(self, code, country_id):
        state = self.env["res.country.state"].search([
            ("code", "=", code),
            ("country_id", "=", country_id)])
        if state:
            return state
        else:
            raise wrapJsonException(
                BadRequest(
                    _("No state for isocode %s and country id %s") %
                    (code, str(country_id))
                )
            )

    def _prepare_create_address(self, address):
        prepared_address = address.copy()
        prepared_address["country_id"] = self._get_country(address["country"]).id
        prepared_address["state_id"] = self._get_state(
            address["state"],
            prepared_address["country"]).id
        prepared_address.pop("country")
        prepared_address.pop("state")
        return prepared_address

    def _prepare_create_isp_info(self, isp_info):
        if not isp_info:
            return

        Partner = self.env["res.partner"]

        isp_info["delivery_address"] = Partner.create(
            self._prepare_create_address(isp_info["delivery_address"])).id

        if "service_address" in isp_info.keys():
            isp_info["service_address"] = Partner.create(
                self._prepare_create_address(isp_info["service_address"])).id

        return isp_info

    def _prepare_create_line(self, line):
        product = self.env["product.product"].browse(line["product_id"])
        if not product:
            raise wrapJsonException(
                BadRequest(
                    _('Product with id %s not found' % (
                        line['product_id'], ))
                )
            )
        if "broadband_isp_info" in line.keys():
            line["broadband_isp_info"] = self.env["broadband.isp.info"].create(
                self._prepare_create_isp_info(line["broadband_isp_info"])).id

        if "mobile_isp_info" in line.keys():
            line["mobile_isp_info"] = self.env["mobile.isp.info"].create(
                self._prepare_create_isp_info(line["mobile_isp_info"])).id

        line.update({
            "name": product.name,
            "product_tmpl_id": product.product_tmpl_id.id,
            "category_id": product.categ_id.id
        })

        return line

    def _prepare_create(self, params):
        if not self.env['subscription.request'].search(
                [('id', '=', params['subscription_request_id'])]
        ):
            raise wrapJsonException(
                BadRequest(
                    _('SubscriptionRequest with id %s not found' % (
                        params['subscription_request_id'], ))
                )
            )

        crm_line_ids = [
            self.env["crm.lead.line"].create(self._prepare_create_line(line)).id
            for line in params["lead_line_ids"]
        ]
        return {
            "name": params["name"],
            "subscription_request_id": params["subscription_request_id"],
            "lead_line_ids": [(6, 0, crm_line_ids)]
        }
