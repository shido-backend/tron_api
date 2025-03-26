import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models import Base, WalletQuery
from app.api.dependencies import get_db
from datetime import datetime, timedelta
from app.schemas import WalletQueryCreate
from unittest.mock import patch

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def test_client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client

TEST_WALLET_ADDRESS = "TNPeeaaFB7K9cmo4uQpcU32zGK8G1NYqeL"
MOCK_WALLET_INFO = {
    "address": TEST_WALLET_ADDRESS,
    "bandwidth": 1000,
    "energy": 500,
    "trx_balance": 10.5
}

@pytest.fixture
def mock_tron_service():
    with patch("app.services.tron.TronService") as mock:
        mock_instance = mock.return_value
        mock_instance.get_wallet_info.return_value = MOCK_WALLET_INFO
        yield mock_instance

def test_get_wallet_info_success(test_client, mock_tron_service, db_session):
    request_data = {"wallet_address": TEST_WALLET_ADDRESS}

    response = test_client.post("/api/wallet-info/", json=request_data)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["address"] == TEST_WALLET_ADDRESS
    assert "id" in response_data
    assert "created_at" in response_data

    db_record = db_session.query(WalletQuery).first()
    assert db_record is not None
    assert db_record.address == TEST_WALLET_ADDRESS

def test_get_wallet_info_invalid_address(test_client, mock_tron_service):
    mock_tron_service.get_wallet_info.side_effect = Exception("Invalid address")
    
    request_data = {"wallet_address": "invalid_address"}
    response = test_client.post("/api/wallet-info/", json=request_data)
    
    assert response.status_code == 503
    assert "API request failed" in response.json()["detail"]

def test_get_query_history_empty(test_client, db_session):
    response = test_client.get("/api/query-history/")
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["total"] == 0
    assert response_data["page"] == 1
    assert response_data["per_page"] == 10
    assert len(response_data["items"]) == 0

def test_get_query_history_with_data(test_client, db_session):

    test_records = [
        WalletQuery(
            address=f"address_{i}",
            bandwidth=100 * i,
            energy=50 * i,
            trx_balance=1.0 * i,
            created_at=datetime.now() - timedelta(minutes=i)
        )
        for i in range(1, 15)
    ]
    db_session.add_all(test_records)
    db_session.commit()

    response = test_client.get("/api/query-history/?page=2&per_page=5")
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["total"] == 14
    assert response_data["page"] == 2
    assert response_data["per_page"] == 5
    assert len(response_data["items"]) == 5
    assert response_data["items"][0]["address"] == "address_6"

def test_get_query_history_invalid_pagination(test_client):
    response = test_client.get("/api/query-history/?page=0&per_page=0")
    
    assert response.status_code == 400
    assert "Page and per_page must be positive integers" in response.json()["detail"]
