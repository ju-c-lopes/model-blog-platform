from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from website.models import Author, Reader
from website.forms.ProfileUpdateForm import ProfileUpdateForm
from website.views.SignUpView import treat_accentuation
import unicodedata

@login_required
def update_profile(request):
    user = request.user
    current_profile_type = None
    current_profile = None
    
    # Determine current profile state
    if hasattr(user, 'author'):
        current_profile_type = 'author'
        current_profile = user.author
    elif hasattr(user, 'reader'):
        current_profile_type = 'reader'
        current_profile = user.reader
    
    if request.method == 'POST':
        form = ProfileUpdateForm(user=user, data=request.POST, files=request.FILES)
        if form.is_valid():
            new_profile_type = form.cleaned_data['profile_type']
            name = form.cleaned_data['name']
            image = form.cleaned_data.get('image')
            
            # Handle profile type change
            if current_profile_type and current_profile_type != new_profile_type:
                # Delete old profile
                if current_profile_type == 'author':
                    user.author.delete()
                    user.is_staff = False
                else:
                    user.reader.delete()
                
                current_profile_type = None
                current_profile = None
            
            # Create or update profile
            if new_profile_type == 'author':
                if current_profile_type == 'author':
                    # Update existing author
                    author = user.author
                    author.author_name = name
                    if image:
                        if author.image:
                            author.image.delete(save=False)
                        author.image = image
                    author.save()
                else:
                    # Create new author
                    user.is_staff = True
                    user.save()
                    
                    # Generate slug
                    author_name_replaced = treat_accentuation(name)
                    slug = '-'.join(author_name_replaced.split()).lower()
                    
                    author = Author.objects.create(
                        user=user,
                        author_name=name,
                        author_url_slug=slug,
                        access_level=1,
                        image=image
                    )
                
                messages.success(request, 'Perfil de Autor atualizado com sucesso!')
            
            else:  # reader
                if current_profile_type == 'reader':
                    # Update existing reader
                    reader = user.reader
                    reader.reader_name = name
                    if image:
                        if reader.image:
                            reader.image.delete(save=False)
                        reader.image = image
                    reader.save()
                else:
                    # Create new reader
                    reader = Reader.objects.create(
                        user=user,
                        reader_name=name,
                        access_level=2,
                        image=image
                    )
                
                messages.success(request, 'Perfil de Leitor atualizado com sucesso!')
            
            return redirect('/')
    else:
        form = ProfileUpdateForm(user=user)
    
    context = {
        'form': form,
        'has_profile': current_profile_type is not None,
        'profile_type': current_profile_type,
        'is_creating': current_profile_type is None,
    }
    return render(request, 'profile-update/update-profile.html', context)