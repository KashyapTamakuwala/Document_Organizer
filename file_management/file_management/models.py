from djongo import models
from django import forms
class Dataobject(models.Model):
    File_id = models.BigIntegerField()
    Name = models.CharField(max_length=200)
    Path = models.URLField()
    Family = models.CharField(max_length=2)
    type0 = 'None'
    type1='Book'
    type2='Resume'
    type3='Publication'
    type4='Legal Document'
    cat=((type1,'Book'),(type2,'Resume'),(type3,'Publication'),(type4,'Legal Document'),(type0,'None'))
    Category = models.CharField(max_length=255,choices=cat,default=type0)

    class Meta:
        abstract = True

class DataobjectForm(forms.ModelForm):
    class Meta:
        model = Dataobject
        fields = ('File_id','Name','Path','Family','Category')
        


class FolderDetails(models.Model):
    
    User_id = models.BigIntegerField(null=False)
    Folder_Name = models.CharField(default='root' ,max_length=300)
    FileList = models.ArrayField(model_container=Dataobject,model_form_class=DataobjectForm)
    objects = models.DjongoManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['User_id','Folder_Name'],
                                    name="Unique Folder Constraint"
                                    )
        ]
