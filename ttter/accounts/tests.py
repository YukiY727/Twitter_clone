from django.test import TestCase
# from models import MyUser
from .views import UserDataInput
from django.urls import reverse, resolve
from .models import MyUser

class SignUpTests(TestCase):
    def setUp(self):
        self.url = reverse('accounts:create_data_input')

    def test_signup_get(self):
        response = self.client.get(self.url)
        # ユーザーがURL/signup/のページをGETすれば、ステータスコードは200、すなわち’成功’となる。
        self.assertEquals(response.status_code, 200)

    def test_successful_signup_post(self):
        data = {
            'username': 'new_user',
            'password1': 'testpass1',
            'password2': 'testpass1',
        }
        post_response = self.client.post(self.url, data=data)
        self.assertEquals(post_response.status_code, 200)
        mypostlist_url = reverse('accounts:create_confirm')
        # 'tweet:myposlist'にリダイレクトされることを確認
        self.assertRedirects(post_response, mypostlist_url)
        

        # Userオブジェクトが作成されていることを確認
        # self.assertTrue(MyUser.objects.exists())
        # ユーザーが認証済みであることを確認
        # get_response = self.client.get(mypostlist_url)
        # user = get_response.context.get('user')
        # self.assertTrue(user.is_authenticated)

    # def test_invalid_signup_post(self):
    #     # 無効なフォームを送信すると、同じページ（'accounts:signup'）にリダイレクトする
    #     response = self.client.post(self.url, {})
    #     self.assertEquals(response.status_code, 200)
    #     # エラーメッセージがあることを確認
    #     form = response.context.get('form')
    #     self.assertTrue(form.errors)
        # Userオブジェクトが作成されていないことを確認
        # self.assertFalse(MyUser.objects.exists())

    # def test_with_different_passwords(self):
    #     response = self.client.post(self.url, {'username': 'new_user', 'password1': 'testpass2', 'password2': 'testpass3'})
    #     self.assertFormError(response, 'form', 'password2', '確認用パスワードが一致しません。')

    # def test_with_short_passwords(self):
    #     response = self.client.post(self.url, {'username': 'new_user', 'password1': 'fghj39', 'password2': 'fghj39'})
    #     self.assertFormError(response, 'form', 'password2','このパスワードは短すぎます。最低 8 文字以上必要です。')

    # def test_with_easily_passwords(self):
    #     response = self.client.post(self.url, {'username': 'new_user', 'password1': 'abcd1234', 'password2': 'abcd1234'})
    #     self.assertFormError(response, 'form', 'password2','このパスワードは一般的すぎます。')

    # def test_with_existed_user(self):
    #     MyUser.objects.create_user('existing_user', '', 'testpass1')
    #     response = self.client.post(self.url, {'username': 'existing_user', 'password1': 'testpass1', 'password2': 'testpass1'})
    #     self.assertFormError(response, 'form', 'username','同じユーザー名が既に登録済みです。')