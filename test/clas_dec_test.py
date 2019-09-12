# 使用描述符作为装饰器
# 使用描述符来作装饰器的理由是__get__(self,instance,owner)
# 能够接受2个实例对象, 一个是描述符本身,还有一个是被装饰的对象
# 描述符对象作装饰器能弥补普通类作装饰器无法很好的作用于类的方法上
class tracer:
    def __init__(self, func):  # 描述符接受一个函数对象
        self.calls = 0
        self.func = func

    def __call__(self, *args, **kwargs):  # 能用于函数装饰器
        self.calls += 1
        print('tracer call %s to %s' % (self.calls, self.func.__name__), ',args:', args)
        return self.func(*args, **kwargs)

    def __get__(self, instance, owner):  # __get__ 获取2个实例对象,1个self(描述符对象) , instance(被装饰的对象)
        print('__get__')
        return wrapper(self, instance)  # 返回一个临时对象


# 包装类,接受2个参数,1个是描述符对象,用于描述符__get__的返回值
class wrapper:
    def __init__(self, desc, instance):
        self.desc = desc
        self.instance = instance

    def __call__(self, *args, **kwargs):  # 用于函数调用
        return self.desc(self.instance, *args, **kwargs)  # 调用tracer的__call__


class Person:
    def __init__(self, name='person'):
        self.name = name

    @tracer
    def lastName(self):  # lastName 是一个tracer实例
        return self.name.split()[-1]


p = Person()
print(p.lastName())
