from django.shortcuts import render, redirect
from django.contrib import messages


# def register(request):
#     if request.user.is_authenticated:
#        return redirect('blog-home')
#     else:
#         if request.method == 'POST':
#             print(request.POST)
#             print('================================', request.body)
#             form = UserRegisterForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 username = form.cleaned_data.get('username')
#                 messages.success(request, f'Account created, you can now login!')
#                 return redirect('login')
#         else:
#             form = UserRegisterForm()
#         return render(request, 'users/register.html', {'form': form})
