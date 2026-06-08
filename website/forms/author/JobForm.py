from django import forms

from website.models.author.JobsModel import Job

DATE_BR_INPUT_FORMATS = ["%d/%m/%Y", "%Y-%m-%d"]


class JobForm(forms.ModelForm):
    start_date = forms.DateField(
        input_formats=DATE_BR_INPUT_FORMATS,
        widget=forms.DateInput(
            format="%d/%m/%Y",
            attrs={"class": "form-control", "placeholder": "dd/mm/aaaa"},
        ),
    )
    end_date = forms.DateField(
        required=False,
        input_formats=DATE_BR_INPUT_FORMATS,
        widget=forms.DateInput(
            format="%d/%m/%Y",
            attrs={"class": "form-control", "placeholder": "dd/mm/aaaa"},
        ),
    )

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
            "roles_description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }
