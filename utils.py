from langchain.llms import OpenAI
from pypdf import PdfReader
# from langchain.llms.openai import OpenAI
import pandas as pd
import re
import replicate
from langchain.prompts import PromptTemplate
import os
# from dotenv import load_dotenv,find_dotenv
from langchain.chat_models import ChatOpenAI
# load_dotenv(find_dotenv())



#Extract Information from PDF file
def get_pdf_text(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text



#Function to extract data from text
def extracted_data(pages_data,OpenAI_key):

    # template = """Extract all the following values : invoice no., Description, Quantity, date,
    #     Unit price , Amount, Total, email, phone number and address from this data: {pages}
    #
    #     Expected output: make sure output is in json format with curly braces {{'Invoice no.': '1001329','Description': 'Office Chair,Table','Quantity': '2,1','Date': '5/4/2023','Unit price': '1100.00, 400.00','Amount': '2200.00, 400.00','Total': '2600.00','Email': 'ravibatra@gmail.com','Phone number': '9999999999','Address': 'Bengalore, India'}}
    #     """

    template = """Extract all the following values : invoice no., Description, Quantity, date, 
        Unit price , Amount, Total, email, phone number and address from this data: {pages}

        Expected output: make sure output is in json format with curly braces {{'Invoice no.': '1001329','Description': 'Office Chair,Table','QTY/HR Rate': '2,1','Date': '5/4/2023','Unit cost': '1100.00, 400.00','Amount': '2200.00, 400.00','Total': '2600.00','Email': 'ravibatra@gmail.com','Phone number': '9999999999','Address': 'Bengalore, India'}}
        """
    prompt_template = PromptTemplate(input_variables=["pages"], template=template)

    llm = OpenAI(temperature=.1, openai_api_key=OpenAI_key)
    full_response=llm(prompt_template.format(pages=pages_data))
    

    #The below code will be used when we want to use LLAMA 2 model,  we will use Replicate for hosting our model...
    
    #output = replicate.run('replicate/llama-2-70b-chat:2c1608e18606fad2812020dc541930f2d0495ce32eee50074220b87300bc16e1', 
                           #input={"prompt":prompt_template.format(pages=pages_data) ,
                                  #"temperature":0.1, "top_p":0.9, "max_length":512, "repetition_penalty":1})
    
    #full_response = ''
    #for item in output:
        #full_response += item
    

    #print(full_response)
    return full_response


# iterate over files in
# that user uploaded PDF files, one by one
def create_docs(user_pdf_list,OpenAI_key):
    
    df = pd.DataFrame({'Invoice no.': pd.Series(dtype='str'),
                   'Description': pd.Series(dtype='str'),
                   'QTY/HR Rate': pd.Series(dtype='str'),
                   'Date': pd.Series(dtype='str'),
	                'Unit cost': pd.Series(dtype='str'),
                   'Amount': pd.Series(dtype='int'),
                   'Total': pd.Series(dtype='str'),
                   'Email': pd.Series(dtype='str'),
	                'Phone number': pd.Series(dtype='str'),
                   'Address': pd.Series(dtype='str')
                    })

    for filename in user_pdf_list:
        
        print(filename)
        raw_data=get_pdf_text(filename)
        #print(raw_data)
        #print("extracted raw data")

        llm_extracted_data=extracted_data(raw_data,OpenAI_key)
        print("llm extracted data", llm_extracted_data)
        #Adding items to our list - Adding data & its metadata

        pattern = r'{(.+)}'
        match = re.search(pattern, llm_extracted_data, re.DOTALL)

        if match:
            extracted_text = match.group(1)
            # Converting the extracted text to a dictionary
            data_dict = eval('{' + extracted_text + '}')
            print(data_dict)
        else:
            print("No match found.")
        d_keys = list(data_dict.keys())
        d_data = list(data_dict.values())
        this_df = pd.DataFrame(columns= d_keys)
        this_df.loc[0] = d_data
        df=pd.concat([df,this_df], ignore_index=True)
        print("********************DONE***************")
        #df=df.append(save_to_dataframe(llm_extracted_data), ignore_index=True)

    df.head()
    return df