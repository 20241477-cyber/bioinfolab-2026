# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 저장소 성격

생물정보학실험 수업의 주차별 실습 저장소이다. 소프트웨어 프로젝트가 아니므로 빌드 시스템, 패키지 관리자, 린터, 테스트가 없다. 문서, 주석, 커밋 메시지는 모두 한국어로 작성한다.

## 폴더 구조와 규칙

- 주차마다 `lab-template/`을 복사해 `labNN/` 폴더를 만든다 (`cp -r lab-template labNN`). 각 폴더에는 다음이 있다.
  - `data/`: 내려받거나 만들어 낸 데이터 (FASTA 등)
  - `doc/`: 보고서, 결과 요약 (`.md`, `.tsv`), 치트시트
  - `src/`: 직접 작성한 `.sh` / `.py` 스크립트
- 주차 폴더끼리는 서로 import 하지 않는다. 코드는 주차마다 일부러 중복되고 발전한다 (예: lab05/lab06에서는 FASTA 읽기를 스크립트마다 직접 작성하고, lab07에서 `lab07/src/fasta.py` 모듈로 묶는다). 여러 주차에 걸쳐 리팩터링하지 않는다.
- `resources/`에는 강의자가 준 예제 데이터와 스크립트가 있다.
- `bug*.sh` / `bug*.py`는 디버깅 연습용으로 일부러 넣은 오류 파일이다.

## 스크립트 실행

테스트는 없고, 스크립트를 상대 경로로 직접 실행한다.

```
python3 src/count_agent.py data/seqs.fasta      # 주차 폴더에서 실행
cd lab07/src && python3 summary.py ../data/seqs.fasta ../doc/summary.tsv
bash src/batchinfo.sh data
```

`lab07/src/`의 스크립트는 `from fasta import ...`를 쓰므로 `lab07/src/` 안에서 실행해야 한다 (또는 그 폴더를 `PYTHONPATH`에 넣는다). `python3 fasta.py <FASTA>`를 실행하면 역상보 서열을 두 번 구해 원래 서열로 돌아오는지 스스로 확인한다.

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
