# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SurveySurvey(models.Model):
    _inherit = 'survey.survey'

    actividad_id = fields.Many2one('avt.actividad', string='Actividad')
