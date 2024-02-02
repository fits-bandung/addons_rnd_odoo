# -*- coding: utf-8 -*-
# from odoo import http


# class FitsPph21Pasal58(http.Controller):
#     @http.route('/fits_pph21_pasal58/fits_pph21_pasal58', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fits_pph21_pasal58/fits_pph21_pasal58/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('fits_pph21_pasal58.listing', {
#             'root': '/fits_pph21_pasal58/fits_pph21_pasal58',
#             'objects': http.request.env['fits_pph21_pasal58.fits_pph21_pasal58'].search([]),
#         })

#     @http.route('/fits_pph21_pasal58/fits_pph21_pasal58/objects/<model("fits_pph21_pasal58.fits_pph21_pasal58"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fits_pph21_pasal58.object', {
#             'object': obj
#         })
