from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view

from modules.review.serializers import ReviewSerializer
from modules.review.models import Review

# Create your views here.
#@api_view(['GET'])
def review_list(request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)

    #return Response(serializer.data)
    return JsonResponse({
        'data': serializer.data
    })

#@api_view(['GET'])
def current_review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    serializer = ReviewSerializer(review)

    #return Response(serializer.data)
    return JsonResponse({
        'data': serializer.data
    })
