import csv
from django.http import HttpResponse
from .models import UserProfile

def export_as_csv_action(description="Export selected users as CSV file", fields=None):
    def export_as_csv(modeladmin, request, queryset, fields=fields):
        opts = modeladmin.model._meta
        if not fields:
            field_names = [field.name for field in opts.fields]
        else:
            field_names = fields

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % str(opts).replace('.', '_')

        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            user = UserProfile.objects.get(user=obj)
            row = []
            for field in field_names:
                if hasattr(obj, field):
                    row.append(getattr(obj, field))
                else:
                    row.append(getattr(user, field))
            writer.writerow(row)
        return response
    export_as_csv.short_description = description
    return export_as_csv
