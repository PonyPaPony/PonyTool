[![PyPI version](https://badge.fury.io/py/ponytool.svg)](https://pypi.org/project/ponytool/)

# PonyTool

PonyTool — это CLI-инструмент для Python-разработчиков,
который убирает рутину при работе с проектами.

---

## Зачем он нужен

PonyTool появился из очень конкретной боли:

- каждый раз вручную создавать одни и те же папки и файлы
- каждый раз писать `.gitignore` с нуля
- постоянно ловить глюки `pytest` из-за виртуального окружения
- страдать с зависимостями, не понимая, что относится к стандартной библиотеке, а что — нет

Если тебе знакомо хоть что-то из этого — инструмент, скорее всего, будет полезен.

---

## Для кого этот инструмент

PonyTool — для Python-разработчиков,  
**которые устали от рутины и хотят тратить время на код, а не на подготовку проекта**.

Он особенно полезен, если ты:
- часто создаёшь новые проекты
- пишешь небольшие утилиты, библиотеки или pet-проекты
- не хочешь каждый раз вспоминать одни и те же команды и файлы

---

## Чего PonyTool НЕ делает

Это важно понимать заранее:

- PonyTool **не пишет код вместо вас**
- PonyTool **не думает за вас**
- PonyTool **не учит вас Python**
- PonyTool **не навязывает архитектуру**
- PonyTool **не является фреймворком**

Он делает только одно — **упрощает ежедневную рутину**.

---

## Установка
```bash
pip install -U ponytool
```

## Основные команды

### `pony init`

Создаёт структуру проекта.

- использует дефолтную структуру
- либо читает её из `.ponyinit`
- безопасен при повторном запуске

```bash
pony init
```

### `pony bootstrap`

Создаёт базовые файлы проекта:

- .gitignore
- README.md
- LICENSE (MIT, с текущим годом)

**Ничего не перезаписывает, если файлы уже существуют.**

```bash
pony bootstrap
```

### `pony deps`

- Анализирует проект и генерирует requirements.txt
на основе реально используемых импортов, а не pip freeze.

```bash
pony deps
```

### `pony test`

- Запускает тесты корректно внутри активного виртуального окружения.
- Поддерживает дополнительные режимы:

```bash
pony test
pony test --coverage
pony test --coverage --html
```

## Типичный сценарий использования

### В идеале PonyTool используют так:

```text
я создаю проект →
пишу код →
тестирую →
создаю служебные файлы (gitignore, README, license, зависимости)
```
Без лишних шагов и постоянного гугления.

## Статус проекта

### PonyTool — живой pet-проект, который развивается по мере реальных потребностей.

- Он не пытается понравиться всем.
- Он решает конкретные проблемы — и делает это честно.

## Contents
- Installation
- Commands
- Example
- Project status
- Releases
- License

## Example

```bash
$ pony init
✔ Project structure created

$ pony bootstrap
✔ .gitignore created
✔ README.md created
✔ LICENSE created

$ pony deps
✔ requirements.txt generated

$ pony test --coverage
✔ Tests passed
✔ Coverage report generated
```

## Releases
This project is published on PyPI and versioned via GitHub Releases.
See the Releases page for changelogs and version history.

## Лицензия

### MIT

---
