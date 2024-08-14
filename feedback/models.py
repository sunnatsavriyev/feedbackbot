from django.db import models


class Feedback(models.Model):
    feedback = models.TextField()
    craeted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'feedback'

    def __str__(self):
        return f'{self.feedback}'