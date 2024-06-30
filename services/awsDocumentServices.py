from .main import ExtractStrategyWrapper
import os
from textractor import Textractor
from textractor.data.constants import TextractFeatures
import pypdfium2 as pdfium
from typing import List,Dict

class AwsExtractStrategy(ExtractStrategyWrapper):

    def __init__(self,config_type:str="AWS_DOCUMENT_AI_SERVICE"):

        os.environ['AWS_CONFIG_FILE'] = './config/config.ini'
        self.extractor = Textractor(profile_name="default")

    def contains_pdf(self, file_string: str) -> bool:
        file_string = file_string.lower()
        return '.pdf' in file_string
    
    def convert_pdf_to_img(self,pdf_file_path:str)->List:

        specific_path_list = []
        specific_path_output = []

        if not os.path.exists("Ticket"):
            os.makedirs("Ticket")
            
        pdf = pdfium.PdfDocument(pdf_file_path)
        
        for i in range(len(pdf)):
            page = pdf[i]
            image = page.render(scale=3).to_pil()
            specific_path = f"Ticket/{i}.jpg"
            image.save(specific_path)
            specific_path_list.append(specific_path)

        for i in specific_path_list:
            specific_output = self.extract(i)
            specific_path_output.append(specific_output)
            os.remove(i)

        return specific_path_output
    
    def extract(self,path:str)->List:

        if not(self.contains_pdf(path)):
            
            document = self.extractor.analyze_document(
                file_source = path,
                features=TextractFeatures.LAYOUT
            )
            output = document.lines 
            
            return output
        
        else:

            output = self.convert_pdf_to_img(path)

            return output[0]





# aws = AwsExtractStrategy()
# extracted_data = aws.extract("C:/Users\ASUS\MyWorks\Projects\GSTExtract\storage\IMG-20240601-WA0024.jpg")

