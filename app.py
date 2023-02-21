from flask import Flask, request, jsonify
from util import compute_tfidf_vectors, match_job_description
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['employee_db']
collection = db['Employee']

# Fetch employees from db
employee_db = []
for emp in collection.find({}, {'_id':0}):
    employee_db.append(emp)

vectorizer, tfidf_matrix = compute_tfidf_vectors(employee_db)


@app.route('/api/rank-employees', methods=['POST'])
def rank_employees():
    data = request.get_json()
    job_description = data.get('jobDescription')
    updated_employee_db = match_job_description(job_description, employee_db, vectorizer, tfidf_matrix)
    updated_employee_db.sort(key=lambda emp: emp['MatchScore'], reverse=True)
    return jsonify(updated_employee_db[:50])


if __name__ == '__main__':
    app.run(debug=True)
