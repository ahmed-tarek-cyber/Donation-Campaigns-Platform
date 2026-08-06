from django import forms
from django.contrib.auth.models import User
from .models import Post, UserProfile
from django.forms import DateTimeInput

class SimpleSignupForm(forms.Form):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField()
    mobile_phone = forms.CharField(max_length=11, required=False)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if not username:
            raise forms.ValidationError("Username is required")
        allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
        for ch in username:
            if ch not in allowed:
                raise forms.ValidationError("Username can contain letters, numbers, - and _ only")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '').strip()
        if not first_name:
            raise forms.ValidationError("First name is required")
        
         
        allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -.'"
        for char in first_name:
            if char not in allowed_chars:
                raise forms.ValidationError("First name can contain letters and spaces only")
        
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '').strip()
        if not last_name:
            raise forms.ValidationError("Last name is required")
        
         
        allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -.'"
        for char in last_name:
            if char not in allowed_chars:
                raise forms.ValidationError("Last name can contain letters and spaces only")
        
        return last_name

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data.get('mobile_phone', '').strip()
        if mobile_phone:   
             
            if len(mobile_phone) != 11:
                raise forms.ValidationError("Phone is invalid")
            
             
            if not mobile_phone.isdigit():
                raise forms.ValidationError("Phone must contain only Numbers")
            
             
            valid_starts = ['010', '011', '012', '015']
            if not any(mobile_phone.startswith(start) for start in valid_starts):
                raise forms.ValidationError("Phone must be Egyptian number")
        
        return mobile_phone

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if not p1 or not p2:
            raise forms.ValidationError("Please enter password twice")
        if p1 != p2:
            raise forms.ValidationError("Passwords do not match")
        if len(p1) < 4:
            raise forms.ValidationError("Password must be at least 4 characters")
        return cleaned



class PostForm(forms.ModelForm):
    image_file = forms.ImageField(
        required=False,
        widget=forms.FileInput()
    )

    video_url = forms.URLField(
        required=False, 
        label="YouTube Video Link (Optional)",
        widget=forms.URLInput(attrs={'placeholder': 'https://www.youtube.com/watch?v=...'})
    )

    start_time = forms.DateTimeField(
        widget=DateTimeInput(attrs={'type': 'datetime-local'}),
        required=True
    )

    end_time = forms.DateTimeField(
        widget=DateTimeInput(attrs={'type': 'datetime-local'}),
        required=True
    )

    class Meta:
        model = Post
        fields = ['title', 'description', 'image_url', 'image_file', 'video_url', 'target_amount', 'start_time', 'end_time']
