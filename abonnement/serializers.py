from datetime import date
from rest_framework import serializers
from .models import Subscription, SubscriptionPlan
from dateutil.relativedelta import relativedelta

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'name', 'description', 'price', 'duration_months']

class SubscriptionSerializer(serializers.ModelSerializer):
    plan = serializers.PrimaryKeyRelatedField(queryset=SubscriptionPlan.objects.all())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    end_date = serializers.DateField(read_only=True)  # Mark as read-only

    class Meta:
        model = Subscription
        fields = ['user', 'plan', 'start_date', 'end_date', 'is_active', 'billing_history']

    def create(self, validated_data):
        plan = validated_data['plan']
        user = validated_data['user']
        start_date = validated_data.get('start_date', date.today())
        end_date = start_date + relativedelta(months=plan.duration_months)

        subscription = Subscription.objects.create(
            user=user,
            plan=plan,
            start_date=start_date,
            end_date=end_date,
            is_active=True,
            billing_history={}
        )
        return subscription
