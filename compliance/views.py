from farm_management_system.crud import crud_views

from .forms import CertificationForm
from .models import Certification

(CertificationListView, CertificationCreateView,
 CertificationUpdateView, CertificationDeleteView) = crud_views(
    Certification, CertificationForm, app='compliance', prefix='certification',
    label='Certification', icon='fa-certificate',
    columns=[('Name', 'name'), ('Issued by', 'issuing_body'), ('Reference', 'reference_number'),
             ('Issued', 'issue_date'), ('Expires', 'expiry_date'), ('Status', 'status')])
