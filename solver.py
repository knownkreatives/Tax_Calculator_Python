import math

def _calculate_general_tax(income, percentage):
    return math.ceil(income * percentage / 100)

def _calculate_taxable_income(income, high, low):
    taxable = min(income, high) - low

    if taxable < 0:
        return 0
    
    return taxable

def _calculate_income_tax(income, percentage, high, low):
    taxable = _calculate_taxable_income(income, high, low)
    
    return _calculate_general_tax(taxable, percentage)