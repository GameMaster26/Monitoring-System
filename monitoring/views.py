from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Patient, History, Treatment,Barangay,Municipality
from django.db.models import Count, F
import json
from django.db.models.functions import ExtractWeek, ExtractYear, ExtractDay, ExtractMonth
from datetime import datetime, timedelta,date
from dateutil.relativedelta import relativedelta 
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.admin.models import LogEntry
from django.template.loader import get_template
#from weasyprint import HTML
import pandas as pd
from django.db.models import Q
from django.db.models.functions import TruncDay,TruncDate,TruncMonth, TruncQuarter,TruncYear
from collections import Counter
from urllib.parse import urlencode
from django.http import JsonResponse
from django.template.loader import render_to_string
from calendar import month_name
from django.contrib.auth.models import Group,User
from django.shortcuts import redirect
from django.contrib import messages



def index(request):
    # Retrieve all totals
    total_patients = Patient.objects.count()
    total_history = History.objects.count()
    total_treatments = Treatment.objects.count()

    # Count male and female patients
    male_patients = Patient.objects.filter(sex='male').count()
    female_patients = Patient.objects.filter(sex='female').count()

    # Calculate counts for different animal bites
    dog_bites = History.objects.filter(source_of_exposure='Dog').count()
    cat_bites = History.objects.filter(source_of_exposure='Cat').count()
    
    # Perform a query to count the occurrences of each municipality of exposure
    municipality_exposures = History.objects.values('muni_id__muni_name').annotate(count=Count('muni_id')).order_by('-count').first()

    # Determine which animal has the highest count
    animal_counts = History.objects.values('source_of_exposure').annotate(count=Count('source_of_exposure')).order_by('-count').first()
    most_cases_animal = animal_counts

    gender_counts = Patient.objects.values('sex').annotate(count=Count('sex')).order_by('-count').first()

    histories = History.objects.all()  # Retrieve all Histories from the database

    # Count the number of male and female patients
    gender = Patient.objects.values('sex').annotate(count=Count('sex')).order_by('sex')
    
    gen = [data['sex'].capitalize() for data in gender]
    dataGender = [data['count'] for data in gender]

    # Count the number animal source of exposure
    source_exposure = History.objects.values('source_of_exposure').annotate(count=Count('source_of_exposure')).order_by('source_of_exposure')
    
    animal = [data['source_of_exposure'].capitalize() for data in source_exposure]
    dataAnimal = [data['count'] for data in source_exposure]

    # Count occurrences of each municipality using Django ORM
    municipality_counts = History.objects.values('muni_id__muni_name').annotate(count=Count('muni_id')).order_by('muni_id__muni_name')

    # Prepare data for chart
    municipalities = [data['muni_id__muni_name'] for data in municipality_counts]
    municipality_case_counts = [data['count'] for data in municipality_counts]
    """ municipalities = Municipality.objects.all()
    municipality_case_counts = [data['count'] for data in municipality_counts] """

    

    # Group cases by month
    monthly_cases = History.objects.annotate(month=TruncMonth('date_registered')).values('month').annotate(count=Count('history_id')).order_by('month')

    months = [data['month'].strftime('%B') for data in monthly_cases]
    case_counts = [data['count'] for data in monthly_cases]

    # Calculate the number of cases per week
    weekly_cases = History.objects.annotate(
        week=ExtractWeek('date_registered'),
        year=ExtractYear('date_registered')
    ).values('year', 'week').annotate(count=Count('history_id')).order_by('year', 'week')

    # Prepare the data for the chart with start dates of weeks
    weeks = []
    weekly_case_counts = []
    for entry in weekly_cases:
        year = entry['year']
        week = entry['week']
        start_date = datetime.strptime(f'{year}-W{week}-1', "%Y-W%U-%w")  # Ensure the week starts from Sunday
        week_label = start_date.strftime('%Y-%m-%d')
        weeks.append(week_label)
        weekly_case_counts.append(entry['count'])

    # Calculate the number of cases per day
    daily_cases = (
        History.objects
        .annotate(day=TruncDate('date_registered'))
        .values('day')
        .annotate(count=Count('history_id'))
        .order_by('day')
    )

    days = []
    daily_case_counts = []

    for data in daily_cases:
        day = data['day']
        count = data['count']
        
        if day is not None:
            days.append(day.strftime('%Y-%m-%d'))
        else:
            days.append('Unknown')  # Handle None case with a fallback
        
        daily_case_counts.append(count)

    # Calculate the number of cases per quarter
    quarterly_cases = (
        History.objects
        .annotate(quarter=TruncQuarter('date_registered'))
        .values('quarter')
        .annotate(count=Count('history_id'))
        .order_by('quarter')
    )

    # Prepare quarters and quarterly counts
    quarters = []
    quarterly_case_counts = []
    
    for data in quarterly_cases:
        quarter_str = f"Quarter {((data['quarter'].month - 1) // 3) + 1} {data['quarter'].year}"
        quarters.append(quarter_str)
        quarterly_case_counts.append(data['count'])

        
    # Calculate the number of cases per year
    annual_cases = (
        History.objects
        .annotate(year=TruncYear('date_registered'))
        .values('year')
        .annotate(count=Count('history_id'))
        .order_by('year')
    )

    years = [data['year'].strftime('%Y') for data in annual_cases]
    annual_case_counts = [data['count'] for data in annual_cases]


    total_cases = History.objects.count()

    # Retrieve latitude, longitude, and metric data for heatmap
    heatmap_data = History.objects.values('latitude', 'longitude').annotate(count=Count('history_id'))
    heatmap_data = [[entry['latitude'], entry['longitude'], entry['count']] for entry in heatmap_data]
    


    context = {
        'total_patients': total_patients,
        'total_history': total_history,
        'total_treatments': total_treatments,
        'male_patients': male_patients,
        'female_patients': female_patients,
        'dog_bites': dog_bites,
        'cat_bites': cat_bites,
        'most_cases_animal': most_cases_animal,
        'municipality': municipality_exposures,
        'gender_counts': gender_counts,
        'histories': histories,
        'gen': gen,
        'dataGender': dataGender,
        'animal': animal,
        'dataAnimal': dataAnimal,
        'municipalities': municipalities,
        'municipality_case_counts': municipality_case_counts,
        'months': months,
        'case_counts': case_counts,
        'weeks': weeks,
        'weekly_case_counts': weekly_case_counts,
        'days': days,
        'daily_case_counts': daily_case_counts,
        'quarters': quarters,
        'quarterly_case_counts': quarterly_case_counts,
        'years': years,
        'annual_case_counts': annual_case_counts,
        'total_cases': total_cases,
        'heatmap_data': json.dumps(heatmap_data),

        

    }
    return render(request, 'monitoring/index.html', context)



