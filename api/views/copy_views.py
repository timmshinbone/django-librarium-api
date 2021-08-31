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
        the_book = Book.objects.filter(isbn=request.data['book']['isbn']).get_or_create(request.data['book'])
        print('made this in the db', the_book[0].id)
        # LOOK at django method for finding if a record already exists, maybe create upon receiving error?
        if(the_book[1]):
          copy = CopySerializer(data={"book": the_book[0].id, "owner": request.user.id})
          print('this is the new copy to send to db', copy)

          if copy.is_valid():
              copy.save()
              return Response({'copy': copy.data}, status=status.HTTP_201_CREATED)
          return Response(make_copy.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
          copy = CopySerializer(data={"book": the_book[0].id, "owner": request.user.id})
          print('this is the new book', copy)

          if copy.is_valid():
              copy.save()
              return Response({'copy': copy.data}, status=status.HTTP_201_CREATED)
          return Response(make_copy.errors, status=status.HTTP_400_BAD_REQUEST)
        #   if book.is_valid():
        #       book.save()


        #   copy = CopySerializer(data={"book": book.id, "owner": request.user.id})
        #   print('THE NEW COPY', copy)

        # Serialize/create copy
        # copy = CopySerializer(data=request.data)
        # print('this is the copy', copy)
        # If the copy data is valid according to our serializer...
        # if copy.is_valid():
            # Save the created copy & send a response
            # copy.save()
            # return Response({'copy': copy.data}, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        # return Response(copy.errors, status=status.HTTP_400_BAD_REQUEST)
