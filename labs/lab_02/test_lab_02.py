import csv
import os
from pathlib import Path
import subprocess
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lab_02 as book


@pytest.fixture
def students():
    return [
        {"name": "Явор Олег Іванович", "phone": "+380000000001",
         "email": "oleg@example.com", "group": "КБ-252"},
        {"name": "Бондар Анна Олегівна", "phone": "0000000002",
         "email": "anna@example.com", "group": "КБ-252"},
    ]


def names(records):
    return [student["name"] for student in records]


def feed(monkeypatch, values):
    values = iter(values)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(values))


def test_add_sorts_and_copies_input(students):
    directory = []
    book.add_student(directory, students[0])
    book.add_student(directory, students[1])
    assert names(directory) == [
        "Бондар Анна Олегівна", "Явор Олег Іванович"
    ]
    students[1]["phone"] = "changed outside directory"
    assert directory[0]["phone"] == "0000000002"
    assert set(directory[0]) == {"name", "phone", "email", "group"}


def test_duplicate_names_are_separate_records(students):
    directory = []
    first = students[0].copy()
    second = {**first, "phone": "0000000003"}
    book.add_student(directory, first)
    book.add_student(directory, second)
    removed = book.delete_student(directory, 1)
    assert removed["phone"] == "0000000003"
    assert directory == [first]


def test_rename_reorders_without_losing_contacts(students):
    directory = []
    for student in students:
        book.add_student(directory, student)
    index = book.edit_student(
        directory, 1, {"name": "Адамчук Олег Іванович"}
    )
    assert index == 0
    assert names(directory) == [
        "Адамчук Олег Іванович", "Бондар Анна Олегівна"
    ]
    assert directory[0] == {**students[0], "name": "Адамчук Олег Іванович"}


def test_invalid_edit_preserves_old_record(students):
    directory = [students[0].copy()]
    original = directory[0].copy()
    with pytest.raises(ValueError):
        book.edit_student(directory, 0, {"email": "  "})
    assert directory == [original]


@pytest.mark.parametrize("index", [-1, 2, 1.5, True])
def test_invalid_index_does_not_delete(students, index):
    original = [student.copy() for student in students]
    with pytest.raises(IndexError):
        book.delete_student(students, index)
    assert students == original


@pytest.mark.parametrize("index,remaining", [
    (0, "Бондар Анна Олегівна"), (1, "Явор Олег Іванович")
])
def test_delete_removes_selected_record(students, index, remaining):
    book.delete_student(students, index)
    assert names(students) == [remaining]


def test_load_sorts_case_insensitive_headers_and_keeps_phone(tmp_path):
    path = tmp_path / "вхідні дані.csv"
    path.write_text(
        " Group , EMAIL , Phone , Name \n"
        "КБ-252,oleg@example.com,+380000000001,Явор Олег Іванович\n"
        "КБ-252,anna@example.com,0000000002,Бондар Анна Олегівна\n",
        encoding="utf-8-sig",
    )
    loaded = book.load_students(path)
    assert names(loaded) == [
        "Бондар Анна Олегівна", "Явор Олег Іванович"
    ]
    assert loaded[0]["phone"] == "0000000002"
    assert loaded[1]["phone"] == "+380000000001"


def test_save_load_roundtrip_quotes_and_unicode(tmp_path, students):
    path = tmp_path / "roundtrip.csv"
    students[1]["name"] = 'Бондар, Анна "А"'
    book.save_students(path, students)
    assert path.read_bytes().startswith(b"\xef\xbb\xbf")
    assert book.load_students(path) == [students[1], students[0]]
    assert names(students) == [
        "Явор Олег Іванович", 'Бондар, Анна "А"'
    ]
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        assert reader.fieldnames == ["name", "phone", "email", "group"]
        assert next(reader)["name"] == 'Бондар, Анна "А"'


