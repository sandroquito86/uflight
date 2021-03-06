from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)
from odoo import models, fields, api
from string import ascii_letters, digits
import string 
import time
import datetime

class GestionPlanSemanal(models.Model):
    _name = 'flight.gestion.plan.semanal'
    _description = 'flight.gestion.plan.semanal' 
    _rec_name='descripcion' 
  
    
    vuelo_planificado = fields.Selection(
        string='Vuelo Planificado',
        selection=[('VUELO PLANIFICADO', 'VUELO PLANIFICADO'), ('ORDEN DE VUELO', 'ORDEN DE VUELO')]
    )
    
    descripcion = fields.Char(string='Descripción',size=80,required=True)

    fecha_inicial = fields.Date( string='Desde',required=True)        
    fecha_final = fields.Date( string='Hasta',required=True)        
       
    state = fields.Selection([
        ('activo', 'Activo'),
        ('planificado', 'Planificado'),
        ('aprobado_reparto', 'Aprobado Comandante Reparto'),
        ('ope_coavna', 'Aprobado Operador COAVNA'),
        ('aprobado_coavna', 'Aprobado Comandante COAVNA'),
        ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='activo')    
    
    observacion_reparto = fields.Text(
        string='Observaciones Director Reparto:',
    )
    
    observacion_coavna = fields.Text(
        string='Observaciones Director COAVNA',
    )    
    
    
    vuelosplanificados_ids = fields.One2many(
        string='Vuelos',
        comodel_name='flight.vuelos.planificados',
        inverse_name='gestion_plan_semanal_id',
    )

    def action_retornar_activo(self):
        self.write({'state': 'activo'})
    
    def action_confirm_operador_reparto(self):
        self.write({'state': 'planificado'})
        
    def action_confirm_comandante_reparto(self):
        self.write({'state': 'aprobado_reparto'})
        
    def action_confirm_operador_coavna(self):
        self.write({'state': 'ope_coavna'})
        
    def action_confirm_comandante_coavna(self):
        self.write({'state': 'aprobado_coavna'})

    
    def transformar_mayuscula(self,values):
        for k, v in values.items():
            if set(str(values.get(k))).difference(digits) and values.get(k) and isinstance(values.get(k), str):                
                values[k] = values.pop(k).upper()

    @api.model
    def create(self, values):
        self.transformar_mayuscula(values)       
        result = super(GestionPlanSemanal, self).create(values)    
        return result

    def write(self, values):  
      self.transformar_mayuscula(values)         
      result = super(GestionPlanSemanal, self).write(values)   
      return result
    
      

class VuelosPlanificados(models.Model):
    _name = 'flight.vuelos.planificados'
    _description = 'flight.vuelos.planificados'

    
    aeronave_id = fields.Many2one(
        string='Aeronaves',comodel_name='flight.aircraft',ondelete='restrict',required=True)

    matricula = fields.Char(
        string='matricula',related='aeronave_id.name', store=False ) 
    
    mision_planvuelo_ids = fields.Many2many(
        string='Misiones Plan de Vuelo',
        comodel_name='flight.mision.planvuelo',
        relation='plavuelo_misionplanvuelo_rel',
        column1='vueloplanificado_id',
        column2='misionvueloplanificado_id', 
        domain="[('aeronave_id', '=', aeronave_id)]",
        ondelete='restrict'
     )
    
    
    fecha_vuelo = fields.Date(
        string='Fecha de vuelo',default=fields.Date.context_today,required=True,               
        domain=[('fecha_vuelo','>=',fields.Date.context_today)])    
       
    hora = fields.Many2one(
        string='Hora', comodel_name='flight.items', ondelete='restrict',
        domain="[('catalogo_id', '=', 11)]", required=True)

    piloto_id = fields.Many2one(
        string='Piloto', comodel_name='flight.qualification', ondelete='restrict', )    
    
    copiloto_id = fields.Many2one(
        string='Copiloto', comodel_name='flight.qualification',ondelete='restrict')    
    
    ingeniero_vuelo_id = fields.Many2one(
        string='Ingeniero de vuelo', comodel_name='flight.qualification', ondelete='restrict')
    
    operador_electro_id = fields.Many2one(
        string='Operador Electro/óptico', comodel_name='flight.qualification', ondelete='restrict')
    
    radarista_id = fields.Many2one(
        string='Radarista', comodel_name='flight.qualification', ondelete='restrict', )    

    taco_id = fields.Many2one(
        string='Taco', comodel_name='flight.qualification', ondelete='restrict')
    
    ruta_salida_id = fields.Many2one(
        string='Ruta de salida', comodel_name='flight.ciudad', ondelete='restrict', )

    operacion_id = fields.Many2one(
        string='Operación o Destino', comodel_name='flight.ciudad', ondelete='restrict',)

    ruta_retorno_id = fields.Many2one(
        string='Ruta de retorno', comodel_name='flight.ciudad', ondelete='restrict',)
    
    mecanico_ids = fields.Many2many(
        string='Mecánico',
        comodel_name='flight.qualification',
        relation='vuelo_planificado_mecanico_rel',
        column1='vueloplanificado_id',
        column2='mecanico_id',        
    )


    electricista_ids = fields.Many2many(
        string='Electricista',
        comodel_name='flight.qualification',
        relation='vuelo_planificado_electricista_rel',
        column1='vueloplanificado_id',
        column2='electricista_id',        
    )

    electronico_ids = fields.Many2many(
        string='Electrónico',
        comodel_name='flight.qualification',
        relation='vuelo_planificado_electronico_rel',
        column1='vueloplanificado_id',
        column2='electronico_id',        
    )
    
    
    gestion_plan_semanal_id = fields.Many2one(
        string='Plan Semanal',
        comodel_name='flight.gestion.plan.semanal',
        ondelete='restrict',
    )
    
    warning = {'title': 'Advertancia!', 'message' : 'Your message.' }
    
    
    @api.onchange('fecha_vuelo')
    def _onchange_fecha_vuelo(self):        
        if str(self.fecha_vuelo) < str(datetime.datetime.now().strftime("%Y-%m-%d")):                
            self.fecha_vuelo=datetime.datetime.now().strftime("%Y-%m-%d")
            self.warning['message']="Fecha no puede ser menor a la fecha del sistema"
            return {'warning': self.warning}
    
            
            
            
            
            
    
    
    
    
   
            
  
    
    
    
   
    
    
    
    

    

    
    

    

    
    

    

    
    




    



