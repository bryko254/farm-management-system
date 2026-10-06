from farm_management_system.crud import crud_views

from .forms import EquipmentForm
from .models import Equipment

COLUMNS = [
    ('Name', 'name'), ('Condition', 'condition'), ('Purchased', 'purchase_date'),
    ('Last maintenance', 'last_maintenance'), ('Next maintenance', 'next_maintenance'),
]

EquipmentListView, EquipmentCreateView, EquipmentUpdateView, EquipmentDeleteView = crud_views(
    Equipment, EquipmentForm, app='equipment', prefix='equipment', label='Equipment',
    columns=COLUMNS, icon='fa-tractor')


class MaintenanceScheduleView(EquipmentListView):
    """Equipment with a maintenance date, soonest first."""
    template_name = 'equipment/maintenance_schedule.html'

    def get_queryset(self):
        return super().get_queryset().filter(next_maintenance__isnull=False).order_by('next_maintenance')
