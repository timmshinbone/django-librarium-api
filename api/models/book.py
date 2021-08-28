from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class Book(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
  title = models.CharField(max_length=255)
  author = models.CharField(max_length=255)
  isbn = models.CharField(max_length=255, unique=True)
  genre = models.CharField(max_length=100)
  pages = models.IntegerField()
  image = models.CharField(max_length=255)
  published = models.CharField(max_length=100)

  def __str__(self):
    # This must return a string
    return f"The book '{self.title}' was written by {self.author} . It was published {self.published} and is {self.pages} pages in length.({self.genre})"

  def as_dict(self):
    """Returns dictionary version of Mango models"""
    return {
        'id': self.id,
        'title': self.title,
        'author': self.author,
        'isbn': self.isbn,
        'genre': self.genre,
        'pages': self.pages,
        'image': self.image,
        'published': self.published
    }
