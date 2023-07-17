<img src="https://huggingface.co/datasets/huggingface/brand-assets/resolve/main/hf-logo-with-title.png" alt="Hugging Face Logo" width="300">


**Atlas Triggers And Huggingface Sentence Transformers**

The sample python code provided uses the all-MiniLM-L6-v2 sentence transformer model, from Hugging Face. It maps the sentences (docs to insert in collection as well as for query string) to a 384 dimensional dense vector space, and creates corresponding vector embeddings (list of numbers). This tutorial requires basic knowledge of Python, and assumes that you have an existing Atlas Cluster. Simple Vector demo below

Steps:

1. Install pymongo:

```
pip install pymongo
```
Install sentence-transformers:

```
pip install -U sentence-transformers
```
Run the following code to create the test collection with corresponding vector embeddings:

```
import pymongo
client = pymongo.MongoClient("SRV URL TO YOUR ATLAS CLUSTER")
db = client.vector_tests

from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

docs = [
    "The students studied for their exams.",
    "Studying hard, the students prepared for their exams.",
    "The chef cooked a delicious meal.",
    "The chef cooked the chicken with the vegetables.",
    "Known for its power and aggression, Mike Tyson's boxing style was feared by many."
]

print(docs)

result_doc = {}
for doc in docs:
    doc_vector = model.encode(doc).tolist()
    result_doc['sentence'] = doc
    result_doc['vectorEmbedding'] = doc_vector
    result = db.vectors_demo_1.insert_one(result_doc.copy())
    print(result)
Create the following Atlas Search index on the vectors_demo_1 collection:

json
Copy code
{
  "mappings": {
    "dynamic": true,
    "fields": {
      "vectorEmbedding": {
        "type": "knnVector",
        "dimensions": 384,
        "similarity": "euclidean"
      }
    }
  }
}
```
Now you can run the following code to perform semantic search for various sentences (uncomment the query you want to run) - note that my index is named "default" and that's why the query does not specify the index name; if your index is not named default then please include your index's name in the query:

```
import pymongo
client = pymongo.MongoClient("SRV URL TO YOUR ATLAS CLUSTER")
db = client.vector_tests

from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# sample searches

#query = "The cook prepared a meal of poultry and veggies."
#query = "The pupils worked hard for their test."
#query = "Studying hard, the students prepped for their exams."
#query = "A delicious meal was cooked by the chef."
#query = "Tyson's boxing style was feared for its power and aggression."

vector_query = model.encode(query).tolist()
pipeline = [
    {
        "$search": {
            "knnBeta": {
                "vector": vector_query,
                "path": "vectorEmbedding",
                "k": 3
            }
        }
    },
    {
        "$limit": 1
    },
    {
        "$project": {
            "vectorEmbedding": 0,
            "_id": 0,
            'score': {
                '$meta': 'searchScore'
            }
        }
    }
]

results = db.vectors_demo_1.aggregate(pipeline)
for result in results:
    print("\n")
    print("*************Vector Search Result*****************")
    print(result['sentence'])
    print("**************************************************")
```
[Hugginface Documentation](https://huggingface.co/docs)
[Atlas Triggers Documentation](https://www.mongodb.com/docs/atlas/app-services/triggers/)
