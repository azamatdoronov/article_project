import factory.fuzzy

from webapp.models import Article


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article

    title = factory.Faker("name")
    author = factory.Sequence(lambda n: f"author-{n}")
    content = factory.Faker("text")
