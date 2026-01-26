기존 실행 방법

1) eclipse plugin 으로 실행

2) curl -X POST [http://localhost:3000/agent/qa](http://localhost:3000/agent/qa) -H ... -d ... 와 같은 형식으로 실행

추가 실행 방법

3) CLI 명령어 실행

	a) 코드 생성: coder generate --product xframe5 --input schema.sql --format stdout
	
	b) QA: coder qa "How to open a popup?" --product xframe5 --language ko
	
	c) 코드 리뷰: coder review benchmark/cli_test/sample_code.xml --product xframe5 --language ko --format json