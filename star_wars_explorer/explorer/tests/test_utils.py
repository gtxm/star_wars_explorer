import pytest

from explorer.utils import compute_selected_fields_after_clicking_field_button


@pytest.mark.parametrize(
    "current_field,selected_fields,expected_outcome",
    [
        ("name", "year", "name,year"),  # selecting new value
        ("name", "name", ""),  # deselecting only value selected
        ("name", "name,year", "year"),  # deselecting one value from two selected
    ],
)
def test_compute_selected_fields_after_clicking_field_button(
    current_field, selected_fields, expected_outcome
):
    assert (
        compute_selected_fields_after_clicking_field_button(
            current_field, selected_fields.split(",")
        )
        == expected_outcome
    )
