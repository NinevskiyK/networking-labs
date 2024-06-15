### Реализация скрипта для тестирования MTU в канале

В данной самостоятельной работе реализован простой скрипт для поиска минимального значения MTU в канале между конечными хостами на python.

Для запуска в докере:
```
docker run --rm  $(docker build -q .) [OPTIONS] DEST

Options:
  -v, --verbose
  --help         Show this message and exit.
```

Например
`docker run --rm  $(docker build -q .) google.com`
