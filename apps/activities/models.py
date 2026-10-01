from django.db import models






class Activity(models.Model):
    user_id = models.IntegerField()

    action = models.CharField(max_length=50)

    target_type = models.CharField(max_length=50)

    target_id = models.IntegerField()

    metadata = models.JSONField(default=dict, blank=True)

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    user_agent = models.TextField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "activities"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.action} - {self.user_id}"