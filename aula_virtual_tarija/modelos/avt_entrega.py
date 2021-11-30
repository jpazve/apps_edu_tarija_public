# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AvtEntrega(models.Model):
    _name = 'avt.entrega'
    _description = 'Entregas'

    estudiante_id = fields.Many2one('avt.estudiante', string='Estudiante')
    actividad_id = fields.Many2one('avt.actividad', string='Actividad', ondelete='cascade')
    link_documento_online = fields.Char(string='Documento Online')
    documento_local = fields.Binary(string='Documento')
    comentario = fields.Text(string='Comentario')
    observaciones = fields.Char(string='Observaciones')
    nota = fields.Float(string='Nota', default=0)

    def calificar_entrega(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id(
            'aula_virtual_tarija.calificar_entrega_estudiante_accion')
        ctx = dict(self.env.context)
        ctx.pop('active_id', None)
        ctx['active_ids'] = self.ids
        ctx['active_model'] = 'avt.entrega'
        ctx['entrega_id'] = self.id
        ctx['default_nota'] = self.nota
        ctx['default_observaciones'] = self.observaciones
        action['context'] = ctx
        return action
