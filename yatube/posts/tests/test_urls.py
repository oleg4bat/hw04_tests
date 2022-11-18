from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='HasNoName')
        cls.user1 = User.objects.create_user(username='user')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client1 = Client()
        cls.authorized_client1.force_login(cls.user1)
        cls.authorized_client.force_login(cls.user)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/': 'posts/index.html',
            '/group/test-slug/': 'posts/group_list.html',
            '/profile/HasNoName/': 'posts/profile.html',
            '/posts/1/': 'posts/post_detail.html',
            '/posts/1/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_urls_exist_at_desired_location(self):
        """Страницы доступна любому пользователю."""
        urls = {
            '/': 200,
            '/group/test-slug/': 200,
            '/profile/HasNoName/': 200,
            '/posts/1/': 200,
            '/posts/1/edit/': 302,
            '/create/': 302,
        }
        for address, status in urls.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, status)

    def test_create_url_redirect_anonymous_on_login(self):
        response = PostURLTests.guest_client.get(
            '/create/', follow=True)
        self.assertRedirects(
            response, ('/auth/login/?next=/create/'))

    def test_post_edit_url_redirect_anonymous_on_login(self):
        response = PostURLTests.guest_client.get(
            '/posts/1/edit/', follow=True)
        self.assertRedirects(
            response, ('/auth/login/?next=/posts/1/edit/'))

    def test_post_edit_url_redirect_not_author_on_detail(self):
        response = PostURLTests.authorized_client1.get(
            '/posts/1/edit/', follow=True)
        self.assertRedirects(
            response, ('/posts/1/'))

    def test_unexisting_page(self):
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, 404)
