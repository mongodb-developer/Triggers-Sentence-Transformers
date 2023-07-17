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
