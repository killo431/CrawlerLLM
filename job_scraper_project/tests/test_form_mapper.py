"""Unit tests for form mapper."""
import pytest
from automation.models import FormField, FieldType


def test_form_field_creation():
    """Test FormField dataclass creation."""
    field = FormField(
        selector='#email',
        field_type=FieldType.EMAIL,
        label='Email Address',
        required=True
    )
    
    assert field.selector == '#email'
    assert field.field_type == FieldType.EMAIL
    assert field.label == 'Email Address'
    assert field.required == True
    assert field.readonly == False
    assert field.disabled == False


def test_form_field_purpose_detection():
    """Test field purpose detection."""
    # Email field
    email_field = FormField(
        selector='#email',
        field_type=FieldType.EMAIL,
        label='Email Address'
    )
    email_field.detected_purpose = 'email'
    assert email_field.detected_purpose == 'email'
    
    # Name field
    name_field = FormField(
        selector='#first_name',
        field_type=FieldType.TEXT,
        label='First Name'
    )
    name_field.detected_purpose = 'first_name'
    assert name_field.detected_purpose == 'first_name'


def test_field_type_enum():
    """Test FieldType enum values."""
    assert FieldType.TEXT.value == 'text'
    assert FieldType.EMAIL.value == 'email'
    assert FieldType.PHONE.value == 'phone'
    assert FieldType.FILE.value == 'file'
    assert FieldType.SELECT.value == 'select'
    assert FieldType.CHECKBOX.value == 'checkbox'
    assert FieldType.TEXTAREA.value == 'textarea'


def test_form_field_string_representation():
    """Test FormField __str__ method."""
    field = FormField(
        selector='#email',
        field_type=FieldType.EMAIL,
        label='Email Address',
        required=True
    )
    
    field_str = str(field)
    assert 'email' in field_str.lower()
    assert 'required=True' in field_str


def test_form_field_with_options():
    """Test FormField with select options."""
    field = FormField(
        selector='#country',
        field_type=FieldType.SELECT,
        label='Country',
        options=['USA', 'Canada', 'UK']
    )
    
    assert len(field.options) == 3
    assert 'USA' in field.options
    assert 'Canada' in field.options


def test_form_field_confidence():
    """Test confidence scoring."""
    field = FormField(
        selector='#email',
        field_type=FieldType.EMAIL,
        confidence=0.95
    )
    
    assert field.confidence == 0.95
    assert 0.0 <= field.confidence <= 1.0
