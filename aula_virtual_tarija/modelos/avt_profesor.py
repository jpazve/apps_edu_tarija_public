# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AvtProfesor(models.Model):
    _name = 'avt.profesor'
    _inherit = ['avt.usuario']
    _description = 'Profesores'
    _rec_name = 'nombre_profesor'

    nombre_profesor = fields.Char(string='Nombre')
    contacto_profesor = fields.Char(string='Contacto')
    fecha_ingreso = fields.Date(string='Fecha de Ingreso')

    @api.model
    def create(self, valores):
        usuarios_odoo_orm = self.env['res.users']
        valores_usuario_odoo = {
            'name': valores.get('nombre_profesor'),
            'login': valores.get('nombre_usuario'),
            'password': valores.get('contrasena_usuario'),
        }
        usuario_odoo = usuarios_odoo_orm.sudo().create(valores_usuario_odoo)
        group_profesor_aula_virtual = self.env.ref(
            'aula_virtual_tarija.modulo_aula_virtual_tarija_profesor')
        group_profesor_aula_virtual.sudo().write({'users': [(4, usuario_odoo.id)]})
        valores['usuario_relacionado_id'] = usuario_odoo.id
        resultado = super(AvtProfesor, self).create(valores)
        usuario_odoo.partner_id.sudo().write(
            {
                'email': usuario_odoo.login + '@aula-virtual.com'
            })
        usuario_odoo.sudo().write({'avt_usuario_id': resultado.id})
        return resultado
