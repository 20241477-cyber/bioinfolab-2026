# fasta.py의 함수 목록
- read_fasta(filename)
- gc_content(seq)
- write_fasta(seqs, filename)
- reverse_complement(seq)
- length_stats(seqs)

## 1. read_fasta(filename) 
- 입력으로 받은 FASTA파일을 읽어서 딕셔너리{이름:서열}로 반환한다.
- 사용 예시)
  from fasta import read_fasta
  dic=read_fasta("../data/seqs.fasta")

## 2. gc_content(seq)
- 입력으로 받은 seq(염기서열)의 GC 비율을 반환한다.
- 사용 예시)
  from fasta import gc_content
  gc=gc_content("AATTGGCC")

## 3. write_fasta(seqs, filename) 
- {이름 : 서열}로 저장된 딕셔너리(seqs)와
   출력 파일 경로(filename)을 입력으로 받아서 FASTA 파일로 저장한다. 
  (파일을 생성하는 함수이며, 별도의 return문이 없으므로 기본적으로 None을 반환한다.)
  (seqs는 딕셔너리 형태이다.)
- 사용 예시)
  from fasta import write_fasta
  write_fasta(dic, "../doc/result.fasta")

## 4. reverse_complement(seq)
- 입력으로 받은 seq(염기서열)를 상보 염기(A↔T, C↔G)로 변환한 후,
  서열의 순서를 뒤집어 역상보서열을 문자열로 반환한다.
- 사용 예시)
  from fasta import reverse_complement
  reverse=reverse_complement("AATTGGCC")

## 5. length_stats(seqs)
- 입력으로 받은 딕셔너리{이름 : 서열}를 이용하여
  서열의 길이 통계(서열의 개수, 전체 길이, 평균 길이, 최소 길이, 최대 길이)를
  딕셔너리로 반환한다.  (seqs는 딕셔너리 형태이다.)
- 반환되는 딕셔너리 형태 :
  {'count':서열의 수, 'total': 모든 서열 길이의 합, 'average': 서열의 평균 길이,
   'min':서열 중 가장 짧은 길이, 'max':서열 중 가장 긴 길이}
- 사용 예시)
  from fasta import length_stats
  stat_dic=length_stats(dic)

## 부족한 점 및 추가하고 싶은 함수

1. 빈 FASTA 파일 처리 기능 
  : length_stats()는 빈 딕셔너리를 받으면 오류가 발생한다. length_stats()에서
    평균 서열 길이를 구하는 코드인 "average": sum(lengths) / len(lengths)에서 len(lengths)=0이 되므로 오류가 발생한다.
    또한 "min": min(lengths), "max": max(lengths)의 경우에도 오류가 발생한다.
    따라서 입력받은 딕셔너리가 비어 있는 경우를 확인하고, 별도의 결과를 반환하거나 실행을 종료하는
    예외 처리 기능을 추가하는 것이 좋다.

2. A, T, G, C 외 다른 염기 기호 처리 기능
  : reverse_complement() 함수에는 A, T, G, C인 경우에는 바꾸는 염기가 존재하지만 
    그 외의 문자에 대해서는 지정하고 있지 않다. 실제 DNA 데이터에서 나타날 수 있는 N 등의 기호가
    염기 서열에 포함될 수 있다. 이런 기호에 대응하는 값이 딕셔너리에 정의되어있지 않아서 KeyError가 발생한다.
    따라서 A, T, G, C가 아닌 다른 염기 기호도 처리할 수 있도록 딕셔너리를 확장하면 좋다.

3. 평균 GC 비율을 구하는 함수 추가 
  : 실험 문제 4번에서 만든 batchinfo2.py에서 length_stats(seqs)를 이용하여
    서열 개수와 전체 길이를 계산하고, 파일 이름과 함께 TSV 파일에 작성하였다. 평균 GC비율을 구하는 함수는
    따로 지정되어있지 않아서 batchinfo2.py에서 따로 계산하여 TSV 파일에 저장하였다.
    평균 GC 비율을 구하는 함수도 fasta.py에 따로 만들어 두면 이후 다른 스크립트에서 쉽게 재사용할 수 있을 것이다.