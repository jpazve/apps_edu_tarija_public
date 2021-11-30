# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AvtColegio(models.Model):
    _name = 'avt.colegio'
    _description = 'Colegios'
    _rec_name = 'nombre_colegio'

    nombre_colegio = fields.Char(string='Nombre')
    avt_administrador_colegio = fields.Many2one('avt.administrador', string='Administrador')
