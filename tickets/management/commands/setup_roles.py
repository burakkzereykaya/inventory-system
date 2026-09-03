from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group,Permission



class Command(BaseCommand):
    def handle(self, *args, **options):
        it_staff_group, _ = Group.objects.get_or_create(name="IT Staff")
        employee_group, _ = Group.objects.get_or_create(name="Employee")
        it_staff_permissions = [
            ("tickets", "add_ticket"),
            ("tickets", "change_ticket"),
            ("tickets", "view_ticket"),

            ("tickets", "add_ticketcomment"),
            ("tickets", "view_ticketcomment"),

            ("tickets", "view_ticketassignmenthistory"),
            ("tickets", "view_ticketstatushistory"),

            ("locations","view_department"),

            ("locations", "add_device"),
            ("locations", "change_device"),
            ("locations", "view_device"),

            ("locations","view_devicestatushistory"),

            ("locations","view_manufacturer"),

            ("locations", "view_devicetype"),

            ("locations","view_location"),

            ("locations","view_networkinterface"),
            ("locations","add_networkinterface"),
            ("locations","change_networkinterface"),

            ("locations", "add_ipaddress"),
            ("locations", "change_ipaddress"),
            ("locations", "view_ipaddress"),

        ]
        employee_permissions=[
            ("tickets","add_ticket"),
            ("tickets","view_ticket"),

            ("locations","view_device"),

            ("locations","view_manufacturer"),

            ("locations","view_devicetype"),

            ("locations","view_location"),

            ("locations","view_department"),
        ]

        permission_objects=[]
        for app_label,codename in it_staff_permissions:
            permission = Permission.objects.get(
                codename=codename,
                content_type__app_label=app_label,
            )
            permission_objects.append(permission)
        it_staff_group.permissions.set(permission_objects)
        employee_permission_objects=[]
        for app_label,codename in employee_permissions:
            permission= Permission.objects.get(
                codename=codename,
                content_type__app_label=app_label,
            )
            employee_permission_objects.append(permission)
        employee_group.permissions.set(employee_permission_objects)
        self.stdout.write(
            self.style.SUCCESS("Roles and permissions configured successfully.")
        )