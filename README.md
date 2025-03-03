# AWS IAM Manager API

AWS IAM 사용자를 관리하기 위한 FastAPI 기반 REST API입니다.

## 설치 방법

1. 의존성 설치:
```bash

uv venv .venv

uv venv .venv --python=python3.11

source .venv/bin/activate

pip install -r requirements.txt


```

2. 환경 변수 설정:
`.env` 파일에 AWS 인증 정보를 입력하세요:
```
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=ap-northeast-2
```

## 실행 방법

```bash
uvicorn main:app --reload
```

서버는 기본적으로 http://localhost:8000 에서 실행됩니다.
API 문서는 http://localhost:8000/docs 에서 확인할 수 있습니다.

## API 엔드포인트

### 1. IAM 사용자 생성
- POST `/users/`
```json
{
    "username": "new-user",
    "group_names": ["group1", "group2"],
    "policy_arns": ["arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"]
}
```

### 2. IAM 사용자 목록 조회
- GET `/users/`

### 3. IAM 사용자 삭제
- DELETE `/users/{username}` 