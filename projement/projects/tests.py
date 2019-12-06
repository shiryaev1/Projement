import pdb
from django.contrib.auth.models import User
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.text import slugify

from projects.models import Project, Tag, HistoryOfChanges, Company


def create_company():
    company = Company.objects.create(
        name='Test'
    )
    return company


class DashboardTestCase(TestCase):

    fixtures = ['initial.json']

    def setUp(self):
        super().setUp()

        username, password = 'Thorgate', 'thorgate123'
        User.objects.create_user(username=username, email='info@throgate.eu', password=password)

        self.authenticated_client = Client()
        self.authenticated_client.login(username=username, password=password)

    def test_dashboard_requires_authentication(self):

        # Anonymous users can't see the dashboard

        client = Client()
        response = client.get('/dashboard/')
        self.assertRedirects(response, '/login/?next=/dashboard/')

        # Authenticated users can see the dashboard

        response = self.authenticated_client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_projects_on_dashboard(self):

        # There are 3 projects on the dashboard (loaded from the fixtures)

        response = self.authenticated_client.get('/dashboard/')
        projects = response.context['projects']
        self.assertEqual(len(projects), 3)

    def test_order_projects(self):
        response = self.authenticated_client.get('/dashboard/')
        projects = response.context['projects'][0]
        active_project = Project.objects.get(end_date__isnull=True)
        self.assertEqual(projects, active_project)


class ProjectsTestCase(TestCase):
    fixtures = ['initial.json']

    def setUp(self):
        super().setUp()
        username, password = 'Thorgate', 'thorgate123'
        User.objects.create_user(username=username, email='info@throgate.eu',
                                 password=password)

        self.authenticated_client = Client()
        self.authenticated_client.login(username=username, password=password)
        self.projects = Project.objects.order_by('id')

    def test_project_has_ended(self):

        # 2 of the projects have ended
        self.assertListEqual([p.has_ended for p in self.projects], [True, True, False])

    def test_project_is_over_budget(self):

        # 1 of the projects is over budget
        self.assertListEqual([p.is_over_budget for p in self.projects], [True, False, False])

    def test_total_estimated_hours(self):

        self.assertListEqual([p.total_estimated_hours for p in self.projects], [690, 170, 40])

    def test_total_actual_hours(self):

        self.assertListEqual([p.total_actual_hours for p in self.projects], [739, 60, 5])

    # def test_export_projects_to_excel(self):
    #     client = self.authenticated_client
    #     response = client.get('export/excel/')
    #     self.assertEqual(response.status_code, 200)

    def test_range_actual_hours(self):
        project = Project.objects.get(id=self.projects[0].id)
        Project.objects.update(
            actual_testing=4
        )
        project.refresh_from_db()
        self.assertEqual(project.actual_testing, 4)


class TagTestCase(TestCase):
    def setUp(self):
        super().setUp()

        username, password = 'TestUser', 'thorgate123'
        User.objects.create_user(username=username, email='info@throgate.eu',
                                 password=password)

        self.authenticated_client = Client()
        self.authenticated_client.login(username=username, password=password)

    def create_tag(self):
        tag = Tag.objects.create(
            title='python'
        )
        return tag

    def create_project(self):
        company = create_company()
        tag = self.create_tag()
        project = self.authenticated_client.post('/projects/create/', {
            'company': company,
            'title': 'test-company',
            'start_date': '2012-01-12',
            'end_date': '',
            'estimated_design': 1,
            'actual_design': 3,
            'estimated_development': 4,
            'actual_development': 3,
            'estimated_testing': 3,
            'actual_testing': 4,
            'tags': tag,
            'additional_hour_design': '',
            'additional_hour_development': '',
            'additional_hour_testing': '',
        })
        return project

    # def test_save_history_of_changes(self):
    #     company = create_company()
    #     project = self.create_project()
    #     tag = self.create_tag()
    #     up = Project.objects.filter(id=1).update(actual_design=F('actual_design')+1)
    #     # up.refresh_from_db()
    #     self.assertEqual(up.id, 4)

        #
        # update_project = self.authenticated_client.post(
        #     reverse('project-update', kwargs={'pk': 1, 'slug': slugify('test-company')}),
        #     {
        #         'company': company,
        #         'title': 'test-company',
        #         'start_date': '2012-01-12',
        #         'end_date': '',
        #         'estimated_design': 1,
        #         'actual_design': 45,
        #         'estimated_development': 4,
        #         'actual_development': 3,
        #         'estimated_testing': 3,
        #         'actual_testing': 4,
        #         'tags': tag,
        #         'additional_hour_design': '',
        #         'additional_hour_development': '',
        #         'additional_hour_testing': '',
        #     }
        # )
        #
        # pdb.set_trace()
        # history = HistoryOfChanges.objects.get(project=update_project)

    def test_tags_list_requires_authentication(self):

        # All users can see the tags-list.
        # Anonymous user

        client = Client()
        response = client.get('/tags/')
        self.assertEqual(response.status_code, 200)

        # Authenticated client
        response = self.authenticated_client.get('/tags/')
        self.assertEqual(response.status_code, 200)

    def test_tag_create(self):

        # Anonymous users can't create tag

        client = Client()
        response = client.get('/tag/create/')
        self.assertRedirects(response, '/login/?next=/tag/create/')
        self.assertEqual(response.status_code, 302)

        # Authenticated users can create tag

        response = self.authenticated_client.post('/tag/create/', {
            'title': self.create_tag()
        })

        self.assertRedirects(response, '/tags/')

    def test_update_tag(self):

        # Anonymous users can't update tag

        client = Client()
        tag = self.create_tag()
        # pdb.set_trace()
        response = client.post(
            reverse('tag-edit', kwargs={'pk': tag.id}),
            {
                'title': 'django',
            }
        )
        self.assertEqual(tag.id, not None)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/login/?next=/tag/{tag.id}/edit/')

        tag.refresh_from_db()
        self.assertEqual(tag.title, 'python')

        # Authenticated users can update tag

        response = self.authenticated_client.post(
            reverse('tag-edit', kwargs={'pk': tag.id}),
            {
                'title': 'django',
            }
        )
        self.assertEqual(response.status_code, 302)

        tag.refresh_from_db()
        self.assertEqual(tag.title, 'django')

    def test_tag_delete(self):

        # Anonymous users can't delete tag

        client = Client()
        tag = self.create_tag()
        response = client.delete(
            reverse('tag-delete', kwargs={'pk': tag.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/login/?next=/tag/{tag.id}/delete/')

        tag.refresh_from_db()
        self.assertEqual(tag.title, 'python')

        # Authenticated users can delete tag
        #
        # response = self.authenticated_client.post(
        #     reverse('tag-delete', kwargs={'id': tag.id})
        # )
        # # remote_tag = self.authenticated_client.get(f'/tag/{tag.id}/delete/')
        #
        # self.assertEqual(tag.id, None )

    def test_add_tag_on_project(self):

        # self.company = create_company()
        self.response = self.create_project()
        self.assertEqual(self.response.status_code, 200)



