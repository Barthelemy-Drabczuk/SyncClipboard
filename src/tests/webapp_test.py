import pytest
import json
from unittest.mock import Mock, patch, MagicMock

from webapp import app, db
from clip_user import ClipUser


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_db():
    """Mock the database"""
    with patch('webapp.db') as mock:
        yield mock


def test_index_route(client):
    """Test the index route returns the HTML page"""
    response = client.get('/')
    assert response.status_code == 200


def test_register_success(client, mock_db):
    """Test successful user registration"""
    mock_db.insert_user.return_value = mock_db
    mock_db.get_user.return_value = None

    response = client.post('/api/register',
                          data=json.dumps({
                              'username': 'testuser',
                              'password': 'testpass',
                              'email': 'test@example.com'
                          }),
                          content_type='application/json')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'user_id' in data
    assert data['username'] == 'testuser'


def test_login_success(client, mock_db):
    """Test successful user login"""
    test_user = ClipUser('testuser', 'testpass', 'test@example.com')
    mock_db.get_user.return_value = test_user

    response = client.post('/api/login',
                          data=json.dumps({
                              'username': 'testuser',
                              'password': 'testpass'
                          }),
                          content_type='application/json')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['username'] == 'testuser'


def test_login_failure(client, mock_db):
    """Test failed user login with invalid credentials"""
    mock_db.get_user.return_value = None

    response = client.post('/api/login',
                          data=json.dumps({
                              'username': 'testuser',
                              'password': 'wrongpass'
                          }),
                          content_type='application/json')

    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['success'] is False


def test_add_clipboard(client, mock_db):
    """Test adding a clipboard entry"""
    mock_db.insert_transaction.return_value = mock_db

    response = client.post('/api/clipboard',
                          data=json.dumps({
                              'user_id': 123,
                              'content': 'test clipboard content'
                          }),
                          content_type='application/json')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True


def test_add_clipboard_missing_data(client):
    """Test adding clipboard with missing data"""
    response = client.post('/api/clipboard',
                          data=json.dumps({
                              'user_id': 123
                          }),
                          content_type='application/json')

    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False


def test_get_clipboard_history(client, mock_db):
    """Test getting clipboard history"""
    mock_transactions = [
        {'content': 'item1', 'timestamp': 1234567890},
        {'content': 'item2', 'timestamp': 1234567891}
    ]
    mock_db.get_n_last_user_transaction.return_value = mock_transactions

    response = client.get('/api/clipboard/123?limit=10')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert len(data['history']) == 2
    assert data['history'][0]['content'] == 'item1'
