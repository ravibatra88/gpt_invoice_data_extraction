from langchain.llms import OpenAI
from pypdf import PdfReader
# from langchain.llms.openai import OpenAI
import pandas as pd
import re
import replicate
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())

OpenAI_key = os.environ.get("OPEN_AI_KEY")
print(OpenAI_key)
OpenAI_key = "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"

df = pd.DataFrame()
data_dict = {'Invoice no.': '1001329', 'Description': 'Office Chair', 'Quantity': '2', 'Date': '5/4/2023', 'Unit price': '1100.00', 'Amount': '2200.00', 'Total': '2200.00', 'Email': 'Santoshvarma0988@gmail.com', 'Phone number': '9999999999', 'Address': 'Mumbai, India'}
data_dict = {'Invoice no.': 'INVO-006', 'Description': ['Monitor', 'Headphone', 'Wireless Mouse'], 'Quantity': ['1', '1', '1'], 'Date': '11/10/2023', 'Unit price': ['99', '69', '29'], 'Amount': ['$99', '$69', '$29'], 'Total': '$197', 'Email': 'example1@gmail.com', 'Phone number': '(097) 428-0005', 'Address': '20 Dowing Street, Delicious town, Bangalore, Karnataka, 562125'}
d_keys = list(data_dict.keys())
d_data = list(data_dict.values())
fr = pd.DataFrame(columns= d_keys)
fr.loc[0] = d_data
print(fr)
print(fr['Description'])
df = pd.concat([df,pd.DataFrame.from_dict(data_dict)], ignore_index=True)

llm = OpenAI(temperature=.5, openai_api_key=OpenAI_key,
             model_name='gpt-3.5-turbo')
full_response = llm('Who is the president of India')

print(full_response)

#Extract Information from PDF file
def get_pdf_text(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


# Function to extract data from text
def extracted_data(pages_data):
    template = """Extract all the following values : invoice no., Description, Quantity, date, 
        Unit price , Amount, Total, email, phone number and address from this data: {pages}

        Expected output: remove any dollar symbols {{'Invoice no.': '1001329','Description': 'Office Chair','Quantity': '2','Date': '5/4/2023','Unit price': '1100.00','Amount': '2200.00','Total': '2200.00','Email': 'Santoshvarma0988@gmail.com','Phone number': '9999999999','Address': 'Mumbai, India'}}
        """
    prompt_template = PromptTemplate(input_variables=["pages"], template=template)

    llm = OpenAI(temperature=.7, openai_api_key=OpenAI_key)
    full_response = llm(prompt_template.format(pages=pages_data))

    # The below code will be used when we want to use LLAMA 2 model,  we will use Replicate for hosting our model...

    # output = replicate.run('replicate/llama-2-70b-chat:2c1608e18606fad2812020dc541930f2d0495ce32eee50074220b87300bc16e1',
    # input={"prompt":prompt_template.format(pages=pages_data) ,
    # "temperature":0.1, "top_p":0.9, "max_length":512, "repetition_penalty":1})

    # full_response = ''
    # for item in output:
    # full_response += item

    # print(full_response)
    return full_response