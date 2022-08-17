from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from webapp.forms import ProjectCreateForm, ChangeUsersInProjectForm
from webapp.models import Project


class ProjectsListView(ListView):
    model = Project
    template_name = "projects/index.html"
    context_object_name = "projects"


class CreateProjectView(PermissionRequiredMixin, CreateView):
    form_class = ProjectCreateForm
    template_name = "projects/create.html"
    permission_required = "webapp.add_project"

    def get_success_url(self):
        return reverse("webapp:projects_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.users.add(self.request.user)
        return response


class DetailProjectView(PermissionRequiredMixin, DetailView):
    model = Project
    template_name = "projects/detail.html"
    permission_required = "webapp.view_project"

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().users.all()


class ChangeUsersInProjectView(PermissionRequiredMixin, UpdateView):
    model = Project
    template_name = "projects/change_users.html"
    permission_required = "webapp.add_users_in_project"
    form_class = ChangeUsersInProjectForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["pk"] = self.request.user.pk
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.users.add(self.request.user)
        return response

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().users.all()

    def get_success_url(self):
        return reverse("webapp:projects_list")
