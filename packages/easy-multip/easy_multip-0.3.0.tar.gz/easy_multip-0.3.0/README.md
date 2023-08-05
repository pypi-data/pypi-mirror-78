# easy_multip

easy_multip is a small tool designed to quickly allow Python multiprocessing capabilities while greatly simplifying code for easier use.

# Current Features

  - easy_multip.map(func, arg_group, leave_one_cpu_free=True)
    - map() or list comprehension type functionality that is parallelized using multiprocessing and includes a progress bar
    - Usage is similar to the below constructs:
        ```sh
        list(map(func, arg_group))
            or
        [func(arg) for arg in arg_group]
        ```
  - easy_multip.doloop(func, arg_group, leave_one_cpu_free=True)
    - for loop equivalent that runs a function that returns None
    - Useful in situations like file processing where each operation is expensive and totally independent
    - Allocates jobs evenly among processors and provides a progress bar... of sorts
    - Usage is similar to the below construct:
        ```sh
        for arg in arg_group:
            func(arg)
        ```
  - easy_multip.decorators.use_multip(func, leave_one_cpu_free=True)
    - Decorator providing capability of quickly adding multiprocessing to a function operating on a list
    - ONLY for functions taking a list first arg that returns a list or None
    - DO NOT USE `@decorator` syntax!  Must use the following pattern:
        ```sh
        def _func(list_arg, *args, **kwargs):
            # stuff happens
            return [] (or None)
        func = use_multip(_func)
        ```

License
----
MIT
