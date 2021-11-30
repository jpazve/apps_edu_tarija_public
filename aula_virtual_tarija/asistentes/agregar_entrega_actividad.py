# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AgregarEntregaActividad(models.TransientModel):
    _name = 'agregar.entrega.actividad'
    _description = 'Agregar entrega actividad'

    link_documento_online = fields.Char(string='Documento Online')
    documento_local = fields.Binary(string='Documento')
    comentario = fields.Text(string='Comentario')

    def confirmar_entrega(self):
        self.ensure_one()
        avt_entrega = self.env['avt.entrega']
        valores_entrega = {
            'link_documento_online': self.link_documento_online,
            'documento_local': self.documento_local,
            'comentario': self.comentario,
        }
        if self.env.context.get('entrega_pasada_id'):
            avt_entrega.browse(self.env.context.get('entrega_pasada_id')).write(valores_entrega)
        else:
            valores_entrega['estudiante_id'] = self.env.user.avt_usuario_id.id
            valores_entrega['actividad_id'] = self.env.context.get('active_id')
            avt_entrega.create(valores_entrega)
