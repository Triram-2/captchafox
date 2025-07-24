import os
import shutil
import tomllib

from pathlib import Path
from typing import Any, Dict, List, Iterator

import nox

from nox import Session


nox.options.default_venv_backend = "uv"

# Type hint for PYPROJECT_CONTENT
PYPROJECT_CONTENT: Dict[str, Any] = tomllib.loads(
    Path("pyproject.toml").read_text(encoding="utf-8")
)

PROJECT_NAME: str = PYPROJECT_CONTENT["project"]["name"]
PYTHON_VERSIONS: List[str] = ["3.12", "3.13"]
SRC_DIR: str = "src"
TESTS_DIR: str = "tests"
DOCS_DIR: str = "docs"
COVERAGE_FAIL_UNDER: int = 80
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"


def install_project_with_deps(session: Session, *groups: str) -> None:
    """Устанавливает проект и его зависимости из указанных групп используя uv pip install."""
    install_args: List[str] = (
        ["-e", f".[{','.join(groups)}]"] if groups else ["-e", "."]
    )
    # Construct a string for logging that represents the command as it would be typed
    log_command_str = "uv pip install " + " ".join(install_args)
    session.log(f"Installing with: {log_command_str}")
    session.run_always("uv", "pip", "install", *install_args, external=True)
    session.log(f"Finished: {log_command_str}")


def create_dev_data_dir():
    current_dir = os.path.dirname(__file__)
    dev_dir = os.path.join(current_dir, "data", "dev")
    os.makedirs(dev_dir, mode=775, exist_ok=True)


@nox.session(python=PYTHON_VERSIONS)
def lint(session: Session) -> None:
    """Запускает линтеры (Ruff, Pyright) и проверку формата."""
    session.log("Установка зависимостей для линтинга...")
    install_project_with_deps(session, "lint")

    session.log("Запуск Ruff (format)...")
    session.run("ruff", "format", ".")

    session.log("Запуск Ruff (check)...")
    session.run("ruff", "check", ".")

    session.log("Запуск Pyright...")
    session.run("pyright", ".")

    session.log("Линтинг завершен успешно.")


@nox.session(python="3.13")
def audit(session: Session) -> None:
    "Запускает аудит зависимостей с `pip-audit`"
    session.log("Установка зависимостей для аудита...")
    install_project_with_deps(session, "all")

    create_dev_data_dir()

    session.log("Запуск pip-audit для проверки уязвимостей...")
    session.run("pip-audit", "--local", "-o", "data/dev/pip-audit.txt", ".")

    session.log("Аудит зависимостей завершён.")


@nox.session(python=PYTHON_VERSIONS)
def test(session: Session) -> None:
    """Запускает тесты с pytest, coverage и hypothesis"""
    session.log("Установка зависимостей для тестирования...")
    install_project_with_deps(session, "test")

    session.log("Запуск тестов с coverage...")
    session.run(
        "coverage",
        "run",
        "--source",
        SRC_DIR,
        "-m",
        "pytest",
        TESTS_DIR,
        *session.posargs,
        env={"PYTHONPATH": SRC_DIR},
    )

    session.log(f"Проверка покрытия кода (должно быть >= {COVERAGE_FAIL_UNDER}%)...")
    session.run("coverage", "report", "-m", f"--fail-under={COVERAGE_FAIL_UNDER}")

    session.log("Генерация отчета о покрытии в формате HTML и XML...")
    session.run("coverage", "html", "-d", "data/dev")
    session.run("coverage", "xml", "-o", "data/dev")

    session.log("Тестирование завершено успешно.")


@nox.session(python=PYTHON_VERSIONS[0])
def docs(session: Session) -> None:
    """Сборка документации с помощью Sphinx."""
    session.log("Установка зависимостей для сборки документации...")
    install_project_with_deps(session, "docs")

    docs_build_dir: Path = Path(DOCS_DIR) / "_build"

    session.log(f"Очистка старой документации в {docs_build_dir}...")
    if docs_build_dir.exists():
        shutil.rmtree(docs_build_dir)

    session.log("Сборка HTML документации...")
    session.run(
        "sphinx-build",
        "-b",
        "html",
        "-W",
        "--keep-going",
        "-E",  # no cached env
        "-T",  # full traceback
        "-j",
        "auto",  # parallel
        "-n",  # nitpicky
        DOCS_DIR,
        str(docs_build_dir),
    )
    session.log(f"Документация собрана в: {docs_build_dir.resolve()}")


@nox.session(python=PYTHON_VERSIONS[0])
def profile(session: Session) -> None:
    """Запуск профилировщика Scalene."""
    session.log("Установка зависимостей для профилирования...")
    install_project_with_deps(session, "profile")

    session.log("Запуск Scalene...")
    try:
        session.run("scalene", f"src/{PROJECT_NAME}/main.py", *session.posargs)

        outfile_setting = (
            PYPROJECT_CONTENT.get("tool", {}).get("scalene", {}).get("outfile")
        )
        outfile: str
        if isinstance(outfile_setting, str):
            outfile = outfile_setting
        else:
            outfile = "scalene_report.html"

        session.log(f"Отчет Scalene сохранен в: {Path(outfile).resolve()}")
    except Exception as e:
        session.error(
            f"Ошибка при запуске Scalene: {e}. Проверьте команду запуска и конфигурацию."
        )


