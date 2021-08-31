from django.urls import path
from .views.mango_views import Mangos, MangoDetail
from .views.book_views import Books, BookCreate, BookDetail
from .views.copy_views import Copies, CopyDetail
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword

urlpatterns = [
  	# Restful routing
    path('books/', Books.as_view(), name='books'),
    path('books/create/', BookCreate.as_view(), name='book_create'),
    # '/<int: pk>/' is similar to '/<:id>/' but defines a type, in this case integer
    # pk is the name, or primary key(in this case the id)
    path('books/<int:pk>/', BookDetail.as_view(), name='book_detail'),
    path('copies/', Copies.as_view(), name='copies'),
    path('copies/<int:pk>/', CopyDetail.as_view(), name='copy_detail'),
    path('mangos/', Mangos.as_view(), name='mangos'),
    path('mangos/<int:pk>/', MangoDetail.as_view(), name='mango_detail'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw')
]
