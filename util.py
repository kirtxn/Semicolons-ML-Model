from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


# my_stop_words = ['web','system','science','software','systems','development','computer']

# # Combine English stop words and manual stop words
# stop_words = ENGLISH_STOP_WORDS.union(my_stop_words)



def compute_tfidf_vectors(employee_db):
    primary_skills = []
    secondary_skills = []
    other_skills = []
    for emp in employee_db:
        primary_skills.append(' '.join(emp['skills']['primarySkills']))
        secondary_skills.append(' '.join(emp['skills']['secondarySkills']))
        other_skills.append(' '.join(emp['skills']['otherSkills']))
    
    vectorizer = TfidfVectorizer(stop_words="english", lowercase=True, analyzer='word', token_pattern=r'\b\w+\b', ngram_range=(1, 1))
    primary_tfidf_matrix = vectorizer.fit_transform(primary_skills)
    primary_tfidf_matrix = primary_tfidf_matrix.multiply(3)  # multiply by 3 to give primary skills a weight of 3

    secondary_tfidf_matrix = vectorizer.transform(secondary_skills)
    secondary_tfidf_matrix = secondary_tfidf_matrix.multiply(2)  # multiply by 2 to give secondary skills a weight of 2

    other_tfidf_matrix = vectorizer.transform(other_skills)  # weight of other skills is already 1

    tfidf_matrix = primary_tfidf_matrix + secondary_tfidf_matrix + other_tfidf_matrix
    return vectorizer, tfidf_matrix


def match_job_description(job_description, employee_db, vectorizer, tfidf_matrix):
    job_description_tfidf = vectorizer.transform([job_description])
    # feature_names = vectorizer.get_feature_names()
    # for col in job_description_tfidf.nonzero()[1]:
    #     print(f"Word: {feature_names[col]}, TF-IDF Score: {job_description_tfidf[0, col]}")

    for i, emp in enumerate(employee_db):
        emp_tfidf = tfidf_matrix[i]
        match_score = cosine_similarity(job_description_tfidf, emp_tfidf)[0][0]
        emp['MatchScore'] = match_score
    return employee_db
