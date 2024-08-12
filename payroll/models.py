from django.db import models
from employees.models import Employee, Company

class TaxBand(models.Model):
    lower_limit = models.DecimalField(max_digits=10, decimal_places=2)
    upper_limit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rate = models.DecimalField(max_digits=5, decimal_places=2)  # Represented as a percentage
    effective_date = models.DateField()  # Date from which this rate is effective

    def __str__(self):
        if self.upper_limit:
            return f"{self.rate}% on income between £{self.lower_limit} and £{self.upper_limit}"
        else:
            return f"{self.rate}% on income above £{self.lower_limit}"


class NIContributionRate(models.Model):
    lower_threshold = models.DecimalField(max_digits=10, decimal_places=2)
    upper_threshold = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rate = models.DecimalField(max_digits=5, decimal_places=2)  # Represented as a percentage
    effective_date = models.DateField()  # Date from which this rate is effective

    def __str__(self):
        if self.upper_threshold:
            return f"{self.rate}% on earnings between £{self.lower_threshold} and £{self.upper_threshold}"
        else:
            return f"{self.rate}% on earnings above £{self.lower_threshold}"


class PensionContributionRate(models.Model):
    contribution_rate = models.DecimalField(max_digits=5, decimal_places=2)  # Represented as a percentage
    is_auto_enrolled = models.BooleanField(default=False)  # Indicates if this rate is for auto-enrolled employees
    effective_date = models.DateField()  # Date from which this rate is effective

    def __str__(self):
        return f"Pension Contribution: {self.contribution_rate}% {'(Auto-enrolled)' if self.is_auto_enrolled else ''}"


class Allowance(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    effective_date = models.DateField()  # Date from which this rate is effective

    def __str__(self):
        return self.name


class Deduction(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    effective_date = models.DateField()  # Date from which this rate is effective

    def __str__(self):
        return self.name


class PayrollRun(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    gross_pay = models.DecimalField(max_digits=10, decimal_places=2)
    total_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_pay = models.DecimalField(max_digits=10, decimal_places=2)
    tax_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ni_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pension_contribution = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    allowances = models.ManyToManyField(Allowance, blank=True)
    deductions = models.ManyToManyField(Deduction, blank=True)

    def calculate_tax(self):
        taxable_income = max(0, self.gross_pay - self.get_personal_allowance())  # Assuming get_personal_allowance() is defined
        total_tax = 0

        tax_bands = TaxBand.objects.all().order_by('lower_limit')

        for band in tax_bands:
            if band.upper_limit:
                if taxable_income > band.lower_limit:
                    income_in_band = min(taxable_income, band.upper_limit) - band.lower_limit
                    total_tax += income_in_band * (band.rate / 100)
            else:
                total_tax += (taxable_income - band.lower_limit) * (band.rate / 100)

        self.tax_deduction = total_tax
        return total_tax

    def calculate_ni(self):
        ni_deduction = 0

        ni_rates = NIContributionRate.objects.all().order_by('lower_threshold')

        for rate in ni_rates:
            if rate.upper_threshold:
                if self.gross_pay > rate.lower_threshold:
                    earnings_in_band = min(self.gross_pay, rate.upper_threshold) - rate.lower_threshold
                    ni_deduction += earnings_in_band * (rate.rate / 100)
            else:
                ni_deduction += (self.gross_pay - rate.lower_threshold) * (rate.rate / 100)

        self.ni_deduction = ni_deduction
        return ni_deduction

    def calculate_pension(self):
        pension_rate = PensionContributionRate.objects.filter(is_auto_enrolled=True).first()

        if pension_rate:
            self.pension_contribution = self.gross_pay * (pension_rate.contribution_rate / 100)
        else:
            self.pension_contribution = 0

        return self.pension_contribution

    def calculate_other_deductions(self):
        sick_leave_deduction = 50  # Example value
        holiday_deduction = 30  # Example value
        bank_holiday_deduction = 20  # Example value

        self.other_deductions += sick_leave_deduction + holiday_deduction + bank_holiday_deduction
        return self.other_deductions

    def calculate_net_pay(self):
        self.calculate_tax()
        self.calculate_ni()
        self.calculate_pension()
        self.calculate_other_deductions()
        self.total_deductions = self.tax_deduction + self.ni_deduction + self.pension_contribution + self.other_deductions
        self.net_pay = self.gross_pay - self.total_deductions
        self.save()

    def __str__(self):
        return f"Payroll for {self.employee} on {self.date} - Gross: £{self.gross_pay}, Net: £{self.net_pay}"


class PayrollRunTotals(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    run_date = models.DateField(auto_now_add=True)
    total_gross_pay = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_ni = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_pension = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_deductions = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_net_pay = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def calculate_totals(self):
        payroll_runs = PayrollRun.objects.filter(employee__company=self.company, date=self.run_date)
        self.total_gross_pay = sum(pr.gross_pay for pr in payroll_runs)
        self.total_tax = sum(pr.tax_deduction for pr in payroll_runs)
        self.total_ni = sum(pr.ni_deduction for pr in payroll_runs)
        self.total_pension = sum(pr.pension_contribution for pr in payroll_runs)
        self.total_deductions = sum(pr.total_deductions for pr in payroll_runs)
        self.total_net_pay = sum(pr.net_pay for pr in payroll_runs)
        self.save()

    def __str__(self):
        return f"Payroll Run for {self.company.name} on {self.run_date}"
