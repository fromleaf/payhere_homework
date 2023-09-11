# 사전 준비
이 프로젝트를 실행하기 위해 아래의 환경설정이 필요합니다.
1. python 3.11.4 환경이 설치되어 있어야 함
2. docker가 실행될 수 있는 환경이 설정되어 있어야 함

# Requirement

1. install packages
```
$ pip install -r requirements.txt
```

# docker 실행 방법

1. docker-compose build
```
$ docker-compose -f docker-compose.yml build
```

2. docker-compose up
```
$ docker-compose -f docker-compose.yml up -d
```

3. docker container 확인
```
$ docker ps
```

# 실행 방법
아래 내용들은 docker 실행 후 진행해주세요.

## Swagger에서 signup API 사용해보기
1. Swagger(http://localhost/swagger) 접속
2. /accounts/signup/ API 선택
3. [Try it out] 버튼 클릭
4. cellphone, password, name 항목 입력
5. [Execute] 버튼 클릭

## Database 확인
1. database docker container 접속
```
docker exec -it payhere_homework-database-1 /bin/bash
```
2. MySQL 접속 (password는 12345)
```
mysql -u root -p
```
3. 'payhere' scheme 생성 확인
```
SHOW DATABASES;
```
4. 'payhere' scheme 선택 
```
USE payhere;
```
5. Table 생성 확인 
```
SHOW TABLES;
```
6. (만약 signup API로 사용자를 등록했다면) accounts_user table 확인
```
SELECT * FROM accounts_user;
```

## TestCase 실행 하기

각 TestCase에 대한 설명은 각각의 app > tests > test_{test case name}.py 의 코드를 참고해주세요.

1. database docker container 접속
```
docker exec -it payhere_homework-payhere-server-1 /bin/bash
```
2. 전체 TestCase 실행 하기
```
python manage.py test
```
3. Accounts TestCase 실행 하기
```
python manage.py test accounts
```
4. Products TestCase 실행 하기
```
python manage.py test products
```
# 참고

## 폴더 구조 설명
* accounts: 사용자(User) App
* deploy: docker 실행을 위해 필요한 폴더
  * nginx.conf: nginx 서버 운영을 위한 설정 파일
  * wait-for-it.sh: 
    * 특정 서버의 특정 포트로 접근할 수 있을 때까지 기다려주는 스크립트
    * docker service 실행시, 다른 service가 실행될 때까지 기다린 후 실행되도록 함
* payhere: payhere_homework 서버 설정 파일 및 공통으로 사용되는 파일들을 저장
  * constants: 상수, 메시지 등을 정의한 파일들을 저장
  * core: exception, pagination, permissions와 같이 재정의되거나 공통으로 사용되는 파일들을 저장
  * settings: 각 실행환경별 Django settings 파일들을 저장
  * utils: util 함수들이 구현된 파일들을 저장
* products: 상품(Product) App

## 초성검색 기능 구현 설명
초성 검색로직은 아래와 같습니다.

1. 상품 등록 또는 업데이트 API 요청
2. 상품 정보 저장 전, 상품 이름의 초성 추출
3. 상품 이름의 초성을 Product.name_to_choseong에 저장

위의 코드는 Product model의 pre_save_product에서 확인하실 수 있습니다.
초성 추출을 위해 jamo(https://pypi.org/project/jamo/) 라이브러리를 사용했습니다.

