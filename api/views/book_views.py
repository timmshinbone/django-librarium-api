from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test

from ..models.book import Book
from ..serializers import BookSerializer

# Create your views here.
class Books(APIView):
    serializer_class = BookSerializer
    def get(self, request):
        """Index request"""
        # Get all the books:
        books = Book.objects.all()

        # Run the data through the serializer
        data = BookSerializer(books, many=True).data
        return Response({ 'books': data })

class BookCreate(generics.ListCreateAPIView):
    def post(self, request):
      # ##################
      # ADD CUSTOM REROUTER TO CREATE COPY IF BOOK ALREADY EXISTS
      # ##################
        """Create request"""
        # Serialize/create book
        book = BookSerializer(data=request.data['book'])
        # If the mango data is valid according to our serializer...
        if book.is_valid():
            # Save the created book & send a response
            book.save()
            return Response({ 'book': book.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(book.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        print('this is the request', request)
        # Locate the mango to show
        book = get_object_or_404(Book, pk=pk)

        # Run the data through the serializer so it's formatted
        data = BookSerializer(book).data
        return Response({ 'book': data })

    # @user_passes_test(lambda u: u.is_superuser)
    def delete(self, request, pk):
        """Delete request"""
        # Locate book to delete
        book = get_object_or_404(Book, pk=pk)
        if(request.user.is_superuser):
          # Only delete if the user owns the  mango
          book.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)
        else:
          raise PermissionDenied('Unauthorized, you do not have permission to delete this book')

    def partial_update(self, request, pk):
        """Update Request"""
        # Locate Mango
        # get_object_or_404 returns a object representation of our Book
        book = get_object_or_404(Book, pk=pk)
        # Check if user is the same as the request.user.id
        # if not request.user.id == mango.owner.id:
        #     raise PermissionDenied('Unauthorized, you do not own this book')
        if(request.user.is_superuser):
          # Ensure the owner field is set to the current user's ID
          # request.data['book']['owner'] = request.user.id
          # Validate updates with serializer
          data = BookSerializer(book, data=request.data['book'], partial=True)
          if data.is_valid():
              # Save & send a 204 no content
              data.save()
              return Response(status=status.HTTP_204_NO_CONTENT)
          # If the data is not valid, return a response with the errors
          return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
          raise PermissionDenied('Unauthorized, you do not have permission to update this book')
