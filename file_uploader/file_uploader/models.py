from django.db import models

def upload_folder(instance,filename):
	return 'document/{0}/{1}'.format(instance.user_id,instance.name)

class File(models.Model):
	user_id            = models.BigIntegerField(null=False)
	name 				= models.CharField(max_length=50, null=False, blank=True)
	one_file 			= models.FileField(upload_to=upload_folder, null=False, blank=True)

	def __str__(self):
		return self.name