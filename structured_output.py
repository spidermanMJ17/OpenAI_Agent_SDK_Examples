#structured outputs are a way to fomrat the output of an llm in a structured manner, this can be useful for tasks that require specific formatting or data extraction

from dotenv import load_dotenv
from agents import Agent, Runner
import asyncio
from pydantic import BaseModel

load_dotenv()

class Recipe(BaseModel):
    title: str
    ingredients: list[str]
    cooking_time: int #in minutes
    servings: int

async def main():
    recipe_agent = Agent(
        name="recipe Agent",
        instructions="You are shef and you need to tell user an recipe for given food",
        output_type=Recipe #this is important now AI will return the output in given class structure
    )
    ask_recipe = await Runner.run(recipe_agent, "Mysore Dosa")
    #print(ask_recipe)
    print(f"title is {ask_recipe.final_output.title}")
    print(f"ingrediants are as follow {ask_recipe.final_output.ingredients}")
    print(f"cooking time is as follow: {ask_recipe.final_output.cooking_time} minutes")
    print(f"serrving is as follow {ask_recipe.final_output.servings}")

asyncio.run(main())