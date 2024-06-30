from typing import *
from abc import ABC, abstractmethod
from configparser import ConfigParser

class ExtractStrategyWrapper(ABC):
    def __init__(self,config_type:str) -> None:
        try:
            
            config=ConfigParser()
            config.read("./config/config.ini")
            print("printed",config[config_type])
        
            self.config=config[config_type]
        except Exception as e:
            print(f"Error in wrapper class extration {e}")
        
    @abstractmethod
    def extract(self,file_path:str)->dict:
        #implementation should be in implementation class
        pass




class LLMServices():

    def __init__(self,config_type:str) ->None:
        config=ConfigParser()
        config.read("./config/config.ini")
        self.config=config[config_type]

    @abstractmethod
    def getLLMResponse(self,extractData:List[dict]):
        pass



