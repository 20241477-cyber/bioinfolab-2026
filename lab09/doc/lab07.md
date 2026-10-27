# lab07 요약: 함수와 파일 저장

lab06에서 스크립트마다 반복하던 FASTA 처리 코드를 **함수로 묶어 `fasta.py` 모듈 하나로 정리**하고,
다른 스크립트에서 이 모듈을 불러와 결과를 **파일(FASTA, TSV)로 저장**하는 실습이다.

## 1. 함수 기초
- `src/fgc.py`: GC 비율을 계산하는 `gc_content()` 함수를 정의하고 호출한다.
- `src/fseqlen.py`: 값을 `print`만 하는 함수와 `return`하는 함수를 비교한다.
  `print`만 하는 함수의 결과를 변수에 담으면 `None`이 된다.
- `src/filter.py`: 기존 FASTA 읽기 코드를 `read_fasta()` 함수로 바꾼다.
  길이(20~40), GC 비율(0.4~0.6), N 개수(5개 미만) 조건으로 서열을 걸러낸다.

## 2. 공통 모듈 `src/fasta.py`

| 함수 | 기능 |
|---|---|
| `read_fasta(filename)` | FASTA 파일을 `{이름: 서열}` 딕셔너리로 읽는다 |
| `gc_content(seq)` | GC 비율(0~1)을 반환한다. 빈 서열이면 0.0 |
| `write_fasta(seqs, filename)` | 딕셔너리를 FASTA 파일로 저장한다 (반환값 없음) |
| `reverse_complement(seq)` | 역상보 서열을 반환한다 |
| `length_stats(seqs)` | 서열 개수, 전체·평균·최소·최대 길이를 딕셔너리로 반환한다 |

- `if __name__ == "__main__":` 블록에서 각 서열의 길이와 GC 비율을 출력하고,
  역상보를 두 번 구하면 원래 서열로 돌아오는지 확인한다.
- 사용법은 `src/README.md`에 정리되어 있다.

## 3. 모듈을 사용하는 스크립트

| 스크립트 | 기능 | 결과 파일 |
|---|---|---|
| `countseq2.py` | 서열 개수 출력 (인자·파일 존재 여부 검사 포함) | - |
| `seqlen2.py` | 서열별 길이 출력 | - |
| `stats.py` | `length_stats`로 길이 통계 출력 | - |
| `summary.py` | 서열별 이름, 길이, GC 비율을 TSV로 저장 | `doc/summary.tsv` |
| `filter_fasta.py` | 최소 길이 이상인 서열만 FASTA로 저장 | `doc/long.fasta` |
| `batchinfo2.py` | 폴더 안 모든 `*.fasta`를 `glob`으로 찾아 파일별 개수, 전체 길이, 평균 GC를 TSV로 저장 | `doc/batchinfo.tsv` |

## 4. 데이터와 결과
- 입력 데이터: `data/seqs.fasta`, `data/seqs2.fasta`, `data/lower.fasta`(소문자가 섞인 서열)
- `doc/summary.tsv`: gene1(30bp, GC 0.5), gene2(15bp, GC 0.4667), gene3(22bp, GC 0.5455)
- `doc/batchinfo.tsv`: 파일 3개의 서열 개수, 전체 길이, 평균 GC

## 5. 문서
- `doc/python_cheatsheet.md`: Bash 명령어와 대응하는 Python 코드를 비교해 정리했다.
  - 예: `grep -v ">"` → `not line.startswith(">")`, `$1` → `sys.argv[1]`, `wc -l` → `len(lines)`
- `src/README.md`에 적은 개선할 점
  1. 빈 딕셔너리가 들어오면 `length_stats`에서 0으로 나누기 오류가 난다.
  2. `reverse_complement`에 N 같은 문자가 들어오면 KeyError가 난다.
  3. 평균 GC를 계산하는 함수를 `fasta.py`에 따로 만들면 재사용하기 좋다.

## 6. 참고: 코드에서 발견한 문제
- `filter_fasta.py`: `minlen = sys.argv[2]`가 문자열이라 `len(...) >= minlen`에서 TypeError가 난다.
  `int(sys.argv[2])`로 바꿔야 한다.
- `gc_content`: 대문자 G와 C만 세기 때문에 소문자 서열의 GC 비율이 낮게 나온다.
  그래서 `batchinfo.tsv`에서 `lower.fasta`의 평균 GC가 실제 0.65가 아닌 0.2로 기록되었다.
  `seq = seq.upper()`를 먼저 실행하면 해결된다.
- `countseq2.py`: `from fasta import read_fasta`가 두 번 들어가 있다. 실행에는 문제가 없다.
