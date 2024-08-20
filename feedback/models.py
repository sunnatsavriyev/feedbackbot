from django.db import models


class Feedback(models.Model):
    feedback = models.TextField()
    craeted_at = models.DateTimeField(auto_now_add=True)
    status_choices = (
    ("NEW", "new"),
    ("DONE", "done"),
    ("CANCEL", "cancel")
)

    status = models.CharField(max_length=9,
                  choices=status_choices,
                  default="NEW")


    class Meta:
        db_table = 'feedback'

    def __str__(self):
        return f'{self.feedback}'
    
    

