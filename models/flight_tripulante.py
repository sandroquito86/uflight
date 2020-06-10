from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)
from odoo import models, fields, api
from string import ascii_letters, digits
import string 

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
            
        )
   
    crew_result_id = fields.Many2one(
        string='Resultado',
        comodel_name='flight.items',
        ondelete='restrict',
        domain="[('catalogo_id', '=', 5)]",        
        related='medical_record_ids.result_id',
        readonly=False,
        store=True       
        )
   
    crew_date_report = fields.Date(
       string='Fecha de Informe',
        related='medical_record_ids.date_report',
        readonly=False,
        store=True     
        )

    crew_referent_document = fields.Char(
       string='Documento de Referencia',  
       required=True,
       size=70,        
       related='medical_record_ids.referent_document',
        readonly=False,
        store=True )

    crew_observation = fields.Char(
       string='Observaciones',       
       size=200,  
       related='medical_record_ids.observation',
        readonly=False,
        store=True )
   
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
            domain="[('catalogo_id', '=', 5)]",
            required=True    )
        
    date_report = fields.Date(
        string='Fecha de Informe',
           )

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
        selection=[('ACTIVO', 'ACTIVO'), ('CADUCADO', 'CADUCADO')]
    )
    
    warning = {
            'title': 'Advertancia!',
            'message' : 'Your message.'
            }


    @api.onchange('result_id')
    def _onchange_field(self):        
            if(int(self.result_id.catalogo_id)!=5):
                self.result_id=""
    
    def transformar_mayuscula(self,values):
        for k, v in values.items():
            if set(str(values.get(k))).difference(digits) and values.get(k) and isinstance(values.get(k), str):             
                values[k] = values.pop(k).upper()   


    @api.model
    def create(self, values):        
        self.transformar_mayuscula(values) 
        result = super(MedicalRecord, self).create(values)        
        hr_record= self.env['hr.employee'].browse(values['hr_employee_id'])        
        domain=[('date_report','>',values['date_report'])]         
        count_record= self.env['flight.medical.record'].search_count(domain)                                      
        if count_record==0:                                                
            hr_record.crew_result_id=values['result_id']
            hr_record.crew_date_report=values['date_report']
            hr_record.crew_referent_document=values['referent_document']
            hr_record.crew_observation=values['observation']           
        return result

    
   
    def write(self, values):    
        result = super(MedicalRecord, self).write(values)
        self.transformar_mayuscula(values) 
          
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
    
    
    
    
    

   



   
   


   


   






    
    