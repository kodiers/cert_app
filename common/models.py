from django.db import models

# Create your models here.


class BaseModel(models.Model):
    """
    Base model to add created/updated fields
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
