import json
from dotenv import load_dotenv
import openai
import os
load_dotenv('.env')  # This is the line that loads .env
openai_api_key = os.getenv('API_KEY')
openai.api_key = openai_api_key

class Chatbot:

  #defining gpt function
  def resumeReview(self, resume, jobDescription, score):
    self.message_history = [
        {"role": "system", "content": "You are an assistant that evaluates resumes against job descriptions. You are given a similarity score between the resume and the job description, explain why they are similar or different, and offer specific recommendations to improve the resume to better align with the job description."},
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

