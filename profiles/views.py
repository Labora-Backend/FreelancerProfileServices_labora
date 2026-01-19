from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from .serializers import FreelancerProfileViewSerializer
from .models import FreelancerProfile

@api_view(["POST"])
@permission_classes([AllowAny])
def freelancer_profile_add(request):
    try:

        serializer = FreelancerProfileViewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile added"}, status=201)
        return Response(serializer.errors, status=400)

    except Exception as e:
        print("🔥 ERROR:", e)
        return Response({"error": str(e)}, status=500)


@api_view(["PUT", "PATCH"])
@permission_classes([AllowAny])
def freelancer_profile_update(request):
    user_id =request.data.get("user_id")


    try:
        profile = FreelancerProfile.objects.get(user_id=user_id)
    except FreelancerProfile.DoesNotExist:
        return Response(
            {"error": "Profile not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer=FreelancerProfileViewSerializer(instance=profile,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"profile updated"},status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def freelancer_profile_view(request):

    user_id = request.query_params.get("user_id")
    print(user_id)

    if not user_id:
        return Response(
            {"error": "user_id is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        profile = FreelancerProfile.objects.get(user_id=user_id)
    except FreelancerProfile.DoesNotExist:
        return Response(
            {"error": "Profile not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = FreelancerProfileViewSerializer(profile)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([AllowAny])
def freelancer_profile_delete(request):
    user_id = request.data.get("user_id")

    try:
        profile = FreelancerProfile.objects.get(user_id=user_id)
    except FreelancerProfile.DoesNotExist:
        return Response( {"error": "Profile not found"})

    profile.delete()
    return Response(
        {"message": "Profile deleted successfully"},
        status=status.HTTP_204_NO_CONTENT
    )

