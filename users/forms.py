# from django.contrib.auth.forms import UserCreationForm
# from .models import Profile, ProfileComment, CommentReply

# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField()
#     # Hey Corey, I belive the extra line "email = forms.EmailField()"
#     #  for the UserRegisterForm is not necessary. Since the
#     #  UserCreationForm is a model.Form based on the User model, we
#     #  can call in the Meta class the field named "email". 

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']
    
#     def clean_email(self):
#         if User.objects.filter(email=self.cleaned_data['email']).exists():
#             raise forms.ValidationError("the given email is already registered")
#         return self.cleaned_data['email']
        