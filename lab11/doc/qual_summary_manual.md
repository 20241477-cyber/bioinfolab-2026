# qual_summary.py 사용법 및 코드 설명서

대상 파일: `lab11/src/qual_summary.py`

## 1. 프로그램의 목적

FASTQ 파일에 들어 있는 모든 read의 품질 문자열을 Phred 점수로 바꾸어, **read마다 평균 품질을 구한 뒤 그 값들을 다시 평균 내어** 화면에 한 줄로 출력한다.

출력하는 값은 하나뿐이다.

- 전체 read 평균 품질

## 2. 실행 방법

`lab11` 폴더에서 다음과 같이 실행한다.

```
python3 src/qual_summary.py data/SRR1553607_1.fastq
```

형식:

```
python3 src/qual_summary.py <FASTQ 파일>
```

- 인자는 `sys.argv[1]`로 받는 FASTQ 파일 경로 하나이다.
- 코드에는 인자 개수를 검사하는 부분이 없다. 인자를 주지 않으면 `sys.argv[1]`에서 `IndexError`가 난다.

## 3. 입력 파일

FASTQ 형식의 텍스트 파일이다. read 하나는 **4줄**로 이루어진다.

| 줄 | 내용 | 예 (`data/SRR1553607_1.fastq`의 첫 read) |
|---|---|---|
| 1 | `@`로 시작하는 read 이름 | `@SRR1553607.1 1 length=101` |
| 2 | 염기 서열 | `GTTAGCGTTGTTGATCGCG...` |
| 3 | `+` 줄 | `+SRR1553607.1 1 length=101` |
| 4 | 품질 문자열 (서열과 길이가 같음) | `BB@FFFFFHHHHHJJJJJ...` |

`read_fastq()`는 파일이 정확히 4줄 단위로 되어 있다고 가정한다. 줄 수가 4의 배수가 아니면 `lines[i + 1]`이나 `lines[i + 3]`에서 `IndexError`가 날 수 있다.

## 4. 출력 결과

화면(표준 출력)에 다음 형식으로 한 줄을 출력한다. 파일로 저장하지는 않는다.

```
전체 read 평균 품질: <숫자>
```

`lab11` 폴더에서 `data/SRR1553607_1.fastq`로 실제 실행한 결과는 다음과 같다.

```
$ python3 src/qual_summary.py data/SRR1553607_1.fastq
전체 read 평균 품질: 33.4497222958299
```

소수점 아래 자릿수를 정리하는 코드가 없으므로 계산된 값이 그대로 출력된다.

## 5. 함수 설명

### 5.1 `read_fastq(filename)` — FASTQ 파일 읽기

```python
def read_fastq(filename):
    records = []
    with open(filename) as f:
        lines = f.readlines()
    for i in range(0, len(lines), 4):
        name = lines[i].rstrip()[1:]
        seq = lines[i + 1].rstrip()
        qual = lines[i + 3].rstrip()
        records.append((name, seq, qual))
    return records
```

역할: FASTQ 파일을 읽어 read마다 `(이름, 서열, 품질)` 튜플을 만들고, 그 튜플들의 리스트를 돌려준다.

- `f.readlines()`: 파일의 모든 줄을 한꺼번에 리스트 `lines`로 읽는다.
- `range(0, len(lines), 4)`: `i`가 0, 4, 8, ...으로 4씩 커진다. 즉 `i`는 각 read의 첫 줄 위치이다.
- `lines[i].rstrip()[1:]`: 1번째 줄에서 줄바꿈을 지우고(`rstrip()`), 맨 앞의 `@`를 뺀 나머지(`[1:]`)를 이름으로 쓴다.
- `lines[i + 1]`: 2번째 줄 = 서열.
- `lines[i + 3]`: 4번째 줄 = 품질 문자열. 3번째 줄(`+` 줄, `lines[i + 2]`)은 사용하지 않는다.

### 5.2 `mean_quality(qual)` — read 하나의 평균 품질

```python
def mean_quality(qual):
    scores = []
    for ch in qual:
        scores.append(ord(ch) - 33)
    return sum(scores) / len(scores)
```

역할: 품질 문자열 하나를 받아 각 문자를 Phred 점수(정수)로 바꾸고, 그 점수들의 평균을 돌려준다.

각 줄의 동작 원리:

1. `scores = []`
   점수를 모아 둘 빈 리스트를 만든다.

2. `for ch in qual`
   문자열 `qual`을 앞에서부터 한 글자씩 꺼내 `ch`에 넣으며 반복한다. 품질 문자열의 글자 하나가 염기 하나의 품질이다.

