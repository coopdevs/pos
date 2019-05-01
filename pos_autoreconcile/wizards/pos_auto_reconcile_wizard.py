# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs
# 	    Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class AutoReconcileWizard(models.Model):
    _name = 'pos.autoreconcile.wizard'

    account_id = fields.Many2one(
        comodel_name='account.account',
        string='Account to Reconcile',
        domain=[('reconcile', '=', True)],
    )
    start_date = fields.Date(
        string='Start Date',
    )
    end_date = fields.Date(
        string='End Date',
    )

    @api.multi
    def reconcile(self):
        print(self.account_id, self.start_date, self.end_date)
