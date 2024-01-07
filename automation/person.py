class Person:
    def __init__(self, name, email, discord):
        self.name = name
        self.email = email
        self.discord = discord
        
    def __eq__(self, other):
        return self.name == other.name and self.email == other.email and self.discord == other.discord

    def __hash__(self):
        return hash((self.name, self.email, self.discord))

    def __repr__(self):
        return f"({self.name}, {self.email}, {self.discord})"

    def __str__(self):
        return f"({self.name}, {self.email}, {self.discord})"