#watch again found it confusing
import asyncio
from agents import Agent, Runner, ItemHelpers
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    name='Joke agent',
    instructions='You are a helpful assistant'
)

# async def main():
#     result = Runner.run_streamed(agent, input='tell me 5 unique words which dont contains vowels')
#     async for event in result.stream_events():
#         if event.type == 'raw_response_event' and isinstance(event.data, ResponseTextDeltaEvent): #isinstance(object, Class)
#             print(event.data.delta, end="", flush=True)

# result.stream_events() 
#   → filters event.type == 'raw_response_event' 
#   → further filters isinstance(event.data, ResponseTextDeltaEvent)
#   → gets the actual text chunk (event.data.delta)
#   → prints it in real-time

# event = {
#     type: 'raw_response_event',    # What kind of event
#     data: <some object>             # The actual payload/content
# }

# Multiple data types in raw_response_event - Even within raw_response_event, the event.data can be different types:

# ResponseTextDeltaEvent - actual text chunks
# ResponseDoneEvent - completion signal
# ResponseRefusalDeltaEvent - refusal messages
# Other response-related events

async def main():
    result = Runner.run_streamed(agent, input='tell me 5 unique words which dont contains vowels')
    async for event in result.stream_events():
        # We'll ignore the raw responses event deltas
        if event.type == "raw_response_event":
            continue
        # When the agent updates, print that
        elif event.type == "agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
            continue
        # When items are generated, print them
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("-- Tool was called")
            elif event.item.type == "tool_call_output_item":
                print(f"-- Tool output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
            else:
                pass  # Ignore other event types

    print("=== Run complete ===")

asyncio.run(main())