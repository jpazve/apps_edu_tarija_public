# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    def write(self, valores):
        res = super(SurveyUserInput, self).write(valores)
        if valores.get('state') == 'done':
            for record in self:
                actividad = record.survey_id.actividad_id
                estudiante = self.env['avt.estudiante'].search(
                    [('usuario_relacionado_id.partner_id', '=', record.partner_id.id)])
                self.env['avt.entrega'].create({
                    'estudiante_id': estudiante.id,
                    'actividad_id': actividad.id,
                    'comentario': 'Respuestas Examen',
                    'nota': record.scoring_percentage
                })
        return res
