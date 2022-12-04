<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

<br />
<div align="center">
  <a href="">
    <img src="https://user-images.githubusercontent.com/51291185/205490536-fdd434ef-c655-4b0c-9416-a74f805531e5.png" alt="Logo" width="200">
  </a>

<h3 align="center">Flastagram</h3>

  <p align="center">
    인스타그램 클론코딩
    <br />
    <hr />
    <a href="#프로젝트-소개">소개</a>
    ·
    <a href="#사용-기술">사용 기술</a>
    ·
    <a href="#구성">구성</a>
  </p>
</div>



## 프로젝트 소개

<div align="center">
  <img src="https://user-images.githubusercontent.com/51291185/205490840-a269819a-555c-47c1-8dd6-9ed2fd93d7de.JPG" alt="screenshot" width="400">
</div>

파이썬 마이크로 웹 프레임워크인 **Flask의 학습**과 **프론트엔드, 백엔드의 개념을 이해**하기 위해 인스타그램을 클론 한 프로젝트입니다.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## 사용 기술

<span>
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" />
  <img src="https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens" />
  <img src="https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white" />
  <img src="https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white" />
  <img src="https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E" />
</span>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## 구성


### 백엔드

#### 기능

- `requirements.txt`를 이용한 패키지 관리
- 어플리케이션 팩토리[^applicationfactory] 방식 사용
- 게시물, 댓글, 유저 CRUD
- 이미지 조회와 삭제
- `marshmallow`를 이용한 데이터 검증
- JWT 토큰을 이용한 인증, 인가 처리
- 게시물 목록 페이지네이션


#### 요청 처리 구조

- `api/resources`에서 사용자 요청을 받아 처리
  * `api/schema`나 `api/model`에서 필요한 schema나 model을 import하여 사용
  * `api/model`에서 데이터베이스 이용


### 프론트엔드

#### 기능

- 백엔드의 게시물 API를 이용한 화면 표시
- 무한 스크롤
- access, refresh 토큰을 사용한 로그인
- 로그인 정보(토큰)를 로컬 스토리지에 저장
- 마이페이지 API를 이용한 사용자 정보 조회, 수정

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## 보완할 점

- [ ] 프로젝트 배포

<p align="right">(<a href="#readme-top">back to top</a>)</p>


[^applicationfactory]: app 객체를 생성하는 함수 `create_app()`을 의미

