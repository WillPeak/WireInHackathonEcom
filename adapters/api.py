import weaviate
import numpy as np
from numpy import dot
from numpy.linalg import norm
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()

WEAVIATE_URL = os.getenv('WEAVIATE_URL')
WEAVIATE_API_KEY = os.getenv('WEAVIATE_API_KEY')

# WEAVIATE_URL = 'https://intention-engine-d4t7ls1a.weaviate.network'
# WEAVIATE_API_KEY = '2lhMPjmmHp3qzJKHhZfHOOf2f6WyBdSgRW09'

def cosine_similarity(a, b):
    return dot(a, b)/(norm(a)*norm(b))

def get_products(username):

    print("Extracting products for username %s" % username)

    auth_config = weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY)  # Replace w/ your Weaviate instance API key

    # Instantiate the client with the auth config
    client = weaviate.Client(
        url=WEAVIATE_URL,  # Replace w/ your endpoint
        auth_client_secret=auth_config
    )

    product_cols = ['name','description','vector']
    query_products = (
        client.query.get("Product", product_cols)
    ).do()

    product_embeddings = np.array([x['vector'] for x in query_products['data']['Get']['Product']])

    product_df = pd.DataFrame([[x['name'], x['description']] for x in query_products['data']['Get']['Product']], columns=['name','description'])

    query_chats = (
        client.query.get("Chat", ['username','role','content','timestamp','vector'])
        .with_additional(["id vector"])
    ).do()

    chat_embeddings = [x for x in query_chats['data']['Get']['Chat'] if x['username'] == username]
    chat_embeddings = [x for x in chat_embeddings if 'vector' in x]
    # chat_embeddings = [x for x in chat_embeddings if x['role'] == 'user']
    chat_embeddings = [x['vector'] for x in chat_embeddings]
    chat_embeddings = np.array(chat_embeddings)

    if chat_embeddings.shape[0] > 0:
        print("Assigning product score from embeddings")
        avg_chat = np.mean(chat_embeddings, axis=0)

        product_distance = []
        for embedding in product_embeddings:
            product_distance.append(cosine_similarity(embedding, avg_chat))
    else:
        print("Assigning product score randomly because we didn't find any embeddings")
        product_distance = np.random.uniform(size=len(product_df))

    product_df['score'] = product_distance

    return product_df