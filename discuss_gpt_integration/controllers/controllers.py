# -*- coding: utf-8 -*-
# from odoo import http


# class DiscussGptIntegration(http.Controller):
#     @http.route('/discuss_gpt_integration/discuss_gpt_integration', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/discuss_gpt_integration/discuss_gpt_integration/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('discuss_gpt_integration.listing', {
#             'root': '/discuss_gpt_integration/discuss_gpt_integration',
#             'objects': http.request.env['discuss_gpt_integration.discuss_gpt_integration'].search([]),
#         })

#     @http.route('/discuss_gpt_integration/discuss_gpt_integration/objects/<model("discuss_gpt_integration.discuss_gpt_integration"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('discuss_gpt_integration.object', {
#             'object': obj
#         })

