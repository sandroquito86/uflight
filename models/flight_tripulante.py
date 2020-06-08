from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)
from odoo import models, fields, api
from string import ascii_letters, digits

class Tripulantes(models.Model):    
    _inherit = ['hr.employee']


    document_id = fields.Char(
      string='Cédula de Identidad',    
      required=True,
      size=10    ) 
   
   
    name = fields.Char(size=15) 
        

    crew_degree = fields.Char(
      string='Grado del Tripulante',    
      required=True    )
 
    medical_record_ids = fields.One2many(
       string='Registro Medico',
       comodel_name='flight.medical.record',
       inverse_name='hr_employee_id',
       limit=2,
        )
   
    crew_result_id = fields.Many2one(
        string='Resultado',
        comodel_name='flight.items',
        ondelete='restrict',
        domain="[('catalogo_id', '=', 8)]",
         )
   
    crew_date_report = fields.Date(
       string='Fecha de Informe',
        )

    crew_referent_document = fields.Char(
       string='Documento de Referencia',  
       required=True,
       size=70,  )

    crew_observation = fields.Char(
       string='Observaciones',       
       size=200,  )
   
    crew_hr_employee_id = fields.Many2one(
       string='Tripulantes',
       comodel_name='hr.employee',
       ondelete='restrict',       
       required=True,    )
    
    quatification_ids = fields.One2many(
       string='Habilitaciones',
       comodel_name='flight.qualification',
       inverse_name='tripulante_id',
   )

    



class MedicalRecord(models.Model):
   _name = 'flight.medical.record'
   _description = 'flight.medical.record'
   _order="date_report desc,create_date desc"
   _rec_name='result_id'
   
   result_id = fields.Many2one(
        string='Resultado',
        comodel_name='flight.items',
        ondelete='restrict',
        domain="[('catalogo_id', '=', 9)]",
        required=True    )
    
   date_report = fields.Date(
       string='Fecha de Informe',
       required=True,   )

   referent_document = fields.Char(
       string='Documento de Referencia',  
       required=True,
       size=70,  )

   observation = fields.Char(
       string='Observaciones',       
       size=200,  )
   
   hr_employee_id = fields.Many2one(
       string='Nombres',
       comodel_name='hr.employee',
       ondelete='restrict',       
       required=True,    )
   
   
   state = fields.Selection(
       string='Estado',
       selection=[('Activo', 'Activo'), ('Caducado', 'Caducado')]
   )

   
   
   
   warning = {
        'title': 'Advertancia!',
        'message' : 'Your message.'
         }


   @api.onchange('result_id')
   def _onchange_field(self):        
        if(int(self.result_id.catalogo_id)!=9):
            self.result_id=""

   @api.model
   def create(self, values):         
        hr_record= self.env['hr.employee'].browse(values['hr_employee_id'])
        #definir si el historial que ingresa corresponde a la ultima fecha
        domain=[('date_report','>',values['date_report'])]         
        medical_record= self.env['flight.medical.record'].search(domain)        
        if not medical_record:                        
            hr_record.crew_result_id=values['result_id']
            hr_record.crew_date_report=values['date_report']
            hr_record.crew_referent_document=values['referent_document']
            hr_record.crew_observation=values['observation']    
        result = super(MedicalRecord, self).create(values)   
        return result


class Qualification(models.Model):
    _name = 'flight.qualification'
    _description = 'flight.qualification'
    _rec_name = 'tripulante_id'
    
    tripulante_id = fields.Many2one(
        string='Tripulantes', comodel_name='hr.employee', ondelete='restrict',) 
    
    aeronave_id = fields.Many2one(
        string='Aeronaves',comodel_name='flight.aircraft',ondelete='restrict',)

   
    habilitacion_id = fields.Many2one(
        string='Habilitacion', comodel_name='flight.habilitaciones', ondelete='restrict',)
       

    
    _sql_constraints = [
        ('name_unique',
         'UNIQUE(tripulante_id,aeronave_id,habilitacion_id)',
         "Ya se encuentra habilitado en la Aeronave seleccionada"),
    ]
    
    
    
    
    

   



   
   


   


   






    
    