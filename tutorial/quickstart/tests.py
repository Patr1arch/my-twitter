from django.contrib.auth.models import User
from django.test import TestCase


# Create your tests here.
from tutorial.quickstart.models import FollowerFollows


class HelloTestCase(TestCase):
    def test_init(self):
        self.assertEqual(1 + 1, 2)


class UsersTestCase(TestCase):
    def test_unknown_url(self):
        self.assertEqual(self.client.get('/incorrect/').status_code, 404)

    def test_empty_request_list_user(self):
        response = self.client.get('/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "count": 0,
            "next": None,
            "previous": None,
            "results": []
        })

    def test_request_list_user_with_users_usernames(self):
        User.objects.create(username='Kelly')
        User.objects.create(username='John')
        response = self.client.get('/v1/users/')
        usernames = {row['username'] for row in response.json()['results']}
        self.assertEqual(usernames, {'Kelly', 'John'})

    def test_request_list_user_with_users(self):
        User.objects.create(username='Kelly')
        User.objects.create(username='John')
        response = self.client.get('/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {'email': '',
                 'first_name': '',
                 'last_name': '',
                 'url': 'http://testserver/v1/users/John/',
                 'username': 'John'},
                {'email': '',
                 'first_name': '',
                 'last_name': '',
                 'url': 'http://testserver/v1/users/Kelly/',
                 'username': 'Kelly'}
            ]
        })


class FollowTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='Kevin')
        self.user2 = User.objects.create(username='Tom')
        self.user3 = User.objects.create(username='Mo')
        FollowerFollows.objects.create(follower=self.user1, follows=self.user2)

    def test_data_exits(self):
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(FollowerFollows.objects.count(), 1)

    def test_new_follow_correct(self):
        self.client.force_login(self.user1)

        response = self.client.post(f'/v1/follow/{self.user3.username}/')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(FollowerFollows.objects.count(), 2)
        self.assertIsNotNone(FollowerFollows.objects.get(
            follower=self.user1,
            follows=self.user3
        ))

    def test_follow_yourself_failed(self):
        self.client.force_login(self.user1)
        response = self.client.post(f'/v1/follow/{self.user1.username}/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(FollowerFollows.objects.count(), 1)
        self.assertIsNone(FollowerFollows.objects.get(
            follower=self.user1,
            follows=self.user1
        ))

    def test_follow_duplicate_failed(self):
        self.client.force_login(self.user1)
        response = self.client.post(f'/v1/follow/{self.user2.username}/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(FollowerFollows.objects.count(), 1)

    def test_new_unfollow_correct(self):
        self.client.force_login(self.user1)
        response = self.client.delete(f'/v1/follow/{self.user2.username}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(FollowerFollows.objects.count(), 0)

    def test_unfollow_not_exists_return_fail(self):
        self.client.force_login(self.user1)
        response = self.client.delete(f'/v1/follow/{self.user2.username}/')
        self.assertEqual(response.status_code, 400)
