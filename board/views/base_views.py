from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404


from board.models import Question

def index(request):
    return render(request, 'board/index.html')

def boardlist(request):
    #질문 목록
    #question_list = Question.objects.all()  #db 전체조회
    # question_list = Question.objects.order_by('-create_date')#작성일 내림차순

    #페이지 처리
    page = request.GET.get('page', 1)  #127.0.0.1:8000/ 기본 1페이지임
    kw = request.GET.get('kw', '')

    # 조회
    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__username__icontains=kw) |
            Q(answer__author__icontains=kw) |
            Q(answer__content__icontains=kw)
        ).distinct() #유일한것 검색

    paginator = Paginator(question_list, 10) #페이지당 10개씩 설정
    page_obj = paginator.get_page(page)    #페이지 가져오기
    context = {'question_list':page_obj, 'page':page, 'kw':kw}
    return render(request, 'board/question_list.html', context)

def detail(request, question_id):
    # 질문/답변 상세
    # question = Question.objects.get(id=question_id) #해당 id의 질문
    question = get_object_or_404(Question, pk=question_id)
    #경로에 오류가 있을 때 404로 처리(페이지가 없음)
    return render(request, 'board/detail.html', {'question':question})



