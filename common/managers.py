from django.db import models

# 동영상 강의 보고 만든 클래스인데 음 안써도 괜찮은거 같기도..
class CustomModelManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None
