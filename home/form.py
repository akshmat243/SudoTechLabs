from django import forms
from .models import LeadUser, BlogPost
from .models import ProjectFile

class LeadUserForm(forms.ModelForm):
    class Meta:
        model = LeadUser
        fields = '__all__'


class ExcelUploadForm(forms.Form):
    file = forms.FileField()
    
class ProjectFileForm(forms.ModelForm):
    class Meta:
        model = ProjectFile
        fields = ['file']


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'caption', 'image', 'video', 'is_published']