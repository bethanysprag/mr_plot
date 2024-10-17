import pytest
from unittest.mock import Mock, patch
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Import the functions from your mr_plot.py file
from mr_plot import (
    initialize_gitlab,
    fetch_merge_requests,
    process_merge_requests,
    prepare_data,
    plot_merge_requests,
)

@pytest.fixture
def mock_gitlab():
    with patch('gitlab.Gitlab') as mock:
        yield mock

@pytest.fixture
def mock_project():
    return Mock()

@pytest.fixture
def mock_merge_requests():
    mr1 = Mock(created_at="2023-01-01T10:00:00.000Z")
    mr2 = Mock(created_at="2023-01-01T14:00:00.000Z")
    mr3 = Mock(created_at="2023-01-02T09:00:00.000Z")
    return [mr1, mr2, mr3]

def test_initialize_gitlab(mock_gitlab):
    url = "https://gitlab.example.com"
    token = "test_token"
    initialize_gitlab(url, token)
    mock_gitlab.assert_called_once_with(url, private_token=token)

def test_fetch_merge_requests(mock_project):
    mock_project.mergerequests.list.return_value = ["mr1", "mr2", "mr3"]
    result = fetch_merge_requests(mock_project)
    assert result == ["mr1", "mr2", "mr3"]
    mock_project.mergerequests.list.assert_called_once_with(all=True)

def test_process_merge_requests(mock_merge_requests):
    result = process_merge_requests(mock_merge_requests)
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 3
    assert list(result.columns) == ["created_at"]

def test_prepare_data():
    dates = [
        datetime(2023, 1, 1, 10, 0),
        datetime(2023, 1, 1, 14, 0),
        datetime(2023, 1, 2, 9, 0),
    ]
    df = pd.DataFrame({"created_at": dates})
    result = prepare_data(df)
    assert isinstance(result, pd.Series)
    assert len(result) == 2
    assert result["2023-01-01"] == 2
    assert result["2023-01-02"] == 1

@patch('matplotlib.pyplot.show')
def test_plot_merge_requests(mock_show):
    dates = pd.date_range(start="2023-01-01", end="2023-01-05")
    data = pd.Series([2, 1, 3, 0, 2], index=dates)
    plot_merge_requests(data)
    mock_show.assert_called_once()

@patch('mr_plot.initialize_gitlab')
@patch('mr_plot.fetch_merge_requests')
@patch('mr_plot.process_merge_requests')
@patch('mr_plot.prepare_data')
@patch('mr_plot.plot_merge_requests')
def test_main(mock_plot, mock_prepare, mock_process, mock_fetch, mock_init):
    from mr_plot import main

    mock_init.return_value = Mock()
    mock_fetch.return_value = ["mr1", "mr2", "mr3"]
    mock_process.return_value = pd.DataFrame({"created_at": [datetime.now()]})
    mock_prepare.return_value = pd.Series([1], index=[datetime.now().date()])

    main("https://gitlab.example.com", "test_token", "test_project")

    mock_init.assert_called_once()
    mock_fetch.assert_called_once()
    mock_process.assert_called_once()
    mock_prepare.assert_called_once()
    mock_plot.assert_called_once()

if __name__ == "__main__":
    pytest.main()

