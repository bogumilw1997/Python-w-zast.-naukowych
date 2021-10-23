import numpy as np
import tensorflow as tf
import timeit
from timeit import Timer

SETUP_CODE_NP = '''
import numpy as np

N=1024
x_np=np.random.rand(N,N)
'''
SETUP_CODE_TF = '''
import tensorflow as tf

N=1024
x_tf=tf.random.uniform((N,N))
'''

TEST_NP = '''
x=x_np@x_np
    '''
TEST_TF = '''
x=x_tf@x_tf
    '''

tests = 1000
t_np = timeit.timeit(setup=SETUP_CODE_NP, stmt=TEST_NP, number=tests)
t_tf = timeit.timeit(setup=SETUP_CODE_TF, stmt=TEST_TF, number=tests)

print(f'Numpy: {t_np/tests} ms')
print(f'TensorFlow: {t_tf/tests} ms')