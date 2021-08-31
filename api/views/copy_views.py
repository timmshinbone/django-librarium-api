from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test

from ..models.book import Book
from ..serializers import BookSerializer
from ..models.copy import Copy
from ..serializers import CopySerializer, CopyReadSerializer


class Copies(generics.ListCreateAPIView):
    serializer_class = CopySerializer

    def get(self, request):
        """Index request"""
        # Get all the copies:
        copies = Copy.objects.all()
        # print('THE COPIES', copies)
        # for copy in copies:
        #   the_book = copy.book.as_dict()
        #   copy.the_book = the_book
        #   print(copy.the_book)

        # Run the data through the serializer
        data = CopyReadSerializer(copies, many=True).data
        # print('THIS IS THE DATA', data)
        return Response({'copies': data})

    def post(self, request):
        """Create request"""
        # Add user to request data object
        # request.data['owner'] = request.user.id
        print('this is the request', request.data['book'])
        # get or create returns a tuple, (object, true if new, false if exists) see below:
        # (<Book: The book 'The Stand' was written by Stephen King . It was published 1978 and is 1153 pages in length.(Fiction)>, False)
        the_book = Book.objects.filter(isbn=request.data['book']['isbn']).get_or_create(request.data['book'])
        print('the_book return tuple', the_book)
        # LOOK at django method for finding if a record already exists, maybe create upon receiving error?
        if(the_book[1]):
          copy = CopySerializer(data={"book": the_book[0].id, "owner": request.user.id})
          # print('this is the new copy to send to db', copy)

          if copy.is_valid():
              copy.save()
              return Response({'copy': copy.data}, status=status.HTTP_201_CREATED)
          return Response(make_copy.errors, status=status.HTTP_400_BAD_REQUEST)
        # DO I EVEN NEED THE CODE BELOW??
        else:
          copy = CopySerializer(data={"book": the_book[0].id, "owner": request.user.id})
          print('this is the new book', copy)

          if copy.is_valid():
              copy.save()
              return Response({'copy': copy.data}, status=status.HTTP_201_CREATED)
          return Response(make_copy.errors, status=status.HTTP_400_BAD_REQUEST)
