from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from django.http.response import JsonResponse
from .models import *
from django.db import transaction
import json
from .serializers import *
from .permission import *
from rest_framework import generics
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache

# Create your views here.

class userviewsets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = userSerializers


class CreateBook(APIView):
    """
    View to create, edit, and delete books.
    """
    serializer_class = BookSerializers
    @classmethod
    def post(self,request):
        res ={}
        resStatus =200
        res["isError"] = False

        postData =BookSerializers(data=request.data)
        if postData.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    instance = Book.objects.create(
                        user = user,
                        title = postData.data.get('title')
                    )
                    res['data'] = {'msg':"Book Create Succesfully",
                                   'uuid':instance.uuid,
                                   'id':instance.id}
            except Exception as e:
                print(e)
                resStatus = 501
                res["isError"] = True
                res["errors"] = "Errors! Please try after some times."
        else:
            resStatus = 400
            res["isError"] = True
            res["msg"] = "Errors! Please try."
            res["errors"] = json.dumps(postData.errors)

        return JsonResponse(res, status=resStatus)
    
    def patch(self,request):
        res ={}
        resStatus =200
        res["isError"] = False

        postData =BookSerializers(data=request.data)
        if postData.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    instance = Book.objects.get(
                        user = user,
                        uuid = postData.data.get('book_id')
                    )
                    instance.title = postData.data.get('title')
                    instance.save()
                    res['msg'] = "Book Title Edit Succesfully"
                    res['data'] = {
                                   'uuid':instance.uuid,
                                   'id':instance.id}
            except Exception as e:
                print(e)
                resStatus = 501
                res["isError"] = True
                res["errors"] = "Errors! Please try after some times."
        else:
            resStatus = 400
            res["isError"] = True
            res["msg"] = "Errors! Please try."
            res["errors"] = json.dumps(postData.errors)

        return JsonResponse(res, status=resStatus)
    
    def delete(self, request):
        res = {}
        resStatus = 200
        res["isError"] = False
        postData = BookSerializers(data=request.data)
        if postData.is_valid():
            try:
                with transaction.atomic():
                    user_obj = request.user
                    # user = JobPosted.objects.filter(user = user_obj)
                    ind = Book.objects.get(uuid=postData.data.get(
                        'book_id'), user=user_obj, is_deleted=False)
                    ind.is_deleted = True
                    # ind.delete()
                    ind.save()
                    res['msg'] = 'succesfully deleted'
            except Exception as e:
                print(e)
                resStatus = 501
                res["isError"] = True
                res["errors"] = "Errors! Please try after some times."
        else:
            resStatus = 400
            res["isError"] = True
            res["msg"] = "Errors! Please try."
            res["errors"] = json.dumps(postData.errors)

        return JsonResponse(res, status=resStatus)




class BookSectionViews(APIView):
    """
    View to create and edit book sections.
    """
    serializer_class = BookSectionSerializer

    @classmethod
    def post(self,request):
        res = {}
        resStatus = 200
        res['isError'] = False
        postData = BookSectionSerializer(data=request.data)
        if postData.is_valid():
            try:
                with transaction.atomic():
                    user_obj = request.user
                    
                    book_id = request.GET.get('book_id')
                    print(book_id)
                    try:
                        book = Book.objects.get(uuid=book_id)
                    except Exception as e:
                        print(e)
                        resStatus = 501
                        res["isError"] = True
                        res["errors"] = "Please! Enter Right Post_id"
                    if user_obj == book.user:
                        instance = Chapter.objects.create(
                            user = user_obj,
                            section = postData.data.get('section'),
                            book = book,
                        )
                        instance.save()
                        res['msg'] = "Section Adds Succefully"
                        res['data'] = {
                                   'uuid':instance.uuid,
                                   'id':instance.id}
                    else:
                        resStatus = 501
                        res["isError"] = True
                        res["error"] = "Errors! You Don't Have Permission."
                        
            except Exception as e:
                print(e)
                resStatus = 501
                res["isError"] = True
                res["errors"] = "Errors! Please try after some times."
        else:
            resStatus = 400
            res["isError"] = True
            res["msg"] = "Errors! Please try."
            res["errors"] = json.dumps(postData.errors)

        return JsonResponse(res, status=resStatus)
    
    def patch(self,request):
        res = {}
        resStatus = 200
        res['isError'] = False
        postData = BookSectionSerializer(data=request.data)
        if postData.is_valid():
            try:
                with transaction.atomic():
                    user_obj = request.user
                    
                    book_id = request.GET.get('book_id')
                    try:
                        book = Book.objects.get(uuid=book_id)
                    except Exception as e:
                        print(e)
                        resStatus = 501
                        res["isError"] = True
                        res["errors"] = "Please! Enter Right Post_id"
                    if user_obj == book.user or user_obj in book.collaborators.all():
                        instance = Chapter.objects.get(
                            # user = user_obj,
                            book = book,
                            uuid = postData.data.get('section_id')
                        )
                        instance.EditUser = user_obj
                        instance.section = postData.data.get('section')
                        instance.save()
                        res['msg'] = "Section Update Succefully"
                        res['data'] = {
                                   'uuid':instance.uuid,
                                   'id':instance.id}
                    else:
                        resStatus = 501
                        res["isError"] = True
                        res["error"] = "Errors! You Don't Have Permission."
            except Exception as e:
                print(e)
                resStatus = 501
                res["isError"] = True
                res["errors"] = "Errors! Please try after some times."
        else:
            resStatus = 400
            res["isError"] = True
            res["msg"] = "Errors! Please try."
            res["errors"] = json.dumps(postData.errors)

        return JsonResponse(res, status=resStatus)



