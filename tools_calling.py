#tool calling is a way to extend the capabilities of an LLM by allowing it to call ecternal tool or APIs this can be useful for tasks that require access to another tooll or functionality

import asyncio
from agents import Agent, Runner, function_tool, WebSearchTool
from dotenv import load_dotenv

load_dotenv()

@function_tool
def get_weather(city: str) -> str:
    print(f"getting the weather of the {city}")
    return f"The weather of the {city} at night on 25/12/25 is"

agent1 = Agent(
        name="weather_detector",
        instructions="Yor given with city, please find weather of it on 25/12/25 at night",
        tools=[get_weather]
    )

#creating web search tool
agent2 = Agent(
    name="new reporter",
    instructions="suppose you are a news reporter please tell the user necessary news for given city",
    tools=[WebSearchTool()]
)
async def main():
    # result = await Runner.run(agent2, 'Chicago')
    # print(result.final_output)
    while True:
        query = input("Enter city name her or (type 'quit' to exit and close the programme)")
        if query == 'quit':
            break

        result = await Runner.run(agent1, query)
        print("Result")
        print(result.final_output)
        print('\n' + '-'*50 + '\n')

asyncio.run(main())