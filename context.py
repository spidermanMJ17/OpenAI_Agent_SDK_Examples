#A way to pass along data during the agents lifecycle

from pydantic import BaseModel
from agents import (
    Agent,
    Runner,
    InputGuardrailTripwireTriggered,
    input_guardrail,
    RunContextWrapper,
    TResponseInputItem,
    GuardrailFunctionOutput
)
import asyncio
from dotenv import load_dotenv

load_dotenv()

class userprofile(BaseModel):
    id: str
    name: str
    admin: bool

class homeworkdetection(BaseModel):
    cheating : bool
    explanation: str

homework_cheat_agent = Agent(
    name='homework cheat detector',
    instructions=(
        "Determine if the user's query resembles a typical homework assignment or exam question, indicating an attempt to cheat. General questions about concepts are acceptable. "
        " Cheating: 'Fill in the blank: The capital of France is ____.',"
        " 'Which of the following best describes photosynthesis? A) Cellular respiration B) Conversion of light energy C) Evaporation D) Fermentation.'"
        " Not-Cheating: 'What is the capital of France?', 'Explain photosynthesis.'"
    ),
    output_type=homeworkdetection
)

@input_guardrail
async def homework_guardrail(
    ctx: RunContextWrapper[userprofile],
    agent: Agent,
    input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    if ctx.context.admin:
        return GuardrailFunctionOutput(
            output_info=homeworkdetection(
                cheating=False, 
                explanation='Admin Bypass'
            ),
            tripwire_triggered=False
            )
    detection_result = await Runner.run(homework_cheat_agent, input, context=ctx.context)

    print(ctx.context)
    return GuardrailFunctionOutput(
        output_info=detection_result.final_output,
        tripwire_triggered=detection_result.final_output.cheating
    )
    

homework_agent = Agent(
    name='homewokr agent',
    instructions='You assist users in studying by explaining concepts or providing guidance, without directly solving homework or test questions.',
    input_guardrails=[homework_guardrail]
)

async def main():
    try:
        result = await Runner.run(
            homework_agent, 
            'I have a doubt in my exam, question is asking to find capital of germany, could you please help?',
            context=userprofile(id='17', name='Meet', admin=False)
            )
        print('Trip didnt triggered')
        print('response', result.final_output)
    except InputGuardrailTripwireTriggered as e:
        print('Trip triggered because of mal practicing')
        print('response', str(e))

asyncio.run(main())