from django.test import TestCase

# Create your tests here.

import datetime
from django.utils import timezone
from .models import CourseTypes


class CourseTypesMethodTests(TestCase):

    def test_was_published_recently_with_future_courseType(self):
        """
        was_published_recently() should return False for courseTypes whose
        created_time is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_courseType = CourseTypes(created_time=time)
        self.assertEqual(future_courseType.was_published_recently(), False)

    def test_was_published_recently_with_old_courseType(self):
        """
        was_published_recently() should return False for courseTypes whose
        pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_courseType = CourseTypes(created_time=time)
        self.assertEqual(old_courseType.was_published_recently(), False)

    def test_was_published_recently_with_recent_courseType(self):
        """
        was_published_recently() should return True for courseTypes whose
        pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_courseType = CourseTypes(created_time=time)
        self.assertEqual(recent_courseType.was_published_recently(), True)