@nox.session(python=False)
def commit(session: Session) -> None:
    """Добавление проекта в git и коммит через commitizen"""
    session.run("git", "add", ".")
    session.run("cz", "commit")


@nox.session(python=False)
def bump(session: Session) -> None:
    "Bump через commitizen + `git push -u origin main`"
    session.run("cz", "bump")
    session.run("git", "push", "-u", "origin", "main")


@nox.session(python=False)
def build(session: Session) -> None:
    """Сборка Docker-образа."""
    project_version_any: Any = PYPROJECT_CONTENT["project"]["version"]
    project_version: str = str(project_version_any)  # Ensure it's a string

    image_tag: str = f"{PROJECT_NAME}:{project_version}"
    latest_tag: str = f"{PROJECT_NAME}:latest"

    session.log(f"Сборка Docker-образа {image_tag} и {latest_tag}...")
    try:
        session.run(
            "docker",
            "build",
            ".",
            "-t",
            image_tag,
            "-t",
            latest_tag,
            *session.posargs,
            external=True,
        )
        session.log("Сборка Docker-образа завершена успешно.")
    except Exception as e:
        session.error(
            f"Ошибка при сборке Docker-образа. Убедитесь, что Docker запущен. Ошибка: {e}"
        )


@nox.session(python=False)
def compose_rebuild(session: Session) -> None:
    """Полностью пересобирает окружение Docker Compose."""
    image_name: str = "{{cookiecutter.project_slug}}-app"

    session.log("Остановка и очистка старых контейнеров...")
    session.run(
        "docker", "compose", "down", "--volumes", "--remove-orphans", external=True
    )

    session.log(f"Удаление старого образа {image_name}...")
    session.run("docker", "rmi", image_name, external=True, success_codes=[0, 1])

    session.log("Очистка кэша сборки Docker...")
    session.run("docker", "builder", "prune", "-a", external=True)

    session.log("Пересборка образов без кэша...")
    session.run("docker", "compose", "build", "--no-cache", "--pull", external=True)

    session.log("Запуск контейнеров...")
    session.run("docker", "compose", "up", external=True)


@nox.session(python=False)
def clean(session: Session) -> None:
    """Удаляет временные файлы и папки сборки/тестирования."""
    session.log("Очистка...")
    patterns_to_remove: List[str] = [
        "dist",
        "build",
        "*.egg-info",
        ".nox",
        ".pytest_cache",
        ".coverage",
        "coverage.xml",
        "coverage_html_report",
        "*.prof",
        "profile_output",
        "scalene_report.html",
        "**/.mypy_cache",
        "**/.ruff_cache",
        "**/__pycache__",
        f"{DOCS_DIR}/_build",
        "vulnerabilities.json",
    ]
    for pattern in patterns_to_remove:
        try:
            if "*" in pattern or "?" in pattern:
                # Path.glob returns a generator of Path objects
                path_iter: Iterator[Path] = Path(".").glob(pattern)
                for path_obj in path_iter:  # path_obj is a Path object
                    session.log(f"Удаление {path_obj}")
                    if path_obj.is_dir():
                        shutil.rmtree(path_obj, ignore_errors=True)
                    else:
                        path_obj.unlink(missing_ok=True)
            else:
                path_obj: Path = Path(pattern)  # path_obj is a Path object
                if path_obj.exists():
                    session.log(f"Удаление {path_obj}")
                    if path_obj.is_dir():
                        shutil.rmtree(path_obj, ignore_errors=True)
                    else:
                        path_obj.unlink(missing_ok=True)
        except Exception as e:
            session.warn(f"Не удалось удалить {pattern}: {e}")
    session.log("Очистка завершена.")


@nox.session(python=PYTHON_VERSIONS[0])
def locust(session: Session) -> None:
    """Запускает нагрузочное тестирование с Locust."""
    session.log("Установка зависимостей для Locust...")
    install_project_with_deps(session, "loadtest")

    locust_file: str = "locustfile.py"
    if not Path(locust_file).exists():
        session.warn(
            f"Файл {locust_file} не найден. Для запуска Locust необходимо создать его и определить сценарии нагрузки."
        )
        session.log(
            "Пример команды, если locustfile.py существует: "
            "locust -f locustfile.py --host=http://localhost:{{cookiecutter.app_port_host}}"
        )
        return

    session.log(f"Запуск Locust (используя {locust_file})...")
    session.run("locust", "-f", locust_file, *session.posargs)


@nox.session(python=PYTHON_VERSIONS, name="ci")
def ci_pipeline(session: nox.Session) -> None:
    """Запускает основные проверки CI: lint и test."""
    python_version = session.python
    session.log(f"Запуск CI для Python {python_version}")

    suffix = f"-{python_version}" if isinstance(python_version, str) else ""
    session.notify(f"lint{suffix}")
    session.notify(f"test{suffix}")


@nox.session(python=False)
def publish(session: nox.Session) -> None:
    session.run('hatch', 'clean')
    session.run('hatch', 'build')
    session.run('hatch', 'publish', '-y')