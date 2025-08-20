from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status

from category.models import Category
from Question.models import Question
from .models import Quizes
from .serializer import QuizSerializer
from users.permission import Is_Teacher,Is_Student


@api_view(['POST'])
@permission_classes([Is_Teacher])
def CreatQuiz(request):
    """
    This Function To Add Quiz by select group of questions from Category this Function For Teachers only 
    teacher who create category can create quizes from same category.
    **Request Body:**
    - category : integer (required) -id of category to create quiz from it.
    - title : string (required) -title of quiz.
    - description : string (required) -description of quiz.
    - lv : string select from list ["Simple","Intermidate","Advanced"].
    - duration_minutes: integer (required) - time to quiz by minutes
    - Questions : array (required) -contain [integer,integer,integer] id for question you want to add it to quiz
    **Example Request:**
     {
      {
       "category":6,
       "title":"css",
       "description":"css",
        "lv":"Simple",
       "duration_minutes":80,
       "Questions":[30,31,32,33,34,35]
      } 
      ]
     }.
    **Responses:**
    - 400 You Dont Have Permission To ADD Quiz To This Category if you not create the category 
    - 205 You Should Select One Question Minuimum To Create This Quiz 
    - 201 The Quiz  Added Successfully
    **Parameters:**
    no parametres
    **Security:**
    - Requires authentacation (Teacher who created category)
    - This Function uses from Account for Teachers only .
    
    """
    Quiz_Info = request.data
    try:
        category = Category.objects.get(id = Quiz_Info['category'])
    except Category.DoesNotExist:
        return Response("The Category {} is Does Not Exist !!".format(Quiz_Info['category']))
    if request.user != category.user:
        return Response("You Dont Have Permission To ADD Quiz To This Category !!",status=status.HTTP_400_BAD_REQUEST)
    correct_questions=[]
    question_all=[]
    worng_question=[]
    mark_For_Quiz = 0
    for question in Quiz_Info['Questions']:
        try:
            question_obj = Question.objects.get(id=question)
            if request.user == category.user and category==question_obj.category:
                  correct_questions.append(question_obj)
                  mark_For_Quiz+=question_obj.mark
                  question_all.append({
                    "id":question_obj.id,
                    "Question":question_obj.question_text,
                    "Category":question_obj.category.name,
                    "Mark":question_obj.mark,
                    "Choices":question_obj.get_choices(question_obj.id)
                   })
        except Question.DoesNotExist:
            worng_question.append(question)
    if len(correct_questions) == 0 :
        return Response("You Should Select One Question Minuimum To Create This Quiz !!",status=status.HTTP_205_RESET_CONTENT)
    quiz = Quizes.objects.create(
        title = Quiz_Info['title'],
        category = category,
        description = Quiz_Info['description'],
        lv = Quiz_Info['lv'],
        mark_total=mark_For_Quiz,
        duration_minutes = Quiz_Info['duration_minutes'],
        count_questions = len(correct_questions)
    )
    quiz.questions.set(correct_questions)
    quiz.save()
    new_quiz = QuizSerializer(quiz).data
    return Response({"Quiz_Info":new_quiz,"Questions":question_all},status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([Is_Teacher])
#id for Category
def GetQuizes(request,id):
    """
    This Function To get Quizes by id from Category this Function For Teachers only 
    teacher who create quiz can get quizes from same category.
    **Request Body:**
     No body
    **Responses:**
    - 404  The Category Does Not Exist.
    - 202 get quizes succesfully.
    - 203 You Dont Have Permission To Access For Quizes.
    **Parameters:**
    - id integer (required) id for category you want to get quizes to it 
    **Security:**
    - Requires authentacation (Teacher who created category)
    - This Function uses from Account for Teachers only .
    
    """
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response("The Category Does Not Exist !!",status=status.HTTP_404_NOT_FOUND)
    if request.user == category.user:
       quizes = Quizes.objects.filter(category=category)
       quiz_serializer = QuizSerializer(quizes,many=True)
       return Response({"Quizes":quiz_serializer.data},status=status.HTTP_202_ACCEPTED)
    else:
        return Response("You Dont Have Permission To Access For Quizes For {}".format(category.name),status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    
@api_view(['GET'])
@permission_classes([Is_Student])
#id for Category
def GetQuizes_S(request,id):
    """
    This Function To get all Quizes by id from Category this Function For students only 
    **Request Body:**
     No body
    **Responses:**
    - 404  The Category Does Not Exist.
    - 202 get quizes succesfully.
    **Parameters:**
    - id integer (required) id for category you want to get quizes to it 
    **Security:**
    - Requires authentacation (Student)
    - This Function uses from Account for Students only .
    
    """
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response("The Category Does Not Exist !!",status=status.HTTP_404_NOT_FOUND)
    quizes = Quizes.objects.filter(category=category)
    quiz_serializer = QuizSerializer(quizes,many=True)
    return Response({"Quizes":quiz_serializer.data},status=status.HTTP_202_ACCEPTED)

    
    
@api_view(['GET'])
#id for Quiz
def GetDetailForQuiz(request,id):
    """
    This Function To get detail for Quiz by id from Category this Function For all (students,teachers)
    **Request Body:**
     No body
    **Responses:**
    - 404  The quiz Does Not Exist.
    - 203 You Dont Have Permission To Access For This quiz.
    - 200 get detail for quiz suucessfully.
    **Parameters:**
    - id integer (required) id for quiz you want to get detail to it 
    **Security:**
    - Requires authentacation (Student or teacher)
    
    """
    try:
        quiz=Quizes.objects.get(id=id)
    except Quizes.DoesNotExist:
        return Response("The Quiz Does Not Exist !!",status=status.HTTP_404_NOT_FOUND)
    category = quiz.category
    if request.user != category.user and request.user.role == "Teacher" :
        return Response("You Dont Have Permission To Access For This quiz !!",status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    quizserializer= QuizSerializer(quiz)
    questions = []
    for question_obj in quiz.questions.all():
        questions.append(
            {
                    "id":question_obj.id,
                    "Question":question_obj.question_text,
                    "Category":question_obj.category.name,
                    "Mark":question_obj.mark,
                    "Choices":question_obj.get_choices(question_obj.id)
            }
        )
    return Response({"quiz":quizserializer.data,"Questions":questions},status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([Is_Teacher])
# id for Quiz
def EditQuiz(request,id):
    """
    This Function To edit Quiz by id Category this Function For Teachers only 
    teacher who create quiz can edit quizes from same category.
    **Request Body:**
    - category : integer (required) -id of category to create quiz from it.
    - title : string (required) -title of quiz.
    - description : string (required) -description of quiz.
    - lv : string select from list ["Simple","Intermidate","Advanced"].
    - duration_minutes: integer (required) - time to quiz by minutes
    - Questions : array (required) -contain [integer,integer,integer] id for question you want to add it to quiz
    **Example Request:**
     {
      {
       "category":6,
       "title":"css",
       "description":"css",
        "lv":"Simple",
       "duration_minutes":80,
       "Questions":[30,31,32,33,34,35]
      } 
      ]
     }.
    **Responses:**
    - 404 The Quiz {} Does Not Exist ,There Are Question Does Not Exist
    - 203 You Dont Have Permission To Access For This quiz !!
    - 200 TThe Quiz {} Has Edited Sucsess
    **Parameters:**
     - id integer (required) - id for quiz you edit it
    **Security:**
    - Requires authentacation (Teacher who created quiz)
    - This Function uses from Account for Teachers only .
    
    """
    Quiz_Info = request.data
    try:
        quiz = Quizes.objects.get(id=id)
    except Quizes.DoesNotExist:
        return Response("The Quiz {} Does Not Exist ".format(id),status=status.HTTP_404_NOT_FOUND)
    category = quiz.category
    if request.user != category.user:
        return Response("You Dont Have Permission To Access For This quiz !!",status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    correct_questions = []
    mark_For_Quiz=0
    question_all=[]
    for question in Quiz_Info['Questions']:
        try:
            question_obj = Question.objects.get(id=question)
            if request.user == category.user and category==question_obj.category:
                  correct_questions.append(question_obj)
                  mark_For_Quiz+=question_obj.mark
                  question_all.append({
                    "id":question_obj.id,
                    "Question":question_obj.question_text,
                    "Category":question_obj.category.name,
                    "Mark":question_obj.mark,
                    "Choices":question_obj.get_choices(question_obj.id)
                   })
        except Question.DoesNotExist:
            return Response("There Are Question Does Not Exist  !!",status=status.HTTP_404_NOT_FOUND)
    if quiz :
        quiz.title = Quiz_Info['title']
        quiz.description = Quiz_Info['description']
        quiz.lv = Quiz_Info['lv']
        quiz.duration_minutes = Quiz_Info['duration_minutes']
        quiz.duration_minutes = Quiz_Info['duration_minutes']
        quiz.mark_total = mark_For_Quiz
        quiz.count_questions=len(correct_questions)
        quiz.questions.set(correct_questions)
    quiz.save() 
    quiz_data = QuizSerializer(quiz).data 
    return Response({"message":"The Quiz {} Has Edited Sucsess".format(quiz.id),"Quiz_Info":quiz_data,
                     "Questions_For_Quiz":question_all
                     },status=status.HTTP_200_OK )
    
    
@api_view(['DELETE'])
@permission_classes([Is_Teacher])
# id for quiz
def DeleteQuiz(request,id):
    """
    This Function To delete  quiz from List quizes this Function For teachers only .
    **Request Body:**
    - No body
    **Responses:**
    - 200 delete quiz Successfully.
    - 400 You Dont Have Permission To Remove For This quiz
    - 404 id for quiz does not exist. 
    **Parameters:**
    - id integer id for quiz you want delete it .
    **Security:**
    - Requires authentacation (teacher who created quiz)
    - This Function uses from Account for teacher only .
    """
    try:
        quiz = Quizes.objects.get(id=id)
    except Quizes.DoesNotExist:
        return Response("The Quiz id {} Has Does Not Exist !! ".format(id),status=status.HTTP_404_NOT_FOUND)
    category = quiz.category
    if request.user != category.user:
        return Response({"You Dont Have Permission To Remove For This quiz !!"},status=status.HTTP_400_BAD_REQUEST)

    quiz.delete()
    return Response("The Quiz id {} Has Remove Success !! ".format(id),status=status.HTTP_200_OK)
    




    
    
    
    
    







