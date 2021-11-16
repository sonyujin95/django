# board/views.py
from django.core import paginator
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, ListView
from django.urls import reverse_lazy  # urls.py에 등록된 path의 이름으로 url을 만들어서 반환하는 함수

# 함수형 View에 설정할 decorator : 로그인 여부를 체크해서 로그인 안된 상태에서 요청 시에 settings.py의 LOGIN_URL의 URL로 이동.
from django.contrib.auth.decorators import login_required

# 클래스의 메소드에 decorator를 선언할 수 있도록 도와주는 class decorator
from django.utils.decorators import method_decorator

# 요청한 로그인한 사용자의 User 모델 객체를 반환. View에서 로그인한 사용자의 정보를 조회할 때 이 함수를 이용하면 간단하게 적용할 수 있다.
from django.contrib.auth import get_user  

from .models import Post
from .forms import PostForm


# 1개 게시물을 조회한 View
# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'board/post_detail.html'

# def detail_view(request, pk):
#     post = Post.objects.get(pk=pk)
#     return render(request, 'board/post_detail.html', {'object':post})

# 글을 등록하는 View
#   1. 등록폼 제공-GET, 2. 등록처리-POST
#   insert 작업처리하는 View -> CreateView를 상속해서 정의

# 사용자 요청 -> dispatch()-get요청-get()
#                          -post요청->post()
@method_decorator(login_required, name="dispatch")  # dispatch() 메소드(view시작)에 login_required 데코레이터를 적용
class PostCreateView(CreateView):
    template_name = "board/post_create.html"  # 입력 폼 - GET 방식 요청일 경우 이동할(render) template
    form_class = PostForm  # 등록 시 사용할 Form 클래스 설정.
    # success_url = reverse_lazy("board:detail")  # 등록 처리 후 이동할(redirect) url 등록

    # redirect() 할 url을 만들 때
    #   단순히 urls.py에 path 이름만 사용할 경우: success_url에 등록
    #   insert/update한 model객체의 속성값을 path 파라미터로 전송해야 하는 경우: get_success_url() 을 overriding
    #   url 생성: reverse_lazy() 사용 (reveser()는 함수형 View에서만 사용.)
    def get_success_url(self):
        return reverse_lazy('board:detail', args=[self.object.pk])
        # self.object : insert된 Model 객체

    def form_valid(self, form):
        """
        - form_valid() : CreateView/UpdateView에 정의된 메소드.
        - POST방식으로 요청이 들어왔을 때 요청파라미터를 검증(is_valid())한 뒤에 호출되는 메소드로
        요청파라미터들을 DB에 insert/update 처리를 한다.
        - 요청파라미터들을 저장하기 전이나 후에 추가적으로 처리해야 할 것이 있으면 overriding한다.
        - 글 등록 시 사용자가 입력한 글제목, 내용, 카테고리에 글을 작성한 로그인한 사용자의 CustomUser모델을 writer에 넣는 작업을 추가.

        [매개변수]
            form : 요청파라미터 검증을 통과한 값들을 가진 ModelForm

        ModelForm 객체의 모델 Field 조회
            - ModelForm객체. cleaned_data 속성 : 딕셔너리
        ModelForm 객체의 모델 Field 값들을 변경
            - ModelForm을 Model로 변경 후에 처리.
            - ModelForm객체.save([commit=False]) : insert/update 후의 Model객체. commit=False를 지정하면 실제 디비에는 적용되지 않는다.
        """
        # form : title, content, category <- writer를 추가.
        # print('------------------',form.title)
        # dict = form.cleaned_data
        # print('------------------',type(dice))
        # print(dict, dict['title'])

        # CreateView : 임시로 insert
        post_model = form.save(commit=False)  # ModelForm의 요청파라미터를 연결된 Model을 이용해서 insert(CreateView)/update(UpdateView) : 모델객체 반환
        # GenericView 메소드에서 HttpRequest 객체 사용 : self.request로 호출
        post_model.writer = get_user(self.request)  # 로그인한 사용자를 조회해서 모델의 writer에 추가.
        # post_model.save()  # update and commit 처리 => super 처리
        return super().form_valid(form)  # form.save()


