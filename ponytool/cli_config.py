# project
from ponytool.project.init import project_init
from ponytool.project.clear import project_clean
from ponytool.project.status_writer import get_project_status
from ponytool.cli_parsers import project_init_parser, project_clear_parser, project_status_parser

# git
from ponytool.git.doctor import git_doctor
from ponytool.git.info import git_info
from ponytool.git.init import git_init
from ponytool.git.push import push_to_git
from ponytool.git.remove import remove_git_data
from ponytool.git.rollback import git_rollback
from ponytool.cli_parsers import (
    git_info_parser,
    git_init_parser,
    git_push_parser,
    git_rollback_parser,
)

# pytest_script
from ponytool.pytest_script.run_tests import run_tests
from ponytool.pytest_script.coverage import run_coverage_test
from ponytool.pytest_script.test_doctor_writer import doctor_for_tests
from ponytool.cli_parsers import run_py_test_parser, cov_py_test_parser, doc_py_test_parser

# requirements
from ponytool.req.generate import (freeze_requirements, generate_requirements, clean_requirements)
from ponytool.cli_parsers import (req_gen_parser, req_freeze_parser, req_clean_parser, req_doctor_parser)
from ponytool.req.req_doctor import doctor_for_requirements


# DISPATCH_TABLE: (section -> action -> handler)
DISPATCH_TABLE = {
    'project': {
        "init": project_init,
        "status": get_project_status,
        'clear': project_clean,
    },
    'git': {
        "init": git_init,
        "info": git_info,
        'doctor': git_doctor,
        'push': push_to_git,
        'remove': remove_git_data,
        'rollback': git_rollback,
    },
    'test': {
        "run": run_tests,
        "cov": run_coverage_test,
        "doctor": doctor_for_tests,
    },
    'req': {
        "gen": generate_requirements,
        "freeze": freeze_requirements,
        "doctor": doctor_for_requirements,
        "clean": clean_requirements,
    },
}

# PARSER_TABLE: (section, action) -> argparse setup
PARSER_TABLE = {
    ("project", 'init'): project_init_parser,
    ("project", 'clear'): project_clear_parser,
    ("project", 'status'): project_status_parser,
    ("git", 'init'): git_init_parser,
    ("git", 'info'): git_info_parser,
    ('git', 'push'): git_push_parser,
    ('git', 'rollback'): git_rollback_parser,
    ("test", 'run'): run_py_test_parser,
    ("test", 'cov'): cov_py_test_parser,
    ("test", 'doctor'): doc_py_test_parser,
    ('req', 'gen'): req_gen_parser,
    ('req', 'freeze'): req_freeze_parser,
    ('req', 'clean'): req_clean_parser,
    ('req', 'doctor'): req_doctor_parser,
}