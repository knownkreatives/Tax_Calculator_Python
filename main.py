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
my_console = console.Console(color_system="auto", width=80)

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

def tax_bracket_selector(bands, rates, income, auto=False):
    if auto:
        for i in range(len(bands)):
            if (bands[i - 1] < income <= bands[i]) if i > 0 else income <= bands[i]:
                return i
        return len(bands) - 1
    
    my_console.print("Select the tax bracket:", style="bold green")
    for i in range(len(bands)):
        suggested = bands[i - 1] < income <= bands[i] if i > 0 else income <= bands[i]
        indicator = " *" if suggested else ""
        my_console.print(f"{i + 1}. Up to {bands[i]} at {rates[i]}% {indicator}")
    
    my_console.print("Selection: ")
    selection = int(my_console.input()) - 1
    return selection

def select_tax_system():
    while True:
        my_console.print("Select the tax system:", style="bold green")
        my_console.print("1. England")
        my_console.print("2. Scotland")
        my_console.print("3. USA")
        my_console.print("Selection: ")
        selection = int(my_console.input())

        if selection == 1:
            return tax_bands_eng_2627, tax_rates_eng_2627
        elif selection == 2:
            return tax_bands_sct_2627, tax_rates_sct_2627
        elif selection == 3:
            return tax_bands_usa_2627, tax_rates_usa_2627
        else:
            my_console.print("Invalid selection.", style="bold red")

        my_console.line()
    
def SingleTaxBracketCalculator():
    bands, rates = select_tax_system()

    my_console.print("Enter your income (salary):")
    income = float(my_console.input())
    my_console.line()

    bracket_index = tax_bracket_selector(bands, rates, income, auto=False)
    
    tax = _calculate_income_tax(income, rates[bracket_index], bands[bracket_index], 0)
    
    my_console.print(f"The tax on an income of {income} in the selected bracket is: {tax}")
    my_console.line()

def FullTaxBracketCalculator():
    bands, rates = select_tax_system()
    
    my_console.print("Enter your income (salary):")
    income = float(my_console.input())
    my_console.line()

    remainder = income
    total_tax = 0

    my_console.print(f"Tax breakdown for an income of {income}:", style="bold green")
    my_console.print(f"{'Bracket':<15}{'Taxable':<15}{'Rate':<15}{'Result':<15}", style="bold white")
    while remainder > 0:
        bracket_index = tax_bracket_selector(bands, rates, remainder, auto=True)
        low = 0 if bracket_index == 0 else bands[bracket_index - 1]

        taxed = _calculate_income_tax(remainder, rates[bracket_index], bands[bracket_index], low)
        taxable = _calculate_taxable_income(remainder, bands[bracket_index], low)
        
        my_console.print(f"{bracket_index + 1:<15}{taxable:<15.2f}{rates[bracket_index]:<15.2f}{taxed:<15.2f}")

        remainder -= taxable
        total_tax += taxed

    my_console.line()
    my_console.print(f"{'Total Tax':<45}{total_tax:<15.2f}")
    my_console.line()

def TakeHomePayBreakdown():
    bands, rates = select_tax_system()

    my_console.print("Enter your income (salary):")
    income = float(my_console.input())
    my_console.line()

    remainder = income
    total_tax = 0

    while remainder > 0:
        bracket_index = tax_bracket_selector(bands, rates, remainder, auto=True)
        low = 0 if bracket_index == 0 else bands[bracket_index - 1]

        taxed = _calculate_income_tax(remainder, rates[bracket_index], bands[bracket_index], low)

        remainder -= _calculate_taxable_income(remainder, bands[bracket_index], low)
        total_tax += taxed

    take_home_pay = income - total_tax
    my_console.print(f"Take-home pay breakdown for an income of {income:.2f}:", style="bold green")
    my_console.print(f"{' ':<15}{'Yearly':<15}{'Monthly':<15}{'Weekly':<15}{'Daily':<15}")
    my_console.print(f"{'Gross Pay':<15}{income:<15.2f}{income / 12:<15.2f}{income / 52:<15.2f}{income / 365:<15.2f}")
    my_console.print(f"{'Total Tax':<15}{total_tax:<15.2f}{total_tax / 12:<15.2f}{total_tax / 52:<15.2f}{total_tax / 365:<15.2f}")
    my_console.print(f"{'Net Pay':<15}{take_home_pay:<15.2f}{take_home_pay / 12:<15.2f}{take_home_pay / 52:<15.2f}{take_home_pay / 365:<15.2f}")
    my_console.line()

if __name__ == "__main__":
    my_console.print("Welcome to the Tax Calculator!", style="bold blue")
    
    while True:
        my_console.print("Please select the type of tax you want to calculate (Input '0' to exit):")
        my_console.print("1. Tax Bracket Calculator")
        my_console.print("2. Tax Bracket Breakdown")
        my_console.print("3. Take-Home Pay Breakdown")
        my_console.print("Selection: ")
        selection = int(my_console.input())

        if selection == 0:
            my_console.print("Exiting...", style="bold red")
            break
        else:
            my_console.line()

        if selection == 1:
            SingleTaxBracketCalculator()
        elif selection == 2:
            FullTaxBracketCalculator()
        elif selection == 3:
            TakeHomePayBreakdown()
        else:
            my_console.print("Invalid selection.", style="bold red")
    
    my_console.print("Thank you for using the Tax Calculator!")