# 글 수정처리 View
# 1. 수정 Form(수정할 내용을 입력받는 Form) 제공-GET, 2. 수정 처리-POST.
#   update 작업을 처리 -> UpdateView를 상속해서 정의
@method_decorator(login_required, name="dispatch")
class PostUpdateView(UpdateView):
    template_name = 'board/post_update.html'  # 수정 폼을 제공하는 template의 경로
    form_class = PostForm
    model = Post  # UpdateView: form_class, model 두가지 다 설정.
                  # model: GET 요청 시에 수정할 데이터를 조회해서 넘겨주기 위해 model을 설정.

    def get_success_url(self):
        # 수정 처리 후 redirect 방식으로 이동할 url을 반환
        #   - 수정된 글 상세를 보여주는 페이지로 이동.
        #   - self.object: update된 Model객체.
        return reverse_lazy('board:detail', args=[self.object.pk])


# 글삭제 처리 View
# CBV - DeleteView 상속 - template_name="삭제확인페이지" (GET), success_url="삭제 후 이동할 View url" (POST)
@login_required  # 함수형 View는 login_required 데코레이터를 직접 적용한다.
def delete_post(request, post_id):
    """
    path 파라미터로 삭제할 게시물의 id를 받아서 삭제처리
    """
    post = Post.objects.get(pk=post_id)
    post.delete()
    return redirect("/")  # 삭제 후 home으로 이동

# 글 목록
# ListView를 상속해서 구현
# Post.objects.all() 전체 조회를 한 뒤에 그것을 template_name의 페이지로 context_data(name: object_list, post_list)로 전달.
# 
# paginate_by 설정 - 페이징 처리 => Paginator 객체를 생성해서 context data로 저장
# 페이지번호 링크처리를 위한 값들을 context data의 Paginator 객체를 이용해 추출한 뒤 template에게 전달.
class PostListView(ListView):
    template_name = "board/post_list.html"  # 목록페이지 (응답페이지)
    model = Post  # 데이터를 조회할 Model 클래스
    paginate_by = 10 # 한번에 10개씩만 조회
    # {"object_list":Post.objects.all(), "Paginator":PN()}
    # context data : view가 template에게 전달하는 값들을 모아논 dictionary
    # get_context_data() 메소드 : Generic View에 정의된 메소드.
    #                   View Class들이 생성해서 전달하는 context data이외에 추가적으로 전달할 값이 있을 경우 overriding 한다.
    # 페이징관련 추가할 context data
    # - 이전/다음 페이지 그룹 유무
    # - 이전/다음 페이지 번호
    # - 현재 페이지가 속한 페이지 그웁의 페이지 범위
    
    def get_context_data(self, **kwargs):
        # 부모클래스에 정의된 get_context_data() 호출. 반환: Context Data 딕셔너리 반환
        # ListView : paginate_by를 설정하면 paginator:Paginator객체를 등록해서 제공.
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_group_count = 10  # 한 페이지그룹당 페이지 수
        # HttpRequest 객체조회: self.request
        current_page = int(self.request.GET.get('page', 1))  # 사용자 요청한 페이지 번호(?page=번호 : 이값을 조회)

        # 현재 페이지가 속한 페이지 그룹의 페이지 범위(index: pn.page_range)
        start_idx = int((current_page-1)/page_group_count)*page_group_count
        end_idx = start_idx + page_group_count
        page_range = paginator.page_range[start_idx:end_idx]  # page_range : 전체 페이지를 기준으로 시작 ~ 끝 페이지

        # 이전/다음 페이지 그룹이 있는지 여부, 이전/다음 페이지번호
        # 현재 페이지가 속한 page group이 이전페이지(그룹)이 있는지 => page group의 시작페이지/마지막페이지 기준으로 찾는다.
        start_page = paginator.page(page_range[0])  # 시작페이지의 Page 객체
        end_page = paginator.page(page_range[-1])  # 마지막페이지의 Page 객체

        has_previous = start_page.has_previous()  # 시작페이지의 이전페이지가 있는지. (True: 이전페이지그룹이 있다.)
        has_next = end_page.has_next()  # 마지막페이지의 다음페이지가 있는지. (True: 다음페이지그룹이 있다.)

        # 조회결과를 context data에 추가. => super().get_context_data(**kwargs)에서 리턴받은 context data 딕셔너리에 추가.
        context['page_range'] = page_range
        if has_previous:  # 이전페이지 그룹이 있다면
            context['has_previous'] = has_previous
            context['previous_page_no'] = start_page.previous_page_number()  # 시작페이지의 이전페이지 번호

        if has_next:  # 다음 페이지 그룹이 있다면
            context['has_next'] = has_next
            context['next_page_no'] = end_page.next_page_number()  # 마지막페이지의 다음페이지 번호

        return context  # overrding한 메소드에서 리턴한 context data dictionary가 template에 전달.
