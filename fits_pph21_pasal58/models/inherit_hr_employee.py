from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _


class HREmployees(models.Model):
    _inherit = 'hr.employee'

    status_sipil = fields.Selection([('TK/0', 'TK/0'), ('TK/1', 'TK/1'),
                                     ('TK/2', 'TK/2'), ('TK/3', 'TK/3'),
                                     ('K/0', 'K/0'), ('K/1', 'K/1'),
                                     ('K/2', 'K/2'), ('K/3', 'K/3')], string="Status Sipil")

    no_npwp = fields.Char(string="NPWP")
