from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView

from .role_permissions import IsFreelancer
from .serializers import FreelancerProfileViewSerializer, InternalFreelancerListSerializer
from .models import FreelancerProfile
from rest_framework.decorators import authentication_classes
import requests
from django.conf import settings
from .permissions.internal_service import IsInternalService

@api_view(["POST"])
@permission_classes([IsAuthenticated, IsFreelancer])
def freelancer_profile_add(request):

    if FreelancerProfile.objects.filter(
        user_id=request.user.id
    ).exists():

        return Response(
            {"error": "Profile already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    data = request.data.copy()
    data["user_id"] = request.user.id

    serializer = FreelancerProfileViewSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()

        return Response(
            {
                "message": "Profile created successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated, IsFreelancer])
def freelancer_profile_update(request):

    try:
        profile = FreelancerProfile.objects.get(
            user_id=request.user.id
        )

    except FreelancerProfile.DoesNotExist:

        return Response(
            {"error": "Profile not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = FreelancerProfileViewSerializer(
        profile,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():

        serializer.save()

        return Response(
            {
                "message": "Profile updated successfully",
                "data": serializer.data
            }
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsFreelancer])
def freelancer_profile_view(request):

    try:
        profile = FreelancerProfile.objects.get(
            user_id=request.user.id
        )

    except FreelancerProfile.DoesNotExist:

        return Response(
            {"error": "Profile not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    profile_data = FreelancerProfileViewSerializer(
        profile
    ).data

    # Fetch skills from Skill Service
    try:

        url = f"{settings.SKILL_SERVICE_URL}/api/internal/users/{request.user.id}/skills/"

        response = requests.get(
            url,
            headers={
                "X-Service-Key": settings.SERVICE_API_KEY
            },
            timeout=5
        )

        if response.status_code == 200:
            profile_data["skills"] = response.json()
        else:
            profile_data["skills"] = []

    except Exception:
        profile_data["skills"] = []

    return Response(
        profile_data,
        status=status.HTTP_200_OK
    )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated, IsFreelancer])
def freelancer_profile_delete(request):

    try:
        profile = FreelancerProfile.objects.get(
            user_id=request.user.id
        )

    except FreelancerProfile.DoesNotExist:

        return Response(
            {"error": "Profile not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    profile.delete()

    return Response(
        {
            "message": "Profile deleted successfully"
        },
        status=status.HTTP_200_OK
    )

@api_view(["PATCH"])

@authentication_classes([])
@permission_classes([IsInternalService])
def update_freelancer_rating(request, user_id):

    try:
        profile = FreelancerProfile.objects.get(
            user_id=user_id
        )

    except FreelancerProfile.DoesNotExist:
        return Response(
            {
                "error": "Freelancer profile not found"
            },
            status=status.HTTP_404_NOT_FOUND
        )

    average_rating = request.data.get(
        "average_rating"
    )

    total_reviews = request.data.get(
        "total_reviews"
    )

    if average_rating is not None:
        profile.average_rating = average_rating

    if total_reviews is not None:
        profile.total_reviews = total_reviews

    profile.save()

    return Response(
        {
            "message": "Rating updated successfully"
        },
        status=status.HTTP_200_OK
    )

class InternalFreelancerListView(APIView):
    authentication_classes = []
    permission_classes = [IsInternalService]

    def get(self, request):

        freelancers = FreelancerProfile.objects.all().order_by("-created_at")

        paginator = PageNumberPagination()
        paginator.page_size = 20

        page = paginator.paginate_queryset(
            freelancers,
            request
        )

        serializer = InternalFreelancerListSerializer(
            page,
            many=True
        )

        return paginator.get_paginated_response(
            serializer.data
        )