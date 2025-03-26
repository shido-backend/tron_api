import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from sqlalchemy import exc
from app.models import WalletQuery
from app.schemas import WalletInfo
from app.api.errors import DatabaseError
from app.repositories.wallet import WalletRepository

def test_create_wallet_query_success():
    mock_session = Mock(spec=Session)
    wallet_repo = WalletRepository(mock_session)
    
    wallet_info = WalletInfo(
        address="test_address",
        bandwidth=100,
        energy=50,
        trx_balance=1000
    )

    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    result = wallet_repo.create_wallet_query(wallet_info)

    assert result.address == wallet_info.address
    assert result.bandwidth == wallet_info.bandwidth
    assert result.energy == wallet_info.energy
    assert result.trx_balance == wallet_info.trx_balance
    
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()

def test_create_wallet_query_database_error():

    mock_session = Mock(spec=Session)
    wallet_repo = WalletRepository(mock_session)
    
    wallet_info = WalletInfo(
        address="test_address",
        bandwidth=100,
        energy=50,
        trx_balance=1000
    )
    
    mock_session.commit.side_effect = exc.SQLAlchemyError("Database connection error")

    with pytest.raises(DatabaseError, match="Failed to create wallet record"):
        wallet_repo.create_wallet_query(wallet_info)
    
    mock_session.rollback.assert_called_once()

def test_get_wallet_queries_success():

    mock_session = Mock(spec=Session)
    wallet_repo = WalletRepository(mock_session)

    mock_queries = [
        WalletQuery(address="address1", bandwidth=10, energy=5, trx_balance=100),
        WalletQuery(address="address2", bandwidth=20, energy=10, trx_balance=200)
    ]

    mock_query = Mock()
    mock_session.query.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = mock_queries

    results = wallet_repo.get_wallet_queries(skip=0, limit=10)

    assert len(results) == 2
    assert results[0].address == "address1"
    assert results[1].address == "address2"
    
    mock_session.query.assert_called_once_with(WalletQuery)

def test_get_wallet_queries_database_error():

    mock_session = Mock(spec=Session)
    wallet_repo = WalletRepository(mock_session)

    mock_session.query.side_effect = exc.SQLAlchemyError("Query execution error")

    with pytest.raises(DatabaseError, match="Failed to fetch queries"):
        wallet_repo.get_wallet_queries(skip=0, limit=10)

def test_get_total_queries_count_success():
    mock_session = Mock(spec=Session)
    wallet_repo = WalletRepository(mock_session)

    mock_query = Mock()
    mock_session.query.return_value = mock_query
    mock_query.count.return_value = 15

    total_count = wallet_repo.get_total_queries_count()

    assert total_count == 15
    mock_session.query.assert_called_once_with(WalletQuery)

def test_get_total_queries_count_database_error():
    mock_session = Mock(spec=Session)
    wallet_repo = WalletRepository(mock_session)

    mock_session.query.side_effect = exc.SQLAlchemyError("Count query error")

    with pytest.raises(DatabaseError, match="Failed to count queries"):
        wallet_repo.get_total_queries_count()