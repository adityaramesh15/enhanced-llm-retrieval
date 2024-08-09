from transformers import AutoTokenizer, AutoModel
import torch


def embed_text(text):
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
    model = AutoModel.from_pretrained("distilbert-base-uncased")

    inputs = tokenizer(text, return_tensors="pt", truncation = True, padding= True)

    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1).squeeze()
    

    vector = embeddings.numpy().tolist()
    return vector
