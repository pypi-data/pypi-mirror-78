# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['meliorateapp']

package_data = \
{'': ['*']}

install_requires = \
['clang>=6.0.0,<7.0.0', 'jinja2>=2.11.2,<3.0.0']

entry_points = \
{'console_scripts': ['meliorateapp = meliorateapp.main:script_entry']}

setup_kwargs = {
    'name': 'meliorateapp',
    'version': '0.1.0',
    'description': 'A code generator and test runner for C++',
    'long_description': '# Meliorate\nMeliorate is a code generator and test runner for C++.\n\nIt aims to:\n * Simplify the writing and execution of tests.\n * Minimise the amount of strange code (macro magic) often associated with C++ unit test libraries.\n\nMeliorate uses `Clang` to identify test functions (functions beginning with the word `test`) and generates all code necessary to run test functions automatically.\n\n## Prerequisits\nRequires:\n * Python3.7+\n * Clang (dev only)\n\n## Getting started\nMeliorate comes in two parts:\n * `meliorate.h` which includes the `meliorate_run` function for running tests and other useful parameters for customising test execution.\n * `meliorateapp` which is the code generator.\n\n`meliorate.h` should be included into you project by adding a compiler include flag (-I) that points to the `include` directory (and *not* the `include/meliorate` directory).\n\nThe `meliorateapp` can be installed from PyPi.\n\n```\npip install meliorate\n```\n\n## Using Meliorate\n\nWrite some test functions:\n```\n#include "meliorate/meliorate.h"\n\nvoid test_that_something_is_true()\n{\n    // code goes here.\n}\n\n// Not extracted as a test function because the function name\n// does not begin with "test".\nint not_a_test_function()\n{\n    return 0;\n}\n\nvoid test_that_error_is_thrown()\n{\n    throw std::runtime_error("Something went wrong.");\n}\n\n\nvoid test_that_the_result_is_42()\n{\n    // code goes here.\n}\n\n// Not extracted as a test function because the function is static.\nstatic void test_that_something_is_false()\n{\n    // code goes here.\n}\n```\n\nAdd the `meliorate_run` function to `main`:\n```\n#include "meliorate/meliorate.h"\n\nint main()\n{\n    meliorate_stop_on_error = false;\n    return meliorate_run<std::exception>();\n}\n```\nMeliorate assumes your assertion library will use exceptions from the standard library by default (hence why `meliorate_run` is parameterized with `std::exception`). To use a custom assertion library, see the `Customising Assertions` section for more information.\n\nRun the `meliorateapp` on the test directory:\n```\nmeliorateapp <path/to/test/directory>\n```\n\nCheck that `meliorate_gen.cpp` is created in the test directory.\n\nFinally, compile and run you test program as normal, remembering to add `meliorate_gen.cpp` to your build process.\n\nThe output will look something like:\n```\n[RUN     ] test_that_something_is_true\n[  PASSED]\n[RUN     ] test_that_error_is_thrown\nSomething went wrong.\n[  FAILED]\n[RUN     ] test_that_the_result_is_42\n[  PASSED]\n1 tests FAILED out of 3\n```\n\nYou can force test execution to stop when an error occurs by setting `meliorate_stop_on_error` variable to `true` prior to calling the `meliorate_run` function.\n\n\n## Customising Assertions \nMeliorate does not provide any assertions, but by default assumes that the assertion library will use exceptions from the standard library. Should you wish to use another library, such as [snowhouse](https://github.com/banditcpp/snowhouse), follow the instructions below:\n\nProvide a specialisation for the `meliorate_handle_exception` function. This function handles the printing of the exception when an error occurs. By default the function looks like:\n```\ntemplate <typename T>\nvoid meliorate_handle_exception(T const& exception)\n{\n    std::cerr << exception.what() << std::endl;\n}\n```\n\nProvide the specialisation like so:\n```\ntemplate <typename T>\nvoid meliorate_handle_exception(snowhouse::AssertionException const& exception)\n{\n    std::cerr << ex.GetMessage() << std::endl;\n}\n```\n\nThen set the template parameter for the `meliorate_run` function:\n```\n#include "meliorate/meliorate.h"\n\nint main()\n{\n    meliorate_stop_on_error = false;\n    return meliorate_run<snowhouse::AssertionException>();\n}\n```',
    'author': 'David Walker',
    'author_email': 'diwalkerdev@twitter.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/diwalkerdev/Meliorate',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
