from openai import OpenAI
from loggerino import log


def get_ai_response(post_title, modifier, post='post'):
    prompt = f'write me a very short, {modifier} reply for the following reddit {post}: \n"'
    prompt += f'{post_title}'
    client = OpenAI(
        api_key = '' # add your openAI api key here
        )
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                'role':'user',
                'content':prompt
                }
            ],
            model='gpt-3.5-turbo'
        )
        temp_response = chat_completion.choices[0].message.content
        response = temp_response.replace('"', '')
        response = response.replace('!', '')
        response = response.lower()
        if response[:6] == 'reply:':
            response = response[7:]
        log(f'Response received from openAi: {response}')
    except Exception as e:
        log('Error getting a response from openAI:' + e)
    return response