from django.shortcuts import render
from django.http import HttpResponse
from Beta.inData import makeDataOk
from Beta.outData import calcTableData
from Beta.inData.index import fixIndex
from Beta.outData import groupTickers
import csv

# Create your views here.
def beta(request):
    return render(request, 'Beta/base.html', context=None)

def sendCsvData(request):
    if request.method == "GET":

        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="data.csv"'
        writer = csv.writer(response, delimiter=",")

        timeDelta = request.GET.get("time_delta")
        csv_file_url = "Beta/outData/" + timeDelta + ".csv"
        with open(csv_file_url, "r", encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                writer.writerow(row)

        return response

def dataUpdate(request):
    if request.user.is_superuser and request.user.is_staff and request.user.is_authenticated: # Checks for permission.
        if request.method == "POST": # If request is a post request.
            if request.POST.get("action") == "updateFiles":
                isDone = makeDataOk.updateFiles() # Updates Data.
                if isDone:
                    return HttpResponse(".عملیات با موفقیت انجام شد")
            if request.POST.get("action") == "calcReturn":
                makeDataOk.calcReturn() # Calculates return value for all stocks and wirtes to their csv files.
                return HttpResponse(".عملیات با موفقیت انجام شد")
            if request.POST.get("action") == "createOutput":
                makeDataOk.createOutData()
                return HttpResponse(".عملیات با موفقیت انجام شد")
            if request.POST.get("action") == "makeTable":
                calcTableData.controlAll();
                return HttpResponse(".عملیات با موفقیت انجام شد")
            if request.POST.get("action") == "fixIndex":
                fixIndex.fix()
                return HttpResponse(".عملیات با موفقیت انجام شد")
            if request.POST.get("action") == "groupData":
                groupTickers.controlGrouping()
                return HttpResponse(".عملیات با موفقیت انجام شد")
        return render(request, "Beta/controller.html", context=None)
    return HttpResponse("You don't have permission to access this page.") # If request is Get.

