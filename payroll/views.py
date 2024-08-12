from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from weasyprint import HTML
from django.db.models import Sum
from .models import PayrollRun, Employee, Company
from .serializers import PayrollRunSerializer



class PayrollRunViewSet(viewsets.ModelViewSet):
    queryset = PayrollRun.objects.all()
    serializer_class = PayrollRunSerializer

    @action(detail=True, methods=['post'])
    def process_payroll(self, request, pk=None):
        try:
            # Retrieve the employee by primary key (pk)
            employee = get_object_or_404(Employee, pk=pk)

            # Create a PayrollRun instance with the employee's salary as the gross pay
            payroll_run = PayrollRun.objects.create(employee=employee, gross_pay=employee.salary)

            # Calculate the net pay and other deductions
            payroll_run.calculate_net_pay()

            # Serialize the payroll run data and return it as a response
            serializer = self.get_serializer(payroll_run)
            return Response(serializer.data)

        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=404)

    @action(detail=False, methods=['get'])
    def calculate_all_payrolls(self, request):
        # Calculate payroll for all employees
        payroll_runs = []
        for employee in Employee.objects.all():
            payroll_run = PayrollRun.objects.create(employee=employee, gross_pay=employee.salary)
            payroll_run.calculate_net_pay()
            payroll_runs.append(payroll_run)

        serializer = self.get_serializer(payroll_runs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def generate_payslip(self, request, pk=None):
        # Generate payslip for a specific employee's payroll run
        payroll_run = get_object_or_404(PayrollRun, pk=pk)
        employee = payroll_run.employee

        # Calculate total to date figures
        total_gross_pay_to_date = PayrollRun.objects.filter(employee=employee).aggregate(Sum('gross_pay'))['gross_pay__sum']
        total_tax_to_date = PayrollRun.objects.filter(employee=employee).aggregate(Sum('tax_deduction'))['tax_deduction__sum']
        total_ni_to_date = PayrollRun.objects.filter(employee=employee).aggregate(Sum('ni_deduction'))['ni_deduction__sum']
        total_pension_to_date = PayrollRun.objects.filter(employee=employee).aggregate(Sum('pension_contribution'))['pension_contribution__sum']
        total_other_deductions_to_date = PayrollRun.objects.filter(employee=employee).aggregate(Sum('other_deductions'))['other_deductions__sum']
        total_net_pay_to_date = PayrollRun.objects.filter(employee=employee).aggregate(Sum('net_pay'))['net_pay__sum']

        # Add the totals to the context
        context = {
            'employee': employee,
            'payroll_run': payroll_run,
            'company': employee.company,
            'total_gross_pay_to_date': total_gross_pay_to_date or 0,
            'total_tax_to_date': total_tax_to_date or 0,
            'total_ni_to_date': total_ni_to_date or 0,
            'total_pension_to_date': total_pension_to_date or 0,
            'total_other_deductions_to_date': total_other_deductions_to_date or 0,
            'total_net_pay_to_date': total_net_pay_to_date or 0,
        }

        # Render the template with the context
        html_string = render_to_string('payslip_template.html', context)
        html = HTML(string=html_string)
        pdf_file = html.write_pdf()

        # Optionally save or email the PDF
        pdf_path = f'payslips/{employee.id}_{payroll_run.date}.pdf'
        with open(pdf_path, 'wb') as f:
            f.write(pdf_file)

        return Response({"message": "Payslip generated successfully", "payslip_path": pdf_path})


def generate_company_summary(company, run_date):
    payroll_runs = PayrollRun.objects.filter(employee__company=company, date=run_date)
    total_gross = sum(pr.gross_pay for pr in payroll_runs)
    total_tax = sum(pr.tax_deduction for pr in payroll_runs)
    total_ni = sum(pr.ni_deduction for pr in payroll_runs)
    total_pension = sum(pr.pension_contribution for pr in payroll_runs)
    total_deductions = sum(pr.total_deductions for pr in payroll_runs)
    total_net = sum(pr.net_pay for pr in payroll_runs)

    context = {
        'company': company,
        'run_date': run_date,
        'total_gross': total_gross,
        'total_tax': total_tax,
        'total_ni': total_ni,
        'total_pension': total_pension,
        'total_deductions': total_deductions,
        'total_net': total_net,
    }

    html_string = render_to_string('company_summary_template.html', context)
    html = HTML(string=html_string)
    pdf_file = html.write_pdf()

    # Save or send the summary PDF as needed
    with open(f'summaries/{company.id}_{run_date}.pdf', 'wb') as f:
        f.write(pdf_file)
