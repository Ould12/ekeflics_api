# serializers.py
from rest_framework import serializers
from .models import ViewingStatistics, ContentPerformance, UserEngagement, Content

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'title', 'content_type']

class ViewingStatisticsSerializer(serializers.ModelSerializer):
    content = ContentSerializer()

    class Meta:
        model = ViewingStatistics
        fields = ['user', 'content', 'view_date', 'duration_seconds']

class ContentPerformanceSerializer(serializers.ModelSerializer):
    content = ContentSerializer()

    class Meta:
        model = ContentPerformance
        fields = ['content', 'views_count', 'average_duration']

class UserEngagementSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserEngagement
        fields = ['user', 'total_views', 'total_duration']
