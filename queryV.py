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
