import os
import json
import re
import logging
from dotenv import load_dotenv
from together import Together
from Prompts.Negotiate import NEGOTIATION_PROMPT_TEMPLATE
load_dotenv(override=True)
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
logging.basicConfig(filename='negotiation.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def negotiate_with_llama(negotiation_data):
    context = negotiation_data['context']
    user_goal = negotiation_data['user_goal']
    messages = negotiation_data['messages']

    # Construct the conversation history
    conversation_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])

    negotiation_prompt = NEGOTIATION_PROMPT_TEMPLATE

    messages = [{"role": "user", "content": negotiation_prompt}]

    try:
        completion = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=0.9,
            top_k=50,
            repetition_penalty=1,
        )

        ai_response = completion.choices[0].message.content
        logging.info(f"AI Response: {ai_response}")

        # Parse the JSON response
        negotiation_response = json.loads(ai_response)
        return negotiation_response

    except Exception as e:
        logging.error(f"Error in negotiation: {e}")
        return None


def is_ending_message(message):
    ending_patterns = [
        r"thank you,?\s+all the best",
        r"amazing,?\s+thank you"
    ]
    return any(re.search(pattern, message.lower()) is not None for pattern in ending_patterns)


def main(
        context="The seller is selling a couch that is $150, it's blue and in great condition",
        user_goal="Get $50 discount to buy the couch",
        first_message="Hi there! The couch sounds nice. I'm looking for a couch around $100. Would you be open to negotiating the price?"
    ):

    negotiation_data = {
        "context": context,
        "user_goal": user_goal,
        "messages": [
            {"role": "seller", "content": "Hello! It's in great condition and very comfortable."},
            {"role": "assistant", "content": first_message }
        ]
    }

    logging.info(f"Context: {negotiation_data['context']}")
    logging.info("The conversation begins:")

    for message in negotiation_data['messages']:
        print(f"{message['role'].capitalize()}: {message['content']}")

    while True:
        seller_message = input("\nYour response (or 'quit' to end): ")
        if seller_message.lower() == 'quit':
            break

        negotiation_data['messages'].append({"role": "seller", "content": seller_message})
        logging.info(f"Seller: {seller_message}")

        llm_response = negotiate_with_llama(negotiation_data)
        if llm_response:
            print(f"(Reasoning: {llm_response['reasoning']})")
            print(f"\nBuyer: {json.dumps(llm_response, indent=2)}")
            negotiation_data['messages'].append({"role": "assistant", "content": llm_response['content']})

            if is_ending_message(llm_response['content']):
                logging.info("The AI has concluded the negotiation. Ending the conversation.")
                break
        else:
            logging.error("Failed to generate buyer's response. Ending negotiation.")
            break

    logging.info("Negotiation ended.")


if __name__ == "__main__":
    main()