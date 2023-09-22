# from rest_framework import permissions

# class IsAuthorOrCollaborator(permissions.BasePermission):
#     """
#     Custom permission to allow authors and collaborators to edit chapters.
#     """

#     def has_object_permission(self, request, view, obj):
#         # Check if the user is an author or collaborator for the book related to this object
#         user = request.user
#         book = obj.book

#         if user == book.user:
#             # Author can edit if they are the owner of the book
#             return True
#         elif  user in book.collaborators.all():
#             # Collaborator can edit if they are added as a collaborator
#             return True

#         return False

# class IsAuthor(permissions.BasePermission):
#     """
#     Custom permission to allow only authors to perform actions.
#     """

#     def has_permission(self, request, view,obj):
#         print(obj)
#         book = obj.book
#         user = request.user
#         if user.is_authenticated and user == book.user:
#             return True
#         return False

# # class IsCollaborator(permissions.BasePermission):
# #     """
# #     Custom permission to allow only collaborators to perform actions.
# #     """

# #     def has_permission(self, request, view):
# #         user = request.user
# #         return user.is_authenticated and user.is_collaborator
