from odoo import _


def boolean_validator(field, value, error):
    if value and value not in ["true", "false"]:
        error(field, _("Must be a boolean value: true or false"))


S_ADDRESS_CREATE = {
    "street": {"type": "string"},
    "zip": {"type": "string"},
    "city": {"type": "string"},
    "country": {"type": "string"},
    "state": {"type": "string"},
}

S_ISP_INFO_CREATE = {
    "phone_number": {"type": "string"},
    "type": {"type": "string"},
    "delivery_address": {
        "type": "dict",
        "schema": S_ADDRESS_CREATE
    },
    "previous_provider": {"type": "integer"},
    "previous_owner_vat_number": {"type": "string"},
    "previous_owner_name": {"type": "string"},
    "previous_owner_firstname": {"type": "string"},
}

S_MOBILE_ISP_INFO_CREATE = {
    "icc": {"type": "string"},
    "previous_contract_type": {"type": "string"},
}

S_BROADBAND_ISP_INFO_CREATE = {
    "service_address": {
        "type": "dict",
        "schema": S_ADDRESS_CREATE
    }
}

S_CRM_LEAD_RETURN_CREATE = {
    "id": {"type": "integer"}
}

S_CRM_LEAD_CREATE = {
    "name": {"type": "string", "required": True, "empty": False},
    "subscription_request_id": {"type": "integer", "required": True, "empty": False},
    "lead_line_ids": {
        "type": "list",
        "empty": False,
        "schema": {
            "type": "dict",
            "schema": {
                "product_id": {"type": "integer", "required": True},
                "name": {"type": "string"},
                "broadband_isp_info": {
                    "type": "dict",
                    # Merging dicts in Python 3.5+
                    # https://www.python.org/dev/peps/pep-0448/
                    "schema": {**S_ISP_INFO_CREATE, **S_BROADBAND_ISP_INFO_CREATE}  # noqa
                },
                "mobile_isp_info": {
                    "type": "dict",
                    "schema": {**S_ISP_INFO_CREATE, **S_MOBILE_ISP_INFO_CREATE}  # noqa
                },
            }
        },
    }
}

S_CONTRACT_CREATE = {
    "name": {"type": "string", "required": True, "empty": False},
    "partner_id": {"type": "integer", "required": True, "empty": False},
    "service_technology": {"type": "string", "required": True, "empty": False},
    "service_supplier": {"type": "string", "required": True, "empty": False},
    "contract_lines": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "product_id": {"type": "integer", "required": True},
            }
        }
    }
}

S_CONTRACT_RETURN_CREATE = {
    "id": {"type": "integer"}
}

S_PREVIOUS_PROVIDER_REQUEST_SEARCH = {
    "mobile": {"type": "string", "check_with": boolean_validator},
    "broadband": {"type": "string", "check_with": boolean_validator},
}

S_PREVIOUS_PROVIDER_RETURN_SEARCH = {
    "count": {"type": "integer"},
    "providers": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "id": {"type": "integer", "required": True},
                "name": {"type": "string", "required": True},
            }
        }
    }
}
