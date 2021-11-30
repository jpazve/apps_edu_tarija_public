# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AvtUsuario(models.AbstractModel):
    _name = 'avt.usuario'
    _description = 'Usuarios'

    nombre_usuario = fields.Char(string='Nombre de Usuario')
    contrasena_usuario = fields.Char(string='Contraseña')
    usuario_relacionado_id = fields.Many2one('res.users', string='Usuario Relacionado')

    def write(self, valores):
        if 'nombre_usuario' in valores or 'contrasena_usuario' in valores:
            for usuario in self:
                if usuario.usuario_relacionado_id:
                    usuario.usuario_relacionado_id.sudo().write({
                        'login': valores.get('nombre_usuario', usuario.nombre_usuario),
                        'password': valores.get('contrasena_usuario', usuario.contrasena_usuario),
                    })
        return super(AvtUsuario, self).write(valores)

    def unlink(self):
        self.ensure_one()
        self.usuario_relacionado_id.sudo().unlink()
        return super(AvtUsuario, self).unlink()
