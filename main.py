from core import respond
from memory import load_name, save_name
from data.jokes import tell_joke


def get_user_name():

    name = load_name()

    if name is None:
        name = input("What is your name? ").strip()
        save_name(name)

    return name


def main():

    print("J.O.A.T. — Jack Of All Trades")

    name = get_user_name()

    print(f"J.O.A.T.: Welcome back, {name}!")
    print("J.O.A.T.: Type 'exit' to quit, or 'joke' if you want a laugh.")

    while True:

        message = input("You: ").strip()

        if message.lower() == "exit":
            print("J.O.A.T.: Goodbye!")
            break

        if message.lower() == "joke":
            print("J.O.A.T.:", tell_joke())
            continue

        answer = respond(message)

        print("J.O.A.T.:", answer)


if __name__ == "__main__":
    main()
