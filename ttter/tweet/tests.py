import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Tweet

User = get_user_model()


class TestTweetCreateView(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="test", email="test@mail.com", password="test"
        )
        self.client.login(username="test@mail.com", password="test")

    def test_success_get(self):
        response_get = self.client.get(reverse("tweet:tweet_create"))
        self.assertEquals(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "tweet/tweet_create.html")

    def test_success_post(self):
        test_data = {"content": "ぞうがくる像"}
        response_post = self.client.post(reverse("tweet:tweet_create"), test_data)
        tweet = Tweet.objects.get(content="ぞうがくる像")
        self.assertRedirects(
            response_post,
            reverse("tweet:home"),
            status_code=302,
            target_status_code=200,
        )

        self.assertTrue(Tweet.objects.exists())
        self.assertEquals(tweet.content, test_data["content"])

    def test_failure_post_with_empty_content(self):
        data_empty = {"content": ""}
        response_empty = self.client.post(reverse("tweet:tweet_create"), data_empty)
        self.assertFalse(Tweet.objects.exists())
        self.assertFormError(response_empty, "form", "content", "このフィールドは必須です。")

    def test_failure_post_with_too_long_content(self):
        data_too_long = {"content": "a" * 201}
        response_too_long = self.client.post(
            reverse("tweet:tweet_create"), data_too_long
        )
        self.assertFalse(Tweet.objects.exists())
        self.assertFormError(
            response_too_long,
            "form",
            "content",
            "この値は 200 文字以下でなければなりません( 201 文字になっています)。",
        )


class TestTweetDetailView(TestCase):
    def test_success_get(self):
        User.objects.create_user(
            username="test", email="test@mail.com", password="test"
        )
        self.client.login(username="test@mail.com", password="test")
        data = {"content": "秋田に来た"}
        self.client.post(reverse("tweet:tweet_create"), data)
        tweet = Tweet.objects.get(content="秋田に来た")
        response_get = self.client.get(
            reverse("tweet:tweet_detail", kwargs={"pk": tweet.pk})
        )
        self.assertEquals(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "tweet/tweet_detail.html")
        self.assertContains(response_get, data["content"])


class TestTweetDeleteView(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="test", email="test@mail.com", password="test"
        )
        self.client.login(username="test@mail.com", password="test")
        data = {"content": "かもがくるかも"}
        self.client.post(reverse("tweet:tweet_create"), data)

    def test_success_post(self):
        tweet = Tweet.objects.get(content="かもがくるかも")
        response_post = self.client.post(
            reverse("tweet:tweet_delete", kwargs={"pk": tweet.pk})
        )
        self.assertRedirects(
            response_post,
            reverse("tweet:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertFalse(Tweet.objects.filter(content="かもがくるかも").exists())

    def test_failure_post_with_not_exist_tweet(self):
        response = self.client.post(
            reverse("tweet:tweet_delete", kwargs={"pk": str(uuid.uuid4())})
        )
        self.assertEquals(response.status_code, 404)
        self.assertTrue(Tweet.objects.filter(content="かもがくるかも").exists())

    def test_failure_post_with_incorrect_user(self):
        user = User.objects.create_user(
            username="test2", email="test2@mail.com", password="test2"
        )

        Tweet.objects.create(user=user, content="おーいお茶")
        tweet = Tweet.objects.get(content="おーいお茶")
        response = self.client.post(
            reverse("tweet:tweet_delete", kwargs={"pk": tweet.pk})
        )
        self.assertEquals(response.status_code, 403)
        self.assertTrue(Tweet.objects.filter(content="かもがくるかも").exists())
