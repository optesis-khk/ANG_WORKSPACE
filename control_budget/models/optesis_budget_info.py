from odoo import fields, models

class OptesisBudgetInfo(models.TransientModel):
    _name = "optesis.budget.info"

    id_crossovered_budget_line = fields.Integer()
    engage_amount = fields.Float(digits=0)
    available_amount = fields.Float(digits=0)
    planned_amount = fields.Float(digit=0)
