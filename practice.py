import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner

load_dotenv()

#either you can do it by using os module
#import os
#api_key = os.environ.get("OPEN_API_KEY")
#if not api_key:
#   raise ValueError("API Key is not set")

agent = Agent(
    name = "Basic Agnet",
    instructions="You are a helpful assistant."
    #model="" <- you can use model version here also
)

async def main():
    # result = await Runner.run(agent, "Hello Help me urgently!")
    # print(result.final_output)
    tellme_joke_agent = Agent(
    name="Joke Agent",
    instructions="you need to tell a joke in given topic"
    )

    topic= "AI"

    joke = await Runner.run(tellme_joke_agent, topic)

    print(joke.final_output)

    language_helper = Agent(
        name="language translator",
        instructions="translate the joke into another language"
    )

    translate_joke = await Runner.run(language_helper, f"translate it into spanish language{joke.final_output}")

    print(translate_joke.final_output)

asyncio.run(main())