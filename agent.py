# Simple AI agent for a college assignment
# This program asks the user for a question, classifies it, and answers.

# Function to classify the question into one of four categories
# using words that are easy to understand.
def classify_question(question):
    question_lower = question.lower()

    if "code" in question_lower or "program" in question_lower or "python" in question_lower:
        return "programming"
    elif "study" in question_lower or "homework" in question_lower or "exam" in question_lower:
        return "study"
    elif "game" in question_lower or "joke" in question_lower or "fun" in question_lower:
        return "fun"
    else:
        return "general"

# Function to give a response based on category.
def get_response(category):
    if category == "programming":
        return "It sounds like a programming question. Keep practicing your code!"
    elif category == "study":
        return "Study questions are important. Make a plan and take small steps."
    elif category == "fun":
        return "Fun questions are great! A little break can help you feel better."
    else:
        return "That sounds like a general question. I'm here to help however I can."

# Function to show help examples for the user.
def print_help():
    print("You can ask questions about these topics:")
    print("- programming: code, python, program")
    print("- study: study, homework, exam")
    print("- fun: game, joke, fun")
    print("- general: any other question")
    print("Type 'exit' to stop the program.")
    print()

# Main loop that runs until the user types "exit".
def main():
    print("Welcome to the simple AI agent! Type 'help' for examples or 'exit' to stop.")

    while True:
        user_input = input("Enter your question: ")

        # Stop the program when the user types exit.
        if user_input.strip().lower() == "exit":
            print("Goodbye! Thanks for using the AI agent.")
            break

        # Show help examples when the user types help.
        if user_input.strip().lower() == "help":
            print_help()
            continue

        category = classify_question(user_input)
        answer = get_response(category)

        print("Category:", category)
        print("Answer:", answer)
        print()

# This line starts the program when the file is run.
if __name__ == "__main__":
    main()
