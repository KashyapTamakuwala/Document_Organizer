import PyPDF2
import scipy
import numpy as np
import docx
from .apps import UploaderConfig
import requests

tokenized_categories  = [UploaderConfig.tokenizer.encode(cat)[0] for cat in UploaderConfig.categories]



def read_data(path):
    extension = path.split(".")[-1]
    # print(extension)

    if extension in UploaderConfig.code_ext:
        return "Code"
    
    if extension == "pdf":
        with open(path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)
            text = ""
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text = text+" " + page.extract_text()
            cleaned_text = UploaderConfig.cleaner.transform([text])
        return cleaned_text[0]
    
    elif extension == 'txt':
        with open(path, 'r') as f:
            text = f.read()
        cleaned_text = UploaderConfig.cleaner.transform([text])
        return cleaned_text[0]
    
    elif extension == "doc" or extension == "docx" :
        doc = docx.Document(path)
        text = ""
        for para in doc.paragraphs:
            text = text + " "+ para.text
        cleaned_text = UploaderConfig.cleaner.transform([text])
        return cleaned_text[0]
    elif extension in ['png','jpg','jpeg']:
        payload = {
                'apikey': 'K86860089688957',
                'language': 'eng',  # The language of the text in the image
                'isOverlayRequired': False  # Whether to include the image in the response or not
            }

        # Open the image file in read mode
        with open(path, 'rb') as f:
            # Make a POST request to the OCR.space API
            response = requests.post("https://api.ocr.space/parse/image", files={'filename': f}, data=payload)

        ocr_result = response.json()

        text = ocr_result['ParsedResults'][0]['ParsedText']
        cleaned_text = UploaderConfig.cleaner.transform([text])
        return cleaned_text[0]
    else:
        return "None"
    

def token(text):
    
    prefix = f"Classify the following document into a one of the following topically semantic categories. Possible categories: {', '.join(UploaderConfig.categories)}. Document: "
    inputs = prefix + text
    tokens = UploaderConfig.tokenizer(inputs,max_length=512, truncation=True,return_tensors="pt")
    return tokens


def getCategory(path):
    path = "/app/file_uploader/"+path
    text = read_data(path)
    # print("text",text)
    if text=='Code':
        return 'Code'
    elif text =='None':
        return 'None'
    else:
        tokens  = token(text)
        outputs = UploaderConfig.model.generate(**tokens, return_dict_in_generate=True, output_scores=True, max_new_tokens=1, temperature=0)
        scores = [outputs.scores[0][:,t].numpy()[0] for t in tokenized_categories]
        scores = scipy.special.softmax(scores)
        cat = UploaderConfig.categories[np.argmax(scores)]
        if cat == 'Publication':
            return 'Books'
        else:
            return cat




