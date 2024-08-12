from rest_framework import serializers
from .models import PayrollRun, Allowance, Deduction

class AllowanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allowance
        fields = '__all__'

class DeductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deduction
        fields = '__all__'

class PayrollRunSerializer(serializers.ModelSerializer):
    allowances = AllowanceSerializer(many=True, read_only=True)
    deductions = DeductionSerializer(many=True, read_only=True)

    class Meta:
        model = PayrollRun
        fields = '__all__'
