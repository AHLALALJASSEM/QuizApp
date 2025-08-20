from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from .models import Question, Choices
from .serializer import QuestionSerializer
from category.models import Category
from category.serializers import CategorySerializer
from rest_framework import status
from .serializer import ChoiceSerializer
from users.permission import Is_Teacher



@api_view(['POST'])
@permission_classes([Is_Teacher])
# (This Function For Teacher)
def AddQuestion(request):
    """
    This Function To Add question to Category this Function For Teachers only 
    teacher who create category can add question to same category.
    **Request Body:**
    - question_text : string (required) -text question 
    - category : integer (required) -id of category to add question to it.
    - mark : integer (required) -mark for question.
    - Answers : array (required) -contain [
        {
         "choice_text":string,
         "is_correct":bolean
        },
         {
         "choice_text":string,
         "is_correct":bolean
        },
         {
         "choice_text":string,
         "is_correct":bolean
        },
         {
         "choice_text":string,
         "is_correct":bolean
        }
    ]
    one answer is correct 
    number of answer min 2 max 4.
    **Example Request:**
     {
      "question_text":"Whats HTML  ?",
      "category":8,
      "mark":5,
      "Answers":[
        {
         "choice_text":"ANSWER 1",
         "is_correct":"false"
         },
         {
          "choice_text":"ANSWER 2",
          "is_correct":"false"
          },
         {
           "choice_text":"ANSWER 3 ",
           "is_correct":"true"
          },
        {
         "choice_text":"ANSWER 4",
         "is_correct":"false"
        }
      ]
}.
    **Responses:**
    - 404 The Category id = {} is Does Not Exist"
    - 403 IF Teacher Dont created this category!!
    - 205 number of choices min 2 or max 4
    - 205 number of choice correct answer more one 
    - 201 The Question  Added Successfully
    **Parameters:**
    no parametres
    **Security:**
    - Requires authentacation (Teacher who created category)
    - This Function uses from Account for Teachers only .
    
    """
    data = request.data
    try:
        category = Category.objects.get(id=data['category'])
    except Category.DoesNotExist:
        return Response("The Category Is Does Not Exist !!",status=status.HTTP_404_NOT_FOUND)
    if request.user != category.user:
        return Response('You Dont Have Permission To ADD Question To This Category !!',status=status.HTTP_403_FORBIDDEN)
    if len(data["Answers"]) < 2 or len(data["Answers"]) > 4 :
        return Response('Number Of Answers Must Between Tow And Four ONLY !!',status=status.HTTP_205_RESET_CONTENT)
    corect_Answer_num = 0 
    for Answer in data["Answers"]:
        if Answer['is_correct'] == "true":
            corect_Answer_num = corect_Answer_num + 1
    if corect_Answer_num == 0 or corect_Answer_num > 1 :
        return Response('Please Choose One Answer Only Only !!',status=status.HTTP_205_RESET_CONTENT)
    questionSerializer = QuestionSerializer(data=data)
    if questionSerializer.is_valid():
      question_new = Question.objects.create(
            question_text = data['question_text'],
            category=category,
            mark=data['mark']
        )
      if question_new:
       Question.create_choices(data['Answers'],question_new)
      return Response({"message":"The Question  Added Successfully",
                       "id":question_new.id,
                     "Question_text":question_new.question_text,
                     "Choices":data["Answers"]
                     },status=status.HTTP_201_CREATED)
    else:
        return Response(questionSerializer.errors)

        
    



@api_view(['GET'])
@permission_classes([Is_Teacher])
# pk for Category id  (This Function For Teacher)
def GetQuestion_by_Category(request,pk):
    """
    This Function To get question to Category this Function For Teachers only 
    teacher who create category can get question to same category.
    **Request Body:**
     No body 
    **Responses:**
    - 200 The Question  Get Successfully.
    **Parameters:**
    - id integer - id for category to get questions 
    **Security:**
    - Requires authentacation (Teacher who created category)
    - This Function uses from Account for Teachers only .
    
    """
    try:
        category=Category.objects.filter(id=pk)
    except Category.DoesNotExist:
        return Response("the category does not exist ",status=status.HTTP_404_NOT_FOUND)
    try:
        question_objs=Question.objects.filter(category_id=pk)
    except Question.DoesNotExist:
        return Response("There Are not Question for This Category ",status=status.HTTP_404_NOT_FOUND)
    data=[]
    for question_obj in question_objs:
       data.append(
           {
               "id":question_obj.id,
               "Question":question_obj.question_text,
               "Category":question_obj.category.name,
               "Mark":question_obj.mark,
               "Choices":question_obj.get_choices(question_obj.id)
           }
                 )
    
    return Response(data)
