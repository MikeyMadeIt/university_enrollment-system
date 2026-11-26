import pytest

from storage.json_storage import JsonStorage


def test_json_storage_round_trip_missing_and_invalid_files(tmp_path):
    storage = JsonStorage(str(tmp_path))
    assert storage.load("missing.json", []) == []
    storage.save("records.json", [{"id": "S1"}])
    assert storage.load("records.json") == [{"id": "S1"}]
    (tmp_path / "broken.json").write_text("{broken", encoding="utf-8")
    assert storage.load("broken.json", {"fallback": True}) == {"fallback": True}

    (tmp_path / "wrong-shape.json").write_text("{}", encoding="utf-8")
    assert storage.load("wrong-shape.json", []) == []
    (tmp_path / "scalar.json").write_text("null", encoding="utf-8")
    assert storage.load("scalar.json", []) == []


def test_json_storage_write_errors_are_reported(tmp_path, monkeypatch):
    storage = JsonStorage(str(tmp_path))

    def fail_open(*_args, **_kwargs):
        raise OSError("disk is read-only")

    monkeypatch.setattr("builtins.open", fail_open)
    with pytest.raises(OSError, match="read-only"):
        storage.save("records.json", [])


def test_json_storage_read_errors_return_the_requested_default(tmp_path, monkeypatch):
    storage = JsonStorage(str(tmp_path))
    (tmp_path / "unreadable.json").write_text("[]", encoding="utf-8")

    def fail_open(*_args, **_kwargs):
        raise OSError("permission denied")

    monkeypatch.setattr("builtins.open", fail_open)
    fallback = {"records": []}
    assert storage.load("unreadable.json", fallback) == fallback