def test_header_only_and_save_empty_directory(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text("name,phone,email,group\n", encoding="utf-8")
    assert book.load_students(path) == []
    book.save_students(path, [])
    assert book.load_students(path) == []


@pytest.mark.parametrize("text", [
    "",
    "name,phone\nA,1\n",
    "name,phone,email,Name\nA,1,a@example.com,B\n",
    "name,phone,email,group,extra\nA,1,a@example.com,G,X\n",
    "name,phone,email,group\nA,1,a@example.com\n",
    "name,phone,email,group\nA,1,a@example.com,G,X\n",
    "name,phone,email,group\nA,,a@example.com,G\n",
    'name,phone,email,group\n"Unclosed,1,a@example.com,G\n',
    '"name,phone,email,group\n',
])
def test_bad_csv_is_rejected_without_changes(tmp_path, text):
    path = tmp_path / "bad.csv"
    path.write_text(text, encoding="utf-8")
    original = path.read_bytes()
    with pytest.raises(ValueError):
        book.load_students(path)
    assert path.read_bytes() == original


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        book.load_students(tmp_path / "missing.csv")


def test_invalid_record_does_not_truncate_file(tmp_path, students):
    path = tmp_path / "saved.csv"
    book.save_students(path, students)
    original = path.read_bytes()
    with pytest.raises(ValueError):
        book.save_students(path, [{**students[0], "phone": ""}])
    assert path.read_bytes() == original


def test_replace_failure_keeps_old_file_and_cleans_temp(
    tmp_path, students, monkeypatch
):
    path = tmp_path / "saved.csv"
    book.save_students(path, students)
    original = path.read_bytes()

    def fail_replace(source, destination):
        raise OSError("simulated write failure")

    monkeypatch.setattr(book.os, "replace", fail_replace)
    with pytest.raises(OSError):
        book.save_students(path, [students[0]])
    assert path.read_bytes() == original
    assert list(tmp_path.glob("*.tmp")) == []


def test_main_requires_exactly_one_argument(capsys):
    assert book.main([]) == 2
    assert book.main(["one.csv", "two.csv"]) == 2
    assert "Використання:" in capsys.readouterr().out


def test_main_missing_file_does_not_create_it(tmp_path, monkeypatch):
    path = tmp_path / "missing.csv"

    def unexpected_input(prompt):
        raise AssertionError("Menu must not open after load failure")

    monkeypatch.setattr("builtins.input", unexpected_input)
    assert book.main([str(path)]) == 1
    assert not path.exists()


def test_main_bad_input_is_not_overwritten(tmp_path, monkeypatch):
    path = tmp_path / "bad.csv"
    path.write_text("wrong,header\n1,2\n", encoding="utf-8")
    original = path.read_bytes()
    monkeypatch.setattr(
        "builtins.input", lambda prompt: pytest.fail("Unexpected menu")
    )
    assert book.main([str(path)]) == 1
    assert path.read_bytes() == original


@pytest.mark.parametrize("interruption", [EOFError, KeyboardInterrupt])
def test_main_interruption_saves_changes(
    tmp_path, students, monkeypatch, interruption
):
    path = tmp_path / "interrupt.csv"
    book.save_students(path, [])
    answers = iter(["1", *students[0].values()])

    def answer(prompt=""):
        try:
            return next(answers)
        except StopIteration:
            raise interruption

    monkeypatch.setattr("builtins.input", answer)
    assert book.main([str(path)]) == 0
    assert book.load_students(path) == [students[0]]


def test_cancelled_edit_keeps_original_csv_data(
    tmp_path, students, monkeypatch
):
    path = tmp_path / "cancel.csv"
    book.save_students(path, [students[0]])
    feed(monkeypatch, ["2", "1", "New Name", "/cancel", "0"])
    assert book.main([str(path)]) == 0
    assert book.load_students(path) == [students[0]]


def test_main_reports_save_failure(tmp_path, students, monkeypatch, capsys):
    path = tmp_path / "saved.csv"
    book.save_students(path, students)
    original = path.read_bytes()
    feed(monkeypatch, ["0"])

    def fail_save(filename, records):
        raise OSError("simulated save failure")

    monkeypatch.setattr(book, "save_students", fail_save)
    assert book.main([str(path)]) == 1
    assert "Не вдалося зберегти" in capsys.readouterr().out
    assert path.read_bytes() == original


def test_cli_persists_edit_add_delete_and_reload(tmp_path, students):
    path = tmp_path / "довідник з пробілами.csv"
    book.save_students(path, students)
    sample = Path(__file__).with_name("lab2.csv")
    original_sample = sample.read_bytes()
    script = Path(__file__).with_name("lab_02.py")
    commands = [
        "2", "2", "Адамчук Олег Іванович", "", "", "",
        "1", "Ворон Іван Петрович", "0000000003", "ivan@example.com",
        "КБ-252", "3", "2", "4", "0",
    ]
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [sys.executable, "-B", str(script), str(path)],
        input="\n".join(commands) + "\n", capture_output=True,
        text=True, encoding="utf-8", cwd=tmp_path, env=env, timeout=15,
    )
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    assert "Завантажено записів: 2" in result.stdout
    assert "Дані збережено:" in result.stdout
    loaded = book.load_students(path)
    assert names(loaded) == [
        "Адамчук Олег Іванович", "Ворон Іван Петрович"
    ]
    assert loaded[0]["phone"] == "+380000000001"
    assert loaded[0]["email"] == "oleg@example.com"
    assert loaded[1]["phone"] == "0000000003"
    assert sample.read_bytes() == original_sample


def test_display_contains_all_four_fields(students, capsys):
    book.print_students([students[1]])
    output = capsys.readouterr().out
    for text in ("Бондар Анна", "0000000002", "anna@example.com", "КБ-252"):
        assert text in output
