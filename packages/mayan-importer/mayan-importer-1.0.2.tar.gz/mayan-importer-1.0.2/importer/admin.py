from django.contrib import admin

from .models import ImportSetup, ImportSetupItem


class ImportSetupItemInline(admin.StackedInline):
    model = ImportSetupItem
    extra = 1
    classes = ('collapse-open',)
    allow_add = True


@admin.register(ImportSetup)
class ImportSetupAdmin(admin.ModelAdmin):
    inlines = (ImportSetupItemInline,)
    list_display = (
        'label', 'document_type', 'credential', 'filename_regex',
        'folder_regex', 'process_size'
    )
