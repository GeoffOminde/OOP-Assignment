from datetime import datetime

class ArcadePass:
    """
    Base class for an arcade pass with a protected balance and common behaviors.
    """
    def __init__(self, owner: str, starting_balance: float = 0.0):
        self.owner = owner
        self.__balance = 0.0
        self.created_at = datetime.now()
        self.top_up(starting_balance)

    @property
    def balance(self) -> float:
        # Read-only access; direct writes are not allowed
        return round(self.__balance, 2)

    def _charge(self, amount: float):
        # Internal method: encapsulated balance mutation
        if amount < 0:
            raise ValueError("Charge amount must be positive.")
        if amount > self.__balance:
            raise ValueError("Insufficient balance.")
        self.__balance -= amount

    def top_up(self, amount: float):
        if amount < 0:
            raise ValueError("Top-up must be non-negative.")
        self.__balance += amount

    def discount_rate(self) -> float:
        # Default: no discount
        return 0.0

    def play(self, game_name: str, base_cost: float) -> str:
        """
        Polymorphic target: subclasses may override pricing, rewards, or messaging.
        """
        cost = base_cost * (1 - self.discount_rate())
        self._charge(cost)
        return f"{self.owner} played {game_name} for {cost:.2f} credits."

    def __str__(self):
        return f"ArcadePass(owner={self.owner}, balance={self.balance})"


class StandardPass(ArcadePass):
    """
    Standard tier: no discounts, but earns tiny cashback on play.
    """
    def discount_rate(self) -> float:
        return 0.0

    def play(self, game_name: str, base_cost: float) -> str:
        msg = super().play(game_name, base_cost)
        # 1% cashback as a perk
        cashback = 0.01 * base_cost
        # Use top_up to respect encapsulation instead of writing balance directly
        self.top_up(cashback)
        return f"{msg} Earned {cashback:.2f} cashback. New balance: {self.balance:.2f}"


class VIPPass(ArcadePass):
    """
    VIP tier: 20% discount, higher cashback, and priority queueing.
    """
    def discount_rate(self) -> float:
        return 0.20

    def play(self, game_name: str, base_cost: float) -> str:
        # Different behavior: discount + bigger cashback + VIP message
        discounted = base_cost * (1 - self.discount_rate())
        super()._charge(discounted)  # use protected method intentionally
        cashback = 0.05 * base_cost
        self.top_up(cashback)
        return (
            f"[VIP] {self.owner} played {game_name} with 20% off: {discounted:.2f}. "
            f"Cashback: {cashback:.2f}. Balance: {self.balance:.2f}"
        )


# Demo
if __name__ == "__main__":
    standard = StandardPass("Ayo", starting_balance=10.00)
    vip = VIPPass("Nairobi", starting_balance=10.00)

    print(standard)
    print(vip)

    print(standard.play("Neon Drift", base_cost=4.00))
    print(vip.play("Neon Drift", base_cost=4.00))

    # Encapsulation in action: the next line would fail if uncommented
    # standard.__balance = 999  # AttributeError due to name mangling
    print("Final balances:", standard.balance, vip.balance)