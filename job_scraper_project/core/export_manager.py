"""Unified export manager for all data formats with improved error handling."""
import json
import csv
import os
from pathlib import Path
from typing import List, Dict, Any, Union, Literal
import logging

logger = logging.getLogger(__name__)

FormatType = Literal["json", "csv"]


def _validate_filename(name: str) -> str:
    """
    Validate and sanitize filename to prevent path traversal.
    
    Args:
        name: Filename to validate
        
    Returns:
        Sanitized filename
        
    Raises:
        ValueError: If filename is invalid
    """
    # Remove any path separators
    name = os.path.basename(name)
    
    # Check for empty or invalid names
    if not name or name in ('.', '..'):
        raise ValueError("Invalid filename")
    
    # Remove any non-alphanumeric characters except dash and underscore
    safe_name = ''.join(c for c in name if c.isalnum() or c in ('_', '-'))
    
    if not safe_name:
        raise ValueError("Filename contains no valid characters")
    
    return safe_name


def export_data(
    data: Union[List[Dict[str, Any]], Dict[str, Any]],
    name: str,
    format: FormatType = "json",
    folder: str = "data/output"
) -> bool:
    """
    Export data to specified format.
    
    Args:
        data: Data to export (list of dicts or single dict)
        name: Base name for the output file (without extension)
        format: Output format ("json" or "csv")
        folder: Output directory path
        
    Returns:
        True if export successful, False otherwise
        
    Raises:
        ValueError: If data format is invalid or filename is unsafe
        IOError: If file cannot be written
    """
    try:
        # Validate inputs
        if not data:
            logger.warning(f"No data to export to {name}.{format}")
            return False
            
        if format not in ["json", "csv"]:
            raise ValueError(f"Unsupported format: {format}. Use 'json' or 'csv'")
        
        # Sanitize filename to prevent path traversal
        safe_name = _validate_filename(name)
        
        # Ensure output directory exists
        output_path = Path(folder)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Create file path with sanitized name
        file_path = output_path / f"{safe_name}.{format}"
        
        # Ensure the resolved path is still within the output directory
        if not file_path.resolve().is_relative_to(output_path.resolve()):
            raise ValueError("Invalid path: path traversal detected")
        
        # Export based on format
        if format == "json":
            _export_json(data, file_path)
        elif format == "csv":
            _export_csv(data, file_path)
        
        # Calculate record count
        record_count = len(data) if isinstance(data, list) else 1
        logger.info(f"Exported {record_count} records to {file_path}")
        print(f"[Exported] {record_count} records to {file_path}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to export data to {name}.{format}: {e}")
        print(f"[Error] Failed to export: {e}")
        return False


def _export_json(data: Union[List[Dict], Dict], file_path: Path) -> None:
    """Export data to JSON format."""
    with open(file_path, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _export_csv(data: Union[List[Dict], Dict], file_path: Path) -> None:
    """Export data to CSV format."""
    # Convert single dict to list
    if isinstance(data, dict):
        data = [data]
    
    if not data:
        raise ValueError("Cannot export empty data to CSV")
    
    # Get keys from first item
    keys = list(data[0].keys())
    
    with open(file_path, "w", newline="", encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
