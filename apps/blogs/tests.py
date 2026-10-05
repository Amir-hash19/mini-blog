from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.blogs.models import Post


class PostViewsTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        self.post = Post.objects.create(
            author=self.user,
            content="Test content",
            status=Post.Status.DRAFT,
        )

        self.client.force_authenticate(user=self.user)

    def test_create_post(self):
        url = reverse("create-post")

        data = {
            "content": "New post content",
            "status": Post.Status.DRAFT,
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Post.objects.count(), 2)

    def test_get_post_detail(self):
        url = reverse("post-detail", kwargs={"post_id": self.post.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["content"], self.post.content)

        self.assertEqual(response.data["author"], self.user.username)

    def test_update_post(self):
        url = reverse("post-update", kwargs={"post_id": self.post.id})

        data = {
            "content": "Updated content",
            "status": Post.Status.DRAFT,
        }

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.post.refresh_from_db()

        self.assertEqual(self.post.content, "Updated content")

    def test_delete_post(self):
        url = reverse("post-detail", kwargs={"post_id": self.post.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Post.objects.filter(id=self.post.id).exists())
