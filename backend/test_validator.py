from models.state import create_state

from agents.workflow import workflow


questions = [

    "How much did I spend on Amazon?",

    "Give me my financial summary",

    "Am I overspending?",

    "Can I save ₹2 lakh in one year?"

]


for question in questions:

    print()

    print("=" * 80)

    print(question)

    print("=" * 80)

    print()

    state = create_state(

        question,

        "user_001"

    )

    result = workflow.run(

        state

    )

    print("Executed Agent:")

    print(result["current_agent"])

    print()

    print("Answer:")

    print(result["answer"])

    print()