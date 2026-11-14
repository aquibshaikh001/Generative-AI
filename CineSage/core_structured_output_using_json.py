from dotenv import load_dotenv

load_dotenv() 

from langchain_groq import ChatGroq 
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel 
from typing import List,Optional 
from langchain_core.output_parsers import PydanticOutputParser


model = ChatGroq(model = "openai/gpt-oss-20b")

# steps to convert it into machine friendly 
# 1st create the schema
# create a parser 

#This is a schema that is made using Pydantic
class Movie(BaseModel):
    title : str 
    release_year : Optional[int]
    genre : List[str]
    director: Optional[str]
    cast : List[str]
    music_credits: Optional[str]
    ratings : Optional[float] 
    summary : str

# We are actually making it machine friendly    
#parser converts your Movie Pydantic class into a massive text instruction (a JSON Schema) telling the LLM: *"You MUST reply in JSON with keys title, release_year etc.
parser = PydanticOutputParser(pydantic_object=Movie)
    


prompt = ChatPromptTemplate.from_messages([
    ('system', """
    Extract Movie information from the paragraph
    {format_instructions}
"""),
    ('human',"{paragraph}")
])

para = input("Give your paragraph here :")


# Right now, you only called parser.get_format_instructions().

# That method converts your Movie Pydantic class into a text instruction (JSON Schema) and injects it into {format_instructions} so the LLM knows how to format its reply.


final_prompt = prompt.invoke(
    {"paragraph":para,
    "format_instructions": parser.get_format_instructions()
    }
)


response = model.invoke(final_prompt)
movie_data = parser.parse(response.content)

print(movie_data)

