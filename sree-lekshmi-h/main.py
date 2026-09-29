from agents import handle_query

while True:

    user_input = input("\nYou: ")

    if user_input.lower() in ["exit", "quit"]:
        break

    answer = handle_query(user_input)

    print("\nAssistant:", answer)