import openai
openai.api_key = "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"
def chatgptcall(prompt):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
        "role": "user",
        "content": f"give me the 4 main ingredients in {prompt}, following the format ingredient, ingridient, etc - limited to only plainly formatted text without a preamble sentence or numbering. And no period nor and at the finally. furthermore, no generalized ingridients such as (toppings) rather, specify an example. Finally, all characters must be in lower case. Make sure to leave a space after each comma. "

        }
    ],
    temperature=0,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    print(response["choices"][0]["message"]["content"])
    return response["choices"][0]["message"]["content"]
chatgptcall("pizza")