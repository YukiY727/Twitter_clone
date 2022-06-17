from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class SignUpTests(TestCase):
    def setUp(self):
        self.url_input = reverse('accounts:user_data_input')
        self.url_confirm = reverse('accounts:user_data_confirm')
        self.url_create = reverse('accounts:user_data_create')
        self.data = {
            'username': 'newuser',
            'password1': 'testpass1',
            'password2': 'testpass1',
            'email': 'newuser@mail.com',
            'nickname': 'nu',
            'date_of_birth': '2000-01-01',
        }

    def test_signup_get(self):
        response = self.client.get(self.url_input)
        # ユーザーがURL/signup/のページをGETすれば、ステータスコードは200、すなわち’成功’となる。
        self.assertEquals(response.status_code, 200)

    def test_successful_signup_post(self):
        post_response = self.client.post(self.url_confirm, data=self.data)
        self.assertEquals(post_response.status_code, 200)
        self.assertTemplateUsed(post_response, 'accounts/create_confirm.html')

    def test_data_confirm(self):
        confirm_response = self.client.post(self.url_confirm, data=self.data)
        self.assertEqual(confirm_response.status_code, 200)
        self.assertTemplateUsed(
            confirm_response, 'accounts/create_confirm.html')
        self.assertContains(confirm_response, 'newuser')
        self.assertContains(confirm_response, 'testpass1')
        self.assertContains(confirm_response, 'newuser@mail.com')
        self.assertContains(confirm_response, 'nu')
        self.assertContains(confirm_response, '2000-01-01')

    def test_data_create(self):
        create_response = self.client.post(self.url_create, self.data)
        self.assertTrue(User.objects.exists())
        base_url = reverse('base:top')
        self.assertRedirects(create_response, base_url)

    def test_empty_data(self):
        empty_data = {
            'username': '',
            'password1': '',
            'password2': '',
            'email': '',
            'nickname': '',
            'date_of_birth': '',
        }
        empty_data_response = self.client.post(
            self.url_confirm, data=empty_data)
        self.assertTemplateUsed(empty_data_response, 'accounts/create.html')
        self.assertEqual(empty_data_response.status_code, 200)
        self.assertFalse(User.objects.exists())
        self.assertFormError(empty_data_response, 'form',
                             'username', 'このフィールドは必須です。')
        self.assertFormError(empty_data_response, 'form',
                             'password1', 'このフィールドは必須です。')
        self.assertFormError(empty_data_response, 'form',
                             'password2', 'このフィールドは必須です。')
        self.assertFormError(empty_data_response, 'form',
                             'email', 'このフィールドは必須です。')
        self.assertFormError(empty_data_response, 'form',
                             'nickname', 'このフィールドは必須です。')

    def test_empty_username(self):
        empty_username = {
            'username': '',
            'password1': 'testpass1',
            'password2': 'testpass1',
            'email': 'newuser@mail.com',
            'nickname': 'nu',
            'date_of_birth': '2000-01-01',
        }
        empty_name_response = self.client.post(
            self.url_confirm, data=empty_username)
        self.assertEqual(empty_name_response.status_code, 200)
        self.assertFalse(User.objects.exists())
        self.assertFormError(empty_name_response, 'form',
                             'username', 'このフィールドは必須です。')

    def test_short_password(self):
        short_password = {
            'username': 'username',
            'password1': 'acd',
            'password2': 'acd',
            'email': 'newuser@mail.com',
            'nickname': 'nu',
            'date_of_birth': '2000-01-01',
        }
        short_password_response = self.client.post(
            self.url_confirm, data=short_password)
        self.assertEqual(short_password_response.status_code, 200)
        self.assertFalse(User.objects.exists())
        self.assertFormError(short_password_response, 'form',
                             'password2', 'このパスワードは短すぎます。最低 8 文字以上必要です。')

    def test_false_email(self):
        false_email = {
            'username': 'newuser',
            'password1': 'testpass1',
            'password2': 'testpass1',
            'email': 'hogehoge',
            'nickname': 'nu',
            'date_of_birth': '2000-01-01',
        }
        false_email_response = self.client.post(
            self.url_confirm, data=false_email)
        self.assertEqual(false_email_response.status_code, 200)
        self.assertFalse(User.objects.exists())
        self.assertFormError(false_email_response, 'form',
                             'email', '有効なメールアドレスを入力してください。')

    def test_different_password(self):
        different_password = {
            'username': 'newuser',
            'password1': 'testpass1',
            'password2': 'testpass2',
            'email': 'newuser@mail.com',
            'nickname': 'nu',
            'date_of_birth': '2000-01-01',
        }
        different_password_response = self.client.post(
            self.url_confirm, data=different_password)
        self.assertEqual(different_password_response.status_code, 200)
        self.assertFalse(User.objects.exists())
        self.assertFormError(different_password_response,
                             'form', 'password2', '確認用パスワードが一致しません。')

    def test_false_datebirth(self):
        different_password = {
            'username': 'newuser',
            'password1': 'testpass1',
            'password2': 'testpass1',
            'email': 'newuser@mail.com',
            'nickname': 'nu',
            'date_of_birth': '2-01-01',
        }
        false_datebirth_response = self.client.post(
            self.url_confirm, data=different_password)
        self.assertEqual(false_datebirth_response.status_code, 200)
        self.assertFalse(User.objects.exists())
        self.assertFormError(false_datebirth_response,
                             'form', 'date_of_birth', '日付を正しく入力してください。')

    def test_duplicate_username_and_email(self):
        data = {
            'username': 'newuser',
            'password1': 'testpass1',
            'password2': 'testpass1',
            'email': 'newuser@mail.com',
            'nickname': 'nu',
            'date_of_birth': '2000-01-01',
        }
        User.objects.create_user(
            username="newuser", email="newuser@mail.com", password="testpass1")
        data2_response = self.client.post(self.url_confirm, data=data)
        self.assertEqual(data2_response.status_code, 200)
        self.assertFormError(data2_response,
                             'form', 'username', 'この Username を持った My user が既に存在します。')
        self.assertFormError(data2_response,
                             'form', 'email', 'この Email を持った My user が既に存在します。')

    def test_simple_password(self):
        simple_password_data = {
            'username': 'newuser',
            'password1': 'abcdefgh',
            'password2': 'abcdefgh',
            'email': 'newuser@mail.com',
            'nickname': 'nu',
            'date_of_birth': '2000-01-01',
        }
        simple_password_response = self.client.post(
            self.url_confirm, data=simple_password_data)
        self.assertEqual(simple_password_response.status_code, 200)
        self.assertFormError(simple_password_response,
                             'form', 'password2', 'このパスワードは一般的すぎます。')
        error_message = simple_password_response.context.get('form')
        print(error_message.errors)
        self.assertFalse(User.objects.exists())

    def test_short_password(self):
        short_password_data = {
            'username': 'newuser',
            'password1': 'fg',
            'password2': 'fg',
            'email': 'newuser@mail.com',
            'nickname': 'nu',
            'date_of_birth': '2000-01-01',
        }
        short_password_response = self.client.post(
            self.url_confirm, data=short_password_data)
        self.assertEqual(short_password_response.status_code, 200)
        self.assertFormError(short_password_response, 'form',
                             'password2', 'このパスワードは短すぎます。最低 8 文字以上必要です。')
