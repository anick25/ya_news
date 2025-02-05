import pytest as pytest

from django.urls import reverse

from yanews.settings import NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_count(client, many_news):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, many_news):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comments_order(many_comments, client, news):
    detail_url = reverse('news:detail', args=(news.id,))
    response = client.get(detail_url)
    news_on_page = response.context['news']
    all_comments = news_on_page.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, news):
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert 'form' not in response.context


def test_authorized_client_has_form(author_client, news):
    url = reverse('news:detail', args=(news.id,))
    response = author_client.get(url)
    assert 'form' in response.context
