# lero_accesories
ТЗ


### Запуск:
- **docker-compose up --build** либо для фоновой работы: **docker-compose up -d --build**

### Архитектура:
- app/
  - db - модели и репозитории базы данных
  - services - бизнес-логика (сервисы)
  - bot - бот и его составляющие
  - monitoring - модуль отвечающий за мониторинг сайтов в фоне
- tests - тесты

#### Стиль: Слоистая архитектура
#### Существующие слои: repositories, services, routers(handlers)

### Пример работы
#### Запись сайта: AddWebsiteRouter -> SiteService(create_site) -> task_checker(BackgroundResponses) + WeekReporter
#### Недоступность сайта: BackgroundResponses(run) -> SiteChecker -> BackgroundResponses -> NotifyService
#### Проверка сайта(SiteChecker): check_site -> get_response -> normalize_url -> get_response -> return status_code, response_time, content

### Схема базы данных описана в app/db/models. **Настройка не требуется.**


