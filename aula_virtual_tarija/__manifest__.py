# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Aula Virtual Tarija',
    'version': '1.0',
    'summary': 'Aula Virtual Tarija',
    'description': """
Aula Virtual Tarija
    """,
    'category': 'Education',
    'depends': ['base', 'mail', 'web', 'survey'],
    'data': [
        'data/data.xml',
        'seguridad/recurso_grupos.xml',
        'seguridad/ir.model.access.csv',
        'reportes/reporte_calificaciones.xml',
        'reportes/reportes.xml',
        'vistas/avt_colegio.xml',
        'vistas/avt_administrador.xml',
        'vistas/avt_profesor.xml',
        'vistas/avt_estudiante.xml',
        'vistas/avt_curso.xml',
        'vistas/avt_materia.xml',
        'vistas/avt_tipo_actividad.xml',
        'vistas/avt_actividad.xml',
        'vistas/avt_entrega.xml',
        'vistas/avt_cronograma_evaluacion.xml',
        'asistentes/generar_reporte_calificaciones.xml',
        'vistas/menus.xml',
        'vistas/survey_survey.xml',
        'vistas/res_users.xml',
        'asistentes/calificar_entrega_estudiante.xml',
        'asistentes/agregar_entrega_actividad.xml',
    ],
    'qweb': [
        'static/src/xml/menu_usuario.xml',
        'static/src/xml/conversaciones_menu_lateral.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
