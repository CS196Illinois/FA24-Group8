from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import pdfplumber
from bot import Chatbot

class Extractor:
    def clean_text(self,text):
        # Replace newlines with spaces
        text = text.replace("\n", " ")
        text = text.replace("\t", " ")
        text = re.sub(r'\s+', ' ', text)
        text = text.encode("ascii", "ignore").decode()
        return text.strip()
    
    def __init__(self, resume, job_desc):
        #Needed for lengths
        self.reader = PdfReader(resume)
        with pdfplumber.open(resume) as pdf:
            first_page = pdf.pages[0]
            raw_text = first_page.extract_text()
            self.resume = self.clean_text(raw_text)

        with pdfplumber.open(job_desc) as pdf:
            first_page = pdf.pages[0]
            raw_text = first_page.extract_text()
            self.job_desc = self.clean_text(raw_text)
        
    def pagesLen(self):
        return (len(self.reader.pages))

    def calculate_similarity(self):
        #TF = number of times a term appears / total number of terms
        #ID = measures how important a word is across document with less importance to little words
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([self.resume, self.job_desc])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return similarity[0][0]
    
    

sampleResume = "/Users/sriramnatarajan/Documents/FA24-Group8/uploads/sampleResume.pdf"
jobDesc = "/Users/sriramnatarajan/Documents/FA24-Group8/uploads/sampleJobDesc.pdf"
nlpBot = Chatbot()


tester = Extractor(sampleResume, jobDesc)
print(nlpBot.resumeReview(sampleResume, jobDesc,tester.calculate_similarity()))
# print(nlpBot.resumeReview(tester.resume, tester.job_desc, tester.calculate_similarity()))




# print(bot(tester.get_resume(), tester.job_desc(jobDesc), tester.calculate_similarity(jobDesc)))
