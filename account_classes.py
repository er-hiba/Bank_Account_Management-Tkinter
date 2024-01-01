from abc import ABC, abstractmethod

class Account(ABC):
    __counter = 0

    def __init__(self, number, owner, balance, opening_date):
        self.__number = number
        self.__owner = owner
        self.__balance = balance
        self.__opening_date = opening_date
        Account.__counter += 1

    @staticmethod
    def get_counter():
        return Account.__counter

    @property
    def get_number(self):
        return self.__number

    @property
    def get_owner(self):
        return self.__owner

    @property
    def get_balance(self):
        return self.__balance

    @property
    def get_opening_date(self):
        return self.__opening_date

    def set_counter(new_number):
        Account.__counter = new_number

    @abstractmethod
    def __str__(self):
        pass


class CurrentAccount(Account):
    def __init__(self, number, owner, balance, opening_date, overdraft):
        super().__init__(number, owner, balance, opening_date)
        self.__overdraft = overdraft

    @property
    def get_overdraft(self):
        return self.__overdraft

    def __str__(self):
        return f"Account number: {self.get_number}; Owner: {self.get_owner}; Balance: {self.get_balance}; Opening date: {self.get_opening_date}; Overdraft amount: {self.__overdraft}"


class SavingsAccount(Account):
    def __init__(self, number, owner, balance, opening_date, interest):
        super().__init__(number, owner, balance, opening_date)
        self.__interest = interest

    @property
    def get_interest(self):
        return self.__interest

    def __str__(self):
        return f"Account number: {self.get_number}; Owner: {self.get_owner}; Balance: {self.get_balance}; Opening date: {self.get_opening_date}; Interest rate: {self.__interest}"
