from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class ServiceSupplierTest(TransactionCase):
    def setUp(self, *args, **kwargs):
        result = super().setUp(*args, **kwargs)
        self.contract_adsl_args = {
            'name': 'Contract w/service technology to adsl',
            'service_technology_id': self.ref(
                'somconnexio.service_technology_adsl'
            ),
            'partner_id': self.ref(
                'easy_my_coop.res_partner_cooperator_2_demo'
            ),
            'service_partner_id': self.ref(
                'easy_my_coop.res_partner_cooperator_2_demo'
            ),
            'invoice_partner_id': self.ref(
                'easy_my_coop.res_partner_cooperator_2_demo'
            ),
        }
        self.contract_mobile_args = {
            'name': 'Contract w/category contract to mobile '
                    'and w/o service technology',
            'service_technology_id': self.ref(
                'somconnexio.service_technology_mobile'
            ),
            'partner_id': self.ref(
                'easy_my_coop.res_partner_cooperator_2_demo'
            ),
            'invoice_partner_id': self.ref(
                'easy_my_coop.res_partner_cooperator_2_demo'
            ),
        }
        self.contract_fiber_args = {
            'name': 'Contract w/service technology to fiber',
            'service_technology_id': self.ref(
                'somconnexio.service_technology_fiber'
            ),
            'partner_id': self.ref(
                'easy_my_coop.res_partner_cooperator_2_demo'
            ),
            'service_partner_id': self.ref(
                'easy_my_coop.res_partner_cooperator_2_demo'
            ),
            'invoice_partner_id': self.ref(
                'easy_my_coop.res_partner_cooperator_2_demo'
            ),
        }

        return result

    def test_default_adsl_orange(self):
        contract_adsl = self.env['contract.contract'].create(
            self.contract_adsl_args
        )
        self.assertEqual(
            contract_adsl.service_supplier_id,
            self.browse_ref('somconnexio.service_supplier_orange')
        )

    def test_default_mobile_masmovil(self):
        contract_mobile_args = self.contract_mobile_args.copy()
        contract_mobile = self.env['contract.contract'].create(
            contract_mobile_args
        )
        self.assertEqual(
            contract_mobile.service_supplier_id,
            self.browse_ref('somconnexio.service_supplier_masmovil')
        )

    def test_default_mobile_masmovil_with_service_technology(self):
        contract_mobile_args = self.contract_mobile_args.copy()
        contract_mobile = self.env['contract.contract'].create(
            contract_mobile_args
        )
        self.assertEqual(
            contract_mobile.service_supplier_id,
            self.browse_ref('somconnexio.service_supplier_masmovil')
        )

    def test_wrong_adsl_vodafone(self):
        contract_adsl_args = self.contract_adsl_args.copy()
        contract_adsl_args.update({
            'service_supplier_id': self.ref(
                'somconnexio.service_supplier_vodafone'
            )
        })
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            [contract_adsl_args]
        )

    def test_wrong_adsl_masmovil(self):
        contract_adsl_args = self.contract_adsl_args.copy()
        contract_adsl_args.update({
            'service_supplier_id': self.ref(
                'somconnexio.service_supplier_masmovil'
            )
        })
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            [contract_adsl_args]
        )

    def test_right_adsl_orange(self):
        contract_adsl_args = self.contract_adsl_args.copy()
        contract_adsl_args.update({
            'service_supplier_id': self.ref(
                'somconnexio.service_supplier_orange'
            )
        })
        self.assertTrue(self.env['contract.contract'].create(
            contract_adsl_args
        ))

    def test_right_fiber_vodafone(self):
        contract_fiber_args = self.contract_fiber_args.copy()
        contract_fiber_args.update({
            'service_supplier_id': self.ref(
                'somconnexio.service_supplier_vodafone'
            )
        })
        self.assertTrue(self.env['contract.contract'].create(
            contract_fiber_args
        ))

    def test_wrong_fiber_masmovil(self):
        contract_fiber_args = self.contract_fiber_args.copy()
        contract_fiber_args.update({
            'service_supplier_id': self.ref(
                'somconnexio.service_supplier_masmovil'
            )
        })
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            [contract_fiber_args]
        )

    def test_right_fiber_orange(self):
        contract_fiber_args = self.contract_fiber_args.copy()
        contract_fiber_args.update({
            'service_supplier_id': self.ref(
                'somconnexio.service_supplier_orange'
            )
        })
        self.assertTrue(self.env['contract.contract'].create(
            contract_fiber_args
        ))
        self.contract_adsl_args = {
            'name': 'Contract w/category contract to broadband',
            'service_technology_id': self.ref(
                'somconnexio.service_technology_adsl'
            ),
            'partner_id': self.ref(
                'easy_my_coop.res_partner_cooperator_2_demo'
            ),
        }

    def test_wrong_mobile_vodafone(self):
        contract_mobile_args = self.contract_mobile_args.copy()
        contract_mobile_args.update({
            'service_supplier_id': self.ref(
                'somconnexio.service_supplier_vodafone'
            )
        })
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            [contract_mobile_args]
        )

    def test_wrong_mobile_orange(self):
        contract_mobile_args = self.contract_mobile_args.copy()
        contract_mobile_args.update({
            'service_supplier_id': self.ref(
                'somconnexio.service_supplier_orange'
            )
        })
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            [contract_mobile_args]
        )

    def test_right_mobile_masmovil(self):
        contract_mobile_args = self.contract_mobile_args.copy()
        contract_mobile_args.update({
            'service_supplier_id': self.ref(
                'somconnexio.service_supplier_masmovil'
            )
        })
        self.assertTrue(self.env['contract.contract'].create(
            contract_mobile_args
        ))
