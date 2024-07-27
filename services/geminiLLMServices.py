
from  .main import LLMServices
from typing import List,Dict
import google.generativeai as genai
import os,re,json

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

            pattern = r'"([^"]+)"\s*:\s*"([^"]*)"|(\w+)\s*:\s*(null)'
            matches = re.findall(pattern, response)
            result = {}
            for match in matches:
                if match[0] and match[1]:
                    result[match[0]] = match[1]
                elif match[2]:
                    result[match[2]] = None
 
            return result
        
        except Exception as e:
            print("Error parsing the response, Returning the raw text response back")
            return response
        
    def getLLMResponse(self,data:List[str])->str:
        print('in ge llm resp',data)
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
        print(response)
        response = self.constructDictResponse(response.text)

        return response
    
if __name__=="__main__":

    llmService=GeminiLLMServices("GEMINI")
    data={
    "CustomerAddress":{
       "type":"address",
       "content":"PATTANUR\nTAMILNADU",
       "valueAddress":{
          "streetAddress":"",
          "house":"PATTANUR\nTAMILNADU"
       }
    },
    "CustomerAddressRecipient":{
       "type":"string",
       "valueString":"TINDIVANAM BY-PASS",
       "content":"TINDIVANAM BY-PASS"
    },
    "CustomerName":{
       "type":"string",
       "valueString":"DEVANATHAN",
       "content":"DEVANATHAN"
    },
    "InvoiceDate":{
       "type":"date",
       "valueDate":"2022-11-20",
       "content":"20/11/2022."
    },
    "InvoiceId":{
       "type":"string",
       "valueString":"N8:8.2.3",
       "content":"N8:8.2.3"
    },
    "InvoiceTotal":{
       "type":"currency",
       "valueCurrency":{
          "amount":49560.0,
          "currencyCode":"INR"
       },
       "content":"49560"
    },
    "Items":{
       "type":"array",
       "valueArray":[
          {
             "type":"object",
             "valueObject":{
                "Amount":{
                   "type":"currency",
                   "valueCurrency":{
                      "amount":42000.0,
                      "currencyCode":"INR"
                   },
                   "content":"42000",
                   "boundingRegions":[
                      {
                         "pageNumber":1,
                         "polygon":[
                            2351,
                            1348,
                            2535,
                            1348,
                            2536,
                            1417,
                            2351,
                            1418
                         ]
                      }
                   ],
                   "confidence":0.952,
                   "spans":[
                      {
                         "offset":658,
                         "length":5
                      }
                   ]
                },
                "Description":{
                   "type":"string",
                   "valueString":"1×1\"-CERATI FLOOR TILES.",
                   "content":"1×1\"-CERATI FLOOR TILES.",
                   "boundingRegions":[
                      {
                         "pageNumber":1,
                         "polygon":[
                            440,
                            1301,
                            1298,
                            1301,
                            1298,
                            1409,
                            440,
                            1409
                         ]
                      }
                   ],
                   "confidence":0.958,
                   "spans":[
                      {
                         "offset":612,
                         "length":24
                      }
                   ]
                },
                "ProductCode":{
                   "type":"string",
                   "valueString":"69072200",
                   "content":"69072200",
                   "boundingRegions":[
                      {
                         "pageNumber":1,
                         "polygon":[
                            1386,
                            1315,
                            1646,
                            1311,
                            1648,
                            1393,
                            1386,
                            1396
                         ]
                      }
                   ],
                   "confidence":0.95,
                   "spans":[
                      {
                         "offset":637,
                         "length":8
                      }
                   ]
                },
                "Quantity":{
                   "type":"number",
                   "valueNumber":350,
                   "content":"350",
                   "boundingRegions":[
                      {
                         "pageNumber":1,
                         "polygon":[
                            1765,
                            1347,
                            1893,
                            1342,
                            1897,
                            1410,
                            1769,
                            1417
                         ]
                      }
                   ],
                   "confidence":0.952,
                   "spans":[
                      {
                         "offset":646,
                         "length":3
                      }
                   ]
                },
                "Unit":{
                   "type":"string",
                   "valueString":"BOX",
                   "content":"BOX",
                   "boundingRegions":[
                      {
                         "pageNumber":1,
                         "polygon":[
                            1767,
                            1448,
                            1885,
                            1429,
                            1895,
                            1489,
                            1777,
                            1508
                         ]
                      }
                   ],
                   "confidence":0.958,
                   "spans":[
                      {
                         "offset":664,
                         "length":3
                      }
                   ]
                },
                "UnitPrice":{
                   "type":"currency",
                   "valueCurrency":{
                      "amount":5.0,
                      "currencyCode":"INR"
                   },
                   "content":"120/5.0",
                   "boundingRegions":[
                      {
                         "pageNumber":1,
                         "polygon":[
                            2025,
                            1338,
                            2263,
                            1367,
                            2261,
                            1461,
                            2027,
                            1418
                         ]
                      }
                   ],
                   "confidence":0.968,
                   "spans":[
                      {
                         "offset":650,
                         "length":7
                      }
                   ]
                }
             },
             "content":"1.\n1×1\"-CERATI FLOOR TILES.\n69072200\n350\n120/5.0\n42000\nBOX\n·",
             "boundingRegions":[
                {
                   "pageNumber":1,
                   "polygon":[
                      288,
                      1303,
                      2536,
                      1297,
                      2537,
                      1829,
                      289,
                      1835
                   ]
                }
             ],
             "confidence":0.881,
             "spans":[
                {
                   "offset":609,
                   "length":60
                }
             ]
          }
       ]
    },
    "SubTotal":{
       "type":"currency",
       "valueCurrency":{
          "amount":42000.0,
          "currencyCode":"INR"
       },
       "content":"42000"
    },
    "TotalTax":{
       "type":"currency",
       "valueCurrency":{
          "amount":7560.0,
          "currencyCode":"INR"
       },
       "content":"7560"
    },
    "VendorAddress":{
       "type":"address",
       "content":"w A Yassoda Bhavan, 100 Feet Road, Kodiswamy Nagar, Opp. to Hotel Janaki Raman Inn, PUDUCHERRY - 605 004",
       "valueAddress":{
          "houseNumber":"605 004",
          "road":"100 Feet Road, Kodiswamy Nagar, Opp. to Hotel Janaki Raman Inn, PUDUCHERRY",
          "streetAddress":"605 004 100 Feet Road, Kodiswamy Nagar, Opp. to Hotel Janaki Raman Inn, PUDUCHERRY",
          "house":"w A Yassoda Bhavan"
       }
    },
    "VendorAddressRecipient":{
       "type":"string",
       "valueString":"SWASTIK TILES AGENCY",
       "content":"SWASTIK TILES AGENCY"
    },
    "VendorName":{
       "type":"string",
       "valueString":"SWASTIK TILES AGENCY",
       "content":"SWASTIK TILES AGENCY"
    },
    "VendorTaxId":{
       "type":"string",
       "valueString":"34AOYPR5223A1ZV",
       "content":"34AOYPR5223A1ZV"
    }
 }
    resp=llmService.getLLMResponse(data)
    print(resp)