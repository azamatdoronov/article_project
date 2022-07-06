from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from webapp.factories import ArticleFactory
from webapp.models import Article


class ArticleViewTest(TestCase):

    def setUp(self) -> None:
        pass

    def test_articles_list(self):
        ArticleFactory.create_batch(10)
        url = reverse("index")
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(10, len(response.context.get("articles")))

    def test_search_articles_list(self):
        test_article = ArticleFactory(title="TestTitle")
        ArticleFactory.create_batch(10)
        url = reverse("index")
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(11, len(response.context.get("articles")))
        response = self.client.get(url + f"?search={test_article.title}")
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.context.get("articles")))
        self.assertEqual(test_article.title, response.context.get("articles")[0].title)

    def test_create_article(self):
        url = reverse("create_article")
        data = {"title": "test", "author": "test_author", "content": "test_content"}
        response = self.client.post(url, data=data)
        self.assertEqual(302, response.status_code)
        articles = Article.objects.all()
        self.assertEqual(1, articles.count())
        self.assertEqual("test", articles.first().title)

    def test_create_article_not_title(self):
        url = reverse("create_article")
        data = {"author": "test_author", "content": "test_content"}
        response = self.client.post(url, data=data)
        self.assertEqual(400, response.status_code)
        self.assertTemplateUsed(response, "index.html")
        self.assertTrue(b"This field is required." in response.content)

