#a way of invoking another agent for a current agent
from pydantic import BaseModel
from agents import Agent, Runner, handoff, RunContextWrapper
import asyncio
from dotenv import load_dotenv

load_dotenv()

class recipe_schema(BaseModel):
    title: str
    outline_given_as : str
    recipe: list[str]

# class outline_schema(BaseModel):
#     title: str
#     outline_given_as : str

outline = Agent(
    name="outline builder",
    instructions="given a dish name provide how it tastes",
    # output_type=outline_schema
    # handoff_description='invoke it when you want to prepare recipe as it will provide you first level outline' # <- A description of the agent. This is used when the agent is used as a handoff, so that an LLM knows what it does and when to invoke it
)

# def on_recipe_tutor(ctx: RunContextWrapper[None]):
#     print("outline handoff called")

recipe = Agent(
    name="recipe builder",
    instructions="given the food dish and from generated its outline, prepare recipe which could be helpful for indian people, first handoff to outline agent and then generate recipe and give output in  a strcuture way in a defined schema",
    # handoffs=[outline],
    tools=[
        outline.as_tool(
            tool_name='outline_builder',
            tool_description="use it to generate outline for the food"
        )
    ],
    output_type=recipe_schema, #defining strict schema to follow for output
)

async def main():
    result = await Runner.run(recipe, "Shushi")
    print(result.final_output)

asyncio.run(main())