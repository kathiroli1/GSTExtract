from typing import *
from abc import ABC, abstractmethod
from configparser import ConfigParser

class ExtractStrategyWrapper(ABC):
    def __init__(self,config_type:str) -> None:
        config=ConfigParser()
        config.read("../config/config.ini")
        self.config=config[config_type]
        
    @abstractmethod
    def extract(self,file_path:str)->dict:
        #implementation should be in implementation class
        pass

    def convert_pdf_to_img(self,pdf_file_path:str)->None:
        pass


class LLM():

    def __init__(self,model:str,temp:float=0.3) ->None:
        self.prompt="SAMPLE_PROMPT"
        self.model=model
        self.temp=temp

    def getLLMResponse(self,extractData:List[dict]):
        pass



