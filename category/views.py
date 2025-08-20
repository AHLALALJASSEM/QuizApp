from django.shortcuts import render
from .models import Category
from .serializers import CategorySerializer
from django.http import HttpResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from users.models import User
from rest_framework import status
from users.permission import Is_Teacher,Is_Student

@api_view(['Post'])
@permission_classes([Is_Teacher])
def AddCategory(request):
   """
    This Function To Add New Category To List Category  For this Function For Teachers only.
    **Request Body:**
    - name : string (required) -Name of New Category (Uniqe)
    - description : string (required) -description of New Category.
    **Example Request:**
    {
      "name":"HTML",
      "description":"For Web "
       }.
    **Responses:**
    - 201 Add category Successfully. 
    **Parameters:**
    - No Parameters .
    **Security:**
    - Requires authentacation
    - This Function uses from Account for Teachers only .
    
    """
   data = request.data
   category = CategorySerializer(data=data)
   if category.is_valid():
       Category.objects.create(
           name=data['name'],
           description=data['description'],
           user=request.user
       )
       return Response({'Response':'The Category  Added Succesfully'},status=status.HTTP_201_CREATED)
   else:
       return Response(category.errors)
   
@api_view(['GET'])
@permission_classes([Is_Teacher])
def GetCategory(request):
      """
    This Function To Get All Category from List Category this Function For Teachers only ( category Teacher who created).
    **Request Body:**
    - No body
    **Responses:**
    - 200 Get All Category Successfully. 
    **Parameters:**
    - No Parameters .
    **Security:**
    - Requires authentacation (Teacher)
    - This Function uses from Account for Teachers only .
    
    """
      allcategory = Category.objects.filter(user=request.user)
      if len(allcategory)==0:
          # if user who send request doesnot created any category 
          return Response({"You Are Not Created Any Category !!"},status=status.HTTP_202_ACCEPTED)
      all_category = CategorySerializer(allcategory,many=True).data
      for category in all_category:
          user_name =User.objects.get(id=category['user'])
          # show username for user who created category 
          category['user']=user_name.name
      return Response({'Categories':all_category},status=status.HTTP_200_OK)
 
 
# show all category for students 
@api_view(['GET'])
@permission_classes([Is_Student])
def GetCategory_S(request):
      """
    This Function To Get All Category from List Category this Function For Stusents only .
    **Request Body:**
    - No body
    **Responses:**
    - 200 Get All Category Successfully. 
    **Parameters:**
    - No Parameters .
    **Security:**
    - Requires authentacation (Student)
    - This Function uses from Account for Student only .
    
    """
      allcategory = Category.objects.all()
      if len(allcategory)==0:
          return Response({"Doesnt any category !!"},status=status.HTTP_202_ACCEPTED)
      all_category = CategorySerializer(allcategory,many=True).data
      for category in all_category:
          user_name =User.objects.get(id=category['user'])
          category['user']=user_name.name
      return Response({'Categories':all_category},status=status.HTTP_200_OK)


@api_view(['Put'])
@permission_classes([Is_Teacher])
def ModifyCategory(request,pk):
    """
    This Function To edit  Category in List Category this Function For Teachers only .
    **Request Body:**
    - name : string (required) -Name of New Category (Uniqe)
    - description : string (required) -description of New Category.
    **Example Request:**
    {
      "name":"HTML",
      "description":"For Web Structure "
       }.
    **Responses:**
    - 404 The Category id = {} is Does Not Exist"
    - 404 The Category You Want To Edit Not For You!!
    - 202 category edited succesfully
    **Parameters:**
    - id -int id of category you edit .
    **Security:**
    - Requires authentacation (Teacher who created category)
    - This Function uses from Account for Teachers only .
    
    """
    data = request.data
    try:
        category = Category.objects.get(id=pk)
        name_old = category.name
    except Category.DoesNotExist:
        return Response("The Category id = {} is Does Not Exist".format(id),status=status.HTTP_404_NOT_FOUND)
    
    serializser=CategorySerializer(category,data=data)
    # user who created category who can edited it  
    if request.user == category.user:
        if serializser.is_valid():
            serializser.save()
            return Response({"message":"The Category {} Has Edited Succesfully To New Name {}" .format(name_old,data['name'])},status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializser.errors)
    else:
             return Response("The Category You Want To Edit Not For You!!",status=status.HTTP_404_NOT_FOUND)
         
              
    

@api_view(['Delete'])
@permission_classes([Is_Teacher])
def DeleteCategory(request,pk):
    """
    This Function To delete  Category from List Category this Function For teachers only .
    **Request Body:**
    - No body
    **Responses:**
    - 200 delete Category Successfully.
    - 404 id for category does not exist. 
    **Parameters:**
    - id integer id for category you want edit it .
    **Security:**
    - Requires authentacation (teacher who created category)
    - This Function uses from Account for teacher only .
    
    """
    try:
        category = Category.objects.get(id=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # user who created category who can deleted it 
    if request.user == category.user:
          category.delete()
          return Response("The Category Deleted Has Succesfully")
    
    
   
    
    


