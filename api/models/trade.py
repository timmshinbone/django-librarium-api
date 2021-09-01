from django.db import models
from django.contrib.auth import get_user_model

from .user import User
from .copy import Copy

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
  # copy of book that the trade initiator will send
  copy_from = models.ForeignKey(Copy, on_delete=models.CASCADE, related_name='copy_sender')
  # copy of book desired by the trade initiator
  copy_to = models.ForeignKey(Copy, on_delete=models.CASCADE, related_name='copy_receiver')
  # trade initiator, owner of copy_from
  from_user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='req_sent_from')
  # receiver, owner of copy_to
  to_user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='req_sent_to')
  # date trade is initiated
  trade_date = models.DateTimeField(auto_now_add=True)
  # date when trade was accepted or declined
  updated_at = models.DateTimeField(auto_now=True)
  # status, accepted will switch copy_to.owner and copy_from.owner
  status = models.CharField(
    max_length=255,
    choices=TradeStatuses.choices,
    default=TradeStatuses.PENDING
  )

  def save(self, *args, **kwargs):
    if self.from_user is None:
      self.from_user = self.copy_from.owner
    if self.to_user is None:
      self.to_user = self.copy_to.owner
    super(Trade, self).save(*args, **kwargs)

  def __str__(self):
    # This must return a string
    return f"{self.copy_from.owner.email} would like to trade '{self.copy_from.book.title}' for '{self.copy_to.book.title}', do you accept, {self.copy_to.owner.email}?. (current status: {self.status})"

  def as_dict(self):
    """Returns dictionary version of Mango models"""
    return {
        'id': self.id,
        'copy_from': self.copy_from,
        'copy_to': self.copy_to,
        'from_user': self.from_user,
        'to_user': self.to_user,
        'trade_date': self.trade_date,
        'updated_at': self.updated_at,
        'status': self.status
    }
