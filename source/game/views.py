from django.shortcuts import render

# Create your views here.
from game.service import Game


def index_view(request):
    if request.method == "POST":
        numbers_str = request.POST.get("numbers")
        nums = numbers_str.split()
        print(nums)
        game = Game()
        error = game.validation(nums)
        if error:
            result = error
        else:
            result = game.get_result()
        return render(request, "game.html", {"result": result, "nums": numbers_str})
    else:
        return render(request, "game.html")


def get_stat(request):
    pass
