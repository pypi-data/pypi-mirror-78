import json
import logging
try:
    from cerberus import Validator
except ImportError:
    _logger = logging.getLogger(__name__)
    _logger.debug("Can not import cerberus")
from odoo import http
from odoo.http import request, Response
from odoo.addons.somconnexio.services import contract_contract_service
from werkzeug.exceptions import HTTPException, InternalServerError
_logger = logging.getLogger(__name__)


class UserPublicController(http.Controller):

    @http.route(['/public-api/contract'], type='json', auth='public',
                methods=['POST'], website=True, csrf=False)
    def create_contract(self, **kwargs):
        service = contract_contract_service.ContractService(request.env)
        service.v = Validator()
        data = json.loads(request.httprequest.data)
        _logger.info("contract create body: {}".format(data))
        try:
            if not service.v.validate(data, service.validator_create()):
                raise HTTPException('Bad format - {}'.format(service.v.errors))
            response = service.create(**data)
            if not service.v.validate(response, service.validator_return_create()):
                raise InternalServerError('Bad response - {}'.format(service.v.errors))
            Response.status = "200 OK"
            return response
        except InternalServerError as e:
            Response.status = b"500 " + e.description.encode('utf-8')
            return Response()
        except Exception as e:
            Response.status = b"400 " + e.description.encode('utf-8')
            return Response()
