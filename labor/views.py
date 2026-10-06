from farm_management_system.crud import crud_views

from .forms import TaskForm, WorkerForm
from .models import Task, Worker

WorkerListView, WorkerCreateView, WorkerUpdateView, WorkerDeleteView = crud_views(
    Worker, WorkerForm, app='labor', prefix='worker', label='Worker', icon='fa-users',
    columns=[('Name', 'name'), ('Role', 'role'), ('Phone', 'phone'),
             ('Hired', 'hire_date'), ('Daily wage (KES)', 'daily_wage'), ('Active', 'is_active')])

TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView = crud_views(
    Task, TaskForm, app='labor', prefix='task', label='Task', icon='fa-tasks',
    select=('assigned_to',),
    columns=[('Title', 'title'), ('Assigned to', 'assigned_to'), ('Due', 'due_date'),
             ('Priority', 'priority'), ('Status', 'status')])
