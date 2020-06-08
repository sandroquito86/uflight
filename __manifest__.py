# -*- coding: utf-8 -*-
{
    'name': "flight",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data_catalogo.xml',
        'data/data_items.xml', 
        'data/data_mision.xml',  
        'data/data_habilitacion.xml',  
        'data/data_escuadron.xml',
        'data/data_motor.xml',
        'data/data_equipos_adicionales.xml',        
        'views/flight_menu.xml',    
        'views/flight_registro_medico.xml',
        'views/templates.xml',
        'views/flight_aeronave_view.xml',        
        'views/flight_catalogo_view.xml',
        'views/flight_mision_view.xml',
        'views/flight_tripulante_view.xml',          
        'views/flight_historico_tipo_seguro_view.xml',
        'views/flight_historico_equipamiento.xml',          
        'views/flight_gestion_plan_semanal_view.xml',  
        'views/flight_vuelos_planificados.xml', 
        'views/flight_habilitaciones.xml', 
        'views/flight_escuadron.xml', 
        'views/flight_tipos_motores.xml',
        'views/flight_mision.xml',
        'views/flight_equipos_adicionales.xml',
        'views/flight_equipos.xml',
        
         
        
           
              
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ]
   
  
}
