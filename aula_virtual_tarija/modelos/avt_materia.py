# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AvtMateria(models.Model):
    _name = 'avt.materia'
    _description = 'Materias'
    _rec_name = 'nombre_materia'

    nombre_materia = fields.Char(string='Nombre')
    curso_id = fields.Many2one('avt.curso', string='Curso', ondelete='cascade')
    profesor_id = fields.Many2one('avt.profesor', string='Profesor')
    actividad_ids = fields.One2many('avt.actividad', 'materia_id', string='Actividades')
