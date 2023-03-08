from djongo import models
from django import forms
class Dataobject(models.Model):
    File_id = models.BigIntegerField()
    Name = models.CharField(max_length=200)
    Path = models.URLField()
    Family = models.CharField(max_length=2)
    type1='type1'
    type2='type2'
    cat=((type1,type1),(type2,type2))
    Category = models.CharField(max_length=255,choices=cat,default=type1)

    class Meta:
        abstract = True

class DataobjectForm(forms.ModelForm):
    class Meta:
        model = Dataobject
        fields = ('File_id','Name','Path','Family','Category')
        


class FolderDetails(models.Model):
    
    id = models.BigAutoField(primary_key=True,default=1,null=False)
    User_id = models.BigIntegerField(null=False)
    Folder_Name = models.CharField(default='root' ,max_length=300)
    FileList = models.ArrayField(model_container=Dataobject,model_form_class=DataobjectForm)
    objects = models.DjongoManager()
