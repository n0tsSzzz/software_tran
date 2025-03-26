## Инструментальные средства разработки ПО
## Практическое задание номер 3

### Установка

1. Клонируйте репозиторий
```
git clone https://github.com/n0tsSzzz/software_tran
```

2. Зайдите в папку с проектом и пропишите
```
cd sofware_tran
docker-compose up -d
```

3. После запуска контейнеров для проверки можно ввести
```
docker logs software_tran-app

docker-compose exec db psql -U admin -d shop_db
```
