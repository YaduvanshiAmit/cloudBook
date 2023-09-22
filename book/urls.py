from django.urls import include, path
from .views import *

urlpatterns = [
    path(
        'BookTitle',
        CreateBook.as_view(),
        name = "CreateBookTitle"
    ),

    path(
        'BookSection',
        BookSectionViews.as_view(),
        name = "CreateBookSection"
    ),

    path(
        'SectionSubSection',
        SectionSubSectionViews.as_view(),
        name = "SectionSubSection"
    ),
    
    path(
        'collaborators',
        CollaboratorViewSet.as_view(),
        name = "Collaborator"
    ),
    

    path(
        'BookData',
        RetrieveData.as_view(),
        name = "BookData"
    ),
    
]