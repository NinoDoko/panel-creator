def #Action_Name#(request):
    path = request.get_full_path().replace('#Action_Name#', "", 1)
    return redirect(path)
