def language_code(request):
    language_code_m = request.session['django_language']
    return {'language_code': language_code_m}
