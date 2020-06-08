from odoo import models, fields, api

class HistorySecurityType(models.Model):
    _name = 'flight.aircraft.history.securitytype'
    _description = 'flight.aircraft.history.securitytype'

    tipo_seguro_id = fields.Many2one(string='Tipo de Seguro', comodel_name='flight.items',
        ondelete='restrict', domain="[('catalogo_id', '=', 8)]",)

    radiograma_seguro= fields.Char(string="Radiograma de Cambio de Seguro" ,size=70)

    observacion_seguro= fields.Text(string="Observaciones del seguro" , size=250 )

    equipamento_adicional= fields.Text(string="Equipamento Adicional" , size=250 )
    
    aeronave_id = fields.Many2one(string='Aeronave', comodel_name='flight.aircraft', ondelete='cascade',)
    

    warning = { 'title': 'Advertencia!', 'message' : 'Your message.' }


class HistoryEquipment(models.Model):
    _name = 'flight.aircraft.history.equipment'
    _description = 'flight.aircraft.history.equipment'    

    equipamento_adicional= fields.Text(string="Equipamento Adicional" , size=250 )
    aeronave_id = fields.Many2one(string='Aeronave', comodel_name='flight.aircraft', ondelete='cascade',)
    
    
    



    