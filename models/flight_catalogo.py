from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)
from odoo import models, fields, api
from string import ascii_letters, digits
import string 


class Catalogue(models.Model):
    _name = 'flight.catalogue'
    _description = 'flight.catalogue'

    name = fields.Char(string="Nombre del Catalogo", 
    required=True
    )

    items_ids = fields.One2many(
        string='Catalogo',
        comodel_name='flight.items',
        inverse_name='catalogo_id',
    )

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "Catálogo debe ser único"),
    ]    

    @api.constrains('name')
    def _check_name_insensitive(self):
        model_ids = self.search([('id', '!=',self.id)])        
        list_names = [x.name.upper() for x in model_ids if x.name]        
        if self.name.upper() in list_names:
            raise ValidationError("Ya existe un registro con el nombre: %s " % (self.name.upper()))

    def transformar_mayuscula(self,values):
        for k, v in values.items():
            if set(str(values.get(k))).difference(digits) and values.get(k) and isinstance(values.get(k), str):                
                values[k] = values.pop(k).upper()

    @api.model
    def create(self, values):
        #guardar en mayuscula en  la base
        self.transformar_mayuscula(values)
        result = super(Catalogue, self).create(values)    
        return result
    
    def write(self, values):
        #guardar en mayuscula en  la base
        self.transformar_mayuscula(values)
        result = super(Catalogue, self).write(values)    
        return result

    
    
    


class Items(models.Model):
    _name = 'flight.items'
    _description = 'flight.items'

    name = fields.Char(string="Item", 
    help='Escriba el nombre del item asociado a su catálogo',
    required=True, 
    )    

    descripcion = fields.Char(string="Descripcion", 
    required=True
    )
    
    catalogo_id = fields.Many2one(
        string='Catalogo',
        comodel_name='flight.catalogue',
        ondelete='restrict',
    )

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(catalogo_id,name)',
         "Items debe ser único dentro de cada catálogo"),
    ]    

    @api.constrains('name')
    def _check_name_insensitive(self):
        model_ids = self.search(['&',('id', '!=',self.id),('catalogo_id', '=', int(self.catalogo_id))])        
        list_names = [x.name.upper() for x in model_ids if x.name]        
        if self.name.upper() in list_names:
            raise ValidationError("Ya existe un registro con el nombre: %s " % (self.name.upper()))

    def transformar_mayuscula(self,values):
        for k, v in values.items():
            if set(str(values.get(k))).difference(digits) and values.get(k) and isinstance(values.get(k), str):                
                values[k] = values.pop(k).upper()
    
    @api.model
    def create(self, values):
        #guardar en mayuscula en  la base
        self.transformar_mayuscula(values)
        result = super(Items, self).create(values)    
        return result
    
    def write(self, values):
        #guardar en mayuscula en  la base
        self.transformar_mayuscula(values)
        result = super(Items, self).write(values)    
        return result
    
    

class MisionClass(models.Model):
    _name = 'flight.mission.class'
    _description = 'flight.mission.class'
   
    name = fields.Char(string="Clase de Misión", 
    required=True )


    def transformar_mayuscula(self,values):
        for k, v in values.items():
            if set(str(values.get(k))).difference(digits) and values.get(k) and isinstance(values.get(k), str):                
                values[k] = values.pop(k).upper()

    @api.model
    def create(self, values):
        #guardar en mayuscula en  la base
        self.transformar_mayuscula(values)
        result = super(MisionClass, self).create(values)    
        return result
    
    def write(self, values):
        #guardar en mayuscula en  la base
        self.transformar_mayuscula(values)
        result = super(MisionClass, self).write(values)    
        return result
    
    items_ids = fields.One2many(
        string='Catalogo',
        comodel_name='flight.items',
        inverse_name='catalogo_id',
    )

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "Misión debe ser único"),
    ]    

    @api.constrains('name')
    def _check_name_insensitive(self):
        model_ids = self.search([('id', '!=',self.id)])        
        list_names = [x.name.upper() for x in model_ids if x.name]        
        if self.name.upper() in list_names:
            raise ValidationError("Ya existe un registro con el nombre: %s " % (self.name.upper()))

 

class AdditionalEquipment(models.Model):
    _name = 'flight.addtional.equipment'
    _description = 'flight.addtional.equipment'
    _rec_name= "name"

    name = fields.Char(string="Equipo Adicional", 
    required=True )
    descripcion = fields.Char(string="Descripcion", 
    required=True )

    def transformar_mayuscula(self,values):
        for k, v in values.items():
            if set(str(values.get(k))).difference(digits) and values.get(k) and isinstance(values.get(k), str):                
                values[k] = values.pop(k).upper()

    @api.model
    def create(self, values):
        #guardar en mayuscula en  la base
        self.transformar_mayuscula(values)
        result = super(AdditionalEquipment, self).create(values)    
        return result
    
    def write(self, values):
        #guardar en mayuscula en  la base
        self.transformar_mayuscula(values)
        result = super(AdditionalEquipment, self).write(values)    
        return result
    
    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "Equipos Adicionales debe ser único"),
    ]    

    @api.constrains('name')
    def _check_name_insensitive(self):
        model_ids = self.search([('id', '!=',self.id)])        
        list_names = [x.name.upper() for x in model_ids if x.name]        
        if self.name.upper() in list_names:
            raise ValidationError("Ya existe un registro con el nombre: %s " % (self.name.upper()))

    
    
   
