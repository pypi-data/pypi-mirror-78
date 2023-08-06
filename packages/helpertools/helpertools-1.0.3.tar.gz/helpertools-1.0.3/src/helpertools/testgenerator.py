#import unittest
import functools


# class TestStringMethods(unittest.TestCase):
#
#     def test_upper(self):
#         self.assertEqual('foo'.upper(), 'FOO')
#
#     def test_isupper(self):
#         self.assertTrue('FOO'.isupper())
#         self.assertFalse('Foo'.isupper())
#
#     def test_split(self):
#         s = 'hello world'
#         self.assertEqual(s.split(), ['hello', 'world'])
#         # check that s.split fails when the separator is not a string
#         with self.assertRaises(TypeError):
#             s.split(2)
#
# if __name__ == '__main__':
#     unittest.main()


def generattest(func):


    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        function_name = func.__name__
        input_pram = ""
        output = ""
        error = ""
        try:
            print("args", args)
            print("kwargs", kwargs)

            output= func(*args, **kwargs)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            error=type(ex).__name__

        print(error)
        print(function_name)
        print(output)
        print(input_pram)

    return wrapper



@generattest
def divide(num1,num2):
    return num1/num2

print("test1")
divide(7,1)
print("test2")
divide(7,0)
print("test3")
divide(7,"s")
print("test4")
divide(7)
print("test4")
divide(7,key=1)









