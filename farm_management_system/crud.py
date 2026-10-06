"""Factory for owner-scoped list/create/update/delete views backed by shared templates."""
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .mixins import OwnedDeleteMixin, OwnedFormMixin, OwnedMixin


def crud_views(model, form_class, *, app, prefix, label, columns, select=(), icon='fa-list',
               list_filter=None):
    """Return (List, Create, Update, Delete) views.

    URL names are expected as ``<app>:<prefix>_{list,create,update,delete}``.
    ``columns`` is a list of ``(header, attribute)`` pairs shown in the list table.
    """
    names = {action: f'{app}:{prefix}_{action}' for action in ('list', 'create', 'update', 'delete')}
    list_url = reverse_lazy(names['list'])
    plural = model._meta.verbose_name_plural.title()
    ctx = {'urls': names, 'label': label, 'plural': plural, 'icon': icon}

    class List(OwnedMixin, ListView):
        template_name = 'crud/object_list.html'
        paginate_by = 50

        def get_queryset(self):
            qs = super().get_queryset()
            if select:
                qs = qs.select_related(*select)
            return list_filter(qs) if list_filter else qs

        def get_context_data(self, **kwargs):
            return super().get_context_data(columns=columns, **ctx, **kwargs)

    class Create(OwnedFormMixin, CreateView):
        template_name = 'crud/object_form.html'
        success_url = list_url
        success_message = f'{label} added.'

        def get_context_data(self, **kwargs):
            return super().get_context_data(title=f'Add {label}', **ctx, **kwargs)

    class Update(OwnedFormMixin, UpdateView):
        template_name = 'crud/object_form.html'
        success_url = list_url
        success_message = f'{label} updated.'

        def get_context_data(self, **kwargs):
            return super().get_context_data(title=f'Edit {label}', **ctx, **kwargs)

    class Delete(OwnedDeleteMixin, DeleteView):
        template_name = 'crud/object_confirm_delete.html'
        success_url = list_url
        success_message = f'{label} deleted.'

        def get_context_data(self, **kwargs):
            return super().get_context_data(**ctx, **kwargs)

    for view in (List, Create, Update, Delete):
        view.model = model
    Create.form_class = Update.form_class = form_class
    List.__name__, Create.__name__, Update.__name__, Delete.__name__ = (
        f'{model.__name__}{suffix}View' for suffix in ('List', 'Create', 'Update', 'Delete'))
    return List, Create, Update, Delete
