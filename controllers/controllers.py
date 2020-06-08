# -*- coding: utf-8 -*-
# from odoo import http


# class Flight(http.Controller):
#     @http.route('/flight/flight/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/flight/flight/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('flight.listing', {
#             'root': '/flight/flight',
#             'objects': http.request.env['flight.flight'].search([]),
#         })

#     @http.route('/flight/flight/objects/<model("flight.flight"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('flight.object', {
#             'object': obj
#         })
