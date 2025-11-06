"""Unit tests for export manager."""
import pytest
import json
import csv
from pathlib import Path
from core.export_manager import export_data, _export_json, _export_csv


def test_export_json(tmp_path):
    """Test JSON export functionality."""
    data = [{"name": "Test", "value": 123}]
    file_path = tmp_path / "test.json"
    
    _export_json(data, file_path)
    
    assert file_path.exists()
    with open(file_path, 'r') as f:
        loaded_data = json.load(f)
    assert loaded_data == data


def test_export_csv(tmp_path):
    """Test CSV export functionality."""
    data = [{"name": "Test", "value": 123}]
    file_path = tmp_path / "test.csv"
    
    _export_csv(data, file_path)
    
    assert file_path.exists()
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) == 1
    assert rows[0]["name"] == "Test"


def test_export_data_json(tmp_path):
    """Test export_data with JSON format."""
    data = [{"title": "Job 1"}, {"title": "Job 2"}]
    result = export_data(data, "test", "json", str(tmp_path))
    
    assert result is True
    assert (tmp_path / "test.json").exists()


def test_export_data_csv(tmp_path):
    """Test export_data with CSV format."""
    data = [{"title": "Job 1"}, {"title": "Job 2"}]
    result = export_data(data, "test", "csv", str(tmp_path))
    
    assert result is True
    assert (tmp_path / "test.csv").exists()


def test_export_empty_data(tmp_path):
    """Test export with empty data."""
    data = []
    result = export_data(data, "test", "json", str(tmp_path))
    
    assert result is False


def test_export_invalid_format(tmp_path):
    """Test export with invalid format."""
    data = [{"title": "Job"}]
    with pytest.raises(ValueError):
        export_data(data, "test", "xml", str(tmp_path))