class SectionSubSectionViews(APIView):
    """
    View to create and edit subsections.
    """
    serializer_class = BookSectionSerializer

    @classmethod
    def post(self,request):
        res = {}
        resStatus = 200
        res['isError'] = False
        postData = BookSectionSerializer(data=request.data)
        if postData.is_valid():
            try:
                with transaction.atomic():
                    user_obj = request.user
                    
                    section_id = request.GET.get('section_id')
                    try:
                        section = Chapter.objects.get(uuid=section_id)
                    except Exception as e:
                        print(e)
                        resStatus = 501
                        res["isError"] = True
                        res["errors"] = "Please! Enter Right Section_id"
                    if user_obj == section.book.user:
                        instance = Chapter.objects.create(
                            user = user_obj,
                            section = postData.data.get('section'),
                            book = section.book,
                            parent_chapter = section,
                        )
                        instance.save()
                        res['msg'] = "SubSection Adds Succefully"
                        res['data'] = {
                                   'uuid':instance.uuid,
                                   'id':instance.id}
                    else:
                        resStatus = 501
                        res["isError"] = True
                        res["error"] = "Errors! You Don't Have Permission."
                    
            except Exception as e:
                print(e)
                resStatus = 501
                res["isError"] = True
                res["errors"] = "Errors! Please try after some times."
        else:
            resStatus = 400
            res["isError"] = True
            res["msg"] = "Errors! Please try."
            res["errors"] = json.dumps(postData.errors)

        return JsonResponse(res, status=resStatus)
    
    def patch(self,request):
        res = {}
        resStatus = 200
        res['isError'] = False
        postData = BookSectionSerializer(data=request.data)
        if postData.is_valid():
            try:
                with transaction.atomic():
                    user_obj = request.user
                    
                    section_id = request.GET.get('section_id')
                    try:
                        section = Chapter.objects.get(uuid=section_id)
                    except Exception as e:
                        print(e)
                        resStatus = 501
                        res["isError"] = True
                        res["errors"] = "Please! Enter Right Section_id"
                    
                    if user_obj == section.book.user or user_obj in section.book.collaborators.all():
                        instance = Chapter.objects.get(
                            uuid = section.uuid,
                            # user = user_obj,
                            
                            book = section.book,
                            # parnet_chapter = section,
                        )

                        instance.section = postData.data.get('section')
                        instance.EditUser = user_obj
                        instance.save()
                        res['msg'] = "SubSection Update Succefully"
                        res['data'] = {
                                   'uuid':instance.uuid,
                                   'id':instance.id}
                    else:
                        resStatus = 501
                        res["isError"] = True
                        res["error"] = "Errors! You Don't Have Permission."
                    
            except Exception as e:
                print(e)
                resStatus = 501
                res["isError"] = True
                res["errors"] = "Errors! Please try after some times."
        else:
            resStatus = 400
            res["isError"] = True
            res["msg"] = "Errors! Please try."
            res["errors"] = json.dumps(postData.errors)

        return JsonResponse(res, status=resStatus)
    


##### Add Collabarotor
class CollaboratorViewSet(APIView):
    serializer_class = CollaboratorSerializer

    @classmethod
    def post(self,request):
        res = {}
        resStatus = 200
        res['isError'] = False
        postData = CollaboratorSerializer(data=request.data)
        if postData.is_valid():
            try:
                with transaction.atomic():
                    user_obj = request.user
                    user = User.objects.get(id=postData.data.get('user_id'))
                    book = Book.objects.get(
                        user = user_obj,
                        uuid = postData.data.get('book_id')
                    )
                    if user not in book.collaborators.all():
                        book.collaborators.add(user)
                        res['msg'] = 'Succesfully Added'
                    else:
                        resStatus = 400
                        res["isError"] = True
                        res["errors"] = "User is already a collaborator."

                    
                    



            except Exception as e:
                print(e)
                resStatus = 501
                res["isError"] = True
                res["errors"] = "Errors! Please try after some times."
        else:
            resStatus = 400
            res["isError"] = True
            res["msg"] = "Errors! Please try."
            res["errors"] = json.dumps(postData.errors)

        return JsonResponse(res, status=resStatus)
    
    def delete(self,request):
        res = {}
        resStatus = 200
        res["isError"] = False
        postData = CollaboratorSerializer(data=request.data)
        if postData.is_valid():
            try:
                with transaction.atomic():
                    user_obj = request.user
                    user = User.objects.get(id=postData.data.get('user_id'))
                    book = Book.objects.get(
                        user = user_obj,
                        uuid = postData.data.get('book_id')
                    )
                    if user in book.collaborators.all():
                        book.collaborators.remove(user)
                        res['msg'] = 'Collaborator removed successfully'
                    else:
                        resStatus = 400
                        res["isError"] = True
                        res["errors"] = "User is not a collaborator."
                    
                    



            except Exception as e:
                print(e)
                resStatus = 501
                res["isError"] = True
                res["errors"] = "Errors! Please try after some times."
        else:
            resStatus = 400
            res["isError"] = True
            res["msg"] = "Errors! Please try."
            res["errors"] = json.dumps(postData.errors)

        return JsonResponse(res, status=resStatus)
    


class MyLimitPagination(PageNumberPagination):
    page_size=5


#### Get APi

class RetrieveData(generics.ListCreateAPIView):
    serializer_class = RetrieveBookDataSerializer

    def get_queryset(self):
        book_id = self.request.GET.get('book_id')

        # Try to retrieve the data from cache
        
        queryset = Chapter.objects.filter(book=book_id, is_deleted=False,parent_chapter=None).order_by('-created_date')
        # Cache the queryset for future use
        # Cache for 15 minutes after that it delete

        return queryset
        