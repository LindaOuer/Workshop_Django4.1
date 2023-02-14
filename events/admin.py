from django.contrib import admin, messages
from .models import *

# Register your models here.


class ParticipateInline(admin.TabularInline):
    model = Participation
    extra = 1
    readonly_fields = ['datePart']
    can_delete = False


def set_Accept(ModelAdmin, request, queryset):
    rows = queryset.update(state=True)
    if rows == 1:
        message = "One event was "
    else:
        message = f"{rows} events were"
    messages.success(request, message="% successfully accepted" % message)


set_Accept.short_description = 'Accept'


class ParticipateListFilter(admin.SimpleListFilter):
    title = 'Participation'
    parameter_name = 'nbrParticipants'

    def lookups(self, request, model_admin):
        return (
            ('0', 'No Participants'),
            ('more', 'There are Participants'),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(nbrParticipants__exact=0)
        if self.value() == 'more':
            return queryset.filter(nbrParticipants__gt=0)


class EventAdmin(admin.ModelAdmin):
    def set_Refuse(self, request, queryset):
        rows = queryset.filter(state=False)
        if rows.count() > 0:
            messages.error(request, message=f"{rows} events already refused")
        else:
            rows = queryset.update(state=False)
            if rows == 1:
                message = "One event was "
            else:
                message = f"{rows} events were"
            messages.success(
                request, message="% successfully refused" % message)
    set_Refuse.short_description = 'Refuse'

    actions = [set_Accept, "set_Refuse"]
    inlines = [
        ParticipateInline
    ]
    list_display = (
        'title',
        'category',
        'state'
    )
    ordering = ('title',)
    list_filter = ('state', 'category', ParticipateListFilter)
    search_fields = [
        'title',
        'category'
    ]
    list_per_page = 5

    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (
            'STATE',
            {
                'classes': ('collapse',),
                'fields': (('state', 'category'), ('created_at', 'updated_at'))
            }
        ),
        (
            'ABOUT',
            {
                'fields': (
                    'title',
                    'description',
                    'nbrParticipants',
                    'eventImage',
                    'eventDate',
                    'organizer'
                )
            }
        )
    )


admin.site.register(Event, EventAdmin)
admin.site.register(Participation)
