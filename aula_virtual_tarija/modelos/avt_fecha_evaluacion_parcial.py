# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class AvtFechaEvaluacionparcial(models.Model):
    _name = 'avt.fecha.evaluacion.parcial'
    _description = 'Fechas de evaluaciones parciales'
    _rec_name = 'nombre_evaluacion_parcial'

    cronograma_id = fields.Many2one('avt.cronograma.evaluacion', string='Cronograma')
    nombre_evaluacion_parcial = fields.Char(string='Nombre')
    fecha_inicio = fields.Date(string='Fecha Inicial')
    fecha_final = fields.Date(string='Fecha Final')
