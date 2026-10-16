# 경로 및 파일 확인 명령어 
- pwd 현재 위치 확인 / ls -a 숨김 파일 포함 목록  / ls -R 하위 폴더까지 확인
- cd .. 상위 폴더 / cd ~ 홈 디렉터리 / cd $MYHOME 실습 홈으로 이동 
   → Python으로 옮길 필요 없음: 현재 위친 확인 및 파일 목록 확인, 폴더 구조 확인은 Bash 명령어로 사용하는 것이 편리함
- mkdir A 폴더 생성 
  → Python: os.mkdir("A") 폴더 생성 
- mkdir -p A/B/C 중간 폴더까지 한 번에 생성
  → Python: os.makedirs("A/B/C") 중간 폴더까지 모두 한 번에 생성가능하다.
    예) mkdir -p prob03/A/C/D 
- touch a.txt 빈 파일 생성 / rm a.txt 파일 삭제 / rm -r A 폴더와 내부 삭제 
   → Python으로 옮길 필요 없음: 파일 생성 및 파일 삭제, 폴더 삭제는 Bash 명령어로 처리 가능
※ 현재 위치가 prob03이면 cd prob03/A가 아니라 cd A처럼 상대경로 사용(헷갈린 것)

# 출력 및 리다이렉션과 파이프
- '>' 화면 출력을 파일에 새로 저장 / '>>' 기존 내용 뒤에 추가 / '2>' 오류 메시지만 저장
- ls xyz > doc/err.txt 정상 출력은 파일로, 오류 출력은 화면에 남음
- 명령어1 | 명령어2 앞 명령어의 출력을 뒤 명령어의 입력으로 전달
  → Python으로 옮길 필요 없음: Bash에서 더 간단하게 처리할 수 있음
