# Meliorate
Meliorate is a code generator and test runner for C++.

It aims to:
 * Simplify the writing and execution of tests.
 * Minimise the amount of strange code (macro magic) often associated with C++ unit test libraries.

Meliorate uses `Clang` to identify test functions (functions beginning with the word `test`) and generates all code necessary to run test functions automatically.

## Prerequisits
Requires:
 * Python3.7+
 * Clang (dev only)

## Getting started
Meliorate comes in two parts:
 * `meliorate.h` which includes the `meliorate_run` function for running tests and other useful parameters for customising test execution.
 * `meliorateapp` which is the code generator.

`meliorate.h` should be included into you project by adding a compiler include flag (-I) that points to the `include` directory (and *not* the `include/meliorate` directory).

The `meliorateapp` can be installed from PyPi.

```
pip install meliorate
```

## Using Meliorate

Write some test functions:
```
#include "meliorate/meliorate.h"

void test_that_something_is_true()
{
    // code goes here.
}

// Not extracted as a test function because the function name
// does not begin with "test".
int not_a_test_function()
{
    return 0;
}

void test_that_error_is_thrown()
{
    throw std::runtime_error("Something went wrong.");
}


void test_that_the_result_is_42()
{
    // code goes here.
}

// Not extracted as a test function because the function is static.
static void test_that_something_is_false()
{
    // code goes here.
}
```

Add the `meliorate_run` function to `main`:
```
#include "meliorate/meliorate.h"

int main()
{
    meliorate_stop_on_error = false;
    return meliorate_run<std::exception>();
}
```
Meliorate assumes your assertion library will use exceptions from the standard library by default (hence why `meliorate_run` is parameterized with `std::exception`). To use a custom assertion library, see the `Customising Assertions` section for more information.

Run the `meliorateapp` on the test directory:
```
meliorateapp <path/to/test/directory>
```

Check that `meliorate_gen.cpp` is created in the test directory.

Finally, compile and run you test program as normal, remembering to add `meliorate_gen.cpp` to your build process.

The output will look something like:
```
[RUN     ] test_that_something_is_true
[  PASSED]
[RUN     ] test_that_error_is_thrown
Something went wrong.
[  FAILED]
[RUN     ] test_that_the_result_is_42
[  PASSED]
1 tests FAILED out of 3
```

You can force test execution to stop when an error occurs by setting `meliorate_stop_on_error` variable to `true` prior to calling the `meliorate_run` function.


## Customising Assertions 
Meliorate does not provide any assertions, but by default assumes that the assertion library will use exceptions from the standard library. Should you wish to use another library, such as [snowhouse](https://github.com/banditcpp/snowhouse), follow the instructions below:

Provide a specialisation for the `meliorate_handle_exception` function. This function handles the printing of the exception when an error occurs. By default the function looks like:
```
template <typename T>
void meliorate_handle_exception(T const& exception)
{
    std::cerr << exception.what() << std::endl;
}
```

Provide the specialisation like so:
```
template <typename T>
void meliorate_handle_exception(snowhouse::AssertionException const& exception)
{
    std::cerr << ex.GetMessage() << std::endl;
}
```

Then set the template parameter for the `meliorate_run` function:
```
#include "meliorate/meliorate.h"

int main()
{
    meliorate_stop_on_error = false;
    return meliorate_run<snowhouse::AssertionException>();
}
```