class Habilitaciones(models.Model):
    _name = 'flight.habilitaciones'
    _description = 'flight.habilitaciones'    
    
    name = fields.Char(
        string='Nombre',required=True
    )

    def transformar_mayuscula(self,values):
        for k, v in values.items():
            if set(str(values.get(k))).difference(digits) and values.get(k) and isinstance(values.get(k), str):                
                values[k] = values.pop(k).upper()

    @api.model
    def create(self, values):
        #guardar en mayuscula en  la base
        self.transformar_mayuscula(values)
        result = super(Habilitaciones, self).create(values)    
        return result
    
    def write(self, values):
        #guardar en mayuscula en  la base
        self.transformar_mayuscula(values)
        result = super(Habilitaciones, self).write(values)    
        return result

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "Habilitaciones debe ser único"),
    ]    

    @api.constrains('name')
    def _check_name_insensitive(self):
        model_ids = self.search([('id', '!=',self.id)])        
        list_names = [x.name.upper() for x in model_ids if x.name]        
        if self.name.upper() in list_names:
            raise ValidationError("Ya existe un registro con el nombre: %s " % (self.name.upper()))
    


class MisionPlanVuelo(models.Model):
    _name = 'flight.mision.planvuelo'
    _description = 'flight.mision.planvuelo'
    _rec_name = 'mision_id'    
    
    mision_id = fields.Many2one(
        string='Mision',
        comodel_name='flight.mission.class',
        ondelete='restrict',
    )   
    
    aeronave_id = fields.Many2one(
        string='Aeronave',
        comodel_name='flight.aircraft',
        ondelete='restrict'
    )
    
    
class Escuadron(models.Model):
    _name = 'flight.escuadron'
    _description = 'flight.escuadron'   
    
    name = fields.Char(string='Nombre',required=True)    
    
    siglas = fields.Char(string='Siglas',)    
    
    ciudad_id = fields.Many2one(string='Ciudad',comodel_name='flight.ciudad',
        ondelete='restrict',)

    def transformar_mayuscula(self,values):
        for k, v in values.items():
            if set(str(values.get(k))).difference(digits) and values.get(k) and isinstance(values.get(k), str):                
                values[k] = values.pop(k).upper()
        

    @api.model
    def create(self, values):
        #guardar en mayuscula en  la base
        self.transformar_mayuscula(values)
        result = super(Escuadron, self).create(values)    
        return result
    
    def write(self, values):
        #guardar en mayuscula en  la base
        self.transformar_mayuscula(values)
        result = super(Escuadron, self).write(values)    
        return result

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "Escuadron debe ser único"),
    ]    

    @api.constrains('name')
    def _check_name_insensitive(self):
        model_ids = self.search([('id', '!=',self.id)])        
        list_names = [x.name.upper() for x in model_ids if x.name]        
        if self.name.upper() in list_names:
            raise ValidationError("Ya existe un registro con el nombre: %s " % (self.name.upper()))
    


class Ciudad(models.Model):
    _name = 'flight.ciudad'
    _description = 'flight.ciudad'   
    
    name = fields.Char(string='Ciudad',) 

    def transformar_mayuscula(self,values):
        for k, v in values.items():
            if set(str(values.get(k))).difference(digits) and values.get(k) and isinstance(values.get(k), str):                
                values[k] = values.pop(k).upper()       

    @api.model
    def create(self, values):
        #guardar en mayuscula en  la base
        self.transformar_mayuscula(values)
        result = super(Ciudad, self).create(values)    
        return result
    
    def write(self, values):
        #guardar en mayuscula en  la base
        self.transformar_mayuscula(values)
        result = super(Ciudad, self).write(values)    
        return result

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "Ciudad debe ser único"),
    ]    

    @api.constrains('name')
    def _check_name_insensitive(self):
        model_ids = self.search([('id', '!=',self.id)])        
        list_names = [x.name.upper() for x in model_ids if x.name]        
        if self.name.upper() in list_names:
            raise ValidationError("Ya existe un registro con el nombre: %s " % (self.name.upper()))
     
    

