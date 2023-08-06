
This project provides an ERP system for [Som Connexio](https://somosconexion.coop/) telecommunication users cooperative.

###### DEVELOPER
To generate a database from scratch follow these steps:
```
./odoo-bin -c /etc/odoo/odoo.conf -i easy_my_coop -d odoo --stop-after-init
./odoo-bin -c /etc/odoo/odoo.conf -i easy_my_coop -d odoo --stop-after-init --test-enable
./odoo-bin -c /etc/odoo/odoo.conf -i somconnexio -d odoo --stop-after-init
```

Then, you can run the tests:
```
./odoo-bin -c /etc/odoo/odoo.conf -u somconnexio -d odoo --stop-after-init --test-enable
```

The company data is rewritten every module upgrade

Credits
=======

###### Authors

* Coopdevs Treball SCCL

###### Contributors

* Coopdevs Treball SCCL
