from django.contrib.auth import SESSION_KEY, get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from ttter import settings

from .models import FriendShip

User = get_user_model()


class SignUpTests(TestCase):
    def setUp(self):
        self.url_input = reverse("accounts:user_data_input")
        self.url_confirm = reverse("accounts:user_data_confirm")
        self.url_create = reverse("accounts:user_data_create")
        self.data = {
            "username": "newuser",
            "password1": "testpass1",
            "password2": "testpass1",
            "email": "newuser@mail.com",
            "nickname": "nu",
            "date_of_birth": "2000-01-01",
        }

    def test_signup_get(self):
        response = self.client.get(self.url_input)
        # ユーザーがURL/signup/のページをGETすれば、ステータスコードは200、すなわち’成功’となる。
        self.assertEquals(response.status_code, 200)

    def test_successful_signup_post(self):
        post_response = self.client.post(self.url_confirm, data=self.data)
        self.assertEquals(post_response.status_code, 200)
        self.assertTemplateUsed(post_response, "accounts/create_confirm.html")

    def test_data_confirm(self):
        confirm_response = self.client.post(self.url_confirm, data=self.data)
        self.assertEqual(confirm_response.status_code, 200)
        self.assertTemplateUsed(confirm_response, "accounts/create_confirm.html")
        self.assertContains(confirm_response, "newuser")
        self.assertContains(confirm_response, "testpass1")
        self.assertContains(confirm_response, "newuser@mail.com")
        self.assertContains(confirm_response, "nu")
        self.assertContains(confirm_response, "2000-01-01")

    def test_data_create(self):
        create_response = self.client.post(self.url_create, self.data)
        self.assertTrue(User.objects.exists())
        base_url = reverse("tweet:home")
        self.assertRedirects(create_response, base_url)

    def test_empty_data(self):
        empty_data = {
            "username": "",
            "password1": "",
            "password2": "",
            "email": "",
            "nickname": "",
            "date_of_birth": "",
        }
        empty_data_response = self.client.post(self.url_confirm, data=empty_data)
        self.assertTemplateUsed(empty_data_response, "accounts/create.html")
        self.assertEqual(empty_data_response.status_code, 200)
        self.assertFalse(User.objects.exists())
        self.assertFormError(empty_data_response, "form", "username", "このフィールドは必須です。")
        self.assertFormError(empty_data_response, "form", "password1", "このフィールドは必須です。")
        self.assertFormError(empty_data_response, "form", "password2", "このフィールドは必須です。")
        self.assertFormError(empty_data_response, "form", "email", "このフィールドは必須です。")
        self.assertFormError(empty_data_response, "form", "nickname", "このフィールドは必須です。")

    def test_empty_username(self):
        empty_username = {
            "username": "",
            "password1": "testpass1",
            "password2": "testpass1",
            "email": "newuser@mail.com",
            "nickname": "nu",
            "date_of_birth": "2000-01-01",
        }
        empty_name_response = self.client.post(self.url_confirm, data=empty_username)
        self.assertEqual(empty_name_response.status_code, 200)
        self.assertFalse(User.objects.exists())
        self.assertFormError(empty_name_response, "form", "username", "このフィールドは必須です。")

    def test_short_password(self):
        short_password = {
            "username": "username",
            "password1": "acd",
            "password2": "acd",
            "email": "newuser@mail.com",
            "nickname": "nu",
            "date_of_birth": "2000-01-01",
        }
        short_password_response = self.client.post(
            self.url_confirm, data=short_password
        )
        self.assertEqual(short_password_response.status_code, 200)
        self.assertFalse(User.objects.exists())
        self.assertFormError(
            short_password_response, "form", "password2", "このパスワードは短すぎます。最低 8 文字以上必要です。"
        )

    def test_false_email(self):
        false_email = {
            "username": "newuser",
            "password1": "testpass1",
            "password2": "testpass1",
            "email": "hogehoge",
            "nickname": "nu",
            "date_of_birth": "2000-01-01",
        }
        false_email_response = self.client.post(self.url_confirm, data=false_email)
        self.assertEqual(false_email_response.status_code, 200)
        self.assertFalse(User.objects.exists())
        self.assertFormError(
            false_email_response, "form", "email", "有効なメールアドレスを入力してください。"
        )

    def test_different_password(self):
        different_password = {
            "username": "newuser",
            "password1": "testpass1",
            "password2": "testpass2",
            "email": "newuser@mail.com",
            "nickname": "nu",
            "date_of_birth": "2000-01-01",
        }
        different_password_response = self.client.post(
            self.url_confirm, data=different_password
        )
        self.assertEqual(different_password_response.status_code, 200)
        self.assertFalse(User.objects.exists())
        self.assertFormError(
            different_password_response, "form", "password2", "確認用パスワードが一致しません。"
        )

    def test_false_datebirth(self):
        different_password = {
            "username": "newuser",
            "password1": "testpass1",
            "password2": "testpass1",
            "email": "newuser@mail.com",
            "nickname": "nu",
            "date_of_birth": "2-01-01",
        }
        false_datebirth_response = self.client.post(
            self.url_confirm, data=different_password
        )
        self.assertEqual(false_datebirth_response.status_code, 200)
        self.assertFalse(User.objects.exists())
        self.assertFormError(
            false_datebirth_response, "form", "date_of_birth", "日付を正しく入力してください。"
        )

    def test_duplicate_username_and_email(self):
        data = {
            "username": "newuser",
            "password1": "testpass1",
            "password2": "testpass1",
            "email": "newuser@mail.com",
            "nickname": "nu",
            "date_of_birth": "2000-01-01",
        }
        User.objects.create_user(
            username="newuser", email="newuser@mail.com", password="testpass1"
        )
        data2_response = self.client.post(self.url_confirm, data=data)
        self.assertEqual(data2_response.status_code, 200)
        self.assertFormError(
            data2_response, "form", "username", "この Username を持った My user が既に存在します。"
        )
        self.assertFormError(
            data2_response, "form", "email", "この Email を持った My user が既に存在します。"
        )

    def test_simple_password(self):
        simple_password_data = {
            "username": "newuser",
            "password1": "abcdefgh",
            "password2": "abcdefgh",
            "email": "newuser@mail.com",
            "nickname": "nu",
            "date_of_birth": "2000-01-01",
        }
        simple_password_response = self.client.post(
            self.url_confirm, data=simple_password_data
        )
        self.assertEqual(simple_password_response.status_code, 200)
        self.assertFormError(
            simple_password_response, "form", "password2", "このパスワードは一般的すぎます。"
        )
        self.assertFalse(User.objects.exists())


