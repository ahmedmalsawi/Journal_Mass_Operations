{
    "name": "JOURNAL MASS Operations",
    "version": "19.0.0.0.0",
    "depends": ["account"],
    "summary": "Mass draft, post, cancel and print operations for journal entries",
    "category": "Accounting",
       "description": """
        Bulk manage journal entries with one click
        ==========================================
        
        Features:
        • Mass Set to Draft - Convert posted entries to draft
        • Mass Post Entries - Post multiple draft entries  
        • Mass Cancel - Cancel multiple entries
        • Mass Print - Generate PDF reports for multiple entries
        
        Compatible with Odoo 18 and 19.
    """,
    "author": "NEZAM ERP",
    "license": "LGPL-3",
        "author": "NEZAM ERP",
    "website": "https://www.nezamerp.com",
    "license": "OPL-1",
    "depends": ["account"],
    "data": [
        "views/account_move_views.xml",
    ],
    "images": [
        "static/description/img/1.png", 
        "static/description/img/nezamerp.png"  
    ],
    "installable": True,
    "application": False,
    "price": 1,
    "currency": "USD",
    "support": "admin@nezamerp.com",
}
