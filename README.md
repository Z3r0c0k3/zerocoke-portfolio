# 개발자 포트폴리오 웹사이트

Django로 만든 심플하고 모던한 개발자 포트폴리오 웹사이트입니다.

## 기능

- 반응형 디자인 (Bootstrap 5 사용)
- 프로필 섹션
- 기술 스택 표시
- 프로젝트 포트폴리오
- 연락처 정보
- 모던한 UI/UX

## 기술 스택

- **Backend**: Django 5.2.4
- **Frontend**: HTML5, CSS3, JavaScript
- **CSS Framework**: Bootstrap 5
- **Icons**: Font Awesome 6

## 설치 및 실행

1. 저장소 클론

```bash
git clone <repository-url>
cd my-portfoilo
```

2. 가상환경 생성 및 활성화 (선택사항)

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate  # Windows
```

3. 의존성 설치

```bash
pip install django
```

4. 데이터베이스 마이그레이션

```bash
python manage.py migrate
```

5. 개발 서버 실행

```bash
python manage.py runserver
```

6. 브라우저에서 `http://127.0.0.1:8000` 접속

## 프로젝트 구조

```
my-portfoilo/
├── portfolio/          # Django 프로젝트 설정
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── main/              # 메인 앱
│   ├── views.py       # 뷰 로직
│   ├── urls.py        # URL 패턴
│   └── templates/     # HTML 템플릿
│       └── main/
│           ├── base.html
│           └── home.html
├── manage.py
└── README.md
```

## 커스터마이징

### 개인 정보 수정

`main/views.py` 파일의 `home` 함수에서 다음 정보를 수정하세요:

- `name`: 이름
- `title`: 직함
- `description`: 자기소개
- `skills`: 기술 스택 목록
- `projects`: 프로젝트 정보
- `contact`: 연락처 정보

### 스타일 수정

`main/templates/main/base.html` 파일의 `<style>` 섹션에서 CSS를 수정할 수 있습니다.

## 배포

이 프로젝트는 다음과 같은 방법으로 배포할 수 있습니다:

- **Heroku**: `requirements.txt` 파일 추가 후 배포
- **PythonAnywhere**: WSGI 설정 후 배포
- **VPS**: Gunicorn + Nginx 설정 후 배포

## 라이선스

MIT License
