# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AvtActividad(models.Model):
    _name = 'avt.actividad'
    _description = 'Actividades'
    _rec_name = 'nombre_actividad'

    nombre_actividad = fields.Char(string='Nombre')
    materia_id = fields.Many2one('avt.materia', string='Materia', ondelete='cascade')
    tipo_actividad = fields.Many2one('avt.tipo.actividad', string='Tipo')
    es_examen = fields.Boolean(related='tipo_actividad.es_examen')
    fecha_limite_entrega = fields.Date(string='Fecha Límite Entrega')
    descripcion = fields.Text(string='Descripción')
    entrega_ids = fields.One2many('avt.entrega', 'actividad_id', string='Entregas')

    def entrega(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id(
            'aula_virtual_tarija.agregar_entrega_actividad_accion')
        entrega_pasada = self.env['avt.entrega'].search([
            ('estudiante_id', '=', self.env.user.avt_usuario_id.id),
            ('actividad_id', '=', self.id)],
            limit=1)
        ctx = dict(self.env.context)
        ctx['entrega_pasada_id'] = entrega_pasada.id
        ctx['default_link_documento_online'] = entrega_pasada.link_documento_online
        ctx['default_documento_local'] = entrega_pasada.documento_local
        ctx['default_comentario'] = entrega_pasada.comentario
        ctx['active_id'] = self.id
        ctx['active_ids'] = self.ids
        ctx['active_model'] = 'avt.entrega'
        action['context'] = ctx
        return action

    def accion_examen(self):
        self.ensure_one()
        ctx = dict(self.env.context)
        examen_existente = self.env['survey.survey'].search([('actividad_id', '=', self.id)], limit=1)
        accion = self.env['ir.actions.act_window']._for_xml_id(
            'survey.action_survey_form')
        accion['view_mode'] = 'form'
        accion['views'] = [(False, 'form')]
        accion['binding_view_types'] = 'form'
        if examen_existente:
            accion['res_id'] = examen_existente.id
        if not examen_existente:
            ctx['default_actividad_id'] = self.id
        ctx['default_acess_mode'] = 'public'
        ctx['default_users_login_required'] = True
        ctx['default_is_attempts_limited'] = True
        ctx['default_attempts_limit'] = 1
        ctx['default_session_code'] = False
        accion['context'] = ctx
        return accion

    def dar_examen(self):
        examen_existente = self.env['survey.survey'].search([('actividad_id', '=', self.id)], limit=1)
        if not examen_existente or examen_existente.state != 'open':
            raise UserError(_('El profesor aún no publica el examen'))
        return {
            'name': 'Examen',
            'type': 'ir.actions.act_url',
            'url': examen_existente.session_link,
        }

