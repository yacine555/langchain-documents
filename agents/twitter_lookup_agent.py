from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

from langchain.agents import initialize_agent, Tool, AgentType
from tools.tools import get_profile_url


def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    template = """given the name {name_of_person} I want you to find a link to their Twitter profile page, and extract from it their username.
       In Your Final answer only the person's username"""

    tools_for_agent = [
        Tool(
            name="Crawl Google for a Twitter profile page",
            description="Useful to get the Twitter Page URL",
            func=get_profile_url,
            return_direct=False,
        )
    ]

    agent = initialize_agent(
        tools=tools_for_agent,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
    )

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    linkedin_profile_url = agent.run(prompt_template.format(name_of_person=name))

    return linkedin_profile_url
