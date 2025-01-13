from dotenv import load_dotenv
import os

load_dotenv()

from typing import Tuple

from langchain.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage
from langchain.chains import LLMChain
from langchain_community.callbacks.manager import get_openai_callback

from tools.linkedin import scrape_linkedin_profile
from tools.linkedin import scrape_linkedin_profile_gistgithub
from tools.twitter import scrape_user_tweets
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from output_parser import person_intel_parser, PersonIntel


information = """
Elon Reeve Musk (/ˈiːlɒn/ EE-lon; born June 28, 1971) is a businessman and investor. He is the wealthiest person in the world, with an estimated net worth of US$222 billion as of December 2023, according to the Bloomberg Billionaires Index, and $244 billion according to Forbes, primarily from his ownership stakes in Tesla and SpaceX.[5][6] He is the founder, chairman, CEO, and chief technology officer of SpaceX; angel investor, CEO, product architect and former chairman of Tesla, Inc.; owner, chairman and CTO of X Corp.; founder of the Boring Company and xAI; co-founder of Neuralink and OpenAI; and president of the Musk Foundation.
A member of the wealthy South African Musk family, Elon was born in Pretoria and briefly attended the University of Pretoria before immigrating to Canada at age 18, acquiring citizenship through his Canadian-born mother. Two years later, he matriculated at Queen's University at Kingston in Canada. Musk later transferred to the University of Pennsylvania, and received bachelor's degrees in economics and physics. He moved to California in 1995 to attend Stanford University. However, Musk dropped out after two days and, with his brother Kimbal, co-founded online city guide software company Zip2. The startup was acquired by Compaq for $307 million in 1999, and, that same year Musk co-founded X.com, a direct bank. X.com merged with Confinity in 2000 to form PayPal.
In October 2002, eBay acquired PayPal for $1.5 billion, and that same year, with $100 million of the money he made, Musk founded SpaceX, a spaceflight services company. In 2004, he became an early investor in electric vehicle manufacturer Tesla Motors, Inc. (now Tesla, Inc.). He became its chairman and product architect, assuming the position of CEO in 2008. In 2006, Musk helped create SolarCity, a solar-energy company that was acquired by Tesla in 2016 and became Tesla Energy. In 2013, he proposed a hyperloop high-speed vactrain transportation system. In 2015, he co-founded OpenAI, a nonprofit artificial intelligence research company. The following year, Musk co-founded Neuralink—a neurotechnology company developing brain–computer interfaces—and the Boring Company, a tunnel construction company. In 2022, he acquired Twitter for $44 billion. He subsequently merged the company into newly created X Corp. and rebranded the service as X the following year. In March 2023, he founded xAI, an artificial intelligence company.[7]
Musk has expressed views that have made him a polarizing figure.[8][9][10] He has been criticized for making unscientific and misleading statements, including COVID-19 misinformation, transphobia[11][12][13] and antisemitic conspiracy theories.[8][14][15][16] His ownership of Twitter has been similarly controversial, including laying off a large number of employees, an increase in hate speech on the website,[17][18] and changes to Twitter Blue verification.[19][20] In 2018, the U.S. Securities and Exchange Commission (SEC) sued him for falsely tweeting that he had secured funding for a private takeover of Tesla. To settle the case, Musk stepped down as the chairman of Tesla and paid a $20 million fine. 

"""


def icebreaker(name: str) -> Tuple[PersonIntel, str]:
    linkedin_profile_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)

    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweets(username=twitter_username, num_tweets=5)

    prompt_template = """
         given the Linkedin information {linkedin_information} and twitter {twitter_information} about a person from I want you to create:
         1. a short summary
         2. two interesting facts about them
         3. A topic that may interest them
         4. 2 creative Ice breakers to open a conversation with them 
         \n{format_instruction}
     """

    summary_prompt_template = PromptTemplate(
        input_variables=["linkedin_information", "twitter_information"],
        template=prompt_template,
        partial_variables={
            "format_instruction": person_intel_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = summary_prompt_template | llm 

    # linkedin_data = scrape_linkedin_profile(linkedin_profile_url="gist.github")

    # linkedin_data = scrape_linkedin_profile_gistgithub(
    #     "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/fad4d7a87e3e934ad52ba2a968bad9eb45128665/eden-marco.json"
    # )

    result = chain.invoke(input={
        "linkedin_information":linkedin_data,
        "twitter_information":tweets
        })

    return person_intel_parser.parse(result), linkedin_data.get("profile_pic_url")


def prompt_cost(question: str):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    template = """Question: {question}

    Answer: Let's think step by step."""

    prompt = PromptTemplate(template=template, input_variables=["question"])
    chain = prompt | llm 

    with get_openai_callback() as cb:
        res = chain.invoke({"question": question})
        print(res)
        print(cb)


if __name__ == "__main__":

    print("Hello LangChain")
    print(os.getenv("LANGCHAIN_PROJECT"))

    

    # Estimate API call cost
    prompt_cost("How to create a red sauce pasta")

    # Scape Linked in profile
    print(scrape_linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/yacinebouakkaz/",  mock=True))

    
    result = icebreaker(name="Yacine Bouakkaz Technology")
    print(result)

    pass