class TiposMotores(models.Model):
    _name = 'flight.tipos.motores'
    _description = 'flight.tipos.motores'    
    
    name = fields.Char(string='Nombre',required=True)
    modelo = fields.Char(string='Modelo',)

    def transformar_mayuscula(self,values):
        for k, v in values.items():
            if set(str(values.get(k))).difference(digits) and values.get(k) and isinstance(values.get(k), str):                
                values[k] = values.pop(k).upper()       

    @api.model
    def create(self, values):
        #guardar en mayuscula en  la base
        self.transformar_mayuscula(values)
        result = super(TiposMotores, self).create(values)    
        return result
    
    def write(self, values):
        #guardar en mayuscula en  la base
        self.transformar_mayuscula(values)
        result = super(TiposMotores, self).write(values)    
        return result

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "Tipos de Motores debe ser único"),
    ]    

    @api.constrains('name')
    def _check_name_insensitive(self):
        model_ids = self.search([('id', '!=',self.id)])        
        list_names = [x.name.upper() for x in model_ids if x.name]        
        if self.name.upper() in list_names:
            raise ValidationError("Ya existe un registro con el nombre: %s " % (self.name.upper()))

    

class EquipoDeteccion(models.Model):
    _name = 'flight.equipo.deteccion'
    _description = 'flight.equipo.deteccion'    
    
    name = fields.Char(string='Nombre',required=True)
    descripcion = fields.Char(string='Descripcion',)

    def transformar_mayuscula(self,values):
        for k, v in values.items():
            if set(str(values.get(k))).difference(digits) and values.get(k) and isinstance(values.get(k), str):                
                values[k] = values.pop(k).upper()       

    @api.model
    def create(self, values):
        #guardar en mayuscula en  la base
        self.transformar_mayuscula(values)
        result = super(EquipoDeteccion, self).create(values)    
        return result
    
    def write(self, values):
        #guardar en mayuscula en  la base
        self.transformar_mayuscula(values)
        result = super(EquipoDeteccion, self).write(values)    
        return result

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "Equipos de detección debe ser único"),
    ]    

    @api.constrains('name')
    def _check_name_insensitive(self):
        model_ids = self.search([('id', '!=',self.id)])        
        list_names = [x.name.upper() for x in model_ids if x.name]        
        if self.name.upper() in list_names:
            raise ValidationError("Ya existe un registro con el nombre: %s " % (self.name.upper()))



class EquipoComunicacion(models.Model):
    _name = 'flight.equipo.comunicacion'
    _description = 'flight.equipo.comunicacion'    
    
    name = fields.Char(string='Nombre',required=True)
    descripcion = fields.Char(string='Descripcion',)

    def transformar_mayuscula(self,values):
        for k, v in values.items():
            if set(str(values.get(k))).difference(digits) and values.get(k) and isinstance(values.get(k), str):                
                values[k] = values.pop(k).upper()       

    @api.model
    def create(self, values):
        #guardar en mayuscula en  la base
        self.transformar_mayuscula(values)
        result = super(EquipoComunicacion, self).create(values)    
        return result
    
    def write(self, values):
        #guardar en mayuscula en  la base
        self.transformar_mayuscula(values)
        result = super(EquipoComunicacion, self).write(values)    
        return result

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "Equipos de comunicación debe ser único"),
    ]    

    @api.constrains('name')
    def _check_name_insensitive(self):
        model_ids = self.search([('id', '!=',self.id)])        
        list_names = [x.name.upper() for x in model_ids if x.name]        
        if self.name.upper() in list_names:
            raise ValidationError("Ya existe un registro con el nombre: %s " % (self.name.upper()))

    

class EquipoNavegacion(models.Model):
    _name = 'flight.equipo.navegacion'
    _description = 'flight.equipo.navegacion'    
    
    name = fields.Char(string='Nombre',required=True)
    descripcion = fields.Char(string='Descripcion',)

    def transformar_mayuscula(self,values):
        for k, v in values.items():            
            if set(str(values.get(k))).difference(digits) and values.get(k) and isinstance(values.get(k), str):            
                values[k] = values.pop(k).upper()       

    @api.model
    def create(self, values):
        #guardar en mayuscula en  la base
        self.transformar_mayuscula(values)
        result = super(EquipoNavegacion, self).create(values)    
        return result
    
    def write(self, values):
        #guardar en mayuscula en  la base
        self.transformar_mayuscula(values)
        result = super(EquipoNavegacion, self).write(values)    
        return result
    
    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "Equipos de navegación debe ser único"),
    ]    

    @api.constrains('name')
    def _check_name_insensitive(self):
        model_ids = self.search([('id', '!=',self.id)])        
        list_names = [x.name.upper() for x in model_ids if x.name]        
        if self.name.upper() in list_names:
            raise ValidationError("Ya existe un registro con el nombre: %s " % (self.name.upper()))


    
    
    
    
    
    
    
    

    
    
    
    
    
    
    
    
   
   
    

