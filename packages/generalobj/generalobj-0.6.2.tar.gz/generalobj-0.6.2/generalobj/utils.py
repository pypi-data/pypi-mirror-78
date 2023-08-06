from django.urls import reverse

def get_params_for_search(request, Obj, ObjForm, search_fields, result_fields, \
        relational_obj_values={}, translations={}):
    print('trk = ', translations)
    if not search_fields:
        search_fields = [field.name for field in Obj._meta.fields]
    fields = []
    charfield_exists = False
    datetimefield_exists = False
    booleanfield_exists = False
    for field in search_fields:
        remaining = {}
        remaining['label'] = field
        if field in translations:
            remaining['label'] = translations[field]
        internal_type = Obj._meta.get_field(field).get_internal_type()
        if internal_type in ('IntegerField', 'FloatField', 'DecimalField'):
            fields.append((field, 'number', 'ltgt', remaining))
            charfield_exists = True
        elif internal_type in ('CharField', 'TextField'):
            fields.append((field, 'text', 'text', remaining))
            charfield_exists = True
        elif internal_type in ('DateField', 'DateTimeField'):
            fields.append((field, 'date', 'ltgt', remaining))
            datetimefield_exists = True
        elif internal_type == 'ForeignKey':
            values = []
            if field in relational_obj_values:
                remaining['relational_obj_values'] = relational_obj_values[field]
            fields.append((field, 'relation', 'relation', remaining))
        elif internal_type == 'BooleanField':
            fields.append((field, 'boolean', 'text', remaining))
            booleanfield_exists = True
    print(fields)
    class_name = Obj._meta.object_name
    class_name_lower = class_name.lower()
    ajax_url = reverse('ajax_get_%s_list' % class_name.lower())
    return (fields, class_name, class_name_lower, ajax_url, charfield_exists, \
            datetimefield_exists, booleanfield_exists)