from .main import ExtractStrategyWrapper
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from pathlib import Path
import base64

class AzureExtractStrategy(ExtractStrategyWrapper):
    def __init__(self,config_type:str="AZURE_DOCUMENT_AI_SERVICE") -> None:
        print('in azure init')
        super().__init__(config_type)
        self.endpoint=self.config["endpoint"]
        self.apiKey=self.config["apikey"]
        self.model_id=self.config["model_id"]
        self.client = DocumentIntelligenceClient(endpoint=self.endpoint, credential=AzureKeyCredential(self.apiKey))
        
    def load_file_as_base64(self,file_path:str):
        with open(file_path, "rb") as f:
            data = f.read()
        base64_bytes = base64.b64encode(data)
        base64_string = base64_bytes.decode('utf-8')
        return base64_string
    
    def format_response(self,data:dict)->dict:
        for key, value in data.items() :
            data[key].pop("boundingRegions", None)
            data[key].pop("confidence", None)
            data[key].pop("spans", None)
            data[key].pop("boundingRegions", None)
        
        return data

    def extract(self,file_path:str)->dict:
        try:
            #check whether the file exist
            file_path =Path('.')/rf"{file_path}"

            if not file_path.exists():
                raise FileNotFoundError(f'File {file_path} not found')
            
            print("implement rest",file_path)
            file_base64 = self.load_file_as_base64(file_path)

            poller = self.client.begin_analyze_document(
                     self.model_id, 
                    {"base64Source": file_base64},
                    locale="en-US")
            result = poller.result()

            docs=result.documents[0]
            data=self.format_response(docs["fields"])

            return data
        except Exception as e:
            print(f"Error occured in AzureExtractStrategy {e}")
        

if __name__=="__main__":
    extractor=AzureExtractStrategy("AZURE_DOCUMENT_AI_SERVICE")
    data=extractor.extract("storage/IMG-20240601-WA0025.jpg")
    print(data)