# pk for Question id   (This Function For Teacher)
@api_view(['PUT'])
@permission_classes([Is_Teacher])
def EditQuestion(request,pk):
    """
    This Function To edit question to Category this Function For Teachers only 
    teacher who create category can edit question to same category.
    **Request Body:**
    - question_text : string (required) -text question 
    - category : integer (required) -id of category to add question to it.
    - mark : integer (required) -mark for question.
    - Answers : array (required) -contain [
        {
         "choice_text":string,
         "is_correct":bolean
        },
         {
         "choice_text":string,
         "is_correct":bolean
        },
         {
         "choice_text":string,
         "is_correct":bolean
        },
         {
         "choice_text":string,
         "is_correct":bolean
        }
    ]
    one answer is correct 
    number of answer min 2 max 4.
    **Example Request:**
     {
      "question_text":"Whats HTML  ?",
      "category":8,
      "mark":5,
      "Answers":[
        {
         "choice_text":"ANSWER 1",
         "is_correct":"false"
         },
         {
          "choice_text":"ANSWER 2",
          "is_correct":"false"
          },
         {
           "choice_text":"ANSWER 3 ",
           "is_correct":"true"
          },
        {
         "choice_text":"ANSWER 4",
         "is_correct":"false"
        }
      ]
      }.
    **Responses:**
    - 404 The question id = {} is Does Not Exist"
    - 304 if you are not crated category of question!! 
    - 201 The Question  edited Successfully
    **Parameters:**
    - id integer id for qustion which you edit it .
    **Security:**
    - Requires authentacation (Teacher who created category)
    - This Function uses from Account for Teachers only .
    
    """
    data=request.data
    try:
        question = Question.objects.get(id=pk)
    except Question.DoesNotExist:
         return Response("The Question Is Not Exist !!!",status=status.HTTP_404_NOT_FOUND)
    if question:
        category=Category.objects.get(id=question.category_id)
    if request.user != category.user:
        return Response('You Dont Have Permission To move Question from This Category !!',status=status.HTTP_304_NOT_MODIFIED)
    try:
        category_new = Category.objects.get(name=data['category'])
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.user != category_new.user:
        return Response('You Dont Have Permission To ADD Question To This Category !!',status=status.HTTP_304_NOT_MODIFIED)
    data['category']=category_new.id
    questin_new=QuestionSerializer(question,data=data)
    if questin_new.is_valid():
       questin_new_saved = questin_new.save()
    if questin_new_saved:
        ChoiceSerializer.edit_choices(questin_new_saved,data['Answers'])
    return Response("The Question Has Edited !!",status=status.HTTP_200_OK)
        
@api_view(['DELETE'])
@permission_classes([Is_Teacher])
# pk for Question id   (This Function For Teacher)
def delete_question(request,pk):
    """
    This Function To delete  question from List question this Function For teachers only .
    **Request Body:**
    - No body
    **Responses:**
    - 200 delete question Successfully.
    - 304 if you are not crated category of question!!
    - 404 id for question does not exist. 
    **Parameters:**
    - id integer id for question you want edit it .
    **Security:**
    - Requires authentacation (teacher who created category)
    - This Function uses from Account for teacher only .
    
    """
    try:
        question_obj = Question.objects.get(id=pk)
    except Question.DoesNotExist:
        return Response("The Question Is Not Exist !!!")
    if question_obj:
        category=Category.objects.get(id=question_obj.category_id)
    if request.user != category.user:
        return Response('You Dont Have Permission To ADD Question To This Category !!',status=status.HTTP_304_NOT_MODIFIED)
    qustion_deleted = question_obj.delete() 
    # if qustion_deleted:
    #     ChoiceSerializer.delete_choices(question_obj)   
    return Response("The Question Has Deleted !!",status=status.HTTP_200_OK)
        
        
                
        
    
    
    
    
     
    
    return Response(category.description)
   
    
    
    
    
    
    
