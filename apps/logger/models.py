from django.db import models


class Logger(models.Model):
    request_ip = models.CharField(max_length=255)
    request_data = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)
    request_path = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.request_path} -->  {self.request_ip}'





