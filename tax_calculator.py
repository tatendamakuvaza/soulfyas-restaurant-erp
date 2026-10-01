"""
Zimbabwe Tax & Statutory Payroll Calculation Engine for Soulfyas Quality Restaurant ERP
Calculates PAYE, AIDS Levy, NSSA POBS, NSSA APWCS, VAT, and IMTT in accordance with ZIMRA and NSSA regulations.
"""

def calculate_paye(monthly_gross: float) -> dict:
    """
    Calculates monthly PAYE and AIDS levy based on official progressive tax brackets.
    """
    taxable = max(0.0, float(monthly_gross))
    
    # Statutory USD monthly tax bands
    if taxable <= 100.0:
        base_paye = 0.0
    elif taxable <= 300.0:
        base_paye = (taxable - 100.0) * 0.20
    elif taxable <= 1000.0:
        base_paye = 40.0 + (taxable - 300.0) * 0.25
    elif taxable <= 2000.0:
        base_paye = 215.0 + (taxable - 1000.0) * 0.30
    elif taxable <= 3000.0:
        base_paye = 515.0 + (taxable - 2000.0) * 0.35
    else:
        base_paye = 865.0 + (taxable - 3000.0) * 0.40
        
    aids_levy = base_paye * 0.03
    total_tax = base_paye + aids_levy
    effective_rate = (total_tax / taxable * 100.0) if taxable > 0 else 0.0
    
    return {
        'taxable_income': round(taxable, 2),
        'base_paye': round(base_paye, 2),
        'aids_levy': round(aids_levy, 2),
        'total_paye': round(total_tax, 2),
        'effective_rate': round(effective_rate, 2)
    }

def calculate_nssa(monthly_gross: float, ceiling: float = 700.0) -> dict:
    """
    Calculates NSSA POBS (4.5% employee / 4.5% employer) and APWCS (1.4% employer only).
    """
    gross = max(0.0, float(monthly_gross))
    insurable = min(gross, ceiling)
    
    employee_pobs = insurable * 0.045
    employer_pobs = insurable * 0.045
    employer_apwcs = gross * 0.014  # APWCS applies to total earnings
    
    return {
        'insurable_earnings': round(insurable, 2),
        'employee_pobs': round(employee_pobs, 2),
        'employer_pobs': round(employer_pobs, 2),
        'total_pobs': round(employee_pobs + employer_pobs, 2),
        'employer_apwcs': round(employer_apwcs, 2),
        'total_nssa_remittance': round(employee_pobs + employer_pobs + employer_apwcs, 2)
    }

def compute_employee_payslip(employee_name: str, employee_no: str, gross_salary: float, allowances: float = 0.0, other_deductions: float = 0.0) -> dict:
    """
    Generates a full statutory net pay and breakdown calculation for an employee.
    """
    total_earnings = gross_salary + allowances
    nssa = calculate_nssa(total_earnings)
    paye = calculate_paye(total_earnings - nssa['employee_pobs'])  # NSSA employee is tax deductible
    
    total_employee_deductions = paye['total_paye'] + nssa['employee_pobs'] + other_deductions
    net_pay = total_earnings - total_employee_deductions
    total_employer_cost = total_earnings + nssa['employer_pobs'] + nssa['employer_apwcs']
    
    return {
        'employee_name': employee_name,
        'employee_no': employee_no,
        'basic_salary': round(gross_salary, 2),
        'allowances': round(allowances, 2),
        'gross_earnings': round(total_earnings, 2),
        'nssa_employee': nssa['employee_pobs'],
        'nssa_employer': nssa['employer_pobs'],
        'nssa_apwcs': nssa['employer_apwcs'],
        'base_paye': paye['base_paye'],
        'aids_levy': paye['aids_levy'],
        'total_paye': paye['total_paye'],
        'other_deductions': round(other_deductions, 2),
        'total_deductions': round(total_employee_deductions, 2),
        'net_pay': round(net_pay, 2),
        'total_employer_cost': round(total_employer_cost, 2)
    }

def calculate_imtt(amount: float, rate: float = 0.02, min_threshold: float = 10.0, max_cap: float = 10000.0) -> float:
    """
    Calculates Intermediated Money Transfer Tax (IMTT).
    """
    if amount < min_threshold:
        return 0.0
    imtt = amount * rate
    return round(min(imtt, max_cap), 2)

def calculate_vat(amount_exclusive: float, vat_rate: float = 0.15) -> dict:
    """
    Calculates ZIMRA Standard Rated 15% VAT.
    """
    vat_amt = round(amount_exclusive * vat_rate, 2)
    total_inclusive = round(amount_exclusive + vat_amt, 2)
    return {
        'exclusive': round(amount_exclusive, 2),
        'vat_amount': vat_amt,
        'inclusive': total_inclusive,
        'rate_percentage': round(vat_rate * 100, 1)
    }
