from calendar import c

import rich.console as console
import math

MAX_INCOME = 1e12
tax_bands_eng_2627 = [
    12570, 50270, 150000, MAX_INCOME
]
tax_rates_eng_2627 = [
    0, 20, 40, 45
]
tax_bands_sct_2627 = [
    12570, 14585, 25295, 43430, 150000, MAX_INCOME
]
tax_rates_sct_2627 = [
    0, 19, 20, 21, 41, 46
]
tax_bands_usa_2627 = [
    10275, 41775, 89075, 170050, 215950, 539900, MAX_INCOME
]
tax_rates_usa_2627 = [
    10, 12, 22, 24, 32, 35, 37
]
printer = console.Console(color_system="auto", width=80)

def _calculate_general_tax(income, percentage):
    return math.ceil(income * percentage / 100)

def GeneralTaxCalculator():
    printer.print("Enter your income (salary): ")
    income = float(input())
    print()

    printer.print("Enter the tax percentage: ")
    percentage = float(input())
    print()

    tax = _calculate_general_tax(income, percentage)
    printer.print(f"The general tax on an income of {income} at a rate of {percentage}% is: {tax}")
    print()

def _calculate_taxable_income(income, high, low):
    taxable = min(income, high) - low

    if taxable < 0:
        return 0
    
    return taxable

def _calculate_income_tax(income, percentage, high, low):
    taxable = _calculate_taxable_income(income, high, low)
    
    return _calculate_general_tax(taxable, percentage)


def _select_tax_bracket(bands, rates, income, auto=False):
    if auto:
        for i in range(len(bands)):
            if (bands[i - 1] < income <= bands[i]) if i > 0 else income <= bands[i]:
                return i
        return len(bands) - 1
    
    printer.print("Select the tax bracket:", style="bold green")
    for i in range(len(bands)):
        suggested = bands[i - 1] < income <= bands[i] if i > 0 else income <= bands[i]
        indicator = " *" if suggested else ""
        printer.print(f"{i + 1}. Up to {bands[i]} at {rates[i]}% {indicator}")
    
    selection = int(input()) - 1
    return selection

def _select_system():
    printer.print("Select the tax system:", style="bold green")
    printer.print("1. England")
    printer.print("2. Scotland")
    printer.print("3. USA")
    selection = int(input())
    print()

    if selection == 1:
        return tax_bands_eng_2627, tax_rates_eng_2627
    elif selection == 2:
        return tax_bands_sct_2627, tax_rates_sct_2627
    elif selection == 3:
        return tax_bands_usa_2627, tax_rates_usa_2627
    else:
        printer.print("Invalid selection.", style="bold red")
        return None, None
    
def SingleTaxBracketCalculator():
    bands, rates = _select_system()

    printer.print("Enter your income (salary):")
    income = float(input())
    print()

    bracket_index = _select_tax_bracket(bands, rates, income, auto=False)
    
    tax = _calculate_income_tax(income, rates[bracket_index], bands[bracket_index], 0)
    
    printer.print(f"The tax on an income of {income} in the selected bracket is: {tax}")
    print()

def _full_tax_calculator(income, bands, rates):
    remainder = income
    total_tax = 0

    while remainder > 0:
        bracket_index = _select_tax_bracket(bands, rates, remainder, auto=True)
        low = 0 if bracket_index == 0 else bands[bracket_index - 1]

        taxed = _calculate_income_tax(remainder, rates[bracket_index], bands[bracket_index], low)
        
        remainder -= _calculate_taxable_income(remainder, bands[bracket_index], low)
        total_tax += taxed

    return total_tax

def FullTaxBracketCalculator():
    bands, rates = _select_system()
    
    printer.print("Enter your income (salary):")
    income = float(input())
    print()

    total_tax = _full_tax_calculator(income, bands, rates)

    printer.print(f"The total tax on an income of {income} is: {total_tax}")
    print()

def TakeHomePayBreakdown():
    bands, rates = _select_system()

    printer.print("Enter your income (salary):")
    income = float(input())
    print()

    total_tax = _full_tax_calculator(income, bands, rates)

    take_home_pay = income - total_tax
    printer.print(f"Take-home pay breakdown for an income of {income}:", style="bold green")
    printer.print(f"{' ':<15}{'Yearly':<15}{'Monthly':<15}{'Weekly':<15}{'Daily':<15}")
    printer.print(f"{'Gross Pay':<15}{income:<15.2f}{income / 12:<15.2f}{income / 52:<15.2f}{income / 365:<15.2f}")
    printer.print(f"{'Total Tax':<15}{total_tax:<15.2f}{total_tax / 12:<15.2f}{total_tax / 52:<15.2f}{total_tax / 365:<15.2f}")
    printer.print(f"{'Net Pay':<15}{take_home_pay:<15.2f}{take_home_pay / 12:<15.2f}{take_home_pay / 52:<15.2f}{take_home_pay / 365:<15.2f}")
    print()


if __name__ == "__main__":
    printer.print("Welcome to the Tax Calculator!", style="bold blue")
    print()
    printer.print("Please select the type of tax you want to calculate:")
    printer.print("1. General Tax")
    printer.print("2. Single Tax Bracket")
    printer.print("3. Full Tax Bracket")
    printer.print("4. Take-Home Pay Breakdown")
    selection = int(input())
    print()

    if selection == 1:
        GeneralTaxCalculator()
    elif selection == 2:
        SingleTaxBracketCalculator()
    elif selection == 3:
        FullTaxBracketCalculator()
    elif selection == 4:
        TakeHomePayBreakdown()
    else:
        printer.print("Invalid selection.", style="bold red")
    
    printer.print("Thank you for using the Tax Calculator!")
