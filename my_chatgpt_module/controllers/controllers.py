# -*- coding: utf-8 -*-
# from odoo import http


# class MyChatgptModule(http.Controller):
#     @http.route('/my_chatgpt_module/my_chatgpt_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/my_chatgpt_module/my_chatgpt_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('my_chatgpt_module.listing', {
#             'root': '/my_chatgpt_module/my_chatgpt_module',
#             'objects': http.request.env['my_chatgpt_module.my_chatgpt_module'].search([]),
#         })

#     @http.route('/my_chatgpt_module/my_chatgpt_module/objects/<model("my_chatgpt_module.my_chatgpt_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('my_chatgpt_module.object', {
#             'object': obj
#         })

