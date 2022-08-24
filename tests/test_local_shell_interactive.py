from unittest import TestCase

from shell.interfaces import CommandOptions, InteractiveInput
from shell.local_shell import LocalShell
from tests.helpers import format_error_details


class TestLocalShellInteractive(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shell = LocalShell()

    def test_command_with_one_prompt(self):
        script = "password = input('Password: '); print(password)"

        inputs = [InteractiveInput(prompt_pattern="Password", input="test")]
        result = self.shell.exec(
            f"python -c \"{script}\"",
            CommandOptions(interactive_inputs=inputs)
        )

        self.assertEqual(0, result.return_code)
        self.assertOutputLines(["Password: test", "test"], result.stdout)
        self.assertEqual("", result.stderr)

    def test_command_with_several_prompts(self):
        script = (
            "input1 = input('Input1: '); print(input1); "
            "input2 = input('Input2: '); print(input2)"
        )
        inputs = [
            InteractiveInput(prompt_pattern="Input1", input="test1"),
            InteractiveInput(prompt_pattern="Input2", input="test2"),
        ]

        result = self.shell.exec(
            f"python -c \"{script}\"",
            CommandOptions(interactive_inputs=inputs)
        )

        self.assertEqual(0, result.return_code)
        self.assertOutputLines(["Input1: test1", "test1", "Input2: test2", "test2"], result.stdout)
        self.assertEqual("", result.stderr)

    def test_failed_command_with_check(self):
        script = "invalid script"
        inputs = [InteractiveInput(prompt_pattern=".*", input="test")]

        with self.assertRaises(RuntimeError) as exc:
            self.shell.exec(f"python -c \"{script}\"", CommandOptions(interactive_inputs=inputs))

        error = format_error_details(exc.exception)
        self.assertIn("Error", error)
        # TODO: it would be nice to have return code as well
        # self.assertIn("return code: 1", error)

    def test_failed_command_without_check(self):
        script = "invalid script"
        inputs = [InteractiveInput(prompt_pattern=".*", input="test")]

        result = self.shell.exec(
            f"python -c \"{script}\"",
            CommandOptions(interactive_inputs=inputs, check=False),
        )
        self.assertEqual(1, result.return_code)

    def test_non_existing_binary(self):
        inputs = [InteractiveInput(prompt_pattern=".*", input="test")]

        with self.assertRaises(RuntimeError) as exc:
            self.shell.exec("not-a-command", CommandOptions(interactive_inputs=inputs))

        error = format_error_details(exc.exception)
        self.assertIn("command was not found or was not executable", error)

    def assertOutputLines(self, expected_lines: list[str], output: str) -> None:
        output_lines = [line.strip() for line in output.split("\n") if line.strip()]
        self.assertEqual(expected_lines, output_lines)
