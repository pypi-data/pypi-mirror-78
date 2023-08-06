:: pytest --html=../report/report.html --self-contained-html
:: or
:: pytest --html=../report/report.html --self-contained-html -m jicai_web
:: 报告在当前目录生产
pytest --html=report.html --self-contained-html -o log_cli=true -o log_cli_level=INFO