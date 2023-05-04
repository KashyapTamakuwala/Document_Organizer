import joblib
from transformers import AutoTokenizer


model_name = "t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
clean_transformer = joblib.load('clean_transformer.joblib')


