"""
Performance tests for concurrent users in the chatbot backend.
"""

import pytest
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from fastapi.testclient import TestClient
from main import app  # Assuming the main app is in main.py
from unittest.mock import patch, MagicMock, AsyncMock
from models.user import User
from uuid import uuid4


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_response_time_single_request(client):
    """Test response time for a single request."""
    user = User(
        id=str(uuid4()),
        name="Test User",
        email="test@example.com",
        password_hash="hashed_password"
    )
    user_id = user.id

    message_data = {
        "message": "Add a task to buy groceries",
        "conversation_id": None
    }

    # Mock dependencies
    with patch("api.chat_router.get_current_chat_user") as mock_get_user, \
         patch("api.chat_router.get_db_session") as mock_get_session, \
         patch("api.chat_router.chat_agent") as mock_agent:

        # Mock user authentication
        mock_get_user.return_value = user

        # Mock database session
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_get_session.return_value.__exit__.return_value = None

        # Mock agent response
        mock_agent.initialize_tools = AsyncMock()
        mock_agent.process_with_retry = AsyncMock(return_value={
            "response": "I've created a task for you: buy groceries",
            "tool_calls": [],
            "action": {"type": "task_created", "data": {}}
        })

        # Mock conversation creation
        from models.conversation import Conversation
        mock_conversation = Conversation(
            id=uuid4(),
            user_id=user.id,
            metadata={}
        )
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None
        mock_session.get.return_value = mock_conversation

        # Measure response time
        start_time = time.time()
        response = client.post(f"/api/chat/{user_id}/conversation", json=message_data)
        end_time = time.time()

        response_time = end_time - start_time

        # Assert that response time is under 3 seconds (as specified in requirements)
        assert response_time < 3.0
        assert response.status_code == 200


def test_concurrent_users_performance(client):
    """Test performance with multiple concurrent users."""
    num_concurrent_users = 10
    results = []

    def make_request(user_idx):
        """Function to make a request for a user."""
        user = User(
            id=str(uuid4()),
            name=f"Test User {user_idx}",
            email=f"test{user_idx}@example.com",
            password_hash="hashed_password"
        )
        user_id = user.id

        message_data = {
            "message": f"Add a task for user {user_idx}",
            "conversation_id": None
        }

        # Mock dependencies
        with patch("api.chat_router.get_current_chat_user") as mock_get_user, \
             patch("api.chat_router.get_db_session") as mock_get_session, \
             patch("api.chat_router.chat_agent") as mock_agent:

            # Mock user authentication
            mock_get_user.return_value = user

            # Mock database session
            mock_session = MagicMock()
            mock_get_session.return_value.__enter__.return_value = mock_session
            mock_get_session.return_value.__exit__.return_value = None

            # Mock agent response
            mock_agent.initialize_tools = AsyncMock()
            mock_agent.process_with_retry = AsyncMock(return_value={
                "response": f"Task created for user {user_idx}",
                "tool_calls": [],
                "action": {"type": "task_created", "data": {}}
            })

            # Mock conversation creation
            from models.conversation import Conversation
            mock_conversation = Conversation(
                id=uuid4(),
                user_id=user.id,
                metadata={}
            )
            mock_session.add.return_value = None
            mock_session.commit.return_value = None
            mock_session.refresh.return_value = None
            mock_session.get.return_value = mock_conversation

            # Make the request
            start_time = time.time()
            response = client.post(f"/api/chat/{user_id}/conversation", json=message_data)
            end_time = time.time()

            return {
                "response_time": end_time - start_time,
                "status_code": response.status_code,
                "user_idx": user_idx
            }

    # Execute requests concurrently
    with ThreadPoolExecutor(max_workers=num_concurrent_users) as executor:
        futures = [executor.submit(make_request, i) for i in range(num_concurrent_users)]
        results = [future.result() for future in futures]

    # Analyze results
    response_times = [result["response_time"] for result in results]
    avg_response_time = sum(response_times) / len(response_times)

    # Assertions
    for result in results:
        assert result["status_code"] == 200
        assert result["response_time"] < 5.0  # Should respond within 5 seconds under load

    # Average response time should be reasonable
    assert avg_response_time < 3.0

    print(f"Performance test with {num_concurrent_users} concurrent users:")
    print(f"Average response time: {avg_response_time:.2f}s")
    print(f"Min response time: {min(response_times):.2f}s")
    print(f"Max response time: {max(response_times):.2f}s")


@pytest.mark.asyncio
async def test_async_performance():
    """Test asynchronous performance characteristics."""
    # This test would measure how well the system handles async operations
    # In a real implementation, this would test actual async endpoints
    start_time = time.time()

    # Simulate multiple async operations
    async def simulate_operation(op_id):
        # Simulate some async work
        await asyncio.sleep(0.1)  # Simulate API call or DB operation
        return f"Operation {op_id} completed"

    # Run multiple operations concurrently
    tasks = [simulate_operation(i) for i in range(5)]
    results = await asyncio.gather(*tasks)

    end_time = time.time()
    total_time = end_time - start_time

    # With concurrent execution, this should take ~0.1s not 0.5s
    assert total_time < 0.3  # Allow some overhead
    assert len(results) == 5


def test_load_handling(client):
    """Test system behavior under load."""
    num_requests = 20
    response_times = []

    user = User(
        id=str(uuid4()),
        name="Load Test User",
        email="load@test.com",
        password_hash="hashed_password"
    )
    user_id = user.id

    for i in range(num_requests):
        message_data = {
            "message": f"Load test message {i}",
            "conversation_id": None
        }

        # Mock dependencies
        with patch("api.chat_router.get_current_chat_user") as mock_get_user, \
             patch("api.chat_router.get_db_session") as mock_get_session, \
             patch("api.chat_router.chat_agent") as mock_agent:

            # Mock user authentication
            mock_get_user.return_value = user

            # Mock database session
            mock_session = MagicMock()
            mock_get_session.return_value.__enter__.return_value = mock_session
            mock_get_session.return_value.__exit__.return_value = None

            # Mock agent response
            mock_agent.initialize_tools = AsyncMock()
            mock_agent.process_with_retry = AsyncMock(return_value={
                "response": f"Response to load test message {i}",
                "tool_calls": [],
                "action": {"type": "message_processed", "data": {}}
            })

            # Mock conversation creation
            from models.conversation import Conversation
            mock_conversation = Conversation(
                id=uuid4(),
                user_id=user.id,
                metadata={}
            )
            mock_session.add.return_value = None
            mock_session.commit.return_value = None
            mock_session.refresh.return_value = None
            mock_session.get.return_value = mock_conversation

            start_time = time.time()
            response = client.post(f"/api/chat/{user_id}/conversation", json=message_data)
            end_time = time.time()

            response_times.append(end_time - start_time)

            assert response.status_code == 200

    # Calculate statistics
    avg_time = sum(response_times) / len(response_times)
    max_time = max(response_times)

    # System should maintain performance under load
    assert avg_time < 3.0  # Average response time under load
    assert max_time < 5.0  # Even worst case should be reasonable

    print(f"Load test with {num_requests} requests:")
    print(f"Average response time: {avg_time:.2f}s")
    print(f"Max response time: {max_time:.2f}s")