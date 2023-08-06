from werkzeug.exceptions import BadRequest

from odoo import _

from odoo.addons.base_rest.http import wrapJsonException

from . import schemas


class ContractService:
    _description = """
        Contract creation
    """

    def __init__(self, env=False):
        self.env = env

    @staticmethod
    def validator_create():
        return schemas.S_CONTRACT_CREATE

    @staticmethod
    def validator_return_create():
        return schemas.S_CONTRACT_RETURN_CREATE

    def create(self, **params):
        params = self._prepare_create(params)
        cc = self.env["contract.contract"].sudo().create(params)
        return self._to_dict(cc)

    @staticmethod
    def _to_dict(contract):
        return {
            "id": contract.id
        }

    def _prepare_create_line(self, line):
        product = self.env["product.product"].sudo().browse(line["product_id"])
        if not product:
            raise wrapJsonException(
                BadRequest(
                    _('Product with id %s not found' % (
                        line['product_id'],))
                )
            )
        line.update({
            "name": product.name,
        })
        return line

    def _check_service_combination(self, technology_id, supplier_id):
        if not self.env['service.technology.service.supplier'].sudo().search(
            [
                ('service_technology_id', '=', technology_id),
                ('service_supplier_id', '=', supplier_id)
            ]
        ):
            return False
        else:
            return True

    def _prepare_create(self, params):
        if not self.env['res.partner'].sudo().search(
                [('id', '=', params['partner_id'])]
        ):
            raise wrapJsonException(
                BadRequest(
                    _('Partner id %s not found' % (params['partner_id'], ))
                )
            )
        contract_lines = [
            self._prepare_create_line(line)
            for line in params['contract_lines']
        ]
        response = {
            'name': params['name'],
            'partner_id': params['partner_id'],
            'invoice_partner_id': params['partner_id'],
            'service_technology_id': self._get_service_tech(
                params['service_technology']
            ).id,
            'service_supplier_id': self._get_service_supplier(
                params['service_supplier']
            ).id,
        }
        if not self._check_service_combination(
            response['service_technology_id'],
            response['service_supplier_id']
        ):
            raise wrapJsonException(
                BadRequest(
                    _(
                        'Bad combination {} and {}'.format(
                            params['service_technology'],
                            params['service_supplier']
                        )
                    )
                )
            )
        if contract_lines:
            response.update({
                'contract_line_ids': [
                    (0, False, contract_line)
                    for contract_line in contract_lines
                ],
            })
        return response

    def _get_service_tech(self, name):
        service_tech = self.env['service.technology'].sudo().search(
            [('name', '=', name)]
        )
        if service_tech:
            return service_tech
        else:
            raise wrapJsonException(
                BadRequest(_('No service technology for name %s' % name))
            )

    def _get_service_supplier(self, name):
        service_supplier = self.env['service.supplier'].sudo().search(
            [('name', '=', name)]
        )
        if service_supplier:
            return service_supplier
        else:
            raise wrapJsonException(
                BadRequest(_('No service supplier for name %s' % name))
            )
