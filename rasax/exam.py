import openai

openai.api_key = "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"

def chatgpt_clone(prompt):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt= prompt,
    temperature=1,
    max_tokens=800,
    top_p=1,
    frequency_penalty=0.6,
    presence_penalty=0.6,
    )
    print(response.choices[0].text)
    return response.choices[0].text

print(chatgpt_clone("Xin chào"))