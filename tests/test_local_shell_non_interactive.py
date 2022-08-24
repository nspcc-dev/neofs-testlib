from unittest import TestCase

from shell.interfaces import CommandOptions
from shell.local_shell import LocalShell
from tests.helpers import format_error_details


class TestLocalShellNonInteractive(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shell = LocalShell()

    def test_successful_command(self):
        script = "print('test')"

        result = self.shell.exec(f"python -c \"{script}\"")

        self.assertEqual(0, result.return_code)
        self.assertEqual("test", result.stdout.strip())
        self.assertEqual("", result.stderr)

    def test_failed_command_with_check(self):
        script = "invalid script"

        with self.assertRaises(RuntimeError) as exc:
            self.shell.exec(f"python -c \"{script}\"")

        error = format_error_details(exc.exception)
        self.assertIn("Error", error)
        self.assertIn("return code: 1", error)

    def test_failed_command_without_check(self):
        script = "invalid script"

        result = self.shell.exec(f"python -c \"{script}\"", CommandOptions(check=False))

        self.assertEqual(1, result.return_code)
        self.assertIn("Error", result.stdout)

    def test_non_existing_binary(self):
        with self.assertRaises(RuntimeError) as exc:
            self.shell.exec(f"not-a-command")

        error = format_error_details(exc.exception)
        self.assertIn("Error", error)
        self.assertIn("return code: 127", error)