class TestLoginView(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="test", email="test@ed.jp", password="t12e12s12t"
        )
        self.url = reverse(settings.LOGIN_URL)

    def test_success_get(self):
        response_get = self.client.get(self.url)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "accounts/login.html")

    def test_success_post(self):
        data = {"username": "test@ed.jp", "password": "t12e12s12t"}
        response_post = self.client.post(self.url, data=data)
        self.assertRedirects(response_post, reverse(settings.LOGIN_REDIRECT_URL))
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_not_exists_user(self):
        data_not_exist = {"username": "ないよーが内容", "password": "アルミ缶のうえにあるみかん"}
        response_post = self.client.post(self.url, data=data_not_exist)
        self.assertEquals(response_post.status_code, 200)
        self.assertFormError(
            response_post,
            "form",
            "",
            "正しいEmailとパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。",
        )
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_password(self):
        data = {"username": "test@ed.jp", "password": ""}
        response_post = self.client.post(self.url, data=data)
        self.assertEquals(response_post.status_code, 200)
        self.assertFormError(response_post, "form", "password", "このフィールドは必須です。")
        self.assertNotIn(SESSION_KEY, self.client.session)


class TestLogoutView(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="test", email="test@ed.jp", password="t12e12s12t"
        )
        self.client.login(username="test", password="t12e12s12t")

    def test_success_logout(self):
        response = self.client.get(reverse("accounts:logout"))
        self.assertNotIn(SESSION_KEY, self.client.session)
        self.assertRedirects(
            response,
            reverse(settings.LOGOUT_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
        )


class TestUserProfilesView(TestCase):
    def setUp(self):
        data = {
            "username": "testuser",
            "password": "testpassword",
            "email": "test@co.jp",
        }
        self.user = User.objects.create_user(**data)
        self.client.force_login(self.user)

    def test_success_get(self):
        response = self.client.get(
            reverse("accounts:user_page", kwargs={"username": self.user.username})
        )
        self.assertEqual(response.context["followee_count"], self.user.followee.count())
        self.assertEqual(response.context["follower_count"], self.user.follower.count())


class TestFollowView(TestCase):
    def setUp(self):
        data1 = {
            "username": "testuser1",
            "password": "testpassword",
            "email": "test1@co.jp",
        }
        data2 = {
            "username": "testuser2",
            "password": "testpassword",
            "email": "test2@co.jp",
        }
        self.user1 = User.objects.create_user(**data1)
        self.user2 = User.objects.create_user(**data2)
        self.client.force_login(self.user1)

    def test_success_get(self):
        response = self.client.get(
            reverse("accounts:follow", kwargs={"username": self.user1.username})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/follow.html")

    def test_success_post(self):
        self.assertFalse(
            FriendShip.objects.filter(followee=self.user1, follower=self.user2).exists()
        )
        response = self.client.post(
            reverse("accounts:follow", kwargs={"username": self.user2.username})
        )

        self.assertRedirects(
            response,
            reverse("tweet:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertTrue(
            FriendShip.objects.filter(followee=self.user1, follower=self.user2).exists()
        )

    def test_failure_post_with_not_exist_user(self):
        response = self.client.post(
            reverse("accounts:follow", kwargs={"username": "test"})
        )
        self.assertFalse(
            FriendShip.objects.filter(followee=self.user1, follower=self.user2).exists()
        )
        self.assertEqual(response.status_code, 404)
        self.assertFalse(FriendShip.objects.exists())

    def test_failure_post_with_self(self):
        self.assertFalse(
            FriendShip.objects.filter(followee=self.user1, follower=self.user1).exists()
        )
        response = self.client.post(
            reverse("accounts:follow", kwargs={"username": self.user1.username})
        )

        self.assertRedirects(
            response,
            reverse("tweet:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertFalse(FriendShip.objects.exists())
        self.assertEqual(
            "自分自身はフォローできません。", list(get_messages(response.wsgi_request))[0].message
        )
        self.assertFalse(
            FriendShip.objects.filter(followee=self.user1, follower=self.user2).exists()
        )


class TestUnfollowView(TestCase):
    def setUp(self):
        data1 = {
            "username": "testuser1",
            "password": "testpassword",
            "email": "test1@co.jp",
        }
        data2 = {
            "username": "testuser2",
            "password": "testpassword",
            "email": "test2@co.jp",
        }
        self.user1 = User.objects.create_user(**data1)
        self.user2 = User.objects.create_user(**data2)
        FriendShip.objects.create(followee=self.user1, follower=self.user2)
        self.client.force_login(self.user1)

    def test_success_get(self):
        response = self.client.get(
            reverse("accounts:unfollow", kwargs={"username": self.user1.username})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/unfollow.html")

    def test_success_post(self):
        self.assertTrue(FriendShip.objects.filter(followee=self.user1, follower=self.user2))
        response = self.client.post(
            reverse("accounts:unfollow", kwargs={"username": self.user2.username})
        )

        self.assertRedirects(
            response,
            reverse("tweet:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertFalse(FriendShip.objects.exists())

    def test_failure_post_with_not_exist_user(self):
        self.assertTrue(
            FriendShip.objects.filter(followee=self.user1, follower=self.user2).exists()
        )
        response = self.client.post(
            reverse("accounts:unfollow", kwargs={"username": "test"})
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            FriendShip.objects.filter(followee=self.user1, follower=self.user2).exists()
        )

    def test_failure_post_with_incorrect_user(self):
        self.assertTrue(
            FriendShip.objects.filter(followee=self.user1, follower=self.user2).exists()
        )
        response = self.client.post(
            reverse("accounts:unfollow", kwargs={"username": self.user1})
        )
        self.assertRedirects(
            response,
            reverse("tweet:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertTrue(
            FriendShip.objects.filter(followee=self.user1, follower=self.user2).exists()
        )
        self.assertIn(
            "自分自身のフォロー解除はできません。", list(get_messages(response.wsgi_request))[0].message
        )


class TestFollowingListView(TestCase):
    def setUp(self):
        data = {
            "username": "testuser",
            "email": "test@co.jp",
        }
        data_follow = {
            "username": "followuser",
            "email": "follow@co.jp",
        }
        self.user = User.objects.create_user(**data)
        self.client.force_login(self.user)
        self.follow_user = User.objects.create_user(**data_follow)
        self.client.force_login(self.follow_user)

    def test_success_get(self):
        response = self.client.get(
            reverse("accounts:following_list", kwargs={"username": self.user.username})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/following_list.html")
        self.assertQuerysetEqual(
            response.context["followings"],
            self.user.followees.all(),
        )

    def test_success_get_following_list(self):
        response_before_follow = self.client.get(
            reverse("accounts:following_list", kwargs={"username": self.user.username})
        )
        self.assertQuerysetEqual(
            response_before_follow.context["followings"],
            self.user.followees.all(),
        )
        FriendShip.objects.create(followee=self.user, follower=self.follow_user)
        response_after_follow = self.client.get(
            reverse("accounts:following_list", kwargs={"username": self.user.username})
        )
        self.assertQuerysetEqual(
            response_after_follow.context["followings"],
            self.user.followers.all(),
        )


class TestFollowerListView(TestCase):
    def setUp(self):
        data = {
            "username": "testuser",
            "email": "test@co.jp",
        }
        data_follow = {
            "username": "followuser",
            "email": "follow@co.jp",
        }
        self.user = User.objects.create_user(**data)
        self.client.force_login(self.user)
        self.follow_user = User.objects.create_user(**data_follow)
        self.client.force_login(self.follow_user)

    def test_success_get(self):
        response = self.client.get(
            reverse("accounts:follower_list", kwargs={"username": self.follow_user.username})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/follower_list.html")
        self.assertQuerysetEqual(
            response.context["followers"],
            self.user.followees.all(),
        )

    def test_success_get_follower_list(self):
        response_before_follow = self.client.get(
            reverse("accounts:following_list", kwargs={"username": self.follow_user.username})
        )
        self.assertQuerysetEqual(
            response_before_follow.context["followings"],
            self.user.followees.all(),
        )
        FriendShip.objects.create(followee=self.follow_user, follower=self.user)
        response_after_follow = self.client.get(
            reverse("accounts:follower_list", kwargs={"username": self.follow_user.username})
        )
        self.assertQuerysetEqual(
            response_after_follow.context["followers"],
            self.follow_user.followees.all(),
        )
