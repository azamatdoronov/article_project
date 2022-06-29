from django.shortcuts import render

# Create your views here.
from game.messages import WIN_MESSAGE
from game.service import Game



def index_view(request):
    if request.method == "POST":
        numbers_str = request.POST.get("numbers")
        nums = numbers_str.split()
        game = Game()
        error = game.validation(nums)
        if error:
            result = error
        else:
            result = game.get_result()
            if result != WIN_MESSAGE:
                Game.stat_list.append(f"Вы ввели {numbers_str}, результат - {result}")
        return render(request, "game.html", {"result": result, "nums": numbers_str, "secret_numbers": game.secret_numbers})
    else:
        return render(request, "game.html")


def get_stat(request):
    return render(request, "stat.html", {"stat_list": Game.stat_list})
