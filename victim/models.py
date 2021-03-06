from django.db import models
from operation.models import Operation
from processor.utils import push_record_to_sqs_queue
import logging

SAFETY_LEVELS = (
    (0, 'SAFE'),
    (1, 'NOT CONFIRMED'),
    (2, 'UNREACHABLE'),
    (3, 'NEED_HELP'),
    (4, 'NOT IN ZONE')
)


class Victim(models.Model):
    """
    Used to store refugee information
    """

    name = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=20, unique=True)
    notification_contact_number = models.CharField(max_length=20, blank=True)
    safety_level = models.IntegerField(choices=SAFETY_LEVELS, default=1)
    retry_count = models.IntegerField(default=0)
    location = models.TextField(null=True)
    additional_information = models.TextField(null=True)
    status_updated_by = models.TextField(null=True)
    operation = models.ForeignKey(Operation,blank=True,default=None)

    def save(self, *args, **kwags):
        super(Victim, self).save(*args, **kwags)
        logging.info('Added a new refugee with ID = %d' % self.id)
        push_record_to_sqs_queue(self.id)
