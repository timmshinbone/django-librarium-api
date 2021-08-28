from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class Copy(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
  book = models.ForeignKey('Book', on_delete=models.CASCADE)
  owner = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE
  )

  def __str__(self):
    # This must return a string
    return f"This copy of the book named '{self.book.title}' is owned by {self.owner.email}."

  def as_dict(self):
    """Returns dictionary version of Mango models"""
    return {
        'id': self.id,
        'book': self.book,
        'owner': self.owner
    }
