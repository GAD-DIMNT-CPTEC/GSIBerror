from pathlib import Path

import pytest

import gsiberror as gb


DATA = Path(__file__).parents[1] / "data"
SAMPLE = DATA / "global_berror.l64y386.f77-ncep-dtc.gcv"


def test_reports_actionable_error_for_unfetched_lfs_data():
    with pytest.raises(ValueError, match="git lfs pull"):
        gb.Berror(SAMPLE).read_records()


def test_display_name_can_be_changed_more_than_once():
    berror = gb.Berror(SAMPLE)

    assert berror.get_name() == SAMPLE.name
    assert berror.my_name("first") is berror
    assert berror.my_name("second") is berror
    assert berror.get_name() == "second"


def test_rejects_truncated_file(tmp_path):
    truncated = tmp_path / "truncated.gcv"
    truncated.write_bytes(b"1234")

    with pytest.raises(ValueError, match="truncated GCV header"):
        gb.Berror(truncated).read_records()


def test_rejects_non_positive_grid_dimensions(tmp_path):
    invalid = tmp_path / "invalid.gcv"
    invalid.write_bytes(b"\0" * 20)

    with pytest.raises(ValueError, match="Invalid GCV grid dimensions"):
        gb.Berror(invalid).read_records()
