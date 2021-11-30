# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AvtAdministrador(models.Model):
    _name = 'avt.administrador'
    _inherit = ['avt.usuario']
    _description = 'Administradores'
    _rec_name = 'nombre_administrador'

    nombre_administrador = fields.Char(string='Nombre')

    @api.model
    def create(self, valores):
        usuarios_odoo_orm = self.env['res.users']
        valores_usuario_odoo = {
            'name': valores.get('nombre_administrador'),
            'login': valores.get('nombre_usuario'),
            'password': valores.get('contrasena_usuario'),
        }
        usuario_odoo = usuarios_odoo_orm.sudo().create(valores_usuario_odoo)
        group_administrador_aula_virtual = self.env.ref(
            'aula_virtual_tarija.modulo_aula_virtual_tarija_administrador')
        group_administrador_aula_virtual.sudo().write({'users': [(4, usuario_odoo.id)]})
        valores['usuario_relacionado_id'] = usuario_odoo.id
        resultado = super(AvtAdministrador, self).create(valores)
        usuario_odoo.partner_id.sudo().write(
            {
                'email': usuario_odoo.login + '@aula-virtual.com'
            })
        usuario_odoo.sudo().write({'avt_usuario_id': resultado.id})
        return resultado

