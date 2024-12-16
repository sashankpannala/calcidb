import unittest
from unittest.mock import patch, MagicMock
from main import add, subtract, multiply, divide


class TestCalculatorFunctions(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 5), 4)

    def test_subtract(self):
        self.assertEqual(subtract(10, 4), 6)
        self.assertEqual(subtract(5, 7), -2)

    def test_multiply(self):
        self.assertEqual(multiply(3, 4), 12)
        self.assertEqual(multiply(-2, 3), -6)

    def test_divide(self):
        self.assertEqual(divide(8, 2), 4)
        self.assertEqual(divide(10, 0), "Error: Division by zero")


class TestInteractiveMode(unittest.TestCase):
    @patch("main.call_llm", return_value="The sum of 5 and 3 is 8.")  # Mock call_llm
    @patch("builtins.input", side_effect=["Add 5 and 3", "exit"])    # Mock input
    @patch("sys.stdin.isatty", return_value=True)                   # Simulate interactive terminal
    def test_interactive_mode(self, mock_isatty, mock_input, mock_call_llm):
        # Run the main function
        from main import main
        with patch("sys.stdout", new_callable=lambda: None):  # Suppress stdout
            main()

        # Ensure that call_llm was called with the correct input
        self.assertTrue(mock_call_llm.called, "call_llm was not called!")
        mock_call_llm.assert_called_once_with("Add 5 and 3")


if __name__ == "__main__":
    unittest.main()
