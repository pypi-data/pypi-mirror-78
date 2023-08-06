import json
import odoo

from odoo.addons.easy_my_coop_api.tests.common import BaseEMCRestCase

HOST = "127.0.0.1"
PORT = odoo.tools.config["http_port"]


class BaseEMCRestCaseAdmin(BaseEMCRestCase):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        # Skip parent class in super to avoid recreating api key
        super(BaseEMCRestCase, cls).setUpClass(*args, **kwargs)
        cls.AuthApiKey = cls.env["auth.api.key"]
        admin = cls.env.ref("base.user_admin")
        cls.api_key_test = cls.AuthApiKey.create(
            {"name": "test-key", "key": "api-key", "user_id": admin.id}
        )


class TestContractController(BaseEMCRestCaseAdmin):

    def setUp(self):
        super().setUp()

    def http_public_post(self, url, data, headers=None):
        if url.startswith("/"):
            url = "http://{}:{}{}".format(HOST, PORT, url)
        return self.session.post(url, json=data)

    def test_route_right_create(self):
        url = "/public-api/contract"
        data = {
            "name": "123456",
            "partner_id": self.ref('base.res_partner_12'),
            "service_technology": 'Mobile',
            "service_supplier": "Másmóvil",
            "contract_lines": [],
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.reason, "OK")
        content = json.loads(response.content.decode("utf-8"))
        self.assertIn('id', content)
        contract = self.env['contract.contract'].browse(content['result']['id'])
        self.assertEquals(contract.name, data['name'])
        self.assertEquals(
            contract.partner_id,
            self.browse_ref('base.res_partner_12')
        )
        self.assertEquals(
            contract.invoice_partner_id,
            self.browse_ref('base.res_partner_12')
        )
        self.assertEquals(
            contract.service_technology_id,
            self.browse_ref('somconnexio.service_technology_mobile')
        )
        self.assertEquals(
            contract.service_supplier_id,
            self.browse_ref('somconnexio.service_supplier_masmovil')
        )

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_bad_partner_create(self):
        url = "/public-api/contract"
        data = {
            "name": "123456",
            "partner_id": 666,
            "service_technology": 'Mobile',
            "service_supplier": "Másmóvil",
            "contract_lines": [],
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.reason,
                          str("Partner id 666 not found".encode('utf-8'))
                          )

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_bad_tech_create(self):
        url = "/public-api/contract"
        data = {
            "name": "123456",
            "partner_id": self.ref('base.res_partner_12'),
            "service_technology": 'XXXX',
            "service_supplier": "Másmóvil",
            "contract_lines": [],
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.reason,
                          str("No service technology for name XXXX".encode('utf-8'))
                          )

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_bad_supplier_create(self):
        url = "/public-api/contract"
        data = {
            "name": "123456",
            "partner_id": self.ref('base.res_partner_12'),
            "service_technology": 'Mobile',
            "service_supplier": "XXXX",
            "contract_lines": [],
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.reason,
                          str("No service supplier for name XXXX".encode('utf-8'))
                          )

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_bad_combination_create(self):
        url = "/public-api/contract"
        data = {
            "name": "123456",
            "partner_id": self.ref('base.res_partner_12'),
            "service_technology": 'Fiber',
            "service_supplier": "Másmóvil",
            "contract_lines": [],
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.reason,
                          str("Bad combination Fiber and Másmóvil".encode('utf-8'))
                          )

    def test_route_right_contract_lines(self):
        url = "/public-api/contract"
        data = {
            "name": "123456",
            "partner_id": self.ref('base.res_partner_12'),
            "service_technology": 'Mobile',
            "service_supplier": "Másmóvil",
            "contract_lines": [
                {
                    "product_id": self.ref('somconnexio.100Min1GB'),
                },
                {
                    "product_id": self.ref('somconnexio.EnviamentSIM'),
                }
            ]
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.reason,
                          "OK"
                          )
        content = json.loads(response.content.decode("utf-8"))
        self.assertIn('id', content)
        contract = self.env['contract.contract'].browse(content['result']['id'])
        self.assertEquals(contract.name, data['name'])
        self.assertEquals(
            contract.partner_id,
            self.browse_ref('base.res_partner_12')
        )
        self.assertEquals(
            contract.invoice_partner_id,
            self.browse_ref('base.res_partner_12')
        )
        self.assertEquals(
            contract.service_technology_id,
            self.browse_ref('somconnexio.service_technology_mobile')
        )
        self.assertEquals(
            contract.service_supplier_id,
            self.browse_ref('somconnexio.service_supplier_masmovil')
        )
        self.assertIn(
            self.browse_ref('somconnexio.100Min1GB'), [
                c.product_id
                for c in contract.contract_line_ids
            ]
        )
        self.assertIn(
            self.browse_ref('somconnexio.EnviamentSIM'), [
                c.product_id
                for c in contract.contract_line_ids
            ]
        )

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_bad_product_id(self):
        url = "/public-api/contract"
        data = {
            "name": "123456",
            "partner_id": self.ref('base.res_partner_12'),
            "service_technology": 'Mobile',
            "service_supplier": "Másmóvil",
            "contract_lines": [
                {
                    "product_id": self.ref('somconnexio.100Min1GB'),
                },
                {
                    "product_id": 0,
                }
            ]
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.reason,
                          str("Product with id 0 not found".encode('utf-8'))
                          )

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_bad_format_product(self):
        url = "/public-api/contract"
        data = {
            "name": "123456",
            "partner_id": self.ref('base.res_partner_12'),
            "service_technology": 'Mobile',
            "service_supplier": "Másmóvil",
            "contract_lines": [
                {
                    "product_id": self.ref('somconnexio.100Min1GB'),
                },
                {
                    "product_id": 'XXX',
                }
            ]
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.reason,
                          str((
                              "Bad format - {'contract_lines': "
                              "[{1: [{'product_id': "
                              "['must be of integer type']}]}]}"
                              ).encode('utf-8'))
                          )
