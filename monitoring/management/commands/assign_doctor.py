from django.core.management.base import BaseCommand
from monitoring.models import Patient, Doctor, User

class Command(BaseCommand):
    help = 'Assign all patients connected to a specific user to a specific doctor'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='User ID to update patients for')
        parser.add_argument('doctor_id', type=int, help='Doctor ID to assign to patients')

    def handle(self, *args, **options):
        user_id = options['user_id']
        doctor_id = options['doctor_id']

        try:
            # Fetch the doctor and user by their IDs
            doctor = Doctor.objects.get(id=doctor_id)
            user = User.objects.get(id=user_id)

            # Fetch all patients associated with this user
            patients = Patient.objects.filter(user=user)

            if not patients.exists():
                self.stdout.write(self.style.WARNING(f"No patients found for user with ID {user_id}."))
                return

            # Update each patient's doctor
            updated_count = patients.update(doctor=doctor)

            self.stdout.write(self.style.SUCCESS(
                f"Successfully assigned Doctor (ID: {doctor_id}) to {updated_count} patients associated with User (ID: {user_id})."
            ))

        except Doctor.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Doctor with ID {doctor_id} does not exist."))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"User with ID {user_id} does not exist."))
