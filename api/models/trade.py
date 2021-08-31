from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Trade(models.Model):
  # statuses for enumeration in field 'status'
  class TradeStatuses(models.TextChoices):
    PENDING = 'pending', ('Pending')
    APPROVED = 'approved', ('Approved')
    DECLINED = 'declined', ('Declined')

  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
  # If you are using related_name or related_query_name on a ForeignKey or ManyToManyField, you must always specify a unique reverse name and query name for the field.
  copy_from = models.ForeignKey('Copy', on_delete=models.CASCADE, related_name='copy_sender')
  copy_to = models.ForeignKey('Copy', on_delete=models.CASCADE, related_name='copy_receiver')
  # auto_now_add sets the timestamp when the object is first created
  trade_date = models.DateTimeField(auto_now_add=True)
  # auto_now automatically updates the time anytime the object is saved
  updated_at = models.DateTimeField(auto_now=True)
  status = models.CharField(
    max_length=255,
    choices=TradeStatuses.choices,
    default=TradeStatuses.PENDING
  )

  def __str__(self):
    # This must return a string
    return f"{self.copy_to.owner.email} would like to trade '{self.copy_to.book.title}' for '{self.copy_from.book.title}', do you accept, {self.copy_from.owner.email}?. (current status: {self.status})"

  def as_dict(self):
    """Returns dictionary version of Mango models"""
    return {
        'id': self.id,
        'copy_from': self.copy_from,
        'copy_to': self.copy_to,
        'trade_date': self.trade_date,
        'updated_at': self.updated_at,
        'status': self.status
    }
