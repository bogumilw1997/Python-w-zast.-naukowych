import numpy as np
import tensorflow as tf
import timeit

N=1024
x_np=np.random.rand(N,N)
x_tf=tf.random.uniform((N,N))

print(x_np.dtype, x_tf.dtype)

SETUP_CODE = '''
import numpy as np
import tensorflow as tf

N=1024
x_np=np.random.rand(N,N)
x_tf=tf.random.uniform((N,N))
'''

TEST_NP = '''
x=x_np@x_np
    '''
TEST_TF = '''
x=x_tf@x_tf
    '''

#print(timeit.timeit(setup=SETUP_CODE, stmt=TEST_TF, number=10))

