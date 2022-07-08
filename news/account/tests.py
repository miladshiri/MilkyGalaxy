import pytest

from django.urls import reverse

@pytest.mark.django_db
def test_register_api(client):
    url = reverse('register')

    payload = dict(
        username = 'username_test',
        password = 'password_test',
        first_name = 'firstname_test', 
        last_name = 'lastname_test')

    response = client.post(url, payload)
    assert response.data['user']['first_name'] == payload['first_name']
    assert response.data['user']['last_name'] == payload['last_name']


@pytest.mark.django_db
def test_token_api_success(client):
    url = reverse('register')
    payload = dict(
        username = 'username_test',
        password = 'password_test',
        first_name = 'firstname_test', 
        last_name = 'lastname_test')
    response = client.post(url, payload)
    
    url = reverse('token_obtain_pair')
    payload = dict(
        username = 'username_test',
        password = 'password_test'
    )

    response = client.post(url, payload)
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data

@pytest.mark.django_db
def test_token_api_fail(client):
    url = reverse('token_obtain_pair')
    payload = dict(
        username = 'username_test',
        password = 'password_test'
    )

    response = client.post(url, payload)
    assert response.status_code == 401
    assert 'access' not in response.data
    assert 'refresh' not in response.data
