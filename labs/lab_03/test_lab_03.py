import csv
import os
from pathlib import Path
import subprocess
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lab_03 as app
import storage as storage_module
from storage import StudentStorage
from student import Student
from student_list import StudentList


@pytest.fixture
def students():
    return [
        Student(
            "Явор Олег Іванович", "+380000000001",
            "oleg@example.com", "КБ-252",
        ),
        Student(
            "Бондар Анна Олегівна", "0000000002",
            "anna@example.com", "КБ-252",
        ),
    ]


def names(records):
    return [student.name for student in records]


def feed(monkeypatch, values):
    values = iter(values)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(values))


class TestStudent:
    def test_validate_strips_fields(self):
        student = Student(
            "  Іван  ", " 123 ", " a@b.c ", " КБ-252 "
        ).validate()
        assert student.to_dict() == {
            "name": "Іван",
            "phone": "123",
            "email": "a@b.c",
            "group": "КБ-252",
        }

    @pytest.mark.parametrize("field", ["name", "phone", "email", "group"])
    def test_validate_rejects_empty(self, field):
        data = {
            "name": "Іван",
            "phone": "123",
            "email": "a@b.c",
            "group": "КБ-252",
        }
        data[field] = "   "
        with pytest.raises(ValueError):
            Student.from_dict(data)

    def test_from_dict_rejects_extra_or_missing_fields(self):
        with pytest.raises(ValueError):
            Student.from_dict({
                "name": "Іван", "phone": "123", "email": "a@b.c"
            })
        with pytest.raises(ValueError):
            Student.from_dict({
                "name": "Іван", "phone": "123", "email": "a@b.c",
                "group": "КБ-252", "extra": "x",
            })

    def test_equality_and_text(self):
        first = Student("Іван", "123", "a@b.c", "КБ-252")
        second = Student("Іван", "123", "a@b.c", "КБ-252")
        assert first == second
        assert str(first) == "Іван | 123 | a@b.c | КБ-252"


class TestStudentList:
    def test_add_sorts_and_keeps_objects(self, students):
        group = StudentList()
        group.add(students[0])
        group.add(students[1])
        assert names(group) == [
            "Бондар Анна Олегівна", "Явор Олег Іванович"
        ]
        assert all(isinstance(student, Student) for student in group)
        assert group[0] is students[1]

    def test_duplicate_names_are_separate_records(self):
        group = StudentList()
        first = Student("Однакове Ім'я", "1", "one@example.com", "КБ-252")
        second = Student("Однакове Ім'я", "2", "two@example.com", "КБ-252")
        group.add(first)
        group.add(second)
        removed = group.delete(1)
        assert removed.phone == "2"
        assert names(group) == ["Однакове Ім'я"]

    def test_edit_reorders_without_losing_contacts(self, students):
        group = StudentList(students)
        index = group.edit(1, {"name": "Адамчук Олег Іванович"})
        assert index == 0
        assert names(group) == [
            "Адамчук Олег Іванович", "Бондар Анна Олегівна"
        ]
        assert group[0].phone == students[0].phone
        assert group[0].email == students[0].email
        assert group[0].group == students[0].group

    def test_invalid_edit_preserves_old_record(self, students):
        group = StudentList([students[0]])
        before = group.to_dicts()
        with pytest.raises(ValueError):
            group.edit(0, {"email": "  "})
        assert group.to_dicts() == before

    @pytest.mark.parametrize("index", [-1, 2, 1.5, True])
    def test_invalid_index_does_not_delete(self, students, index):
        group = StudentList(students)
        before = group.to_dicts()
        with pytest.raises(IndexError):
            group.delete(index)
        assert group.to_dicts() == before

    def test_find_returns_all_matching_indexes(self, students):
        group = StudentList(students)
        assert group.find("Явор Олег Іванович") == [1]
        assert group.find("немає") == []


