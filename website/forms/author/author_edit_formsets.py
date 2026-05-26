from django.forms import inlineformset_factory

from website.forms.author.GraduationForm import GraduationForm
from website.forms.author.JobForm import JobForm
from website.forms.author.SocialMediaForm import SocialMediaForm
from website.models.author.AuthorModel import Author
from website.models.author.AuthorSocialMediaModel import SocialMedia
from website.models.author.GraduationsModel import Graduation
from website.models.author.JobsModel import Job

SocialMediaFormSet = inlineformset_factory(
    Author,
    SocialMedia,
    form=SocialMediaForm,
    extra=0,
    can_delete=True,
)
GraduationFormSet = inlineformset_factory(
    Author,
    Graduation,
    form=GraduationForm,
    extra=0,
    can_delete=True,
)
JobFormSet = inlineformset_factory(
    Author,
    Job,
    form=JobForm,
    extra=0,
    can_delete=True,
)

SOCIAL_FORMSET_PREFIX = "social"
GRADUATION_FORMSET_PREFIX = "graduation"
JOB_FORMSET_PREFIX = "job"
