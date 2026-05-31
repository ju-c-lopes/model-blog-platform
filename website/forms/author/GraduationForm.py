from django import forms

from website.models.author.GraduationsModel import Graduation


class GraduationForm(forms.ModelForm):
    class Meta:
        model = Graduation
        fields = [
            "graduation_level",
            "course",
            "school",
            "year_graduation",
            "concluded",
        ]
        labels = {
            "graduation_level": "Tipo de formação",
            "course": "Curso",
            "school": "Instituição",
            "year_graduation": "Ano de conclusão",
            "concluded": "Concluído",
        }
        widgets = {
            "graduation_level": forms.Select(attrs={"class": "custom-select"}),
            "course": forms.TextInput(attrs={"class": "form-control"}),
            "school": forms.TextInput(attrs={"class": "form-control"}),
            "year_graduation": forms.NumberInput(attrs={"class": "form-control", "min": 1900, "max": 2100}),
            "concluded": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
