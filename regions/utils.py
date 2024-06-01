import requests
from gradio_client import Client



def query_predict_nlp(input_message):
    client = Client("https://qwen-qwen1-5-72b-chat.hf.space/--replicas/061qr/")
    result = client.predict(
        input_message,
        [["None", "None"]],
        "None",
        api_name="/model_chat"
    )

    return result[1][1][1]
