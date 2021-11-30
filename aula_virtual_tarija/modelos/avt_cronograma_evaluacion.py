# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class AvtCronogramaEvaluacion(models.Model):
    _name = 'avt.cronograma.evaluacion'
    _description = 'Cronograma de Evaluación'
    _rec_name = 'nombre_cronograma_evaluacion'

    nombre_cronograma_evaluacion = fields.Char(string='Nombre')
    tipo_actividad_permitida = fields.Many2many('avt.tipo.actividad', string='Actividades Permitidas')
    fechas_evaluacion_parcial = fields.One2many(
        'avt.fecha.evaluacion.parcial', 'cronograma_id', string='Fechas Evaluaciones Parciales')
