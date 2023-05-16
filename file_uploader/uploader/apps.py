from django.apps import AppConfig
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os
import joblib
import json

class UploaderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'uploader'
    # Get the current working directory path

    cleaner_path = '/app/file_uploader/uploader/Static/clean.joblib'
    cleaner = joblib.load(cleaner_path)
    model_path = '/app/file_uploader/uploader/Static/t5'
    tokenizer = AutoTokenizer.from_pretrained('t5-small')
    model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
    categories = ['Book', 'Resume', 'Legal', 'Publication', 'News']
    ext_path = '/app/file_uploader/uploader/Static/code_ext.json'
    with open(ext_path,'r') as fi:
        code_ext = json.load(fi) 
    # path = '/app/file_uploader/uploader/Static/code_ext.json'
    # with open(path,'r') as f:
    #     code_ext = json.load(f)
    
