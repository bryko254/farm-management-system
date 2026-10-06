from django.contrib import admin

from .models import Task, Worker


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'is_active', 'owner')
    search_fields = ('name', 'role')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'due_date', 'priority', 'status')
    list_filter = ('status', 'priority')
