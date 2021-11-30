# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResUsers(models.AbstractModel):
    _name = 'res.users'
    _inherit = 'res.users'

    avt_usuario_id = fields.Many2one('avt.user', string='Usuario Aula Virtual', ondelete='cascade')
