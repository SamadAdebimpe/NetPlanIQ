from openpyxl import Workbook

from ip_planner.exporters import (
    sanitize_sheet_name,
    get_unique_sheet_name,
    safe_filename_part,
)


def test_sanitize_sheet_name_replaces_invalid_excel_characters():
    assert sanitize_sheet_name("lag/core:wan") == "lag_core_wan"
    assert sanitize_sheet_name("[servers]*?") == "_servers___"


def test_sanitize_sheet_name_handles_empty_names():
    assert sanitize_sheet_name("") == "Sheet"
    assert sanitize_sheet_name("   ") == "Sheet"


def test_sanitize_sheet_name_limits_to_31_characters():
    long_name = "a" * 40
    assert sanitize_sheet_name(long_name) == "a" * 31


def test_get_unique_sheet_name_adds_suffix_for_duplicates():
    workbook = Workbook()
    workbook.active.title = "lag_core"
    workbook.create_sheet(title="lag_core_1")

    assert get_unique_sheet_name(workbook, "lag/core") == "lag_core_2"


def test_safe_filename_part_replaces_invalid_filename_characters():
    assert safe_filename_part("192.168.1.0/24") == "192.168.1.0_24"
    assert safe_filename_part("site:lagos?core") == "site_lagos_core"