def admin_redirect(request):
    return redirect('/admin/')



# Function to calculate the age of the patient
def calculate_age(birthday):
    today = date.today()
    return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

def staff_or_superuser_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            messages.warning(request, "Only staff members or superusers can access this page.")
            return redirect('/admin/')
        return view_func(request, *args, **kwargs)
    return login_required(_wrapped_view_func)


def superuser_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.warning(request, "Only superusers or admins can access this page.")
            return redirect('/admin/')  # Replace 'some_view_name' with the name of the view you want to redirect to
        return view_func(request, *args, **kwargs)
    return login_required(_wrapped_view_func)

#@superuser_required
#@staff_or_superuser_required
@login_required
def overview(request):
    total_cases = History.objects.count()
    
    # Retrieve latitude, longitude, and metric data for heatmap
    heatmap_data = History.objects.values('latitude', 'longitude').annotate(count=Count('history_id'))
    heatmap_data = [[entry['latitude'], entry['longitude'], entry['count']] for entry in heatmap_data]

    context = {
        'heatmap_data': json.dumps(heatmap_data),
        'total_cases':  total_cases,
    }
    return render(request, 'monitoring/overview.html', context)

@login_required
def reports(request):
    

    return render(request, 'monitoring/report.html')

@login_required
def tables(request):
    return render(request, 'monitoring/table.html')

