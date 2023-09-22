

# Register your models here.
from django.contrib import admin
from .models import Book, Chapter


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'user','created_date', 'is_deleted')
    list_filter = ('is_deleted', 'created_date')
    search_fields = ('title', 'user__username')
    list_per_page = 20

    # Customize the ManyToManyField 'collaborators' with autocomplete
    filter_horizontal = ('collaborators',)

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('section', 'user', 'book', 'parent_chapter', 'is_deleted', 'created_date')
    list_filter = ('is_deleted', 'created_date')
    search_fields = ('section', 'user__username', 'book__title')
    list_per_page = 20

    # Customize the ForeignKey 'book' with autocomplete
    autocomplete_fields = ('book',)

    # Display parent chapter as a clickable link
    list_display_links = ('parent_chapter',)

    # Enable tree-based display for parent-child relationships
    list_select_related = ('parent_chapter',)

    # Hierarchical display using 'list_filter'
    list_filter = (
        'book',
        'parent_chapter__book',
        'is_deleted',
        'created_date',
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent_chapter":
            kwargs["queryset"] = Chapter.objects.filter(parent_chapter__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
