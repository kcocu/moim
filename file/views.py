from django.shortcuts import render, HttpResponse

from .forms import UploadFileForm

# Create your views here.
def upload(request):
    if request.method == 'POST':
        upload_files = request.FILES.getlist('file') #객체-리스트
        result = ''
        for upload_file in upload_files:
            name = upload_file.name #이름
            size = upload_file.size #저장
            with open(name, 'wb') as file: #파일 저장
                for chunk in upload_file.chunks(): 
                    file.write(chunk)
            result += '%s<br>%s<hr>' % (name, size)
        return HttpResponse(result)
    return render(request, 'file/upload.html')



def upload_f(request): #form활용 불러오려면 이걸로
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploadFile = form.save()
            # uploadFile = form.save(commit=False)
            name = uploadFile.file.name
            size = uploadFile.file.size
            return HttpResponse('%s<br>%s' % (name, size))
    else:
        form = UploadFileForm()
    return render(
        request, 'file/upload_f.html', {'form': form})




