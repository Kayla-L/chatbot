"""
Instructions:

0. Run the chatbot (there will be errors because there's missing code)
1. Fill in code for TODOs 1-5
2. Run the chatbot & get rid of all the errors, when you type "hi" into the
   prompt, the chatbot should respond, "Hello!"
3. Add 2 more intents (TODO 6)
4. Run the chatbot & get rid of all errors, get it to notice all 3 intents
5. Randomize response (TODO 7) and add responses to a greeting (TODO 8)
   HINT: use the library:
     import random
6. Run the chatbot & get rid of all errors, run multiple times to see it
   greet the user multiple ways
7. Modify the matching function (TODOs 9, 10, and optionally 11) to make the
   chatbot more likely to understand the user, even if they type things slightly
   differently than the pattern
8. Run the chatbot & get rid of all errors, see if it catches different versions
   of the user's utterances
9. Add an introduction (TODOs 12 & 13)
10. Run the chatbot & get rid of all errors
11. Modify the code so that the conversation ends when the user has the "goodbye" intent
12. Run the chatbot & get rid of all errors
13 (optional). Any other changes you want to make!
"""

"""
Here's where we can store any variables the computer learns from the user.
"""
conversation_state = {
  "user_name": None
}

"""
Here's where we store data of what kinds of intentions the user might have in
talking to the chatbot. Things like greetings, farewells, asking for the
chatbot's name, etc.

Right now, we're starting off with just one intent, a "greeting" intent. Each
intent stores patterns of text the user might say that would signal this intent
and some information about how to respond.\

TODO 6: add more intents
"""
intents = {
  # Each user intent has a name to identify it, in this case, to greet the
  # chatbot
  "greeting": {
    # Things the user might say that would signal their intent to greet the
    # chatbot
    "utterance_patterns": [
      # TODO 3: this should be a comma-separated list of strings that the user
      # might say that are greetings
      "hello", 
      "good morning", 
      "good afternoon", 
      "good evening",
      "hi", 
      "hey"
    ],
    # Ways the chatbot can respond if the user intends to greet the chatbot
    # TODO 8: add more ways the chatbot can respond to a greeting
    "responses": [
      {
        "text": "Hello!"
      },
      {
        # Text to send back to the user might require the chatbot to remember
        # things the user has said in the past.
        "text": "Hello, {user_name}!",
        "required_state_variables": ["user_name"]
      }
    ]
  },
  "ask_name": {
    "utterance_patterns": [
      "what's your name?",
      "what is your name?",
      "who are you?",

    ],
    "responses": [
      {
        "text": "I don't have a name just yet. Hopefully I will have one soon."
      },
      {
        "text": "Hmm, what a good question. I do not know. Might you have any suggestions?"
      }
    ]
  }
  # "INTENT_NAME": {
  #   "utterance_patterns": [
  #     "",
  #     ""
  #   ],
  #   "responses": [
  #     {
  #       "text": ""
  #     }
  #   ]
  # }
}

"""
A default intent. What should we do if we can't understand what the user was
trying to say?
"""
default_intent = {
  "responses": [
    {
      "text": "I'm sorry, I did not understand."
    }
  ]
}

"""
A function that takes in a pattern from the intent and the actual utterance the
user said and decides whether the pattern matches what the user said
TODO 9: improve matching function to ignore case (uppercase vs lowercase)
TODO 10: improve matching function to ignore whitespace
TODO 11: more improvements to matching function?
"""
def match_utterances(utterance, utterance_pattern):
  # TODO 4: check if the utterance is exactly the same as the utterance pattern
  if utterance == utterance_pattern:
    return True
  else:
    return False

"""
Given an utterance from the user, determine what their intention was.

Returns the name of the intent that was matched to the user's utterance
"""
def match_intent(utterance):
  # Look through every intent name in the intents dict
  for intent_name in intents:
    # Grab the dict with data for that intent
    intent = intents[intent_name]
    # Grab the utterance patterns that signal that intent
    utterance_patterns = intent["utterance_patterns"]
    # For each utterance pattern, see if it matches what the
    # user actually said
    for utterance_pattern in utterance_patterns:
      # If a pattern in this intent matches what the user
      # said, then return the name of the intent that
      # was matched.
      if match_utterances(utterance, utterance_pattern):
        return intent_name
  # If we get through all the intents and none of the patterns
  # match, return None to indicate there was no match
  return None

"""
Some of the responses the chatbot might consider include information like the
user's name that get's learned through the conversation. If the user hasn't told
the chatbot that information yet, then the chatbot can't use that information
to create the response. So we filter to only the responses that we have enough
information for.
"""
def filter_responses_to_known_variables(responses):
  possible_responses = []
  for response in responses:
    # If the response requires variables from the conversation
    # state, check if we have those variables
    if "required_variables" in response:
      required_variables = response["required_variables"]
      # Start off assuming that we are NOT missing variables
      missing_variables = False
      for required_variable in required_variables:
        if required_variable in conversation_state:
          if conversation_state[required_variable] is None:
            missing_variables = True
        else:
          # If we find a missing variable, set missing_variables
          # to True
          missing_variables = True
    # If the response doesn't require any variables, then
    # none of the variables are missing
    else:
      missing_variables = False
    if not missing_variables:
      possible_responses.append(response)
  return possible_responses

"""
Given a user's intention, decide how the chatbot should respond.
"""
def decide_response(intent_name):
  if intent_name is None:
    intent = default_intent
  else:
    # Grab the dict with data for that intent
    intent = intents[intent_name]
  # Grab all possible responses for that intent
  all_responses = intent["responses"]
  # Filter to only the responses we have enough information for
  # (exclude any intents that require more variables in the
  # conversation state)
  possible_responses = filter_responses_to_known_variables(all_responses)
  # TODO 7: randomly chose from multiple possible responses
  # TODO 5: return the first element from possible_responses
  response = possible_responses[0]
  return response

"""
Display a prompt and return the user's utterance
"""
def get_user_utterance():
  # get input from the user
  user_utterance = input("Type something here to have a chat: ")
  return user_utterance

"""
Once we've decided on the text of our response, print that text out for the user
"""
def display_chatbot_response(response):
  # TODO 2: print out the chatbot's response
  print("Chat Bot:", response)

"""
Some extra code to add variables that the chatbot remembers from talking to the
user, like the user's name or favorite color.
"""
def add_variables_to_response(response_data):
  text = response_data["text"]
  if "required_variables" in response_data:
    required_variables = response_data["required_variables"]
    text = text.format(**conversation_state)
  return text

"""
Before we get to the main loop of the conversation, start off with a predictable
script where the chatbot introduces themselves and asks the user questions
TODO 12: add introduction text where the chatbot introduces themself to the user
TODO 13: ask user's name and put that into the conversation_state (dict at top)
"""
def introduction():
  pass

"""
Main program loop
"""
def main():
  introduction()
  # TODO 14: allow the computer to stop the conversation if the user says "goodbye"
  continue_conversation = True
  while continue_conversation:
    user_utterance = get_user_utterance()
    user_intent_name = match_intent(user_utterance)
    chatbot_response_data = decide_response(user_intent_name)
    chatbot_response_text = add_variables_to_response(chatbot_response_data)
    display_chatbot_response(chatbot_response_text)

main()