3. `scores.append(ord(ch) - 33)`
   - `ord(ch)`는 문자의 ASCII 번호를 돌려준다. 예: `ord('B')` = 66, `ord('J')` = 74.
   - 여기서 33을 빼면 Phred 점수가 된다. 예: `'B'` → 66 − 33 = **33**, `'J'` → 74 − 33 = **41**.
   - 계산한 점수를 `scores` 리스트 끝에 추가한다.

4. `sum(scores) / len(scores)`
   - `sum(scores)`: 모든 염기의 점수 합.
   - `len(scores)`: 점수 개수 = 품질 문자열 길이 = read 길이.
   - 합을 개수로 나누면 그 read의 **평균 Phred 점수**가 된다. `/` 나눗셈이므로 결과는 실수(float)이다.
   - 품질 문자열이 빈 문자열이면 `len(scores)`가 0이 되어 `ZeroDivisionError`가 난다 (코드에 이를 막는 부분은 없다).

## 6. 전체 read 평균 품질 계산 과정

```python
reads = read_fastq(sys.argv[1])

total = 0
for name, seq, qual in reads:
    q = mean_quality(qual)
    total = total + q

print("전체 read 평균 품질:", total / len(reads))
```

1. `reads = read_fastq(sys.argv[1])`
   명령줄에서 받은 FASTQ 파일을 읽어 `(이름, 서열, 품질)` 튜플의 리스트를 만든다.

2. `total = 0`
   read별 평균 품질을 더해 갈 변수를 0으로 시작한다.

3. `for name, seq, qual in reads`
   `reads`의 튜플을 하나씩 꺼내면서 세 값을 각각 `name`, `seq`, `qual`에 나누어 담는다(튜플 풀기). 이 반복문에서 실제로 쓰는 것은 `qual`뿐이고 `name`, `seq`는 사용하지 않는다.

4. `q = mean_quality(qual)`
   현재 read의 평균 Phred 점수를 구한다.

5. `total = total + q`
   그 값을 `total`에 누적한다. 반복이 끝나면 `total` = 모든 read 평균 품질의 합.

6. `total / len(reads)`
   합을 read 개수로 나누어 **read별 평균 품질의 평균**을 구하고 출력한다.

주의할 점: 이 값은 "read별 평균의 평균"이다. 모든 염기의 점수를 한꺼번에 모아 평균 낸 값과는 read 길이가 서로 다를 때 달라질 수 있다 (read 길이가 모두 같으면 두 값은 같다). 또 파일에 read가 하나도 없으면 `len(reads)`가 0이 되어 `ZeroDivisionError`가 난다.

## 7. Phred+33 인코딩과 평균 Phred 품질 점수의 의미

### 7.1 Phred 품질 점수

Phred 점수 Q는 그 염기가 잘못 읽혔을 확률 P와 다음 관계가 있다.

```
Q = -10 × log10(P)
```

| Q | 오류 확률 P | 정확도 |
|---|---|---|
| 10 | 1/10 | 90% |
| 20 | 1/100 | 99% |
| 30 | 1/1000 | 99.9% |
| 40 | 1/10000 | 99.99% |

점수가 10 오를 때마다 오류 확률이 10분의 1로 줄어든다.

### 7.2 Phred+33 인코딩

FASTQ 파일은 숫자 점수를 그대로 쓰지 않고 **문자 하나**로 바꾸어 저장한다. Phred+33 방식은 `점수 + 33`을 ASCII 번호로 하는 문자를 쓴다.

| 문자 | ASCII 번호 | Phred 점수 (번호 − 33) |
|---|---|---|
| `!` | 33 | 0 |
| `#` | 35 | 2 |
| `B` | 66 | 33 |
| `J` | 74 | 41 |

코드의 `ord(ch) - 33`이 바로 이 변환을 거꾸로 하는 부분이다. 33을 빼는 이유는 ASCII 0~32번이 공백·제어 문자라 화면에 보이지 않기 때문에, 보이는 문자인 `!`(33)부터 쓰도록 정해 두었기 때문이다.

### 7.3 평균 Phred 품질 점수의 의미

- read 하나의 평균 점수는 그 read 전체가 대체로 얼마나 믿을 만한지를 하나의 숫자로 요약한 것이다.
- 프로그램이 출력하는 전체 평균은 파일 전체의 품질 수준을 대략 보여 준다. 위 실행 결과 33.45는 Q30(오류 확률 1/1000)보다 약간 높은 수준이다.
- 다만 평균은 요약값일 뿐이다. read 끝부분처럼 일부 위치에서만 품질이 떨어지는 경우는 평균만으로는 알 수 없다. 또 점수의 평균은 오류 확률의 평균과 같지 않다 (로그 척도이므로).
- 이 프로그램은 평균 하나만 계산하며, 품질이 낮은 read를 걸러 내거나 위치별 품질을 보여 주는 기능은 없다.
