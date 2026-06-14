from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .permissions import IsFreelancer
from .serializers import FreelancerProfileViewSerializer
from .models import FreelancerProfile

import requests
from django.conf import settings


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

        response = requests.get(
            f"{settings.SKILL_SERVICE_URL}/internal/users/{request.user.id}/skills/",
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