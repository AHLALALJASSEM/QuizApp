
# import from django 
from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status 

# import from my apps
from .models import Results
from Quizes.models import Quizes
from .models import Results
from Question.models import Question,Choices
from users.permission import Is_Student,Is_Teacher
from drf_yasg.utils import swagger_auto_schema


# @swagger_auto_schema(
#     operation_summary= "Add Result After Students Finish The Quiz",
#     operation_description="Add Result After Students Finish The Quiz",
#        )
@api_view(['POST'])
@permission_classes([Is_Student])
# id for Quiz
def AddResult(request,id):
    """
    This Function To Add Results To Results Table For Students After Students Finish The Quiz.
    **Request Body:**
    - Questions : array (required) - This Array contain elemants{"IdQuestion":int,"IdChoice":int}
    - IdQuestion : int (required) -id Question When Student Answer it
    - IdChoice : int (required) -id Choice When Student choice it.
    **Example Request:**
    {
       "Questions":[
         {
      "IdQuestion":30,
      "IdChoice":119
         },
         {
      "IdQuestion":31,
      "IdChoice":123
         }
         ]
    }.
    **Responses:**
    - 201 - Add Result Successfully.
    **Parameters:**
    - id : integer (required) - ID of Quiz which student answer it .
    **Security:**
    - Requires authentacation
    - This Function uses from Account for Students only After End Quiz.
    
    """

    correct_questions=[]
    correct_questions_c=[]
    worng_questions=[]
    worng_questions_c=[]
    result=0
    
    try:
        quiz = Quizes.objects.get(id=id)
    except Quizes.DoesNotExist:
        return Response("The Quiz id is {} Is Does Not Exist !!".format(id))
    for question in request.data['Questions']:
        try:
           question_obj = Question.objects.get(id=question['IdQuestion'])
        except Question.DoesNotExist:
           return Response("There Are Question Does Not Exist !!!")
        choice_correct = Question.get_correct_choice(question_obj.id)
        if choice_correct == question['IdChoice']:
             result = result + question_obj.mark
             correct_questions.append(
                 question_obj
             )
             answer = Choices.objects.get(id = choice_correct)
             correct_questions_c.append(
                 {
                     "Question" :question_obj.question_text,
                     "Correct_Answer":answer.choice_text
                 }
             )
        else:
            worng_questions.append(
                 question_obj
             )
            print(choice_correct)
            # Search Text Choice By Id 
            try:
                text_answer = Choices.objects.get(id=question['IdChoice'])
            # If Answer Does Not Exist 
            except Choices.DoesNotExist:
                return Response("Some Thing Go Worng !!")
            # Search Text Choice correct By Id 
            try:
               answer = Choices.objects.get(id = choice_correct)
            except Choices.DoesNotExist:
            # If Answer Does Not Exist 
                return Response("Some Thing Go Worng !!")
            worng_questions_c.append(
                 {
                     "Question" :question_obj.question_text,
                     "Your Answer ":text_answer.choice_text,
                     "Correct_Answer":answer.choice_text
                 }
            )
    result_s =Results.objects.create(
          Result=result,
          Quiz=quiz,
          user=request.user,
    )
    result_s.correct_questions.set(correct_questions)  
    result_s.worng_questions.set(worng_questions) 
    result_s.save()
    if result_s:
            
         return Response({"message":"Your Result Is Saved"," Your Result is marks ":result ,"Quiz_MarkTotal":quiz.mark_total,
                         "CorrectQuestions": correct_questions_c,
                         "WorngQuestions": worng_questions_c,
                         },status=status.HTTP_201_CREATED)
         
         
         
@api_view(['GET'])
@permission_classes([Is_Student])
def MyResult(request):
      """
    This Function To view Results from Results Table For Students .
    **Responses:**
    - 404 - You Are Not Have Any Result !!
    - 200 - view result
    **Parameters:**
    - No Parameter.
    **Security:**
    - Requires authentacation (Students)
    - This Function uses from Account for Students only.
    """
      myresult = Results.objects.filter(user=request.user)
      if len(myresult)==0:
          # if user who send request doesnot have any result 
          return Response({"You Are Not Have Any Result !!"},status=status.HTTP_404_NOT_FOUND)
      all_result = []
      for result in myresult:
          quiz = Quizes.objects.get(id=result.Quiz_id)
          all_result.append(
              {
                  "id" : result.id,
                  "Your Result " : result.Result,
                  "Total Mark":quiz.mark_total,
                  "Category" : quiz.category.name,
                  "Quiz_Title":quiz.title,
                  "Tutor Name":quiz.category.user.name,
                  "Number Of Total Question" :quiz.count_questions,
                  "Number Of Correct Question" :result.correct_questions.count(),
                  "Number Of Worng Question" :result.worng_questions.count(),
                  "Date ":result.created_at,
              }
          )
      return Response(all_result,status=status.HTTP_200_OK)
            
        
           
@api_view(['GET'])  
@permission_classes([Is_Teacher])
# id for quiz  
def ViewResult(request,id):
    """
    This Function To view Results from Results for any Quiz  .
    **Responses:**
    - 404 - The Quiz DoesNotExist !!
    - 203 - You Dont Have Permission To Acceess To Result For This Quiz !!.
    - 200 view result for students
    **Parameters:**
    - id integer - id for quiz to see result student who answer it .
    **Security:**
    - Requires authentacation (Teachers)
    - This Function uses from Account for Teachers only.
    """
    try:
        quiz = Quizes.objects.get(id=id)
    except Quizes.DoesNotExist:
        return Response("The Quiz DoesNotExist !!!",status=status.HTTP_404_NOT_FOUND)
    if request.user != quiz.category.user:
       return Response("You Dont Have Permission To Acceess To Result For This Quiz !!",status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    results = []
    results_obj = Results.objects.filter(Quiz = quiz)
    for result in results_obj:
        results.append(
            {
                "Student_email" : result.user.email,
                "Student_name" : result.user.name,
                "Result":result.Result,
                "Date" : result.created_at,
                "Total Mark":quiz.mark_total,
                "Number Of Total Question" :quiz.count_questions,
                "Number Of Correct Question" :result.correct_questions.count(),
                "Number Of Worng Question" :result.worng_questions.count(),
                
            }
        )
    return Response (results,status=status.HTTP_200_OK)
           
        
            
        
    