예: grep -v ">" data/*.fasta | wc -l

# grep 및 문자열 처리
- grep ">" file 특정 문자열 검색 
  → Python: if ">" in line: 특정 문자열 포함 여부 확인
-c 개수 → Python: count = count + 1 조건에 맞는 개수 세기
-n 줄 번호 → Python으로 옮길 필요 없음: 현재 배운 내용에서는 직접 대응할 필요가 없음
-i 대소문자 무시 → Python: line.lower() 소문자로 변환하여 비교

- grep -v ">" file 조건에 맞지 않는 줄 출력 → Python: if not line.startswith(">"):
- grep -h 파일명 출력 생략                 → Python으로 옮길 필요 없음: Python에서 파일을 읽으면 파일명이 자동으로 출력되지 않음

- cut -d":" -f1 file 구분자로 나누어 원하는 영역 추출
  → Python: line.split(":")[0]
- tr -d "\n" 줄바꿈 제거 / tr -s " " "\n" 연속 공백을 줄바꿈으로 변환(-s옵션 : 연속된 마지막 문자를 하나로 압축)
  → Python: line.rstrip()
- wc -l 줄 수         → Python: len(lines) 줄 개수 세기
- wc -c 문자 수 계산  → Python: len(text) 문자 수 세기 
  예: tr -d "\n" < data/seqs.fasta : 특정 문자 제거

# 와일드 카드 및 권한
- *.fasta 모든 .fasta 파일 / seq*.fq seq로 시작하는 .fq 파일
- *는 모든 문자대체, ?은 1개의 문자대체, []는 대괄호의 문자 하나씩 대체 
   → Python: grob.grob("data/*.fasta")
- chmod 700 file.sh 소유자에게 읽기·쓰기·실행 권한 부여/r은 4, w는 2, x는 1을 나타냄
   → Python으로 옮길 필요 없음: Bash에서 실행 권한을 설정함
  예: chmod 700 src/countseq.sh : 스크립트 실행 권한 부여

# 변수 및 인자
- A=hello 변수 저장        → Python: A = "hello" 변수 저장
- echo "$A" 변수 값 출력   → Python: print(A) 변수 값 출력
- 공백이 있으면 따옴표 사용 → Python: 문자열을 나타날 때따옴표로 작성
  큰따옴표는 공백유지역할, 작은따옴표는 문자 그대로 출력

- $0 실행한 스크립트 이름     → Python: sys.argv[0] 
- $1, $2 첫 번째·두 번째 인자 → Python: sys.argv[1], sys.argv[2]
- $# 인자 개수                → Python: len(sys.argv) - 1
- N=$(grep -c ">" "$F") 명령어 실행 결과를 변수에 저장
  ※ N=grep -c ">" "$F"는 명령어 결과 저장이 아니므로 $( )가 필요 
   → Python: '변수 = 함수식' 형태로 별 다른 기호 없이 변수를 저장 가능
  예: echo "사용법: $0 <파일>" : 스크립트 이름 $0 사용

# 조건문 및 반복문
- if [ -z "$1" ] 인자가 비어 있는지 확인        → Python: if len(sys.argv) < 2:
- if [ ! -f "$1" ] 파일 존재 여부 확인          → Python:if not os.path.isfile(file_name):
- exit 1 오류로 스크립트 종료                   → Python: sys.exit(1)
  성공적인 명령어의 종료 상태는 0, 0이 아니면 성공한 명령어가 아님
- for F in data/*.fasta; do ... done 여러 파일을 반복 처리 
   → Python: for문의 조건식 뒤에 콜론을 쓰고, 들여쓰기 되어있는 부분을 반복 처리
- set -x 실행되는 명령어를 추적하여 디버깅
- echo $? 직전 명령어의 종료 상태 확인 
  → Python으로 옮길 필요 없음: Bash의 디버깅과 종료 상태를 확인하는 방법이 간편하기 때문이다.
  예: if [ ! -d "$1" ] 폴더 존재 여부 확인

# Bash 스크립트 5단계
1. 터미널에서 실행할 명령어들을 미리 실행해서 정상적으로 실행되는지 확인한다.
   → Python: 대화형 파이썬에서 코드를 먼저 실행해 본다.
2. 터미널에서 실행한 명령어를 그대로 스크립트로 옮긴후 실행권한 부여 및 shebamg 작성 후 스크립트를 실행한다.
   → Python: 대화형 파이썬에서 실행한 코드를 그대로 파이썬 스크립트로 옮기고 실행권한 부여 및 shebang을 작성해서 스크립트를 실행해본다. 
3. 계속 바뀔 변수를 기존 파일 또는 폴더를 대신해서 대체한다.
   → Python: 동일(바뀔 변수를 기존에 있는 파일이나 폴더 대신으로 대체)
4. 변수의 값은 $!, $2와 같은 명령행인자로 변경한다.
   → Python: 변수의 값은 sys.argv[1], sys.argv[2]와 같은 인자로 변경한다.
5. 명령어를 잘못실행해도 안전하기 위해서 조건문을 활용해 인자나 파일을 검사하는 부분을 넣는다. 
   → Python: 동일(조건문 검사)

# 내가 실제로 틀렸던 것
- N=grep ...처럼 작성 → N=$(grep ...)로 수정
  → Python : 'N = 결과'처럼 결과를 변수에 저장한다.
- for의 do와 done을 빠뜨려 unexpected end of file 발생
  → Python : for 뒤에 :을 쓰고 들여쓰기를 한다.
- 반드시 $1변수를 큰따옴표로 감싸야 문자처럼 취급하는 줄 착각 → 큰따옴표는 공백유지역할
  → Python : 문자열로 표현 시 따옴표를 사용하며 공백도 유지한다.
- grep -v ">" src/*seqs*.fasta | .. → 와일드카드 사용 시 파일이름과 해당 줄이 같이 출력되어 파아프를 통해 넘어감/글자수 셀 때 주의
  → Python : 파일을 직접 읽고 필요한 줄만 선택할 수 있어 파일명이 같이 출력되지 않음
- ./ 없이 스크립트를 실행하는 것과 src/script.sh 경로를 정확히 구분하기 
  → Python : 동일하게 명령어로 실행시 경로 정확히 표기해야함.

# 07. 파이썬 함수와 파일 저장
  1. def로 함수 만들기
     - def 함수 이름(매개 변수) : 형태로 함수를 정의한다.
     - 함수 내부의 코드는 들여쓰기를 통해 나타내고, return을 사용해 결과를 반환할 수 있다.
       return은 반드시 필요한 것이 아니며 지정하지 않을 경우 None을 반환한다.
     - 사용법 예시)
       def gc_content(seq):
           gc = seq.count("G") + seq.count("C")
           return gc / len(seq)


  2. print와 return의 차이
     - print()는 결과를 화면에 출력한다. 
     - return은 함수의 결과값을 호출한 쪽으로 돌려주며, print()와 달리 화면에 직접 출력하지는 않는다.
     - print()함수만 함수 내부에 있고 return을 지정하지 않은 경우
       변수에 함수를 호출하여 지정하고 변수를 print하면 None이 출력된다.

  3. 다른 모듈에서 함수 불러오기 
     - 방법 1 : 특정함수만 불러오기
       형태 : from 모듈이름 import 함수이름
       다른 파이썬 파일에 저장된 함수를 불러와 사용 가능하다. 
       사용법 예시 )
       from fasta import gc_content
       gc = gc_content("ATGC")

     - 방법 2 : 모듈을 불러오기
       형태 : import 모듈이름
       모듈이름으로 불러온 뒤에 함수 사용 시 모듈과 그 모듈 안에 있는 함수이름을 .으로 연결해서 사용한다.
       사용법 예시 ) 
       import fasta
       gc = fasta.gc_content("ATGC")

  4. `if __name__ == "__main__":`
     - 파이썬 파일을 직접 실행했을 때만 특정 코드를 실행하고,
       다른 파일에서 import할 때는 실행되지 않도록 하기 위해서 추가하는 코드이다.
     - 주로 함수를 시험하는 코드를 작성할 때 사용한다.

     사용법 예시 ) tool.py
     `if __name__ == "__main__":`
        print("테스트 출력입니다")

     bash shell에서 'python3 tool.py'로 직접 실행한 경우 → 테스트 출력입니다.
     (tool.py에 위 예시 코드를 저장했다고 가정)

  5. 파일 저장 모드 "w"와 "a"
     - "w" : 파일을 새로 작성하고, 기존 파일이 있으면 내용을 덮어쓴다. Bash의 >와 같은 역할을 한다.
     - "a" : 기존 파일의 끝에 새로운 내용을 추가한다. Bash의 >>와 같은 역할을 한다.

     사용법 예시)
     with open("result.txt", "w") as out:
        out.write("Hello\n")

  6. 오늘 겪은 오류 두가지
    
    1. IndentationError
       - 오류가 발생한 상황 : fasta.py의 __main__부분에 역상보서열을 두 번 구할 경우 원래 코드로 돌아오는지에 대한
                             검증 코드를 추가한 후 'python3 fasta.py ../data/seqs.fasta'를 실행했을 때,
                            53번째 줄의 for name in seqs:에서 오류가 발생하였다.
       - 오류 원인 : for name in seqs:의 들여쓰기가 앞의 코드 블럭과 일치하지 않아서 
                    'IndentationError: unindent does not match any outer indentation level' 오류가 발생하였다.
       - 해결 방법 : `if __name__ == "__main__":` 의 내부 들여쓰기 수준을 모두 확인하고
                     for문을 다른 for문과 동일하게 공백 4칸으로 들여쓰도록 수정하였다.

    2. SyntaxError
       - 오류가 발생한 상황 : 대화형 파이썬에서 reverse_complement() 함수를 실행하기 위해
                            'a = reverse_complement seqs.fasta'라고 입력하였을 때 오류가 발생하였다.
       - 오류 원인 : 파이썬에서 함수를 호출할 때는 함수 이름 뒤에 괄호를 활용해서
                    원하는 입력 인자를 전달해야한다. 그러나 bash에서 함수와 인자를 공백으로 구분하였던 것과 헷갈려
                    괄호로 인자를 입력하지 않고 공백으로 입력하였다.
       - 해결 방법 : 함수 이름 뒤에 괄호를 추가하고 인자를 괄호 안에 입력해서 전달하였다.
                    'a = reverse_complement("ATGC")'와 같이 작성하여 제대로 실행하였다.