from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .permissions import IsFreelancer
from .serializers import FreelancerProfileViewSerializer
from .models import FreelancerProfile


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsFreelancer])
def freelancer_profile_add(request):

    # Prevent duplicate profile
    if FreelancerProfile.objects.filter(user_id=request.user.id).exists():
        return Response(
            {"error": "Profile already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        data = request.data.copy()

        # Get user_id securely from JWT
        data["user_id"] = request.user.id

        serializer = FreelancerProfileViewSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Profile added successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    except Exception as e:
        print("🔥 ERROR:", e)

        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated, IsFreelancer])
def freelancer_profile_update(request):

    user_id = request.user.id

    try:
        profile = FreelancerProfile.objects.get(user_id=user_id)

    except FreelancerProfile.DoesNotExist:
        return Response(
            {"error": "Profile not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = FreelancerProfileViewSerializer(
        instance=profile,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()

        return Response(
            {
                "message": "Profile updated successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )



@api_view(["GET"])
@permission_classes([IsAuthenticated, IsFreelancer])
def freelancer_profile_view(request):

    user_id = request.user.id

    try:
        profile = FreelancerProfile.objects.get(user_id=user_id)

    except FreelancerProfile.DoesNotExist:
        return Response(
            {"error": "Profile not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = FreelancerProfileViewSerializer(profile)

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )



@api_view(["DELETE"])
@permission_classes([IsAuthenticated, IsFreelancer])
def freelancer_profile_delete(request):

    user_id = request.user.id

    try:
        profile = FreelancerProfile.objects.get(user_id=user_id)

    except FreelancerProfile.DoesNotExist:
        return Response(
            {"error": "Profile not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    profile.delete()

    return Response(
        {"message": "Profile deleted successfully"},
        status=status.HTTP_200_OK
    )