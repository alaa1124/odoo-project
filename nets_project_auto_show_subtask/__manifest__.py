# -*- coding: utf-8 -*-
# Author: Moaz Mabrouk
{
    'name': "Nets",
    
    'summary':"""        
        Project:  Show Subtask
    """,
        
    'description': """
        - Project: Show Subtask
    """,

    'author': "Net Stream Technologies L.L.C",
    'website': "https://www.netstream-me.com",

    # 'local_company': "nets",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'customizations',
    'version': '17.0.1.0',
    'license': 'OPL-1',    
    # any module necessary for this one to work correctly
    'depends': ['base','project'],
    
    # always loaded

    'data': [
        
        #  data -----------------------------
           # "data/mail_data.xml",
        # security rules ----------------------------
            # "security/sale_order_security.xml",
            # "security/ir.model.access.csv",
        
        #  views -----------------------------
            # "views/project_project_view.xml",
            # "views/project_task_view.xml",
            # "views/project_task_type_view.xml",

        # load SCSS & JS Backend -----------------------------
            # 'views/assets_load/assets_backend.xml',
        
        #  wizards -----------------------------
            # "wizards/analytical_tag_view.xml",
        
        #  report -----------------------------

    ],
    'qweb': [],
    'demo': [],
    'test': [],
    'css': [],
    'js': [],
    'images': [],
        
    'installable': True,
    'application': False,
    'auto_install': False,
}
