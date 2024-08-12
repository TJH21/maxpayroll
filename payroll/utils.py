import csv
from .models import PayrollRun

def export_to_csv(company, run_date):
    payroll_runs = PayrollRun.objects.filter(employee__company=company, date=run_date)
    summary_data = {
        'total_gross': sum(pr.gross_pay for pr in payroll_runs),
        'total_tax': sum(pr.tax_deduction for pr in payroll_runs),
        'total_ni': sum(pr.ni_deduction for pr in payroll_runs),
        'total_pension': sum(pr.pension_contribution for pr in payroll_runs),
        'total_deductions': sum(pr.total_deductions for pr in payroll_runs),
        'total_net': sum(pr.net_pay for pr in payroll_runs),
    }

    with open(f'ledger_exports/{company.id}_{run_date}.csv', 'w', newline='') as csvfile:
        fieldnames = ['total_gross', 'total_tax', 'total_ni', 'total_pension', 'total_deductions', 'total_net']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow(summary_data)
