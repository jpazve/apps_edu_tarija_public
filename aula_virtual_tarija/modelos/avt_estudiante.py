# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AvtEstudiante(models.Model):
    _name = 'avt.estudiante'
    _inherit = ['avt.usuario']
    _description = 'Estudiantes'
    _rec_name = 'nombre_estudiante'

    nombre_estudiante = fields.Char(string='Nombre')
    responsable_estudiante = fields.Char(string='Responsable')
    contacto_estudiante = fields.Char(string='Contacto')
    fecha_ingreso = fields.Date(string='Fecha de Ingreso')

    @api.model
    def create(self, valores):
        usuarios_odoo_orm = self.env['res.users']
        valores_usuario_odoo = {
            'name': valores.get('nombre_estudiante'),
            'login': valores.get('nombre_usuario'),
            'password': valores.get('contrasena_usuario'),
        }
        usuario_odoo = usuarios_odoo_orm.sudo().create(valores_usuario_odoo)
        group_estudiante_aula_virtual = self.env.ref(
            'aula_virtual_tarija.modulo_aula_virtual_tarija_estudiante')
        group_estudiante_aula_virtual.sudo().write({'users': [(4, usuario_odoo.id)]})
        valores['usuario_relacionado_id'] = usuario_odoo.id
        resultado = super(AvtEstudiante, self).create(valores)
        usuario_odoo.partner_id.sudo().write(
            {
                'email': usuario_odoo.login + '@aula-virtual.com'
            })
        usuario_odoo.sudo().write({'avt_usuario_id': resultado.id})
        return resultado
