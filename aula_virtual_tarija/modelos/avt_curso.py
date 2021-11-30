# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError


class AvtCurso(models.Model):
    _name = 'avt.curso'
    _description = 'Cursos'
    _rec_name = 'nombre_curso'

    def name_get(self):
        res = []
        for curso in self:
            res.append((curso.id, f'{curso.nombre_curso} ({curso.paralelo})'))
        return res

    @api.model
    def year_selection(self):
        year = 2000
        year_list = []
        while year != 2050:
            year_list.append((str(year), str(year)))
            year += 1
        return year_list

    def get_estudiantes_gestion(self, gestion):
        estudiantes_ids = []
        cursos_gestion = self.search([("gestion", "=", gestion)])
        for curso in cursos_gestion:
            estudiantes_ids += curso.estudiante_ids.ids
        return estudiantes_ids

    def validar_usuario_gestion(self, estudiantes_no_validos_gestion):
        self.ensure_one()
        estudiantes_no_validos_nombres = []
        for estudiante in self.estudiante_ids:
            estudiante_id = estudiante.ids[0]
            if estudiante_id in estudiantes_no_validos_gestion:
                estudiantes_no_validos_nombres.append(estudiante.nombre_estudiante)
        if estudiantes_no_validos_nombres:
            message = 'Los siguientes estudiantes ya están asignados a un curso para la gestión seleccionada:\n%s' % '\n'.join(
                estudiantes_no_validos_nombres)
            raise UserError(message)

    @api.onchange('gestion')
    def onchange_gestion(self):
        res = {}
        for record in self:
            estudiantes_no_validos_gestion = self.get_estudiantes_gestion(record.gestion)
            estudiantes_no_validos_nombres = []
            for estudiante in record.estudiante_ids:
                estudiante_id = estudiante.ids[0]
                if estudiante_id in estudiantes_no_validos_gestion:
                    estudiantes_no_validos_nombres.append(estudiante.nombre_estudiante)
            if estudiantes_no_validos_nombres:
                res['warning'] = {
                    'title': 'Estudiantes Asignados',
                    'message': 'Los siguientes estudiantes ya están asignados a un curso '
                               'para la gestión seleccionada:\n%s' % '\n'.join(estudiantes_no_validos_nombres)
                }
        return res

    @api.depends('gestion')
    def _compute_estudiantes_no_validos(self):
        for record in self:
            estudiantes_ids = self.get_estudiantes_gestion(record.gestion)
            record.estudiantes_no_validos = [(6, 0, estudiantes_ids)]

    nombre_curso = fields.Char(string='Nombre')
    paralelo = fields.Char(string='Paralelo')
    gestion = fields.Selection(year_selection, string='Gestión', default='2000')
    tutor_id = fields.Many2one('avt.profesor', string='Tutor')
    colegio_id = fields.Many2one('avt.colegio', string='Colegio', ondelete='cascade')
    estudiantes_no_validos = fields.Many2many('avt.estudiante', string="Estudiantes Validos", store=False,
                                           compute="_compute_estudiantes_no_validos")
    estudiante_ids = fields.Many2many('avt.estudiante', 'avt_curso_avt_estudiante_rel',
                                      'avt_curso_id', 'avt_estudiante_id', string='Estudiantes')
    materia_ids = fields.One2many('avt.materia', 'curso_id', string='Materias')
    conversacion_id = fields.Many2one('mail.channel', string='Conversación')

    def obtener_participantes_conversacion(self):
        estudiantes = [estudiante.usuario_relacionado_id.partner_id.id for estudiante in self.estudiante_ids]
        maestros = [materia.profesor_id.usuario_relacionado_id.partner_id.id for materia in self.materia_ids]
        tutor = [self.tutor_id.usuario_relacionado_id.partner_id.id]
        administrador = [self.colegio_id.avt_administrador_colegio.usuario_relacionado_id.partner_id.id]
        participantes = estudiantes + maestros + tutor + administrador
        return list(set(participantes))

    def actualizar_conversacion(self):
        channel_last_seen_partner_ids = [(5, 0, 0)]
        channel_last_seen_partner_ids += [(0, 0, {
            'partner_id': participante_id
        }) for participante_id in self.obtener_participantes_conversacion()]
        self.sudo().conversacion_id.write({
            'channel_last_seen_partner_ids': channel_last_seen_partner_ids
        })

    def crear_conversacion(self):
        self.ensure_one()
        channel_values = {
            'name': f'{self.nombre_curso} ({self.paralelo}) - {self.gestion}',
            'public': 'private',
            'channel_last_seen_partner_ids': [(0, 0, {
                'partner_id': participante_id
            }) for participante_id in self.obtener_participantes_conversacion()]
        }
        nueva_conversacion = self.env['mail.channel'].create(channel_values)
        self.write({'conversacion_id': nueva_conversacion.id})

    @api.model
    def create(self, values):
        estudiantes_no_validos_gestion = self.get_estudiantes_gestion(values.get('gestion'))
        curso_nuevo = super(AvtCurso, self).create(values)
        curso_nuevo.validar_usuario_gestion(estudiantes_no_validos_gestion)
        curso_nuevo.crear_conversacion()
        return curso_nuevo

    def write(self, values):
        estudiantes_no_validos_gestion = self.get_estudiantes_gestion(values.get('gestion'))
        res = super(AvtCurso, self).write(values)
        for record in self:
            record.validar_usuario_gestion(estudiantes_no_validos_gestion)
        if 'estudiante_ids' in values or 'materia_ids' in values:
            for record in self:
                record.actualizar_conversacion()
        return res

    def unlink(self):
        self.ensure_one()
        self.conversacion_id.sudo().unlink()
        return super(AvtCurso, self).unlink()