class TestStorage:
    def test_load_sorts_case_insensitive_headers_and_keeps_phone(
        self, tmp_path
    ):
        path = tmp_path / "вхідні дані.csv"
        path.write_text(
            " Group , EMAIL , Phone , Name \n"
            "КБ-252,oleg@example.com,+380000000001,Явор Олег Іванович\n"
            "КБ-252,anna@example.com,0000000002,Бондар Анна Олегівна\n",
            encoding="utf-8-sig",
        )
        loaded = StudentStorage(path).load()
        assert names(loaded) == [
            "Бондар Анна Олегівна", "Явор Олег Іванович"
        ]
        assert loaded[0].phone == "0000000002"
        assert loaded[1].phone == "+380000000001"

    def test_save_load_roundtrip_quotes_and_unicode(
        self, tmp_path, students
    ):
        path = tmp_path / "roundtrip.csv"
        students[1].name = 'Бондар, Анна "А"'
        StudentStorage(path).save(StudentList(students))
        assert path.read_bytes().startswith(b"\xef\xbb\xbf")
        loaded = StudentStorage(path).load()
        assert names(loaded) == [students[1].name, students[0].name]
        assert names(students) == [students[0].name, students[1].name]
        with path.open(encoding="utf-8-sig", newline="") as source:
            reader = csv.DictReader(source)
            assert reader.fieldnames == ["name", "phone", "email", "group"]
            assert next(reader)["name"] == students[1].name

    def test_header_only_and_save_empty(self, tmp_path):
        path = tmp_path / "empty.csv"
        path.write_text("name,phone,email,group\n", encoding="utf-8")
        assert len(StudentStorage(path).load()) == 0
        StudentStorage(path).save(StudentList())
        assert len(StudentStorage(path).load()) == 0

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
    def test_bad_csv_is_rejected_without_changes(self, tmp_path, text):
        path = tmp_path / "bad.csv"
        path.write_text(text, encoding="utf-8")
        original = path.read_bytes()
        with pytest.raises(ValueError):
            StudentStorage(path).load()
        assert path.read_bytes() == original

    def test_missing_file_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            StudentStorage(tmp_path / "missing.csv").load()

    def test_invalid_record_does_not_truncate_file(self, tmp_path, students):
        path = tmp_path / "saved.csv"
        storage = StudentStorage(path)
        group = StudentList(students)
        storage.save(group)
        original = path.read_bytes()
        group[0].phone = ""
        with pytest.raises(ValueError):
            storage.save(group)
        assert path.read_bytes() == original

    def test_replace_failure_keeps_old_file_and_cleans_temp(
        self, tmp_path, students, monkeypatch
    ):
        path = tmp_path / "saved.csv"
        storage = StudentStorage(path)
        group = StudentList(students)
        storage.save(group)
        original = path.read_bytes()

        def fail_replace(source, destination):
            raise OSError("simulated write failure")

        monkeypatch.setattr(storage_module.os, "replace", fail_replace)
        with pytest.raises(OSError):
            storage.save(group)
        assert path.read_bytes() == original
        assert list(tmp_path.glob("*.tmp")) == []


class TestMain:
    def test_main_requires_exactly_one_argument(self, capsys):
        assert app.main([]) == 2
        assert app.main(["one.csv", "two.csv"]) == 2
        assert "Використання:" in capsys.readouterr().out

    def test_main_missing_file_does_not_create_it(
        self, tmp_path, monkeypatch
    ):
        path = tmp_path / "missing.csv"
        monkeypatch.setattr(
            "builtins.input",
            lambda prompt: pytest.fail("Unexpected menu"),
        )
        assert app.main([str(path)]) == 1
        assert not path.exists()

    def test_main_bad_input_is_not_overwritten(
        self, tmp_path, monkeypatch
    ):
        path = tmp_path / "bad.csv"
        path.write_text("wrong,header\n1,2\n", encoding="utf-8")
        original = path.read_bytes()
        monkeypatch.setattr(
            "builtins.input",
            lambda prompt: pytest.fail("Unexpected menu"),
        )
        assert app.main([str(path)]) == 1
        assert path.read_bytes() == original

    @pytest.mark.parametrize("interruption", [EOFError, KeyboardInterrupt])
    def test_main_interruption_saves_changes(
        self, tmp_path, students, monkeypatch, interruption
    ):
        path = tmp_path / "interrupt.csv"
        StudentStorage(path).save(StudentList())
        answers = iter([
            "1",
            students[0].name,
            students[0].phone,
            students[0].email,
            students[0].group,
        ])

        def answer(prompt=""):
            try:
                return next(answers)
            except StopIteration:
                raise interruption

        monkeypatch.setattr("builtins.input", answer)
        assert app.main([str(path)]) == 0
        loaded = StudentStorage(path).load()
        assert names(loaded) == [students[0].name]

    def test_cancelled_edit_keeps_original_csv_data(
        self, tmp_path, students, monkeypatch
    ):
        path = tmp_path / "cancel.csv"
        StudentStorage(path).save(StudentList([students[0]]))
        feed(monkeypatch, ["2", "1", "New Name", "/cancel", "0"])
        assert app.main([str(path)]) == 0
        loaded = StudentStorage(path).load()
        assert names(loaded) == [students[0].name]

    def test_main_reports_save_failure(
        self, tmp_path, students, monkeypatch, capsys
    ):
        path = tmp_path / "saved.csv"
        StudentStorage(path).save(StudentList(students))
        original = path.read_bytes()
        feed(monkeypatch, ["0"])

        def fail_save(self, records):
            raise OSError("simulated save failure")

        monkeypatch.setattr(StudentStorage, "save", fail_save)
        assert app.main([str(path)]) == 1
        assert "Не вдалося зберегти" in capsys.readouterr().out
        assert path.read_bytes() == original

    def test_cli_persists_edit_add_delete_and_reload(
        self, tmp_path, students
    ):
        path = tmp_path / "довідник з пробілами.csv"
        StudentStorage(path).save(StudentList(students))
        script = Path(__file__).with_name("lab_03.py")
        commands = [
            "2", "2", "Адамчук Олег Іванович", "", "", "",
            "1", "Ворон Іван Петрович", "0000000003",
            "ivan@example.com", "КБ-252",
            "3", "2", "4", "0",
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
        loaded = StudentStorage(path).load()
        assert names(loaded) == [
            "Адамчук Олег Іванович", "Ворон Іван Петрович"
        ]
        assert loaded[0].phone == "+380000000001"
        assert loaded[0].email == "oleg@example.com"
        assert loaded[1].phone == "0000000003"

    def test_display_contains_all_four_fields(self, students, capsys):
        app.print_students(StudentList([students[1]]))
        output = capsys.readouterr().out
        for text in (
            "Бондар Анна", "0000000002", "anna@example.com", "КБ-252"
        ):
            assert text in output
