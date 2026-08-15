import random

def add(num1: int , num2: int):
    return num1 + num2 


def substract(num1, num2):
    return num1 - num2




class BankAccount():
    def __init__(self, balance: int, user):
        self.balance = balance
        self.user = user
        self.history = []
        
    def get_acct_no(self):
        acct_no = "".join(random.choice("0123456789") for _ in range(10))
        self.history.append(acct_no)
        return f'for user: {self.user} acct no is :{acct_no}'
        
        
    def deposit(self, amount: int):
        if amount > 0:
            self.balance+=amount
            self.history.append(self.balance)
            
        return f'your new balance {self.balance}'
    
    def withdraw(self, amount: int):
        if amount <= self.balance and amount > 0:
            self.balance-=amount
            self.history.append(self.balance)
            return f'You withdrew {amount} and your new balance is {self.balance}'
        elif self.balance < amount:
            raise Exception("thief")
    
    def check_balance(self):
        return {"trans":self.history}
    
bb= BankAccount(50, "dan")
bb.deposit(40)
bb.withdraw(38)
bb.withdraw(-4)
print(bb.check_balance())

