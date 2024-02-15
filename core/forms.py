from django import forms
from django.db import transaction

from .models import NewsAndEvents, Session, Semester, SEMESTER


# news and events
class NewsAndEventsForm(forms.ModelForm):
    class Meta:
        model = NewsAndEvents
        fields = (
            "title",
            "summary",
            "posted_as",
        )
        labels = {
            'title': 'Título',
            'summary': 'Resumen',
            'posted_as': 'Publicado como',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["summary"].widget.attrs.update({"class": "form-control"})
        self.fields["posted_as"].widget.attrs.update({"class": "form-control"})


class SessionForm(forms.ModelForm):
    next_session_begins = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                "type": "date",
            }
        ),
        label="Próxima sesión comienza",
        required=True,
    )

    class Meta:
        model = Session
        fields = ["session", "is_current_session", "next_session_begins"]
        labels = {
            'session': 'Sesión',
            'is_current_session': '¿Es la sesión actual?',
            'next_session_begins': 'Próxima sesión comienza',
        }


class SemesterForm(forms.ModelForm):
    semester = forms.CharField(
        widget=forms.Select(
            choices=SEMESTER,
            attrs={
                "class": "browser-default custom-select",
            },
        ),
        label="Semestre",
    )
    is_current_semester = forms.CharField(
        widget=forms.Select(
            choices=((True, "Sí"), (False, "No")),
            attrs={
                "class": "browser-default custom-select",
            },
        ),
        label="¿Es el semestre actual?",
    )
    session = forms.ModelChoiceField(
        queryset=Session.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "browser-default custom-select",
            }
        ),
        label="Sesión",
        required=True,
    )

    next_semester_begins = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        ),
        label="Próxima sesión comienza",
        required=True,
    )

    class Meta:
        model = Semester
        fields = ["semester", "is_current_semester", "session", "next_semester_begins"]
        labels = {
            'semester': 'Semestre',
            'is_current_semester': '¿Es el semestre actual?',
            'session': 'Sesión',
            'next_semester_begins': 'Próximo semestre comienza',
        }
