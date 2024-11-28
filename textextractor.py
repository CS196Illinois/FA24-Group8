from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import pdfplumber


class Extractor:
    def clean_text(self,text):
        # Replace newlines with spaces
        text = text.replace("\n", " ")
        text = text.replace("\t", " ")
        text = re.sub(r'\s+', ' ', text)
        text = text.encode("ascii", "ignore").decode()
        return text.strip()
    
    def __init__(self, resume):
        #Needed for lengths
        self.reader = PdfReader(resume)
        with pdfplumber.open(resume) as pdf:
            first_page = pdf.pages[0]
            raw_text = first_page.extract_text()
            self.resume = self.clean_text(raw_text)
        
        
    #Update text to more than just n 
    def get_resume(self):
        return self.resume

    def pagesLen(self):
        return (len(self.reader.pages))
    
    def job_desc(self, job_desc):
        with pdfplumber.open(job_desc) as pdf:
            first_page = pdf.pages[0]
            raw_text = first_page.extract_text()
            self.job_desc = self.clean_text(raw_text)
        return self.job_desc


    def calculate_similarity(self,jobDescription):
        #TF = number of times a term appears / total number of terms
        #ID = measures how important a word is across document with less importance to little words
        self.jD = self.job_desc(jobDescription)
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([self.resume, self.jD])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return similarity[0][0]
    
    

tester = Extractor("/Users/sriramnatarajan/Documents/FA24-Group8/uploads/sample.pdf")
jobDesc = "/Users/sriramnatarajan/Documents/FA24-Group8/uploads/sampleJobDesc.pdf"

print(tester.calculate_similarity("/Users/sriramnatarajan/Documents/FA24-Group8/uploads/sample.pdf"))