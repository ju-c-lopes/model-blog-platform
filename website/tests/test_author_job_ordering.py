from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from website.models.author.AuthorModel import Author
from website.models.author.JobsModel import Job

User = get_user_model()


class AuthorJobOrderingTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="joborder", email="joborder@test.com", password="pw")
        self.author = Author.objects.create(user=user, author_name="Job Order", author_url_slug="job-order")

    def test_get_jobs_orders_by_start_date_most_recent_first(self):
        Job.objects.create(
            employee=self.author,
            occupation="Older Role",
            company="Co A",
            start_date=date(2020, 3, 1),
        )
        Job.objects.create(
            employee=self.author,
            occupation="Newer Role",
            company="Co B",
            start_date=date(2020, 9, 1),
        )

        jobs = list(self.author.get_jobs())
        self.assertEqual(jobs[0].occupation, "Newer Role")
        self.assertEqual(jobs[1].occupation, "Older Role")

    def test_current_job_matches_get_current_job_when_multiple_current(self):
        Job.objects.create(
            employee=self.author,
            occupation="Earlier Current",
            company="Co A",
            start_date=date(2021, 1, 1),
            current_job=True,
        )
        newer = Job.objects.create(
            employee=self.author,
            occupation="Latest Current",
            company="Co B",
            start_date=date(2022, 6, 1),
            current_job=True,
        )

        self.assertEqual(self.author.get_current_job(), newer)
        self.assertEqual(self.author.current_job, newer)
