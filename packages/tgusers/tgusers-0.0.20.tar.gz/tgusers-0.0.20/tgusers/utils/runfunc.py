import inspect


from tgusers.dataclasses.rooms import Arguments


async def run_func_as_async(function, **func_args):
    if inspect.iscoroutinefunction(function):
        return await function(**func_args)
    else:
        return function(**func_args)


async def run_function_with_arguments_by_annotations(function, arguments: Arguments):
    params = list(inspect.signature(function).parameters.items())
    func_args = {}
    num_ = 0
    for o_arg in arguments.obligatory:
        if not len(params) - num_:
            break
        name, _ = params[num_]
        func_args[name] = o_arg.value
        num_ += 1

    while num_ < len(params):
        _, parameter = params[num_]
        for arg in arguments.not_obligatory:
            if arg.annotation == parameter.annotation:
                func_args[parameter.name] = arg.value
        num_ += 1
    await run_func_as_async(function, **func_args)
