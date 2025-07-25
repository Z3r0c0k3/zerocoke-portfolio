# Modern Developer Portfolio

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Django**로 제작된 동적이고 현대적인 개발자 포트폴리오 웹사이트입니다. 모든 콘텐츠는 **Django 관리자 페이지**를 통해 손쉽게 관리할 수 있으며, 실제 서비스 환경에 바로 배포할 수 있도록 설계되었습니다.

![Portfolio Screenshot](https://i.imgur.com/B7hEkZP.png)

---

## ✨ 주요 기능

- **100% 관리자 페이지 기반 콘텐츠 관리**: 프로필, 기술, 프로젝트, 학력, 자격증 등 모든 정보를 코드를 건드리지 않고 관리자 페이지에서 추가/수정/삭제할 수 있습니다.
- **동적 배경 그라데이션**: 시선을 사로잡는 움직이는 그라데이션 배경
- **반응형 디자인**: 데스크탑, 태블릿, 모바일 등 모든 기기에서 최적화된 UI 제공
- **듀얼 테마 (다크/라이트)**: 사용자의 선택을 기억하는 동적 테마 전환 기능 (기본: 다크)
- **보안 강화**:
  - `.env` 파일을 이용한 민감 정보 (비밀 키, 관리자 URL 등) 분리
  - 지정된 IP에서만 관리자 페이지에 접근 가능하도록 제한
- **운영 환경 준비 완료**: `Gunicorn`과 `Whitenoise`를 사용하여 실제 서버 환경과 동일하게 실행 가능

## 🛠️ 기술 스택

- **Backend**: Python, Django
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **WSGI Server**: Gunicorn
- **Static Files**: Whitenoise
- **Icons**: Font Awesome 6
- **Dependencies**: `django-environ`

## 🚀 설치 및 실행

### 1. 프로젝트 클론

```bash
git clone https://github.com/your-username/my-portfoilo.git
cd my-portfoilo
```

### 2. 가상환경 생성 및 활성화

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows
```

### 3. 의존성 패키지 설치

정제된 `requirements.txt` 파일을 사용하여 프로젝트에 필요한 패키지만 설치합니다.

```bash
pip install -r requirements.txt
```

### 4. `.env` 파일 설정

프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 아래 내용을 참고하여 자신의 환경에 맞게 수정합니다.

```env
# .env

# Django Core Settings
SECRET_KEY='django-insecure-your-super-secret-key'
DEBUG=True

# Admin Page Security Settings
ADMIN_URL='pf-admin/' # 원하는 관리자 페이지 주소 (예: my-secret-admin/)
ALLOWED_ADMIN_IPS='127.0.0.1,::1' # 관리자 페이지에 접속할 IP (쉼표로 구분)

# Superuser Auto-creation Settings
SUPERUSER_USERNAME='admin'
SUPERUSER_EMAIL='admin@example.com'
SUPERUSER_PASSWORD='your-strong-password'
```

### 5. 데이터베이스 마이그레이션

```bash
python3 manage.py migrate
```

### 6. 관리자 계정 생성

`.env` 파일에 기입된 정보로 관리자 계정을 자동으로 생성합니다.

```bash
python3 manage.py createsuperuser_from_env
```

### 7. 개발 서버 실행

```bash
python3 manage.py runserver
```

이제 브라우저에서 `http://127.0.0.1:8000` 로 접속하여 포트폴리오를 확인하고, `http://127.0.0.1:8000/설정한ADMIN_URL/` 로 접속하여 콘텐츠를 관리할 수 있습니다.

---

## ⚙️ 운영 서버로 실행하기 (Gunicorn)

`DEBUG=False` 상태에서의 동작을 로컬에서 확인하거나 실제 서버처럼 실행할 수 있습니다.

### 1. `portfolio/settings.py` 수정

- `DEBUG` 값을 `False`로 변경합니다.
- `ALLOWED_HOSTS`에 자신의 도메인이나 `['*']`를 추가합니다.

### 2. 정적 파일 수집

```bash
python3 manage.py collectstatic --noinput
```

### 3. Gunicorn 실행

```bash
# macOS에서는 아래 명령어를 사용하세요.
OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES gunicorn portfolio.wsgi

# Linux 등 다른 환경에서는 아래 명령어를 사용하세요.
gunicorn portfolio.wsgi
```

## ✒️ 콘텐츠 관리 가이드

1. **프로필**: `[ADMIN_URL]/main/profile/`
   - 이름, 직함, 소개를 작성합니다.
   - **Links**: 하단 네비게이션 바에 표시될 소셜 링크(Github, LinkedIn 등)와 이메일(`mailto:your@email.com`)을 추가합니다.
2. **기술**: `[ADMIN_URL]/main/skill/`
   - 보유 기술 스택을 추가합니다.
3. **학력**: `[ADMIN_URL]/main/education/`
   - 학력 사항을 추가합니다. `end_date`를 비워두면 '현재'로 표시됩니다.
4. **프로젝트**: `[ADMIN_URL]/main/project/`
   - 진행한 프로젝트 정보를 추가합니다. `end_date`를 비워두면 '현재'로 표시됩니다.
   - **Links**: 프로젝트와 관련된 Github, Demo, Blog 링크 등을 추가할 수 있습니다.
5. **자격증/수상**: `[ADMIN_URL]/main/certification/`
   - 취득한 자격증이나 수상 내역을 추가합니다.

## 📄 라이선스

이 프로젝트는 [MIT License](LICENSE)를 따릅니다.
