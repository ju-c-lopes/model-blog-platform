from django import forms

from website.models.author.JobsModel import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "occupation",
            "company",
            "current_job",
            "location",
            "start_date",
            "end_date",
            "roles_description",
        ]
        labels = {
            "occupation": "Cargo",
            "company": "Empresa",
            "current_job": "Trabalho atual",
            "location": "Localização",
            "start_date": "Data de início",
            "end_date": "Data de término",
            "roles_description": "Descrição",
        }
        widgets = {
            "occupation": forms.TextInput(attrs={"class": "form-control"}),
            "company": forms.TextInput(attrs={"class": "form-control"}),
            "current_job": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "start_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "end_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "roles_description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }
