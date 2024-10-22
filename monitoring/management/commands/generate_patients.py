from django.core.management.base import BaseCommand
from faker import Faker
import random
from monitoring.models import Patient, Municipality, Barangay, History, Treatment
from django.contrib.auth.models import User
from datetime import timedelta, date,datetime
from nameparser import HumanName

class Command(BaseCommand):
    help = 'Generates 10 random patients with history and treatment records for User 2'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Get the specific User with id=2
        user = User.objects.get(id=2)

        # Get all existing Municipality instances
        municipalities = Municipality.objects.all()

        # Set default municipality to the one with ID 1
        default_municipality = Municipality.objects.get(muni_id=1)

        # Get all Barangays related to the selected Municipality
        barangays = default_municipality.barangays.all()
        if not barangays:
            print(f"No barangays found for {default_municipality.muni_name}")
            return

        # Define possible bite sites
        bite_sites = [
            'right arm', 'left arm', 'right leg', 'left leg', 'right hand',
            'left hand', 'back', 'shoulder', 'abdomen', 'thigh', 'calf', 'ankle',
            'right lower leg','right infrascapular','right index finger',
            '1st digit right foot','right posterior leg','right wrist','left wrist',
        ]

        def determine_sex(first_name):
            """Determine sex based on first name."""
            name = HumanName(first_name)
            if name.first in fake.first_name_male():
                return 'male'
            elif name.first in fake.first_name_female():
                return 'female'
            return 'unknown'  # Return unknown if gender cannot be determined

        def generate_registration_no():
            current_year = date.today().year

            # Find the latest registration number for the current year
            last_history = History.objects.filter(
                registration_no__startswith=f'{current_year}-'
            ).order_by('registration_no').last()

            if last_history:
                last_reg_no = last_history.registration_no
                last_reg_num = int(last_reg_no.split('-')[-1])
                new_reg_num = last_reg_num + 1
            else:
                new_reg_num = 1

            new_registration_no = f'{current_year}-{new_reg_num:05d}'
            return new_registration_no

        def create_patients_with_history_and_treatment(n=10):
            for _ in range(n):

                # Randomly select Barangay within the same Municipality
                barangay = random.choice(barangays)

                # Generate random patient details using Faker
                first_name = fake.first_name()
                middle_name = fake.last_name()
                last_name = fake.last_name()
                birthday = fake.date_of_birth(minimum_age=3, maximum_age=70)
                contact_number = '09' + ''.join([str(random.randint(0, 9)) for _ in range(9)])
                sex = determine_sex(first_name)

                # Create and save the Patient instance
                patient = Patient(
                    user=user,
                    first_name=first_name,
                    middle_name=middle_name,
                    last_name=last_name,
                    muni_id=default_municipality,
                    brgy_id=barangay,
                    birthday=birthday,
                    sex=random.choice(['male', 'female']),
                    contactNumber=contact_number
                )
                patient.save()
                print(f"Patient {first_name} {last_name} created in {barangay.brgy_name}, {default_municipality.muni_name}!")

                # Generate the correct registration number
                registration_no = generate_registration_no()

                # Date Registered - set to a random date in the 1st quarter (Jan - Mar)
                """ start_date = date(2024, 1, 1)
                end_date = date(2024, 3, 31)
                date_registered = fake.date_between(start_date=start_date, end_date=end_date) """

                date_registered = datetime.today().date()

                # Create date of exposure - ensure it is before date_registered
                date_of_exposure = date_registered - timedelta(days=random.randint(1, 30))

                # Create and save a History instance for the patient
                history = History(
                    patient_id=patient,
                    registration_no=registration_no,
                    muni_id=default_municipality,
                    brgy_id=barangay,
                    date_registered=date_registered,
                    date_of_exposure=date_of_exposure,
                    category_of_exposure='II',  # Always set to "II"
                    source_of_exposure=random.choice(['Dog', 'Cat']),
                    exposure_type=random.choice(['Bite', 'Non-Bite']),
                    bite_site=random.choice(bite_sites),  # Random body part
                    provoked_status=random.choice(['Provoked', 'Unprovoked']),
                    immunization_status=random.choice(['Immunized', 'Unimmunized']),
                    status_of_animal=random.choice(['Alive', 'Dead', 'Killed', 'Lost']),
                    confinement_status=random.choice(['Stray', 'Leashed/Caged']),
                    washing_hands=random.choice(['Yes', 'No']),
                    latitude=0.0,  # Placeholder
                    longitude=0.0,  # Placeholder
                    geom=None  # Placeholder
                )
                history.save()
                print(f"History created for {first_name} {last_name}!")

                # Day 0, Day 3, Day 7 based on date_registered
                day0 = date_registered
                day3 = day0 + timedelta(days=3)
                day7 = day3 + timedelta(days=4)

                # Create and save a Treatment instance for the patient
                treatment = Treatment(
                    patient_id=patient,
                    vaccine_generic_name=random.choice(['PCECCV', 'PVRV']),
                    vaccine_brand_name=random.choice(['Verorab', 'Speeda', 'Vaxirab', 'Abhayrab']),
                    vaccine_route='intradermal',  # Always set to "intradermal"
                    tcv_given=day0,  # TCV on the same day as date_registered
                    day0=day0,  # Day 0 same as date_registered
                    day3=day3,  # Day 3 is 3 days after Day 0
                    day7=day7,  # Day 7 is 4 days after Day 3
                )
                treatment.save()
                print(f"Treatment created for {first_name} {last_name}!")

        # Generate 10 patients with history and treatment records
        create_patients_with_history_and_treatment(10)
        self.stdout.write(self.style.SUCCESS('Successfully generated 10 patients with history and treatment records for User 2'))
