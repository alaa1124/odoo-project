# -*- coding: utf-8 -*-
# Author: test
#NOTE# example: only team members that worked on the Module [remove comment in final]
{
    'name': "test manufacturing route",
    
    'summary': 'SO PO Edits',
    'author': "Alaa Rabie",
    'company': '',
    'website': "",
    'version': '17.0',
    'category': 'Purchase',
    'license': 'AGPL-3',
    'sequence': 1,



    # any module necessary for this one to work correctly
    'depends': ['base',
                'mrp',
                'mrp_account',
                'stock',
                'product'
    ],
    
    # always loaded
    'data': [
        
        #  data -----------------------------
            # "data/sequence.xml",
        # security rules ----------------------------
            # "security/sale_order_security.xml",
            # "security/ir.model.access.csv",
        
        #  views -----------------------------
            #"views/prodcuct_template.xml",
        #  wizards -----------------------------
            # "wizards/template_template_add_template_view.xml",
        
        #  report -----------------------------

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}