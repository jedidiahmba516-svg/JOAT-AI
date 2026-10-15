class Genesis:

    def __init__(self, owner):
        self.owner = owner

    def greet(self):
        print(f"Hello! I am Genesis.")
        print(f"My creator is {self.owner}.")

    def answer(self, message):

        if message.lower() == "hello":
            return "Hello!"

        elif message.lower() == "who made you":
            return f"I was created by {self.owner}."

        else:
            return "I don't understand yet."    
        