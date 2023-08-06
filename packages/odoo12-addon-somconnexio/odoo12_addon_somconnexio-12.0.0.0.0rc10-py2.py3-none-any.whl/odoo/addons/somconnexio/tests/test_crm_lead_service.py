import json

import odoo

from .common_service import BaseEMCRestCaseAdmin


class CRMLeadServiceRestCase(BaseEMCRestCaseAdmin):

    def setUp(self):
        super().setUp()

    def test_route_right_create(self):
        url = "/api/crm-lead"
        data = {
            "name": "Lead Test",
            "subscription_request_id": self.browse_ref(
                "easy_my_coop.subscription_request_1_demo").id,
            "lead_line_ids": [
                {
                    "product_id": self.browse_ref('somconnexio.100Min1GB').id,
                    "mobile_isp_info": {
                        "icc": "123",
                        "phone_number": "123",
                        "type": "portability",
                        "delivery_address": {
                            "street": "123",
                            "zip_code": "08000",
                            "city": "Barcelona",
                            "country": "ES",
                            "state": "B"
                        },
                        "previous_provider": 1,
                        "previous_owner_name": "Newus",
                        "previous_owner_firstname": "Borgo",
                        "previous_owner_vat_number": "29461336S",
                        "previous_contract_type": "contract"
                    },
                    "broadband_isp_info": {}
                }
            ]
        }

        response = self.http_post(url, data=data)

        self.assertEquals(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        self.assertIn("id", content)

        crm_lead, = self.env["crm.lead"].browse(content["id"])
        self.assertEquals(crm_lead.name, data["name"])
        self.assertEquals(
            crm_lead.subscription_request_id.id,
            self.browse_ref("easy_my_coop.subscription_request_1_demo").id
        )
        self.assertEquals(
            len(crm_lead.lead_line_ids),
            1
        )
        crm_lead_line = crm_lead.lead_line_ids[0]
        self.assertEquals(
            crm_lead_line.product_id.id,
            self.browse_ref('somconnexio.100Min1GB').id
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.icc,
            "123",
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.type,
            "portability",
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.delivery_address.street,
            "123",
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.delivery_address.country_id.id,
            self.browse_ref('base.es').id
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.delivery_address.state_id.id,
            self.browse_ref('base.state_es_b').id
        )

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_bad_name_create(self):
        url = "/api/crm-lead"
        data = {
            "name": None,
            "subscription_request_id": self.browse_ref(
                "easy_my_coop.subscription_request_1_demo").id,
            "lead_line_ids": [
                {
                    "product_id": self.browse_ref('somconnexio.100Min1GB').id,
                    "mobile_isp_info": {
                        "icc": "123",
                        "phone_number": "123",
                        "type": "portability",
                        "delivery_address": {
                            "street": "123",
                            "zip_code": "08000",
                            "city": "Barcelona",
                            "country": "ES",
                            "state": "B"
                        },
                        "previous_provider": 1,
                        "previous_owner_name": "Newus",
                        "previous_owner_firstname": "Borgo",
                        "previous_owner_vat_number": "29461336S",
                        "previous_contract_type": "contract"
                    },
                    "broadband_isp_info": {}
                }
            ]
        }

        response = self.http_post(url, data=data)
        self.assertEquals(response.status_code, 400)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_bad_subscription_request_id_create(self):
        url = "/api/crm-lead"
        data = {
            "name": "Lead Test",
            "subscription_request_id": 666,
            "lead_line_ids": [
                {
                    "product_id": self.browse_ref('somconnexio.100Min1GB').id,
                    "mobile_isp_info": {
                        "icc": "123",
                        "phone_number": "123",
                        "type": "portability",
                        "delivery_address": {
                            "street": "123",
                            "zip_code": "08000",
                            "city": "Barcelona",
                            "country": "ES",
                            "state": "B"
                        },
                        "previous_provider": 1,
                        "previous_owner_name": "Newus",
                        "previous_owner_firstname": "Borgo",
                        "previous_owner_vat_number": "29461336S",
                        "previous_contract_type": "contract"
                    },
                    "broadband_isp_info": {}
                }
            ]
        }

        response = self.http_post(url, data=data)
        self.assertEquals(response.status_code, 400)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_bad_mobile_isp_info_create(self):
        url = "/api/crm-lead"
        data = {
            "name": "Test Lead",
            "subscription_request_id": self.browse_ref(
                "easy_my_coop.subscription_request_1_demo").id,
            "lead_line_ids": [
                {
                    "product_id": self.browse_ref('somconnexio.100Min1GB').id,
                    "mobile_isp_info": {},
                    "broadband_isp_info": {}
                }
            ]
        }
        response = self.http_post(url, data=data)
        self.assertEquals(response.status_code, 400)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_bad_broadband_isp_info_create(self):
        url = "/api/crm-lead"
        data = {
            "name": "Test Lead",
            "subscription_request_id": self.browse_ref(
                "easy_my_coop.subscription_request_1_demo").id,
            "lead_line_ids": [
                {
                    "product_id": self.browse_ref('somconnexio.ADSL20MBSenseFix').id,
                    "mobile_isp_info": {},
                    "broadband_isp_info": {}
                }
            ]
        }
        response = self.http_post(url, data=data)
        self.assertEquals(response.status_code, 400)
