# Copyright 2019 Coop IT Easy SCRLfs
# @author Pierrick Brun <pierrick.brun@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


import base64
from odoo import fields, models, api, _


class PosOrder(models.Model):
    _inherit = "pos.order"

    email_receipt_sent = fields.Boolean()

    @api.model
    def send_mail_receipt(
        self, pos_reference, email, body_from_ui, force=True
    ):
        order = self.search([("pos_reference", "=", pos_reference)])
        if len(order) < 1:
            return _("Error: no order found")
        if order.email_receipt_sent:
            return _("E-mail already sent")
        if not email and not order.partner_id and not order.partner_id.email:
            return _(
                "Cannot send the ticket, no email address found for the client"
            )
        mail_template = self.env.ref("pos_mail_receipt.email_send_ticket")
        if email:
            mail_template.email_to = email
        else:
            mail_template.email_to = order.partner_id.email
        base64_pdf = self.env["ir.actions.report"]._run_wkhtmltopdf(
            [body_from_ui.encode("utf-16")],
            landscape=False,
            specific_paperformat_args={
                "data-report-margin-top": 10,
                "data-report-header-spacing": 10,
            },
        )
        attachment = self.env["ir.attachment"].create(
            {
                "name": pos_reference,
                "datas_fname": _("Receipt_{}.pdf".format(pos_reference)),
                "type": "binary",
                "mimetype": "application/x-pdf",
                "db_datas": base64.encodestring(base64_pdf),
                "res_model": "pos.order",
                "res_id": order.id,
            }
        )
        mail_template.send_mail(
            order.id,
            force_send=force,
            email_values={"attachment_ids": [attachment.id]},
        )
        order.email_receipt_sent = True

    @api.model
    def create_from_ui(self, orders):
        res = super(PosOrder, self).create_from_ui(orders)
        for order in orders:
            if "email" in order["data"]:
                self.send_mail_receipt(
                    order["data"]["name"],
                    order["data"]["email"],
                    order["data"]["body_from_ui"],
                    force=False,
                )
        return res
