## 데이터로 선거하자 프로젝트

#### url - [dvote 홈페이지](https://dvote.kr)

_____

### 소개
- 유저들이 원하는 모드를 선택하여 다가오는 총선에서 당선될 후보를 예측하는 플랫폼
- 이지모드와 하드모드로 나뉜다.
- 이지모드는 powerbi를 사용 하드모드는 주피터 노트북 파일인 ipynb 형식의 템플릿을 사용한다.
- 하드모드는 유저들의 커스텀 db셋을 사용할수 있도록 한다. ex) csv파일
 
_____
 
### 목적
- django를 이용한 api로 사용자들의 요청을 받은 스프링에서 다시 요청을 받아 db에 반영할수 있도록 한다.

_____

### 사용기술
    - Python, Django, Djnago-rest-framwork, nbconvert, ipython, after-response
    
_____

### 구현

![dvote_모식도](https://user-images.githubusercontent.com/58219293/81810503-044f6d00-955e-11ea-838b-2679fdfa7809.png)


1. python 의 subprocess를 통하여 모든 과정을 제어함

2. ipynb -> python 파일로 변환
    - nbconvert 패키지를 통해 ipynb -> python 변환

3. 변환된 python 파일을 실행
    - 실행시 조건
        - 실행시 위험한 단어를 설정하고 해당 단어가 있는경우 파일 실행을 하지 않는다.
    - 성공적 실행
        - logs.txt 에 성공메시지를 저장하고 db에 반영
    - 비정상적 실행
        - logs.txt 에 터미널에 출력된 오류를 저장

_____



