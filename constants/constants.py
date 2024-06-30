import os
import sys
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)),
            '../')))
from services.awsDocumentServices import AwsExtractStrategy
from services.azureDocumentServices import AzureExtractStrategy
from services.geminiLLMServices import GeminiLLMServices

# adding Folder_2 to the system path
sys.path.insert(0, 'services')


class Constants():
    EXTRACTOR={
        "AZURE_DOCUMENT_AI_SERVICE":AzureExtractStrategy,
        "AWS_DOCUMENT_AI_SERVICE":AwsExtractStrategy
    }
    LLM={
        "GEMINI":GeminiLLMServices
    }
    UPLOAD_FOLDER = 'storage'


if __name__=="__main__":
    const=Constants()
    print(const.UPLOAD_FOLDER)