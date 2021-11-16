from django.db import models
from account.models import CustomUser


# 모델클래스 정의 -> admin.py 에 등록(관리자 앱에서 관리가 가능.)
#   python manage.py makemigrations
#   python manage.py migrate

# Category
#   게시글의 카테고리
#   category_code: PK, 자동증가 정수
#   category_name: varchar, 카테고리 이름
class Category(models.Model):
    # Model Field(테이블 컬럼) 클래스 변수 선언
    # PK - primary_key=True
    # AutoField: 1씩 자동증가하는 정수형 컬럼
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=200, verbose_name="카테고리")
    # verbose_name: 이 필드가 화면에 나올 때 사용할 Label 값 (등록/수정/조회 시 보여질 label값.)

    def __str__(self):
        return f"{self.category_id}. {self.category_name}"

    class Meta:
        ordering=["category_id"]  # 기본 정렬방식 지정

# 게시글
# id(pk-자동생성), title(글제목), content(글내용), category(글카테고리), create_at(처음등록일시), update_at(글수정일시) + writer(작성자-로그인한 사용자 pk), up_file, up_image(업로드된 파일/이미지파일 정보)
class Post(models.Model):
    # 글작성자 : 글쓴 사용자의 PK -> CustomUser를 Foreign Key로 참조.
    writer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='작성자')

    title = models.CharField(max_length=255, verbose_name="글 제목")  # NOT NULL -> Null(None), 빈문자열은 허용 안함.
    content = models.TextField(verbose_name="글 내용")  # TextField: 대용량 Text
    # on_delete=models.CASCADE : 참조하는 부모테이블의 값이 삭제되면 자식테이블의 값도 삭제
    # on_delete=models.SET_NULL : 참조하는 부모테이블의 값이 삭제되면 자식테이블의 foreign key 컬럼을 NULL 로 변경. -컬럼이 nullable
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    # null=True: nullable 컬럼, black=True: 빈문자열을 값으로 가질 수 있다.(blank는 폼 검증과 관련)
    create_at = models.DateTimeField(verbose_name="작성일시", auto_now_add=True)  # auto_now_add=True: insert할 때 일시를 자동으로 입력.
    update_at = models.DateTimeField(verbose_name="수정일시", auto_now=True)  # auto_now_add=True: insert/update할 때 일시를 자동으로 입력.

    ######################################################
    # 업로드 파일 저장을 위한 Field를 추가.
    ######################################################
    up_file = models.FileField(verbose_name='업로드파일', upload_to='files',  # MEDIA_ROOT/files 디렉토리에 저장. 
                               null=True, blank=True)  # 업로드된 일반파일(모든파일)을 위한 model Field
    up_image = models.ImageField(verbose_name='업로드이미지', upload_to='images/%Y_%m_%d',  # MEDIA_ROOT/images/2021_10_19/ 저장.
                                null=True, blank=True)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']


# create table post(
#     id number primary key, --sequence를 이용해서 자동증가
#     title nvarchar(255) not null,
#     content text not null,
#     category number,

#     constraint p_c_fk foreign key(category) reference Category on delete set null
# )