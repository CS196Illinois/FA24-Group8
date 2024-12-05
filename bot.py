import json
from dotenv import load_dotenv
import openai
import os
load_dotenv('.env')  # This is the line that loads .env
openai_api_key = os.getenv('API_KEY')
openai.api_key = openai_api_key
import requests

class Chatbot:

  #defining gpt function
    def resumeReview(self, resume, jobDescription, score):
        self.message_history = [
            {"role": "system", "content": "You are an assistant that evaluates resumes against job descriptions. You will provide an in-depth analysis of the alignment between the resume and the job description. Use the provided similarity score to explain specific overlaps or gaps in key areas, such as required skills, responsibilities, and qualifications. Offer detailed recommendations on how the resume can be improved to better match the job description, focusing on niche requirements and providing actionable advice tailored to the position. If possible, suggest ways to phrase or structure the resume for maximum impact." },
            {"role": "user", "content": ("The resume is: " + resume + ". The job description is: " + jobDescription + " and the similarity score is " + str(score))}
            ]

        try:  
            response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages= self.message_history
            )
            reply_content = response.choices[0].message.content
            return reply_content

        except Exception as e:
            return "failed"


    #Function for getting the professor's most recent paper (Used in chatbot)
    def profPaper(self, name):
        base_url = "https://api.openalex.org/authors"
        response = requests.get(base_url,params={"search": name})
        if response.status_code == 200:
            #Data is the id 
            self.data = response.json()["results"][0]["works_api_url"]
        elif response.status_code == 404:
            return
        
        works_response = requests.get(self.data, params={"sort": "publication_year:desc"})

        return (works_response.json()["results"][0]["title"])
    

    def emailGenerator(self, type, studentName, collegeName, studentMajor, profName ):

        #Creating Message History For Initial Email
        if (type == "initial"):
            try:
                profResearch = self.profPaper(profName)
            
            except Exception as e:
                profResearch = "Unknown"

            with open('/Users/sriramnatarajan/Documents/FA24-Group8/EmailTemplates/initialemail.txt', 'r') as file:
                text = file.read()
                params = [profName, studentName, studentMajor, collegeName, profResearch, studentName, ""]

            response = ""
            message1 = text.split("[")
            for i in range(len(message1)):
                response += message1[i] + params[i]


            

            self.message_history = [
                {"role": "system","content": "You are an assistant that is given a cold email template. With that template, you must adhere to it and fill in the blanks for every single paranthases where it asks you to fill in the blanks"},
                {"role": "user", "content": response},
                { "role": "assistant", "content": "Understood. I will use this template as the foundation for generating emails." }
            ]

            try:  
                response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages = self.message_history
                
                )
                reply_content = response.choices[0].message.content
            
                return reply_content

            except Exception as e:
                return "failed"
            
        elif (type == "followup"):
            try:
                profResearch = self.profPaper(profName)
            
            except Exception as e:
                profResearch = "Unknown"

            with open('/Users/sriramnatarajan/Documents/FA24-Group8/EmailTemplates/followup.txt', 'r') as file:
                text = file.read()
                params = [profName, profResearch, studentName, ""]

            response = ""
            message1 = text.split("[")
            for i in range(len(message1)):
                response += message1[i] + params[i]


            

            self.message_history = [
                {"role": "system","content": "You are an assistant that is given a followup email template. With that template, you must adhere to it and fill in the blanks for every single paranthases where it asks you to fill in the blanks"},
                {"role": "user", "content": response},
                { "role": "assistant", "content": "Understood. I will use this template as the foundation for generating emails." }
            ]

            try:  
                response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages = self.message_history
                
                )
                reply_content = response.choices[0].message.content
            
                return reply_content

            except Exception as e:
                return "failed"
        else:
            return "failed"



# tester = Chatbot()
# print(tester.emailGenerator("followup", "Sriram Natarajan", "UIUC", "CS + Ling", "Tarek Abdelzaher"))




