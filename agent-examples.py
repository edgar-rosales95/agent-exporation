#basic setup for agent structure 
weather_agent = Agent(
    name="weather agent",
    instructions="you are a helpful agent who can talk to users about the warther.",
    tools=[get_weather],
)

#agent showing how to set up tools like data, action, and orchestration 
from agents import Agent, WebSeatchTool, function_tool
@function_tool
def save_restults(output):
    db.insert({"output": output,"timestamp": datetime.time()})
    return "file saved"

search_agent = Agent(
    name="Search agent",
    instructions="Help the user search the internet and save results if asked.",
    tools=[WebSeatchTool(), save_restults],   
)

# SDK agent for Runner.run()
Agents.run(agent, [UserMessage("whats the capital of the USA")])

#implementing manager pattern 
from agents import Agent, Runner 

manger_agent = Agent(
    name="manager_agent",
    instructions=(
        "you are a translation agent. you use the tools given to you to translate."
        
        "if asked for multiple translations, you call the relevant tools"
    ),
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="translate the user's message to Spanish",
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="translate the user's message to French",
        ),
        italian_agent.as_tool(
            tool_name="translate_to_italian",
            tool_description="translate the user's message to Italian",
        ),
    ],
)

async def main():
    msg = input("Translate 'hello' to Spanish, French and Italian for me!")
    
    orchestrator_output = await Runner.run(
        manger_agent,msg)
    
    for message in orchestrator_output.new_message:
        print(f" - Translationstep: {message.content}")
        
        