from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestContract(TransactionCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.Contract = self.env['contract.contract']
        self.product_1 = self.env.ref('product.product_product_1')

    def test_more_than_one_invoice_contact_same_parent(self):
        partner_id = self.ref('easy_my_coop.res_partner_cooperator_2_demo')

        invoice_partner_1_args = {
            'name': 'Partner for invoice 1',
            'type': 'invoice'
        }
        invoice_partner_2_args = {
            'name': 'Partner for invoice 2',
            'type': 'invoice'
        }
        self.assertRaises(
            ValidationError,
            self.env['res.partner'].browse(partner_id).write,
            {
                'child_ids': [
                    (0, False, invoice_partner_1_args),
                    (0, False, invoice_partner_2_args)
                ]
            }
        )

    def test_one_invoice_contact_per_partner(self):
        partner_id = self.ref('easy_my_coop.res_partner_cooperator_2_demo')

        invoice_partner_args = {
            'name': 'Partner for invoice 1',
            'type': 'invoice'
        }
        self.assertTrue(
            self.env['res.partner'].browse(partner_id).write({
                'child_ids': [
                    (0, False, invoice_partner_args),
                ]
            })
        )

    def test_service_contact_wrong_type(self):
        partner_id = self.ref('easy_my_coop.res_partner_cooperator_2_demo')
        service_partner = self.env['res.partner'].create({
            'parent_id': partner_id,
            'name': 'Partner not service'
        })
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_adsl"
            )
        }
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            (vals_contract,)
        )

    def test_service_contact_right_type(self):
        partner_id = self.ref('easy_my_coop.res_partner_cooperator_2_demo')
        service_partner = self.env['res.partner'].create({
            'parent_id': partner_id,
            'name': 'Partner service OK',
            'type': 'service'
        })
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_fiber"
            )
        }
        self.assertTrue(self.env['contract.contract'].create(vals_contract))

    def test_service_contact_wrong_parent(self):
        partner_id = self.ref('easy_my_coop.res_partner_cooperator_2_demo')
        service_partner = self.env['res.partner'].create({
            'parent_id': self.ref('easy_my_coop.res_partner_cooperator_3_demo'),
            'name': 'Partner wrong parent',
            'type': 'service'
        })
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_adsl"
            )
        }
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            (vals_contract,)
        )

    def test_service_contact_wrong_parent_not_broadband(self):
        partner_id = self.ref('easy_my_coop.res_partner_cooperator_2_demo')
        service_partner = self.env['res.partner'].create({
            'parent_id': self.ref('easy_my_coop.res_partner_cooperator_3_demo'),
            'name': 'Partner wrong parent',
            'type': 'service'
        })
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile")
        }
        self.assertTrue(self.env['contract.contract'].create(vals_contract))

    def test_service_contact_wrong_type_not_broadband(self):
        partner_id = self.ref('easy_my_coop.res_partner_cooperator_2_demo')
        service_partner = self.env['res.partner'].create({
            'parent_id': partner_id,
            'name': 'Partner not service'
        })
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile")
        }
        self.assertTrue(self.env['contract.contract'].create(vals_contract))

    def test_email_not_partner_not_child_wrong_type(self):
        partner_id = self.ref('easy_my_coop.res_partner_cooperator_2_demo')
        wrong_email = self.env['res.partner'].create({
            'name': 'Bad email',
            'email': 'hello@example.com'
        })
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'email_ids': [(6, 0, [wrong_email.id])]
        }
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            (vals_contract,)
        )

    def test_email_not_partner_not_child_right_type(self):
        partner_id = self.ref('easy_my_coop.res_partner_cooperator_2_demo')
        wrong_email = self.env['res.partner'].create({
            'name': 'Bad email',
            'email': 'hello@example.com',
            'type': 'contract-email',
        })
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'email_ids': [(6, 0, [wrong_email.id])]
        }
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            (vals_contract,)
        )

    def test_email_same_partner_not_contract_email_type(self):
        partner_id = self.ref('easy_my_coop.res_partner_cooperator_2_demo')
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'email_ids': [(6, 0, [partner_id])]
        }
        self.assertTrue(self.env['contract.contract'].create(vals_contract))

    def test_email_child_partner_wrong_type(self):
        partner_id = self.ref('easy_my_coop.res_partner_cooperator_2_demo')
        child_email = self.env['res.partner'].create({
            'name': 'Bad email',
            'email': 'hello@example.com',
            'parent_id': partner_id,
        })
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'email_ids': [(6, 0, [child_email.id])]
        }
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            (vals_contract,)
        )

    def test_email_child_partner_right_type(self):
        partner_id = self.ref('easy_my_coop.res_partner_cooperator_2_demo')
        child_email = self.env['res.partner'].create({
            'name': 'Right email',
            'email': 'hello@example.com',
            'parent_id': partner_id,
            'type': 'contract-email'
        })
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'email_ids': [(6, 0, [child_email.id])]
        }
        self.assertTrue(self.env['contract.contract'].create(vals_contract))
