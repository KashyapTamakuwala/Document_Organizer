from django.apps import AppConfig
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os
import joblib


class UploaderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'uploader'
    # Get the current working directory path

    cleaner_path = '/app/file_uploader/uploader/static/clean_transformer.joblib'
    cleaner = joblib.load(cleaner_path)
    model_path = '/app/file_uploader/uploader/static/t5'
    tokenizer = AutoTokenizer.from_pretrained('t5-small')
    model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
    categories = ['book', 'resume', 'legal', 'publication', 'other']
    
