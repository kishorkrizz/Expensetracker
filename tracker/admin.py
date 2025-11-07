from django.contrib import admin
from tracker.models import CurrentBalance, TrackingHistory

admin.site.site_header="kishor's Expense Tracker"
admin.site.site_title="kishor's Expense Tracker"
admin.site.site_url="kishor's Expense Tracker"

admin.site.register(CurrentBalance)

#admin.site.disable_action("delete_selected")

@admin.action(description="Make it in Debit")
def make_debit(modeladmin, request, queryset):
    for q in queryset:
        obj = TrackingHistory.objects.get(id=q.id)
        if obj.amount > 0:
            obj.amount = obj.amount * -1
            obj.save()

    queryset.update(expense_type="DEBIT")

@admin.action(description="Mark selected Expenses as Credit")
def make_credit(modeladmin, request, queryset):
    for q in queryset:
        obj = TrackingHistory.objects.get(id=q.id)
        if obj.amount < 0:
            obj.amount = obj.amount * -1
            obj.save()
    queryset.update(expense_type="CREDIT")

class trackinghistoryadmin(admin.ModelAdmin):
    list_display = ('current_balance', 'amount', 'expense_type', 'description', 'created_at',"age")
    search_fields = ('current_balance__current_balance', 'amount', 'expense_type', 'description')
    list_filter = ('expense_type', 'created_at')

    def age(self,obj):
        if obj.amount > 0:
            return "CREDIT"
        
        return "DEBIT"
    actions = [make_credit, make_debit]

admin.site.register(TrackingHistory, trackinghistoryadmin)
