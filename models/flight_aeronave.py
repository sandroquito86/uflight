from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)
from odoo import models, fields, api
from string import ascii_letters, digits
import string 

class Aircraft(models.Model):
    _name = 'flight.aircraft'
    _description = 'flight.aircraft'
    
    #bandera para definir si cambio tipo de seguro

    name = fields.Char(string="Numero de Matrícula", 
        required=True, size=10, 
        help='Technical Field '
         )

    
    contador_historico = fields.Integer(
        string='Historico Tipo Seguro', compute="get_contador"
    )

    
    
    estado = fields.Boolean(
        string='Activar/Desactivar' ,
        default=True        
    )

    tipo_aeronave_id = fields.Many2one(
        string='Tipo de aeronave', comodel_name='flight.items', ondelete='restrict',
        domain="[('catalogo_id', '=', 1)]", required=True)

    modelo_id = fields.Many2one(
        string='Modelo', comodel_name='flight.items', ondelete='restrict',
        domain="[('catalogo_id', '=', 2)]", required=True)
    
    escuadron_id = fields.Many2one(
        string='Escuadron',
        comodel_name='flight.escuadron',
        ondelete='restrict',
    )    

    fecha_adquisicion = fields.Date(
        string='Fecha de Adquisición', required=True)

    aeronavegabilidad = fields.Char(
        string='Certificado de Aeronavegabilidad', size=70)

    fabricante = fields.Char(string="Fabricante", size=70)

    anio_fabricacion = fields.Char(
        string='Año de Fabricación', required=True, size=4)

    envergadura = fields.Float(string='Envergadura',)

    tipo_turbina_id = fields.Many2one(
        string='Tipo de Turbina', comodel_name='flight.items',
        ondelete='restrict', domain="[('catalogo_id', '=', 3)]", required=True)
    
    potencia = fields.Float(
        string='Potencia', required=True)    

    tipo_motor_id = fields.Many2one(
        string='Tipo de Motor', comodel_name='flight.tipos.motores', ondelete='restrict', required=True)    

    velocidad_maniobra = fields.Float(
        string='Velocidad de Maniobra', required=True)  

    longitud = fields.Float(
        string='Longitug', required=True)
    
    altura = fields.Float(
        string='Altura', required=True)  

    velocidad_economica = fields.Float(
        string='Velocidad Económica', required=True)

    crucero_rapido= fields.Float(
        string='Velocidad de Crucero Rápido', required=True)

    crucero_lento = fields.Float(
        string='Velocidad de Crucero Lento', required=True)

    altura_maxima = fields.Float(
        string='Altura Máxima de Vuelo', required=True)
    
    mision_plan_vuelo_ids = fields.One2many(
        string='Misiones',comodel_name='flight.mision.planvuelo',
        inverse_name='aeronave_id')
    
  
    
    equipo_deteccion_ids = fields.Many2many(
        string='Equipos de Detección',
        comodel_name='flight.equipo.deteccion',
        relation='aeronave_deteccion_rel',
        column1='aircraft_id',
        column2='item_id',
        ondelete='restrict',
        required=True
    )  
    equipo_comunicacion_ids = fields.Many2many(
        string='Equipos de Comunicación',
        comodel_name='flight.equipo.comunicacion',
        relation='aeronave_comunicacion_rel',
        column1='aircraft_id',
        column2='item_id',
        ondelete='restrict',
        required=True
    )  
      
    equipo_navegacion_ids = fields.Many2many(
        string='Equipos de Navegación',
        comodel_name='flight.equipo.navegacion',
        relation='aeronave_navegacion_rel',
        column1='aircraft_id',
        column2='item_id',
        ondelete='restrict',
        required=True
    )    

    num_maximo_pasajeros = fields.Integer(
        string='Número Máximo Permitido de Pasajeros', required=True )
    
    num_maximo_carga = fields.Float(string='Número Máximo Dotación de Vuelo', )

    peso_max_pasajero = fields.Float(string='Peso Máximo Permitido por Pasajero', required=True)

    peso_tot_combustible = fields.Float(string='Peso total de combustible',required=True)

    peso_max_despegue = fields.Float(string='Peso máximo de despegue',required=True)  

    tipo_seguro_id = fields.Many2one(
        string='Tipo de Seguro', comodel_name='flight.items', ondelete='restrict',
        domain="[('catalogo_id', '=', 8)]", required=True)

    cambio_radiograma= fields.Char(
        string="Radiograma de Cambio de Seguro", required=True, size=70)

    observacion_seguro= fields.Text(
        string="Observaciones del seguro", required=True, size=250)  

    

    equip_adicional_ids = fields.Many2many(
        string='Equipos Adicionales', comodel_name='flight.addtional.equipment',
        relation='flight_additional_aircraft_rel', column1='aeronave_id',column2='adicional_id')   
    
    
   
   
    tipo_seguro_id = fields.Many2one(
        string='Tipo de Seguro', comodel_name='flight.items', ondelete='restrict',
        domain="[('catalogo_id', '=', 8)]" )
   
    #Abrimos la vista historico
    def history_open_security_type(self):        
        return {
            'name': ('Historico Tipo de Seguro'),
            'domain': [('aeronave_id', '=', self.id)],
            'res_model': 'flight.aircraft.history.securitytype',
            'view_id': False,
            'view_mode': 'tree',
            'type': 'ir.actions.act_window',
        }

    def history_open_equipment(self):        
        return {
            'name': ('Historico Equipamiento Adicional'),
            'domain': [('aeronave_id', '=', self.id)],
            'res_model': 'flight.aircraft.history.equipment',
            'view_id': False,
            'view_mode': 'tree',
            'type': 'ir.actions.act_window',
        }
        
   
    
    def get_contador(self):
        #hace referencia a un objeto y permite contar en base a un criterio
        contar= self.env['flight.aircraft.history.securitytype'].search_count([('aeronave_id', '=', self.id)])
        self.contador_historico=contar
    
    #Ingreso del historico
    @api.model
    def create(self, values):  
        result = super(Aircraft, self).create(values)
        listar=[]
        for item in result.equip_adicional_ids:
             listar.append(item.name)
        vals={
            'tipo_seguro_id':values['tipo_seguro_id'],
            'radiograma_seguro':values['cambio_radiograma'],
            'observacion_seguro':values['observacion_seguro'],  
            'equipamento_adicional':str(listar), 
            'aeronave_id':result.id,
        }        
        self.env['flight.aircraft.history.securitytype'].create(vals)              
        return result
    
   
    #actualizacion de historico
    def write(self, values):        
        result = super(Aircraft, self).write(values)
        if 'equip_adicional_ids' in values:
            listar=[]
            for item in self.equip_adicional_ids:
                listar.append(item.name)
            if 'tipo_seguro_id' in values:               
                vals={
                    'tipo_seguro_id':int(self.tipo_seguro_id),
                    'radiograma_seguro':values['cambio_radiograma'],
                    'observacion_seguro':values['observacion_seguro'],
                    'equipamento_adicional':str(listar), 
                    'aeronave_id':self.id,
                }
                self.env['flight.aircraft.history.securitytype'].create(vals) 
        return result
    

    
    @api.onchange('tipo_aeronave_id','modelo_id','tipo_turbina_id','tipo_motor_id'
   )
    def _onchange_field(self):
        if(int(self.tipo_aeronave_id.catalogo_id)!=1):         self.tipo_aeronave_id=""
        if(int(self.modelo_id.catalogo_id)!=2):                self.modelo_id=""       
        if(int(self.tipo_turbina_id.catalogo_id)!=3):          self.tipo_turbina_id=""           
        
       
       
    
    @api.onchange('tipo_seguro_id')
    def _onchange_field2(self):          
        if(int(self.tipo_seguro_id.catalogo_id)==8):        
            self.cambio_radiograma=""
            self.observacion_seguro=""            
        else:
            self.tipo_seguro_id=""
            
   
    warning = {'title': 'Advertancia!', 'message' : 'Your message.' }
   
    @api.onchange('name','anio_fabricacion','cambio_radiograma',)
    def _name_validation_name(self):
        flag=False
        if set(str(self.name)).difference(ascii_letters + digits + '-'):
            self.warning['message'] ="Caracteres Invalidos en campo NÚMERO DE MATRÍCULA"  
            flag=True 
            self.name=""                            
        if set(str(self.fabricante)).difference(ascii_letters + digits + '-'):  
            self.warning['message'] ="Caracteres Invalidos en campo FABRICANTE"   
            flag=True
            self.fabricante=""             
        if set(str(self.cambio_radiograma)).difference(ascii_letters + digits + '-'):
            self.warning['message'] ="Caracteres Invalidos en campo RADIOGRAMA DE CAMBIO DE SEGURO"      
            flag=True
            self.cambio_radiograma=""   
        if flag:                                 
            return {'warning': self.warning}
    
    @api.onchange('peso_max_despegue')
    def _peso_max_despegue_validate(self):
        if self.peso_max_despegue < (self.num_maximo_carga+self.num_maximo_pasajeros)*self.peso_max_pasajero+self.peso_tot_combustible:
            self.peso_max_despegue=""
            self.warning['message'] = "El peso máximo de despegue no puede ser menor\n(Número Máximo Dotación + Número Máximo Permitido de Pasajeros) * Peso Máximo Permitido por Pasajero)+ Peso total de combustible)"
            return {'warning': self.warning}   
    
   
