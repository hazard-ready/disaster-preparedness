import csv
from django.http import HttpResponse


def export_as_csv_action(description="Export selected objects in a CSV file", fields=None, model=None):
    def export_as_csv(modeladmin, request, queryset, fields=fields):
        opts = modeladmin.model._meta
        if not fields:
            field_names = [field.name for field in opts.fields]
        else:
            field_names = fields

        if not model:
            model_to_export = modeladmin.model
        else:
            model_to_export = model

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % str(
            opts).replace('.', '_')

        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            queryObject = model_to_export.objects.get(id=obj.id)
            row = []
            for field in field_names:
                if hasattr(obj, field):
                    row.append(getattr(obj, field))
                else:
                    data = getattr(queryObject, field)
                    # If a field is a relation to another model, follow it
                    if hasattr(data, 'all') and callable(getattr(data, 'all',)):
                        data = ', '.join(list(str(x) for x in data.all()))

                    row.append(data)
            writer.writerow(row)
        return response
    export_as_csv.short_description = description
    return export_as_csv
