비전공자를 위한 FastAPI 백엔드 서버 기초 과제 프로젝트

**파일 구조**
auth.py - 비밀번호 해싱, 해독, JWT토큰 생성 등 Authentication과 관련된 모든 함수가 들어있음
main.py - entry point, 각 APIRouter 집합체. Lifespan 기능을 활용하여 앱 실행 시 init_db() 함수를 불러와 DB 생성

**login.html**
유저 로그인 & 회원가입 기능 있음.
회원가입은 '비밀번호'와 '비밀번호 확인' 입력란이 일치하여야 하며, 유저네임이 기존 유저와 겹치지 않아야 함 (DB와 대조)
로그인 관련 기능들은 *web/user.py* -> *service/user.py* -> *data/user.py* 순서로 로직이 실행되며, 
결과값은 다시 *web/user.py*로 돌아와 클라이언트에게 HTTPException 또는 결과 값 디스플레이로 나타난다

**index.html**
유저 개인 페이지 - 냉장고 음식 재고를 보여주며, 음식을 추가/제거/수량 조정을 할 수 있다.
*create.html*, *delete.html*, *fridge.html*은 각각 추가, 제거, 재고 확인 및 수정을 맡는 모듈들로 *index.html*에서 불러온다.
냉장고와 관련된 논리는 *web/fridge.py*, *service/fridge.py*, *data/fridge.py*에서 관장.

**SQLite 데이터베이스 구조**
- user table -> name, email (Default = None), hashed_password
- refrigerator table -> food_name, quantity, user (`FOREIGN KEY -> REFERENCES user(name)`)
추가로, `ON DELETE CASCADE` 스테이트먼트로 유저 정보가 없어지면, 유저의 냉장고에 포함되어 있던 음식 데이터도 모두 사라지게 하였다.
user 행을 추가하였기 때문에, *fridge.py*에서 실행되는 모든 코드는 기존 Food 모델에 user 값을 추가로 전달하도록 하였다
