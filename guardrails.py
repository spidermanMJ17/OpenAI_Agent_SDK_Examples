#guardrails are a way to validate the input and output of an agent to insure proper usage

from agents import Agent, Runner, input_guardrail,RunContextWrapper, TResponseInputItem, GuardrailFunctionOutput, InputGuardrailTripwireTriggered, output_guardrail, OutputGuardrailTripwireTriggered
import asyncio
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

#input guardrails

class homework_detection_class(BaseModel):
    cheat: bool
    explaination: str

homework_cheat_agent = Agent(
    name = 'guardrail_agent',
    instructions=(
        "Determine if the user's query resembles a typical homework assignment or exam question, indicating an attempt to cheat. General questions about concepts are acceptable. "
        " Cheating: 'Fill in the blank: The capital of France is ____.',"
        " 'Which of the following best describes photosynthesis? A) Cellular respiration B) Conversion of light energy C) Evaporation D) Fermentation.'"
        " Not-Cheating: 'What is the capital of France?', 'Explain photosynthesis.'"
    ),
    output_type=homework_detection_class
)

@input_guardrail
async def cheat_detection_guardrails(
        ctx: RunContextWrapper[None],
        agent: Agent,
        input: str | list[TResponseInputItem]
    ) -> GuardrailFunctionOutput:

    detection_result = await Runner.run(homework_cheat_agent, input)

    return GuardrailFunctionOutput(
        tripwire_triggered=detection_result.final_output.cheat,
        output_info=detection_result.final_output
    )

study_helper = Agent(
    name  = 'study_helper',
    instructions='You are a study helper and you explain concept or provide guidance, without directly solving homework or test questions.',
    input_guardrails=[cheat_detection_guardrails]
)

# async def main():
#     try:
#         response = await Runner.run(study_helper, "What is the capital of india?")
#         print("Guardrail didn't trigger")
#         print("Response: ", response.final_output)
#     except InputGuardrailTripwireTriggered as e:
#         print("Cheat detected")
#         print("details are as follow", str(e))

# asyncio.run(main())

#-----------------------------------------------------------------------

#output guardrail

@output_guardrail
def llm_output_guardrail(
    ctx: RunContextWrapper,
    agent: Agent,
    output: str
    ) -> GuardrailFunctionOutput: 
    #mentioning forbidden messages
    forbidden_messages = ['cricket', 'football', 'baseball']

    #to avoid incosistance change output to lower
    lower_output = output.lower()

    #now checking if forbidden word exist in output or not
    output_check =  [phrase for phrase in forbidden_messages if phrase in lower_output]
    trip_triggered = bool(output_check)

    print(f"Found forbidden phrases: {output_check}")

    return GuardrailFunctionOutput(
        output_info={
            'reason' : 'Forbidden phrases are found from your query',
            'Forbidden words': output_check
        },
        tripwire_triggered=trip_triggered
    )

customer_support_agent = Agent(
    name='customer_support',
    instructions='You are a good customer support agent, help them with polite answer',
    output_guardrails=[llm_output_guardrail]
)

async def main():
    topic = 'Tell me more about soccer, please dont disappoint me I need reply urgently, please!'
    try:
        result = await Runner.run(customer_support_agent, topic)
        print('Trip didnt triggered')
        print(f"Your output is : {result.final_output}")
    except OutputGuardrailTripwireTriggered as e:
        print('Trip triggered because of forbidden word')
        print(str(e))

asyncio.run(main())