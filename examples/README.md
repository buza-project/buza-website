Command to regenerate this data dump:

    django-admin dumpdata -e admin.logentry -e auth.permission -e contenttypes -e sessions --natural-foreign --natural-primary --indent 2 -o example-data.json
