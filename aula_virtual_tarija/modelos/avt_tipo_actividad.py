# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class AvtTipoActividad(models.Model):
    _name = 'avt.tipo.actividad'
    _description = 'Tipos de Actividades'
    _rec_name = 'nombre_tipo_actividad'

    nombre_tipo_actividad = fields.Char(string='Nombre', required=True)
    ponderacion_parcial = fields.Float(string='Ponderación', required=True)
    es_examen = fields.Boolean(string='Es Examen')
