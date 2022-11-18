from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def test_post_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post = PostModelTest.post
        text = PostModelTest.post.text[:15]
        self.assertEqual(
            str(post), text, '__str__ выводит неправильную инфомацию'
        )

    def test_group_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        title = PostModelTest.group.title
        group = PostModelTest.group
        self.assertEqual(
            str(group), title, '__str__ выводит неправильную инфомацию'
        )
