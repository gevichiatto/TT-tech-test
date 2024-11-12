from typing import List

class CreditCard:
	"""
	Represents a credit card with a balance that can be charged for payments.

	Attributes:
		balance (float): The available balance on the credit card.
	"""

	def __init__(self, balance: float):
		"""
		Initializes the credit card with a specific balance.

		Args:
			balance (float): The initial balance of the credit card.
		"""
		self.balance = balance

	
	def charge(self, amount: float) -> bool:
		"""
		Charges the specified amount to the credit card if sufficient balance is available.

		Args:
			amount (float): The amount to charge.

		Returns:
			bool: True if the charge was successful, False if the balance was insufficient.
		"""
		if self.balance >= amount:
			self.balance -= amount
			return True
		return False


class User:
	"""
	Represents a user in the MiniVenmo system who can make payments, add friends, and view activity.

	Attributes:
		name (str): The name of the user.
		balance (float): The current balance of the user.
		credit_card (CreditCard): An optional credit card assigned to the user.
		friends (List[User]): A list of the user's friends.
		activity_log (List[str]): A log of the user's activities.
	"""

	def __init__(self, name: str, balance: float = 0):
		"""
		Initializes a user with a name and an optional starting balance.

		Args:
			name (str): The name of the user.
			balance (float, optional): The initial balance of the user. Defaults to 0.
		"""
		self.name = name
		self.balance = balance
		self.credit_card = None
		self.friends = []
		self.activity_log = []

	
	def assign_credit_card(self, credit_card: CreditCard):
		"""
		Assigns a credit card to the user for payments.

		Args:
			credit_card (CreditCard): The credit card to assign to the user.
		"""
		self.credit_card = credit_card

	
	def add_friend(self, friend: 'User') -> bool:
		"""
		Adds another user as a friend if not already friends or the same user.

		Args:
			friend (User): The user to add as a friend.

		Returns:
			bool: True if the friend was added successfully, False otherwise.
		"""
		if friend == self:
			return False
		if friend in self.friends:
			return False

		self.friends.append(friend)
		friend.friends.append(self)
		self.activity_log.append(f"{self.name} and {friend.name} are now friends")
		friend.activity_log.append(f"{friend.name} and {self.name} are now friends")
		return True

	
	def pay(self, recipient: 'User', amount: float, description: str = "") -> bool:
		"""
		Makes a payment to another user, using balance first, then credit card if balance is insufficient.

		Args:
			recipient (User): The user receiving the payment.
			amount (float): The amount to pay.
			description (str, optional): A description of the payment.

		Returns:
			bool: True if the payment was successful, False otherwise.
		"""
		if recipient == self:
			return False
		
		if amount <= 0:
			return False

		if self.balance >= amount:
			self.balance -= amount
			recipient.balance += amount
			self.activity_log.append(f"{self.name} paid {recipient.name} ${amount:.2f} for {description}")
			recipient.activity_log.append(f"{self.name} paid {recipient.name} ${amount:.2f} for {description}")
			return True
		elif self.credit_card and self.credit_card.balance >= amount:
			self.credit_card.balance -= amount
			recipient.balance += amount
			self.activity_log.append(f"Paid {recipient.name} ${amount:.2f} for {description} (credit card)")
			recipient.activity_log.append(f"{self.name} paid {recipient.name} ${amount:.2f} for {description}")
			return True

		return False

	
	def retrieve_activity(self) -> List[str]:
		"""
		Retrieves the user's activity log.

		Returns:
			List[str]: The activity log of the user.
		"""
		return self.activity_log


class MiniVenmo:
	"""
	Represents the main application managing users and the transaction feed.

	Attributes:
		users (List[User]): A list of users in the application.
	"""

	def __init__(self):
		"""
		Initializes the MiniVenmo application with an empty user list.
		"""
		self.users = []

	
	def create_user(self, name: str, balance: float = 0) -> User:
		"""
		Creates a new user with a specified name and optional starting balance.

		Args:
			name (str): The name of the new user.
			balance (float, optional): The starting balance of the new user.

		Returns:
			User: The newly created user.
		"""
		new_user = User(name, balance)
		self.users.append(new_user)
		return new_user

	
	def render_feed(self) -> List[str]:
		"""
		Renders a global activity feed of all user transactions and friendships.

		Returns:
			List[str]: The rendered activity feed.
		"""
		feed = []
		for user in self.users:
			for entry in user.retrieve_activity():
				if entry not in feed:
					feed.append(entry)
		return feed
	
def main():
	app = MiniVenmo()

	alice = app.create_user("Alice", balance=100)
	bob = app.create_user("Bob", balance=50)
	charlie = app.create_user("Charlie", balance=0)

	alice_credit_card = CreditCard(balance=200)
	alice.assign_credit_card(alice_credit_card)

	charlie_credit_card = CreditCard(balance=100)
	charlie.assign_credit_card(charlie_credit_card)

	alice.add_friend(bob)
	bob.add_friend(charlie)

	alice.pay(bob, 25, "lunch")
	bob.pay(charlie, 10, "movie ticket")
	charlie.pay(alice, 5, "snack")

	self_payment_try = alice.pay(alice, 10, "self-payment")
	print(f"Self-payment successful? {self_payment_try}")

	charlie.pay(alice, 50, "gift")

	# Render the global feed
	feed = app.render_feed()
	print("\nMiniVenmo Activity Feed:")
	for entry in feed:
		print(entry)

if __name__ == "__main__":
  main()
