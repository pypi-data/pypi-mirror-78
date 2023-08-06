# shorten-func
Reduce to pass the same parameters multiple times when calling a function multiple times

    def shorten_func(func_name, *args_global, **kwargs_global)
    :param func_name: the function name
    :param args_global: arguments passed repeatedly
    :param kwargs_global: keyword arguments passed repeatedly
    :return: The same function but it requires fewer parameters
    
#####Installation:
https://pypi.org/project/shorten-func/

    pip install shorten-func

#####Usage:

    def long_function(variable_passed_repeatedly, variable):
        return variable_passed_repeatedly + variable

`before:`

    value_1 = long_function(variable_passed_repeatedly, 'var_1'')
    value_2 = long_function(variable_passed_repeatedly, 'var_2')

`after:`

    from shorten_func import shorten_func
    get = shorten_func(long_function, variable_passed_repeatedly)
    value_1 = get('var_1')
    value_2 = get('var_2')
        
#####Example:

    def set_child_full_name(family_name, child_first_name):
        return child_first_name + family_name

`before:`

    child_1 = set_child_full_name('family_name', 'Messi')
    child_2 = set_child_full_name('family_name', 'Ronaldo')

`after:`

    from shorten_func import shorten_func
    get = shorten_func(set_child_full_name, 'family_name')
    child_1 = get('Messi')
    child_2 = get('Ronaldo')