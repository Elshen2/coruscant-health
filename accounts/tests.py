from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User

class AuthTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.patient = User.objects.create_user(
            username='testpatient',
            password='Test1234!',
            role='patient',
            is_approved=True,
            first_name='Test',
            last_name='Xəstə'
        )
        self.doctor = User.objects.create_user(
            username='testdoctor',
            password='Test1234!',
            role='doctor',
            is_approved=True,
            first_name='Test',
            last_name='Həkim'
        )
        self.unapproved = User.objects.create_user(
            username='unapproved',
            password='Test1234!',
            role='patient',
            is_approved=False
        )

    def test_login_approved_user(self):
        response = self.client.post(reverse('login'), {
            'username': 'testpatient',
            'password': 'Test1234!'
        }, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_login_unapproved_user(self):
        response = self.client.post(reverse('login'), {
            'username': 'unapproved',
            'password': 'Test1234!'
        })
        self.assertRedirects(response, reverse('pending_approval'))

    def test_login_wrong_password(self):
        response = self.client.post(reverse('login'), {
            'username': 'testpatient',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'yanlışdır')

    def test_patient_dashboard_access(self):
        self.client.login(username='testpatient', password='Test1234!')
        response = self.client.get(reverse('patient_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_doctor_cannot_access_patient_dashboard(self):
        self.client.login(username='testdoctor', password='Test1234!')
        response = self.client.get(reverse('patient_dashboard'))
        self.assertEqual(response.status_code, 302)  # redirect

    def test_register_creates_unapproved_user(self):
        response = self.client.post(reverse('register'), {
            'username':         'newuser',
            'first_name':       'Yeni',
            'last_name':        'İstifadəçi',
            'email':            'new@test.com',
            'phone':            '0501234567',
            'role':             'patient',
            'password':         'Test1234!',
            'password_confirm': 'Test1234!'
        })
        user = User.objects.get(username='newuser')
        self.assertFalse(user.is_approved)


class HealthRecordTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.patient = User.objects.create_user(
            username='patient2',
            password='Test1234!',
            role='patient',
            is_approved=True
        )
        self.client.login(username='patient2', password='Test1234!')

    def test_upload_health_record(self):
        response = self.client.post(reverse('upload_record'), {
            'heart_rate':         72,
            'blood_pressure_sys': 120,
            'blood_pressure_dia': 80,
            'temperature':        '36.6',
            'oxygen_level':       '98.0',
            'notes':              'Normal vəziyyət'
        })
        self.assertRedirects(response, reverse('my_records'))

    def test_records_list_shows_only_own(self):
        from records.models import HealthRecord
        HealthRecord.objects.create(patient=self.patient, heart_rate=70)
        response = self.client.get(reverse('my_records'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '70')