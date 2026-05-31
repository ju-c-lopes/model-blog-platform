from django import forms

from website.models.author.JobsModel import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "occupation",
            "company",
            "location",
            "start_date",
            "end_date",
            "current_job",
            "roles_description",
        ]
        labels = {
            "occupation": "Cargo",
            "company": "Empresa",
            "location": "Localização",
            "start_date": "Data de início",
            "end_date": "Data de término",
            "current_job": "Trabalho atual",
            "roles_description": "Descrição",
        }
        widgets = {
            "occupation": forms.TextInput(attrs={"class": "form-control"}),
            "company": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "start_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "end_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "current_job": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "roles_description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }
