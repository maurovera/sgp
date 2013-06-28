'''
Created on 18/06/2013

@author: victor
'''
from geraldo import Report, ReportBand, DetailBand, SystemField, Label, ObjectValue, ReportGroup
from geraldo.utils import cm, BAND_WIDTH, TA_CENTER, TA_RIGHT,\
    FIELD_ACTION_COUNT
from geraldo.base import SubReport

class MyReport(Report):
    title = 'Reporte de Items por Fase del Proyecto'

    class band_detail(DetailBand):
        height = 0.7*cm
        elements = [
            ObjectValue(expression='Nombre', left=0.5*cm, style={'fontSize': 8}),
            ObjectValue(expression='Descripcion', left=3*cm, style={'fontSize': 8}),
            ObjectValue(expression='Version', left=9.5*cm, style={'fontSize': 8}),
            ObjectValue(expression='Prioridad', left=11.5*cm, style={'fontSize': 8}),
            ObjectValue(expression='Complejidad', left=13.5*cm, style={'fontSize': 8}),
            ObjectValue(expression='Costo', left=16*cm, style={'fontSize': 8}),
        ]
        borders = {'bottom': True}

    class band_page_header(ReportBand):
        height = 1.3*cm
        elements = [
            SystemField(expression='%(report_title)s', top=0.1*cm, left=0, width=BAND_WIDTH,
                style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER}),
            SystemField(expression=u'Page %(page_number)d of %(page_count)d', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
            Label(text="Nombre", top=0.8*cm, left=0.5*cm),
            Label(text="Descripcion", top=0.8*cm, left=3*cm),
            Label(text="Version", top=0.8*cm, left=9.5*cm),
            Label(text="Prioridad", top=0.8*cm, left=11.5*cm),
            Label(text="Complejidad", top=0.8*cm, left=13.5*cm),
            Label(text="Costo", top=0.8*cm, left=16*cm),
        ]
        borders = {'all': True}

    class band_page_footer(ReportBand):
        height = 0.5*cm
        elements = [
            Label(text='Pheta-Manager - Reportes', top=0.1*cm),
            SystemField(expression='Generado el %(now:%d, %b %Y)s a las %(now:%H:%M)s', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
            ]
        borders = {'top': True}

    class band_summary(ReportBand):
        height = 0.5*cm
        elements = [
            Label(text='Costo total del Proyecto:'),
            ObjectValue(expression='sum(Costo)', left=16*cm, style={'fontName': 'Helvetica-Bold'}),
            ]
        borders = {'top': True}

    groups = [
        ReportGroup(
            attribute_name='Fase',
            band_header=DetailBand(
                height=0.6*cm,
                elements=[
                    ObjectValue(expression='Fase', style={'fontSize': 14})
                ]
            ),
            band_footer=ReportBand(
                height = 0.5*cm,
                elements = [
                    ObjectValue(expression='sum(Costo)', left=16*cm),
                    ],
                borders = {'top': True},
            ),
        ),
    ]
    
class Reporte3(Report):
    title = 'Reporte Historial de Item'

    class band_detail(DetailBand):
        height = 0.7*cm
        elements = [
            ObjectValue(expression='Nombre', left=0.5*cm, style={'fontSize': 10}),
            ObjectValue(expression='Descripcion', left=3*cm, style={'fontSize': 10}),
            ObjectValue(expression='Version', left=9.5*cm, style={'fontSize': 10}),
            ObjectValue(expression='Prioridad', left=11.5*cm, style={'fontSize': 10}),
            ObjectValue(expression='Complejidad', left=13.5*cm, style={'fontSize': 10}),
            ObjectValue(expression='Costo', left=16*cm, style={'fontSize': 10}),
        ]
        borders = {'bottom': True}

    class band_page_header(ReportBand):
        height = 1.3*cm
        elements = [
            SystemField(expression='%(report_title)s', top=0.1*cm, left=0, width=BAND_WIDTH,
                style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER}),
            SystemField(expression=u'Page %(page_number)d of %(page_count)d', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
            Label(text="Nombre", top=0.8*cm, left=0.5*cm),
            Label(text="Descripcion", top=0.8*cm, left=3*cm),
            Label(text="Version", top=0.8*cm, left=9.5*cm),
            Label(text="Prioridad", top=0.8*cm, left=11.5*cm),
            Label(text="Complejidad", top=0.8*cm, left=13.5*cm),
            Label(text="Costo", top=0.8*cm, left=16*cm),
        ]
        borders = {'all': True}

    class band_page_footer(ReportBand):
        height = 0.5*cm
        elements = [
            Label(text='Pheta-Manager - Reportes', top=0.1*cm),
            SystemField(expression='Generado el %(now:%d, %b %Y)s a las %(now:%H:%M)s', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
            ]
        borders = {'top': True}

    subreports = [
         SubReport(
             queryset_string = '%(object)s["relaciones"]',
             band_header = ReportBand(
                     height=0.5*cm,
                     elements=[
                         Label(text='Padres', top=0, left=0.2*cm, style={'fontName': 'Helvetica-Bold','fontSize': 9}),
                         Label(text='Hijos', top=0, left=4*cm, style={'fontName': 'Helvetica-Bold','fontSize': 9}),
                         Label(text='Antecesores', top=0, left=8*cm, style={'fontName': 'Helvetica-Bold','fontSize': 9}),
                         Label(text='Sucesores', top=0, left=13*cm, style={'fontName': 'Helvetica-Bold','fontSize': 9}),
                     ],
                     borders={'top': True, 'left': True, 'right': True},
                 ),
             band_detail = ReportBand(
                     height=0.5*cm,
                     elements=[
                         ObjectValue(attribute_name='padres', top=0, left=0.2*cm, style={'fontSize': 8}),
                         ObjectValue(attribute_name='hijos', top=0, left=4*cm, style={'fontSize': 8}),
                         ObjectValue(attribute_name='antecesores', top=0, left=8*cm, style={'fontSize': 8}),
                         ObjectValue(attribute_name='sucesores', top=0, left=13*cm, style={'fontSize': 8}),
                     ],
                     borders={'bottom': True,'left': True, 'right': True},
                 ),
         ),
     ]


class Reporte1(Report):
    title = 'Reporte de Solicitudes de Cambio'

    class band_detail(DetailBand):
        height = 0.7*cm
        elements = [
            ObjectValue(expression='Solicitante', left=0.5*cm, style={'fontSize': 8}),
            ObjectValue(expression='Estado', left=3*cm, style={'fontSize': 8}),
            ObjectValue(expression='LB_Afectada', left=9.5*cm, style={'fontSize': 8}),
            ObjectValue(expression='Voto_Lider', left=13.5*cm, style={'fontSize': 8}),
        ]
        borders = {'bottom': True}

    class band_page_header(ReportBand):
        height = 1.3*cm
        elements = [
            SystemField(expression='%(report_title)s', top=0.1*cm, left=0, width=BAND_WIDTH,
                style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER}),
            SystemField(expression=u'Pagina %(page_number)d de %(page_count)d', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
            Label(text="Solicitante", top=0.8*cm, left=0.5*cm),
            Label(text="Estado", top=0.8*cm, left=3*cm),
            Label(text="LB Afectada", top=0.8*cm, left=9.5*cm),
            Label(text="Voto Lider", top=0.8*cm, left=13.5*cm),
        ]
        borders = {'all': True}

    class band_page_footer(ReportBand):
        height = 0.5*cm
        elements = [
            Label(text='Pheta-Manager - Reportes', top=0.1*cm),
            SystemField(expression='Generado el %(now:%d, %b %Y)s a las %(now:%H:%M)s', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
            ]
        borders = {'top': True}