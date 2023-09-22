from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class userSerializers(serializers.ModelSerializer):
 
    class Meta:
        model = User
        fields =  '__all__'

class CollaboratorSerializer(serializers.Serializer):
    book_id = serializers.CharField(
        required = False,
        label ='book_id'
    )
    user_id = serializers.CharField(
        required = False,
        label ='user_id'
    )
    @classmethod
    def validate(self,data):
        errors = {}
        # if data.get('image'):
        #     if not Helper.checkImageExtension(data.get('image')):
        #             errors["image"] = "Please select valid Image"
           
            

        if errors:
            raise serializers.ValidationError(errors)
        return super(CollaboratorSerializer, self).validate(self, data)




class BookSerializers(serializers.Serializer):
    book_id = serializers.CharField(
        required = False,
        label ='id'
    )
    title = serializers.CharField(
        style={'base_template': 'textarea.html'},
        required=False,
        label='title',
        min_length=1,
        max_length=100,
        error_messages={'blank': "Message can't be blank"},
    )
    @classmethod
    def validate(self,data):
        errors = {}
        # if data.get('image'):
        #     if not Helper.checkImageExtension(data.get('image')):
        #             errors["image"] = "Please select valid Image"
           
            

        if errors:
            raise serializers.ValidationError(errors)
        return super(BookSerializers, self).validate(self, data)
    

class BookSectionSerializer(serializers.Serializer):
    section_id = serializers.CharField(
        required = False,
        label ='section_id'
    )

    section = serializers.CharField(
        style={'base_template': 'textarea.html'},
        required=False,
        label='content',
        min_length=1,
        max_length=500,
        error_messages={'blank': "Message can't be blank"},
    )
    
    @classmethod
    def validate(self,data):
        errors = {}
    

        if errors:
            raise serializers.ValidationError(errors)
        return super(BookSectionSerializer, self).validate(self, data)
    


    

class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data
    
class ChapterSerializer(serializers.ModelSerializer):
    child_chapters = RecursiveSerializer(many=True, read_only=True)

    class Meta:
        model = Chapter
        exclude = ['updated_date', 'deleted_date', 'is_deleted']




# class RetrieveBookDataSerializer(serializers.ModelSerializer):
#     chapters = ChapterSerializer(many=True,read_only=True)
#     class Meta:
#         model = Book
#         fields = ['uuid','title','chapters']
class BookDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id','uuid','title']
    
    
class RetrieveBookDataSerializer(serializers.ModelSerializer):
    book = BookDataSerializer(read_only=True)
    child_chapters = RecursiveSerializer(many=True, read_only=True)
    class Meta:
        model = Chapter
        exclude = ['updated_date', 'deleted_date', 'is_deleted']