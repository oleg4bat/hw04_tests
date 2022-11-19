from django.test import TestCase

from ..models import SLICE_OF_TEXT, Group, Post, User


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
        text = PostModelTest.post.text[:SLICE_OF_TEXT]
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
