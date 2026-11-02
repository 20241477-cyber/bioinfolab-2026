# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 저장소 성격

생물정보학실험 수업의 주차별 실습 저장소이다. 소프트웨어 프로젝트가 아니므로 빌드 시스템, 패키지 관리자, 린터, 테스트가 없다. 문서, 주석, 커밋 메시지는 모두 한국어로 작성한다.

## 폴더 구조와 규칙

- 주차마다 `lab-template/`을 복사해 `labNN/` 폴더를 만든다 (`cp -r lab-template labNN`). 각 폴더에는 다음이 있다.
  - `data/`: 내려받거나 만들어 낸 데이터 (FASTA 등)
  - `doc/`: 보고서, 결과 요약 (`.md`, `.tsv`), 치트시트
  - `src/`: 직접 작성한 `.sh` / `.py` 스크립트
- 주차 폴더끼리는 원칙적으로 서로 import하지 않는다. 단, FASTA 파일을 읽을 때 lab07/src/fasta.py의 read_fasta() 함수를 재사용하는 경우는 예외로 한다. 코드는 주차마다 일부러 중복되고 발전한다 (예: lab05/lab06에서는 FASTA 읽기를 스크립트마다 직접 작성하고, lab07에서 `lab07/src/fasta.py` 모듈로 묶는다). 여러 주차에 걸쳐 리팩터링하지 않는다.
- `resources/`에는 강의자가 준 예제 데이터와 스크립트가 있다.
- `bug*.sh` / `bug*.py`는 디버깅 연습용으로 일부러 넣은 오류 파일이다.

## 스크립트 실행

별도의 자동화 테스트 체계는 없으며, 스크립트를 상대 경로로 직접 실행하여 결과를 확인한다.

```
python3 src/count_agent.py data/seqs.fasta      # 주차 폴더에서 실행
cd lab07/src && python3 summary.py ../data/seqs.fasta ../doc/summary.tsv
bash src/batchinfo.sh data
```

`lab07/src/`의 일부 스크립트(batchinfo2.py, countseq2.py 등)는 `from fasta import ...`를 사용하므로 fasta.py 모듈을 찾을 수 있도록 `lab07/src/` 안에서 실행해야 한다 (또는 그 폴더를 `PYTHONPATH`에 넣는다). `python3 fasta.py <FASTA>`를 실행하면 역상보 서열을 두 번 구해 원래 서열로 돌아오는지 스스로 확인한다.

스크립트 작성 방식: 맨 위에 목적과 `# 사용법:` 줄을 주석으로 적고, 인자는 `sys.argv`로 받으며 (argparse 미사용), 단순한 반복문과 문자열 이어 붙이기를 쓰는 초급 수준의 Python/bash이다. 고급 문법을 들여오지 말고 이 수준에 맞춘다.

## 실행 환경

GitHub Codespaces에서 미리 만든 이미지(`ghcr.io/goshng/bioinfolab:*`)를 쓴다. 주차에 맞는 설정을 `.devcontainer/*/devcontainer.json`에서 고른다.

| 주차 | 설정 | 들어 있는 도구 |
|---|---|---|
| 02~07 | `1-basic` | python3, 리눅스 기본 명령어 |
| conda 실습 | `2-conda` | micromamba (패키지는 직접 설치) |
| 08~09, 12~14 | `3-seq` | seqkit, blast, mafft, iqtree, fastqc, fastp |
| 10~11 | `4-genome` | 위 도구 + shovill, prokka |

`.devcontainer/check.sh`가 어떤 도구가 있는지 보여 준다. `$MYHOME`은 작업 폴더(저장소 루트)이며, 인자 없이 `cd`만 입력하면 그곳으로 돌아온다. 도구를 직접 설치하지 않는다 (설치 자체가 과제인 conda 실습 주차만 예외).

## Git

`.gitignore`는 시퀀싱 데이터(`*.fastq*`, `*.fq*`, `*.sra`), 조립/주석 결과 폴더(`shovill_out/`, `prokka_out/` 등), FastQC 보고서를 제외한다. 이런 데이터는 커밋하지 말고 필요할 때 `wget`으로 다시 내려받는다. 커밋은 `main`에 바로, 실습 단계마다 한다 (예: `lab03 완료`).

## 수업 규칙

### 1. FASTA 파일을 읽을 때
- FASTA 파일을 읽을 때는 기존에 작성한 `lab07/src/fasta.py`의 `read_fasta()` 함수를 사용한다.
- 동일한 기능을 하는 함수를 새로 만들지 않고, 기존 함수를 재사용한다.
- `read_fasta()`를 사용할 수 없는 경우에는 임의로 다른 방법을 사용하지 말고 먼저 사용자에게 이유를 설명한다.

### 2. 새로운 라이브러리를 사용할 때
- Biopython 등 새로운 외부 라이브러리를 사용하기 전에 사용자에게 먼저 허락을 구한다.
- 새로운 라이브러리가 필요한 이유와 기존 Python 기능으로 해결할 수 없는지를 설명한다.
- 사용자의 허락 없이 라이브러리나 프로그램을 설치하지 않는다.

### 3. 실행하지 말아야 할 명령어
- `rm`, `rm -r` 등 기존 파일이나 폴더를 삭제하는 명령어를 실행하지 않는다.
- `pip install`, `apt install`, `sudo` 등 새로운 라이브러리나 프로그램을 설치하거나 시스템 설정을 변경하는 명령어를 실행하지 않는다.
- `git add`, `git commit`, `git push`, `git reset`, `git restore` 등 Git의 기록이나 파일 상태를 변경하는 명령어를 실행하지 않는다. Git 작업은 사용자가 직접 수행한다.
- `mv` 등 파일을 이동하거나 덮어쓰는 명령어는 사용자에게 먼저 설명하고 승인을 요청한다.

### 4. 기존 코드 수정 및 결과 확인
- 기존 코드를 수정할 때는 요청받은 부분만 변경하고, 관련 없는 파일이나 코드는 수정하지 않는다.
- 코드를 수정한 후에는 무엇을 변경했는지와 수정한 이유를 설명한다.
- 실행 결과를 확인하지 않았다면 정상적으로 작동한다고 단정하지 않는다.
- Python과 Bash 코드를 작성할 때는 복잡한 문법이나 새로운 기능을 임의로 사용하지 않고, 코드의 작동 원리를 사용자가 쉽게 이해할 수 있도록 작성한다.
- 서로 충돌하는 규칙이 발견되면 임의로 우선순위를 결정하지 말고, 코드를 작성하기 전에 사용자에게 먼저 확인한다.

