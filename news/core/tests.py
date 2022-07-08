import pytest

from django.urls import reverse

from .models import Article, Channel
from .serializers import ArticleSerializer, ChannelSerializer

@pytest.mark.django_db
def test_list_articles_all(client):
    url = reverse('articles')
    response = client.get(url)
    articles = Article.objects.all()
    expected_data = ArticleSerializer(articles, many=True).data

    assert response.status_code == 200
    assert response.data == expected_data


@pytest.mark.django_db
def test_list_channels_all(client):
    url = reverse('channels')
    response = client.get(url)
    channels = Channel.objects.all()
    expected_data = ChannelSerializer(channels, many=True).data

    assert response.status_code == 200
    assert response.data == expected_data


@pytest.mark.django_db
def test_add_channel_api(client):
    url = reverse('register')
    payload = dict(
        username = 'username_test',
        password = 'password_test',
        first_name = 'firstname_test', 
        last_name = 'lastname_test')
    client.post(url, payload)
    
    url = reverse('token_obtain_pair')
    payload = dict(
        username = 'username_test',
        password = 'password_test'
    )
    response = client.post(url, payload)
    token = response.data['access']
    
    url = reverse('channels')
    payload = {'name': 'channel_test'}
    headers = {
        'HTTP_AUTHORIZATION': 'Bearer {}'.format(token) 
    }
    
    response = client.post(url, payload, **headers)
    assert 'id' in response.data
    