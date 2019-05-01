# Copyright 2019 Coop IT Easy SCRLfs
# 	    Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': "POS Auto Reconcile",
    'version': '9.0.0.1.0',

    'summary': """Adds action and wizard to reconcile POS sales with related 
    accounting entries""",

    "author": "Coop IT Easy SCRLfs, "
              "Odoo Community Association (OCA)",
    'license': "AGPL-3",
    'website': "https://github.com/OCA/pos/",

    'category': 'Point of Sale',

    'depends': [
        'account',
        'point_of_sale'
    ],

    'data': [
        'wizards/pos_autoreconcile_wizard_view.xml',
    ],
    'installable': True,
}
