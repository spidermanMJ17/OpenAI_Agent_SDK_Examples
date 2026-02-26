# For multi-turn conversations, the agent needs to remember what was said before. You use to_input_list() to pass previous context to the next turn:

from agents import Agent, Runner, TResponseInputItem
import asyncio
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    name='MJ',
    instructions='You are friendly assistant reply politely'
)

# async def main():
#     result = await Runner.run(agent, "Hello! Good Morning :)")
#     # print(result.to_input_list())
#     print(result.final_output)
#     print('\n' + '-'*50 +'\n')
#     for message in result.to_input_list():
#         print(message)

async def main():
    conversation : list[TResponseInputItem] = []
    print('Agent MJ live')
    print('Now you are talking with agent MJ, please type your query or type EXIT to leave the chat')
    while True:
        user_input = input('Your Query: ')
        print('You: '+ user_input)
        if user_input == 'EXIT':
            print('Agent terminated')
            break
        conversation.append({'content': user_input, 'role' : 'user'})
        result = await Runner.run(agent, conversation)
        print(f"Agent Response: {result.final_output}")

        conversation = result.to_input_list()

asyncio.run(main())