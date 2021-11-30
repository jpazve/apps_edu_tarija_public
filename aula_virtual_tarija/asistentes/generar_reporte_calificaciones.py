# -*- coding: utf-8 -*-
from odoo import api, fields, models



class GenerarReporteCalificaciones(models.TransientModel):
    _name = 'generar.reporte.calificaciones'
    _description = 'Generador de reporte de calificaciones'

    cronograma_evaluacion_id = fields.Many2one('avt.cronograma.evaluacion', string='Cronograma de Evaluacion')
    curso_id = fields.Many2one('avt.curso', string='Curso')
    estudiante_id = fields.Many2one('avt.estudiante', string='Estudiante')

    @api.onchange('curso_id')
    def onchange_curso_id(self):
        res = {'domain': {}}
        res['domain']['estudiante_id'] = [('id', 'in', self.curso_id.estudiante_ids.ids)]
        res['domain']['materia_id'] = [('id', '=', self.curso_id.materia_ids.ids)]
        return res

    def conseguir_notas(self, materia, parcial, estudiante):
        notas = []
        porcentaje = 0
        entregas = self.env['avt.entrega'].search([
            ('actividad_id.fecha_limite_entrega', '>=', parcial.fecha_inicio),
            ('actividad_id.fecha_limite_entrega', '<=', parcial.fecha_final),
            ('estudiante_id', '=', estudiante.id),
            ('actividad_id.materia_id', '=', materia.id)
        ])
        tipos_actividad = sorted(self.cronograma_evaluacion_id.tipo_actividad_permitida,
               key=lambda tap: tap.nombre_tipo_actividad)
        for tipo_actividad in tipos_actividad:
            nota = 0
            nota_parcial = []
            for entrega in entregas:
                if entrega.actividad_id.tipo_actividad == tipo_actividad:
                    nota_parcial.append(entrega.nota)
            if len(nota_parcial):
                nota = sum(nota_parcial)/len(nota_parcial)
                porcentaje += nota*tipo_actividad.ponderacion_parcial/100
            notas.append(nota)
        notas.append(porcentaje)
        porcentaje = 0
        return notas;

    def armar_parciales(self, materias, estudiante):
        parciales = []
        notas = []
        for parcial in self.cronograma_evaluacion_id.fechas_evaluacion_parcial:
            for materia in materias:
                nota = self.conseguir_notas(materia, parcial, estudiante)
                notas.append([materia.nombre_materia] + nota)
            datos_parcial = {
                'nombre': parcial.nombre_evaluacion_parcial,
                'notas': notas
            }
            notas = []
            parciales.append(datos_parcial)
        return parciales

    def exportar_reporte(self):
        ctx = self.env.context.copy()
        cabeceras = sorted(self.cronograma_evaluacion_id.tipo_actividad_permitida,
                           key=lambda tap: tap.nombre_tipo_actividad)
        resultados_parciales = []
        materias = sorted(self.curso_id.materia_ids,
                          key=lambda tap: tap.nombre_materia)
        estudiantes = sorted(self.curso_id.estudiante_ids,
                          key=lambda tap: tap.nombre_estudiante)
        if(self.estudiante_id):
            estudiantes = [self.estudiante_id]
        for estudiante in estudiantes:
            notas = self.armar_parciales(materias, estudiante)
            datos_estudiante = {
                'nombre': estudiante.nombre_estudiante,
                'parcial': notas
            }
            resultados_parciales.append(datos_estudiante)
        data = {
            'data': {
                'curso': self.curso_id.name_get()[0][1],
                'headers': ['Materia'] + [c.nombre_tipo_actividad for c in cabeceras] + ['Nota Final'],
                'resultados_parciales': resultados_parciales
            }
        }
        return self.env.ref('aula_virtual_tarija.reporte_calificaciones_accion').with_context(
            ctx).report_action(self, data=data)
