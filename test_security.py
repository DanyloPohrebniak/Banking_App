import unittest
from unittest.mock import patch
import main  # import your main script


class TestBankingApp(unittest.TestCase):

    # Invalid input (negative amount)
    @patch('builtins.input', side_effect=['-5'])
    @patch('builtins.print')
    def test_get_positive_amount_invalid(self, mock_print, mock_input):
        result = main.get_positive_amount("Enter amount: ")
        self.assertIsNone(result)
        mock_print.assert_called_with("Invalid amount. Must be a positive number.")

    # Valid amount input
    @patch('builtins.input', side_effect=['100'])
    def test_get_positive_amount_valid(self, mock_input):
        result = main.get_positive_amount("Enter amount: ")
        self.assertEqual(result, 100)

    # Successful account creation
    @patch('builtins.input', side_effect=[
        '1', 'John', 'pass123', 'pass123',  # Create account
        '3'  # Exit
    ])
    @patch('builtins.print')
    @patch('security.generate_mfa_code', return_value=123456)
    @patch('security.hash_password', return_value='hashedpass')
    @patch('database.add_customer', return_value=True)
    def test_create_account_success(self, mock_add, mock_hash, mock_mfa, mock_print, mock_input):
        with self.assertRaises(SystemExit):  # Exits after menu choice 3
            main.login_menu()

        mock_print.assert_any_call("Account created successfully.")
        mock_print.assert_any_call("Your MFA code is: 123456 (you'll need it to log in)")

    # Successful login flow
    @patch('builtins.input', side_effect=[
        '2', 'John', 'pass123', '123456',  # Login input
        '3'  # Exit from login menu
    ])
    @patch('builtins.print')
    @patch('database.get_user_by_name', return_value=(1, 'John', 'email', 'hashedpass', 123456))
    @patch('security.check_password', return_value=True)
    def test_login_success(self, mock_check, mock_get_user, mock_print, mock_input):
        main.current_user = None  # Reset user before test
        main.login_menu()  # Should login, no SystemExit here
        self.assertIsNotNone(main.current_user)  # User should be set
        mock_print.assert_any_call("Welcome, John! You are logged in now!")


if __name__ == '__main__':
    unittest.main()
