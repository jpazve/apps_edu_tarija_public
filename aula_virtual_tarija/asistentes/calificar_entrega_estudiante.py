# -*- coding: utf-8 -*-
from odoo import api, fields, models


class CalificarEntregaEstudiante(models.TransientModel):
    _name = 'calificar.entrega.estudiante'
    _description = 'Asistente para calificar entregas de estudiantes'

    nota = fields.Float(string='Nota')
    observaciones = fields.Text(string='Observaciones')

    def confirmar_calificacion(self):
        self.ensure_one()
        entrega_id = self.env.context.get('entrega_id')
        entrega_model = self.env.context.get('active_model')
        self.env[entrega_model].browse(entrega_id).write({
            'nota': self.nota,
            'observaciones': self.observaciones
        })
