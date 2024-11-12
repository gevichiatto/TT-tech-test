import unittest
from src import MiniVenmo, User, CreditCard

class TestMiniVenmo(unittest.TestCase):
	def setUp(self):
		self.app = MiniVenmo()
		self.user_a = self.app.create_user("Alice", balance=50)
		self.user_b = self.app.create_user("Bob", balance=20)
		self.credit_card_a = CreditCard(balance=100)
		self.user_a.assign_credit_card(self.credit_card_a)

	def test_create_user(self):
		user = self.app.create_user("Charlie", balance=30)
		self.assertIsInstance(user, User)
		self.assertEqual(user.name, "Charlie")
		self.assertEqual(user.balance, 30)

	def test_create_user_with_no_initial_balance(self):        
		user_no_balance = self.app.create_user("Dana")
		self.assertEqual(user_no_balance.balance, 0)

	def test_pay_with_sufficient_balance(self):
		result = self.user_a.pay(self.user_b, amount=10, description="Coffee")
		self.assertTrue(result)
		self.assertEqual(self.user_a.balance, 40)
		self.assertEqual(self.user_b.balance, 30)

	def test_pay_with_insufficient_balance_uses_credit_card(self):
		self.user_a.balance = 5
		result = self.user_a.pay(self.user_b, amount=20, description="Lunch")
		self.assertTrue(result)
		self.assertEqual(self.user_a.balance, 5)
		self.assertEqual(self.credit_card_a.balance, 80)
		self.assertEqual(self.user_b.balance, 40)

	def test_pay_with_insufficient_funds_and_no_credit(self):
		self.user_a.balance = 2
		self.credit_card_a.balance = 5
		result = self.user_a.pay(self.user_b, amount=20, description="Dinner")
		self.assertFalse(result)
		self.assertEqual(self.user_a.balance, 2)
		self.assertEqual(self.credit_card_a.balance, 5)
		self.assertEqual(self.user_b.balance, 20)

	def test_retrieve_activity(self):
		self.user_a.pay(self.user_b, amount=5, description="Coffee")
		self.user_b.pay(self.user_a, amount=15, description="Lunch")
		
		activity_a = self.user_a.retrieve_activity()
		activity_b = self.user_b.retrieve_activity()
		
		self.assertIn("Bob paid Alice $15.00 for Lunch", activity_a)
		self.assertIn("Alice paid Bob $5.00 for Coffee", activity_b)

	def test_render_feed(self):
		self.user_a.pay(self.user_b, amount=5, description="Coffee")
		self.user_b.pay(self.user_a, amount=15, description="Lunch")
		
		feed = self.app.render_feed()
		self.assertIn("Alice paid Bob $5.00 for Coffee", feed)
		self.assertIn("Bob paid Alice $15.00 for Lunch", feed)

	def test_add_friend(self):
		result = self.user_a.add_friend(self.user_b)
		self.assertTrue(result)
		self.assertIn(self.user_b, self.user_a.friends)
	
	def test_feed_shows_friend_addition(self):
		self.user_a.add_friend(self.user_b)
		feed = self.app.render_feed()
		self.assertIn("Alice and Bob are now friends", feed)
		
	def test_feed_shows_payment(self):
		self.user_a.pay(self.user_b, amount=5, description="Coffee")
		feed = self.app.render_feed()
		self.assertIn("Alice paid Bob $5.00 for Coffee", feed)

	def test_duplicate_friend_addition(self):
		self.user_a.add_friend(self.user_b)
		result = self.user_a.add_friend(self.user_b)
		self.assertFalse(result)

	def test_zero_or_negative_payment(self):
		result_zero = self.user_a.pay(self.user_b, amount=0, description="Invalid Payment")
		result_negative = self.user_a.pay(self.user_b, amount=-5, description="Invalid Payment")
		self.assertFalse(result_zero)
		self.assertFalse(result_negative)

	def test_self_payment(self):
		result = self.user_a.pay(self.user_a, amount=10, description="Self Payment")
		self.assertFalse(result)

	def test_pay_exact_credit_balance(self):
		self.user_a.balance = 0
		self.credit_card_a.balance = 20
		result = self.user_a.pay(self.user_b, amount=20, description="Exact Credit")
		self.assertTrue(result)
		self.assertEqual(self.credit_card_a.balance, 0)
		self.assertEqual(self.user_b.balance, 40)

	def test_pay_more_than_total_balance_and_credit(self):
		self.user_a.balance = 10
		self.credit_card_a.balance = 15
		result = self.user_a.pay(self.user_b, amount=30, description="Over Total Balance")
		self.assertFalse(result)

	def test_large_payment_with_sufficient_credit(self):
		self.user_a.balance = 0
		self.credit_card_a.balance = 5000
		result = self.user_a.pay(self.user_b, amount=4500, description="Large Payment")
		self.assertTrue(result)
		self.assertEqual(self.credit_card_a.balance, 500)
		self.assertEqual(self.user_b.balance, 4520)

	def test_friend_rejects_self_as_friend(self):
		result = self.user_a.add_friend(self.user_a)
		self.assertFalse(result)

	def test_add_friend_multiple_users(self):
		user_c = self.app.create_user("Charlie")
		self.user_a.add_friend(self.user_b)
		self.user_b.add_friend(user_c)
		self.assertIn(self.user_b, self.user_a.friends)
		self.assertIn(user_c, self.user_b.friends)
		self.assertNotIn(user_c, self.user_a.friends)

if __name__ == "__main__":
	unittest.main()
