from django import forms
from website.models.PostModel import Post
from website.models.AuthorModel import Author

class PostForm(forms.ModelForm):
    """Enhanced form for creating and editing blog posts with rich text editor"""
    
    class Meta:
        model = Post
        fields = ['title', 'url_slug', 'meta_description', 'text']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter an engaging post title',
                'maxlength': '200'
            }),
            'url_slug': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'my-awesome-post',
                'pattern': '[a-z0-9-]+',
                'title': 'Only lowercase letters, numbers, and hyphens allowed'
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Write a compelling meta description for SEO (max 160 characters)',
                'rows': 3,
                'maxlength': '160'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control rich-text-editor', 
                'id': 'rich-editor',
                'placeholder': 'Start writing your amazing content here...'
            }),
        }
        labels = {
            'title': 'Post Title',
            'url_slug': 'URL Slug',
            'meta_description': 'Meta Description (SEO)',
            'text': 'Content',
        }
        help_texts = {
            'url_slug': 'A unique URL-friendly identifier (use lowercase letters, numbers, and hyphens only)',
            'meta_description': 'This appears in search engine results. Keep it under 160 characters.',
            'text': 'Use the rich text editor to format your content with headings, images, videos, and tables.',
        }
    
    def clean_url_slug(self):
        """Validate that the URL slug is unique and properly formatted"""
        url_slug = self.cleaned_data.get('url_slug')
        
        # Convert to lowercase and replace spaces with hyphens
        url_slug = url_slug.lower().replace(' ', '-')
        
        # Remove any characters that aren't letters, numbers, or hyphens
        import re
        url_slug = re.sub(r'[^a-z0-9-]', '', url_slug)
        
        # Remove multiple consecutive hyphens
        url_slug = re.sub(r'-+', '-', url_slug)
        
        # Remove leading/trailing hyphens
        url_slug = url_slug.strip('-')
        
        if not url_slug:
            raise forms.ValidationError('URL slug cannot be empty after formatting.')
        
        # Check if the slug already exists (excluding the current instance if editing)
        if self.instance.pk:
            if Post.objects.filter(url_slug=url_slug).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('This URL slug is already in use. Please choose a different one.')
        else:
            if Post.objects.filter(url_slug=url_slug).exists():
                raise forms.ValidationError('This URL slug is already in use. Please choose a different one.')
        
        return url_slug
    
    def clean_meta_description(self):
        """Validate meta description length"""
        meta_description = self.cleaned_data.get('meta_description')
        if meta_description and len(meta_description) > 160:
            raise forms.ValidationError('Meta description must be 160 characters or less.')
        return meta_description