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
        # # new_copies = []
        # for copy in copies:
        #   copy.bookinfo = copy.book.as_dict()
        #   # copy.book_info = book_info
        #   # new_copies.push(copy)
        # copy_dicts = [c.as_dict() for c in copies]

        # print(copy_dicts)

        # print('these are the new copies', copies)
        # Run the data through the serializer
        data = CopyReadSerializer(copies, many=True).data
        # print('THIS IS THE DATA', data)
        # data_dicts = [{'id': c.id, 'book': c.book.as_dict(), 'owner': c.owner.id} for c in copies]
        print(data)

        return Response({'copies': data})

    def post(self, request):
        """Create request"""
        # Add user to request data object
        # request.data['owner'] = request.user.id
        print('this is the request', request.data['book'])
        # get_or_create() returns a tuple, (object, true if create/false if get) see below:
        # (<Book: The book 'The Stand' was written by Stephen King . It was published 1978 and is 1153 pages in length.(Fiction)>, False)
        # the_book = Book.objects.filter(isbn=request.data['book']['isbn']).get_or_create(request.data['book'])
        the_book = Book.objects.get_or_create(isbn=request.data['book']['isbn'], defaults=request.data['book'])
        # print('the_book return tuple', the_book)
        # LOOK at django method for finding if a record already exists, maybe create upon receiving error?
        if(the_book[1]):
          # if the copy was created, send a custom message about having added to the database
          copy = CopySerializer(data={"book": the_book[0].id, "owner": request.user.id})
          print('this is the new copy to send to db', copy)

          if copy.is_valid():
              copy.save()
              return Response({'copy': copy.data}, status=status.HTTP_201_CREATED)
          return Response(copy.errors, status=status.HTTP_400_BAD_REQUEST)
        # DO I EVEN NEED THE CODE BELOW??
        else:
          # if the copy was found, be like "we found it and added it"
          copy = CopySerializer(data={"book": the_book[0].id, "owner": request.user.id})
          print('this is the new book', copy)

          if copy.is_valid():
              copy.save()
              return Response({'copy': copy.data}, status=status.HTTP_201_CREATED)
          return Response(copy.errors, status=status.HTTP_400_BAD_REQUEST)


class CopyDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        print('this is the request', request)
        # Locate the copy to show
        copy = get_object_or_404(Copy, pk=pk)

        # the_book = copy.book.as_dict()

        # Run the data through the serializer so it's formatted
        data = CopyReadSerializer(copy).data
        # data['book'] = the_book
        return Response({'copy': data})

    # @user_passes_test(lambda u: u.is_superuser)
    def delete(self, request, pk):
        """Delete request"""
        # Locate book to delete
        copy = get_object_or_404(Copy, pk=pk)

        if(copy.owner.id == request.user.id):
          # Only delete if the user owns the  copy
          copy.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)
        else:
          raise PermissionDenied('Unauthorized, you do not have permission to delete this copy')
