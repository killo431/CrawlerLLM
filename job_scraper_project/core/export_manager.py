"""Unified export manager for all data formats with improved error handling."""
import json
import csv
import os
from pathlib import Path
from typing import List, Dict, Any, Union, Literal
import logging

logger = logging.getLogger(__name__)

FormatType = Literal["json", "csv"]

# Allowed output directories for security
ALLOWED_OUTPUT_DIRS = {
    "data/output",
    "output",
    "/tmp/output",
}


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


def _validate_output_folder(folder: str) -> Path:
    """
    Validate output folder to prevent path traversal.
    
    Args:
        folder: Output folder path
        
    Returns:
        Validated Path object
        
    Raises:
        ValueError: If folder path is invalid or not allowed
    """
    # Normalize the path
    folder_path = Path(folder).resolve()
    
    # Check if it's in the allowed list
    if folder not in ALLOWED_OUTPUT_DIRS:
        # For backward compatibility, allow data/output subdirectories
        if not str(folder_path).endswith(os.path.sep + "output") and "data" not in str(folder_path):
            logger.warning(f"Output folder {folder} not in allowed list, using default")
            folder = "data/output"
    
    return Path(folder)


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
        folder: Output directory path (must be in allowed list)
        
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
        
        # Validate and get safe output directory
        output_path = _validate_output_folder(folder)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Create file path with sanitized name - use only basename for security
        file_path = output_path / safe_name
        file_path = file_path.with_suffix(f".{format}")
        
        # Final safety check: ensure resolved path is within output directory
        try:
            file_path.resolve().relative_to(output_path.resolve())
        except ValueError:
            raise ValueError("Invalid path: attempted path traversal detected")
        
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
    """
    Export data to JSON format.
    
    Args:
        file_path: Validated and safe file path
        data: Data to export
    """
    with open(file_path, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _export_csv(data: Union[List[Dict], Dict], file_path: Path) -> None:
    """
    Export data to CSV format.
    
    Args:
        file_path: Validated and safe file path
        data: Data to export
    """
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
