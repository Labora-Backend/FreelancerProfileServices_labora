from rest_framework import serializers
from .models import FreelancerProfile

class FreelancerProfileViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreelancerProfile
        fields = "__all__"
        # read_only_fields = (
        #     "user_id",
        #     "is_verified",
        #     "is_active",
        #     "created_at",
        #     "updated_at",
        #     "last_seen",
        #     "total_jobs_completed",
        #     "average_rating",
        # )

class InternalFreelancerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = FreelancerProfile
        fields = [
            "user_id",
            "full_name",
            "title",
            "hourly_rate",
            "profile_image",
            "created_at",
        ]