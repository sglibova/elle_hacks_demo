from dotenv import load_dotenv
import time
import os
load_dotenv()

mantium_user = os.getenv('MANTIUM_USER')
mantium_password = os.getenv('MANTIUM_PASSWORD')
prompt_id = os.getenv('PROMPT_ID')

from mantiumapi import client
from mantiumapi import prompt


# this is not necessary to the code, but I like to use it to check that it works
mantium_token = client.BearerAuth().get_token()

#check and confirm successful login
if mantium_token:
    print("Successfully logged in to Mantium API with user {mantium_user}.")

# retrieve Ice Cream Generator Prompt by ID from Mantium
ice_cream_prompt = prompt.Prompt.from_id(prompt_id)

def prompt_results():
    """ Retrieve results from the prompt above - uses a pre-configured prompt from ID.
    Checks to make sure the returned value is not an empty string.
    Returns ice cream flavor as prompt_result.
    """

    executed_prompt = ice_cream_prompt.execute("")
    executed_prompt.refresh()

    time.sleep(1)  # prompt execution takes a small amount of time > this helps ensure a response

    while executed_prompt.output == None or executed_prompt.output == "":
        print("Prompt result empty, re-running prompt.")

        while executed_prompt.status != "COMPLETED":
            print("Prompt processing status: {executed_prompt.status}")
            prompt.refresh()
            time.sleep(1)
        
        executed_prompt.execute("")
        executed_prompt.refresh()
        time.sleep(1)
    
    prompt_result = executed_prompt.output
    

    return prompt_result


if __name__ == "__main__":
    flavor = prompt_results()
    assert isinstance(flavor, str)

    print(flavor)