@login_required
def download(request):
    # Get selected filters from request
    selected_municipality = request.GET.get('municipality')
    selected_barangay = request.GET.get('barangay')
    selected_user = request.GET.get('searchUsername')  # Update: Correct variable name

    start_month = request.GET.get('startMonth')
    end_month = request.GET.get('endMonth')
    search_name = request.GET.get('searchName')
    
    # Fetch the histories with related patient, municipality, and barangay data and order by date_registered
    histories = History.objects.select_related('patient_id', 'muni_id', 'brgy_id').order_by('-registration_no')
    
    patients = Patient.objects.all()

    # Apply filters based on selected municipality and barangay
    if selected_municipality:
        histories = histories.filter(muni_id=selected_municipality)
    if selected_barangay:
        histories = histories.filter(brgy_id=selected_barangay)

    # Apply filter based on username search
    if selected_user:
        histories = histories.filter(patient_id__user__username=selected_user)
    
    # Fetch unique users from the Patient model for the dropdown
    patient_users = Patient.objects.select_related('user').values_list('user', flat=True).distinct()
    users = User.objects.filter(id__in=patient_users)

     # Apply filter based on selected start and end months
    if start_month and end_month:
        current_year = datetime.now().year
        start_date = datetime.strptime(f"{start_month} {current_year}", "%B %Y").replace(day=1)
        end_date = datetime.strptime(f"{end_month} {current_year}", "%B %Y").replace(day=1) + relativedelta(months=1) - relativedelta(days=1)
        histories = histories.filter(date_registered__gte=start_date, date_registered__lte=end_date)

     # Apply filter based on name search
    if search_name:
        histories = histories.filter(Q(patient_id__first_name__icontains=search_name) | Q(patient_id__last_name__icontains=search_name))

    months = month_name[1:]
    
    # Calculate age and attach to each history instance
    for history in histories:
        history.treatment = Treatment.objects.filter(patient_id=history.patient_id).first()
        history.age = calculate_age(history.patient_id.birthday)

    
    # Count the number of male and female patients
    """ male = histories.filter(patient_id__sex='Male').count()
    female = histories.filter(patient_id__sex='Female').count() """

    # Count the number of male and female patients
    male = histories.filter(patient_id__sex__iexact='Male').count()
    female = histories.filter(patient_id__sex__iexact='Female').count()



    # Calculate the number of age
    age_15_or_less_count = 0
    age_above_15_count = 0

    for history in histories:
        age = calculate_age(history.patient_id.birthday)
        if age <= 15:
            age_15_or_less_count += 1
        else:
            age_above_15_count += 1

    # Calculate counts for different animal bites   
    source_of_exposure_counter = Counter(histories.values_list('source_of_exposure', flat=True))
    dog_count = source_of_exposure_counter.get('Dog', 0)
    cat_count = source_of_exposure_counter.get('Cat', 0)
    other_animal_count = source_of_exposure_counter.get('Others', 0)

    paginator = Paginator(histories,10)  # records per page
    page_number = request.GET.get('page')
    histories = paginator.get_page(page_number)

    # Collect current query parameters
    query_params = request.GET.dict()
    if 'page' in query_params:
        del query_params['page']  # Remove the page parameter
    query_string = urlencode(query_params)

    municipalities = Municipality.objects.all()
    barangays = Barangay.objects.all()


    context = {
        'histories': histories,
        'municipalities': municipalities,
        'barangays': barangays,
        'selected_municipality': selected_municipality,
        'selected_barangay': selected_barangay,
        'selected_user':selected_user,
        'start_month': start_month,
        'end_month': end_month,
        'search_name': search_name,
        'months': months,
        'male' : male,
        'female' : female,
        'dog_count' : dog_count,
        'cat_count' : cat_count,
        'other_animal_count' : other_animal_count,
        'age_15_or_less_count' : age_15_or_less_count,
        'age_above_15_count' : age_above_15_count,
        'query_string' : query_string,
        'users':users
    }

    return render(request, 'monitoring/download.html',context)





def notification(request):
    patient = Patient.objects.first()
    if patient:
            print(f"Patient found: {patient.first_name}")
            notification_message = f"Patient {patient.first_name} has an appointment"
    else:
            print("No patients found")
            notification_message = "No patients found"

    context = {
        'notification_message': notification_message,
    }

    return render(request, 'admin/base.html', context)
