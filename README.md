# PonyTool 🐎

PonyTool — универсальный CLI-инструмент для работы с Python-проектами:
инициализация, тесты, очистка, git-операции — всё в одном месте.

## Установка

```bash
pip install ponytool
```

## Команды

### 📦 Инициализация проекта

```bash
pony project init
pony project init --name my_app
pony project init --no-git
```

* Создаёт структуру:
```css
src/
tests/
docs/
README.md
.gitignore
```

### 🧹 Очистка проекта

```bash
pony project clean
pony project clean --dry-run
pony project clean -y
```
* Удаляет кэш, coverage, build-артефакты
* Список настраивается в defaults.toml.

### 🧪 Тесты

```bash
pony test run
pony test run -k api
pony test coverage
pony test coverage --html
```

* Тесты запускаются через текущий Python (sys.executable).

### 🌱 Git

```bash
pony git status
pony git push
pony git push -m "message"
pony git push --dry-run
```

## Конфигурация

* **ponytool/config/defaults.toml**

```toml
[project.clean]
trash = ["__pycache__", ".pytest_cache", "htmlcov"]
```

* Можно переопределять через user.toml.

