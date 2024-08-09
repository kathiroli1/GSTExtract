
from  .main import LLMServices
from typing import List,Dict
import google.generativeai as genai
import os,re,json,time

class GeminiLLMServices(LLMServices):
    def __init__(self, config_type:str="GEMINI"):
        super().__init__(config_type)

        self.api_key = self.config['api_key']
        genai.configure(api_key=self.config['api_key'])

        self.model = self.config['model']
        self.temperature = self.config['temperature']
        self.top_p = self.config['top_p']
        self.top_k = self.config['top_k']
        self.max_output_tokens = self.config['max_output_tokens']
        self.response_mime_type = self.config['response_mime_type']

        self.generation_config = {
                                "temperature": float(self.temperature),
                                "top_p": int(self.top_p),
                                "top_k": int(self.top_k),
                                "max_output_tokens": int(self.max_output_tokens),
                                "response_mime_type": str(self.response_mime_type),
                                }
        
    def constructDictResponse(self,response:str):
        try:
            try:
                response = response.strip("```JSON\n```")
            except Exception as e:
                pass

            pattern = r"""
            '([^']*)'\s*:\s*(None|"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'|\d+(?:\.\d*)?)
            | "([^"]*)"\s*:\s*(None|"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'|\d+(?:\.\d*)?)
            """

            matches = re.findall(pattern, response, re.VERBOSE)

            result = {}
            for match in matches:
                key = match[0] or match[2]
                value = match[1] or match[3]
                
                if value == 'None':
                    result[key] = None
                elif value.startswith('"') and value.endswith('"'):
                    result[key] = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    result[key] = value[1:-1]
                elif value.isdigit():
                    result[key] = int(value)
                else:
                    try:
                        result[key] = float(value)
                    except ValueError:
                        result[key] = value
            return result
        
        except Exception as e:
            print("Error parsing the response, Returning the raw text response back")
            return response
        
    def getLLMResponse(self,data:List[str])->str:
        data = f"""{data}"""
        self.prompt=f"""The below is text extracted from the bill/invoice form image using AWS/AZURE. 
                        Understand the data and extract the field which I have mentioned below
                        Data: {data}

                        Output Fields:
                            Invoice no
                            GSTIN
                            Name
                            M/s
                            Party's GSTIN
                            E-way Bill No
                            State
                            State code
                            Date
                            Description
                            HSN
                            Unit
                            Rate
                            CGST
                            SGST
                            Igst
                            Total
                            Grand total

                        NOTE: THE OUTPUT SHOULD BE IN JSON FORMAT. 
                        ONLY INCLUDE THE FILEDS WHICH I HAVE MENTIONED IN THE OUTPUT FIELD. 
                        DO NOT RETURN ANY EXTRA TEXT. KEEP IT STRAIGHT TO THE REQUEST."""

        model = genai.GenerativeModel(
                                        model_name = self.model,
                                        generation_config = self.generation_config,
                                    )
        
        chat_session = model.start_chat(
                                            history=[]
                                       )
        response = chat_session.send_message(str(self.prompt))

        def is_response_received(response):
            status = True if response.text else False
            return status

        while not is_response_received(response):
            print("Waiting for response...")
            time.sleep(1)

        try:
            response = self.constructDictResponse(response.text)
            return response
        except:
            return "Can't able to extract text from the generated response"
            
        
        
if __name__=="__main__":
    print("")