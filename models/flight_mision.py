from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)
from odoo import models, fields, api
from string import ascii_letters, digits
import string 

class Mission(models.Model):
   _name = 'flight.mission'
   _description = 'flight.mission'

   name = fields.Char(string="Código de la Misión", 
   required=True, size=20
   )
       
   tipo_mision_id = fields.Many2one(
        string='Tipo de Misión', comodel_name='flight.mission.class',
        ondelete='restrict', )

   programa_entrenamiento = fields.Char(
      string="Programa de entrenamiento o Programa operativo", 
      related='attachment_ids.name', )
   #adjuntar archivo PDF
   attachment_ids = fields.Many2many(
        comodel_name='ir.attachment', relation='attachments_rel',
        column1='mission_id', column2='attachment_id', string='Archivo Adjunto')
   
   
   estado = fields.Boolean(string='Estado',default=True)
   

   warning = {
        'title': 'Advertancia!',
        'message' : 'Archivo PDF subido con exito.'
         }
  
      
   @api.onchange('name')
   def _name_validation(self):                      
      if set(str(self.name)).difference(ascii_letters + digits + '-'): 
         self.warning['message'] ="Caracteres Invalidos en CÓDIGO DE LA MISIÓN!! \nSolo permite letras numeros y guión medio (-)"                     
         self.name=""
         return {'warning': self.warning}         
            
   @api.onchange('attachment_ids')
   def _archive(self):
      self.warning['message'] ="Archivo PDF subido con exito."                     
      if(self.attachment_ids):     
         if(len(self.attachment_ids)>1): 
            self.attachment_ids.unlink() 
            self.warning['message'] ="Por favor seleccione un archivo a la vez!!"      
         text=str(self.attachment_ids.name)
         if self.attachment_ids.name:
            if not text.endswith(".pdf"): 
               self.attachment_ids.unlink()
               self.warning['message'] ="Solo se puede subir archivos PDF!!"                        
            else:
               if set(text).difference(ascii_letters + digits + '-' + '.'+ ' '):                                
                     self.attachment_ids.unlink() 
                     self.warning['message'] ="El nombre del archivo pdf tiene caracteres no validos!!"                              
         return {'warning': self.warning}

   def transformar_mayuscula(self,values):
      for k, v in values.items():
         if set(str(values.get(k))).difference(digits) and values.get(k) and isinstance(values.get(k), str):                
            values[k] = values.pop(k).upper()


   @api.model
   def create(self, values): 
      self.transformar_mayuscula(values)     
      result = super(Mission, self).create(values)   
      return result   
  
   def write(self, values):  
      self.transformar_mayuscula(values)         
      result = super(Mission, self).write(values)   
      return result
   
   
      




      
         
    
               
               
         
               
            
      
     
    