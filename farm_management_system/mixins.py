"""Shared building blocks that keep every record scoped to its owner."""
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


class UserScopedForm(forms.ModelForm):
    """ModelForm that receives the request user so it can restrict choices."""

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                css = 'form-check-input'
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                css = 'form-select'
            else:
                css = 'form-control'
            widget.attrs['class'] = f"{widget.attrs.get('class', '')} {css}".strip()
        if user is not None:
            self.restrict_choices(user)

    def restrict_choices(self, user):
        """Override to limit related-object choices to the user's own data."""


class OwnedMixin(LoginRequiredMixin):
    """Login required; querysets limited to the current user's rows.

    ``owner_lookup`` is the ORM path to the owning user, e.g. ``'owner'`` or
    ``'animal__owner'``. Set ``assign_owner = False`` for models that are
    owned indirectly (no ``owner`` column).
    """

    owner_lookup = 'owner'
    assign_owner = True

    def get_queryset(self):
        return super().get_queryset().filter(**{self.owner_lookup: self.request.user})


class OwnedFormMixin(OwnedMixin, SuccessMessageMixin):
    """For Create/Update views using a UserScopedForm."""

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if self.assign_owner and not form.instance.pk:
            form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnedDeleteMixin(OwnedMixin, SuccessMessageMixin):
    """DeleteView with a success message (DeleteView.delete() is no longer called in Django 4+)."""

    success_message = 'Deleted successfully.'
