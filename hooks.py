from agents import Agent, Runner, RunHooks, function_tool
import time
import asyncio
from dotenv import load_dotenv
load_dotenv()

#creating class for Hooks
class logginghooks(RunHooks):

    def __init__(self):
        self.start_times = {}

    async def on_agent_start(self, context, agent):
        print(f"Agent Started{agent.name}")
        self.start_times[agent.name] = time.time()

    async def on_llm_start(self, context, agent, system_prompt, input_items):
        print(f"LLM call started: {agent.name}")
    
    async def on_llm_end(self, context, agent, response):
        print(f"LLLM response recieved: {agent.name}")
        if response.usage:
            print("Tocken Used: ", response.usage.total_tokens)
    
    async def on_tool_start(self, context, agent, tool):
        print(f"Tool called: {tool.name}")

    async def on_tool_end(self, context, agent, tool, result):
        print("Tool finished: ", tool.name)
        print("Tool response: ", result)

    async def on_handoff(self, context, from_agent, to_agent):
        print(f"Handoff triggered: {from_agent} to {to_agent}")

    async def on_agent_end(self, context, agent, output):
        start_time = self.start_times.get(agent.name)
        if start_time:
            duration = time.time() - start_time
            print("Agent run duration is: ", duration)
        
        print("Agent Finished", agent.name)

#creating TOOL
@function_tool
async def calculator(expression: str) -> str:
    try:
        result = eval(expression, {"__builtins__": {}})
        return str(result)
    except Exception as e:
        print("Error", e)

#creating summary agent
summary_agent = Agent(
    name="Summary Agent",
    instructions="""
    you are a summary generator keep it short and readable friendly
    """
)

#creating research agent
research_agent = Agent(
    name="Research Agent",
    instructions="""
    you are a research assistant you have to reseach on it
    if user ask to do simple math use calculator tool or response by your capability
    """,
    tools=[calculator],
    handoffs=[summary_agent]
)

#main workflow
async def main():
    # runner = Runner(
    #     hooks=logginghooks()
    # )
    result = await Runner.run(
        research_agent,
        input="what is the solution for given pattern: 17 *17, explain briefly",
        hooks=logginghooks()
    )
    print("Final Result")
    print("your response is as follow: ", result.final_output)
    print("Thank you for visiting, Visit Again!")

asyncio.run(main())