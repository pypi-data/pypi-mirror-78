from tensorflow.python.ops import array_ops

def kronecker_product(mat1, mat2):
  """Computes the Kronecker product two matrices."""
  m1, n1 = mat1.get_shape().as_list()
  mat1_rsh = array_ops.reshape(mat1, [m1, 1, n1, 1])
  m2, n2 = mat2.get_shape().as_list()
  mat2_rsh = array_ops.reshape(mat2, [1, m2, 1, n2])
  return array_ops.reshape(mat1_rsh * mat2_rsh, [m1 * m2, n1 * n2])
def kronecker_product_b1(mat1, mat2):
  """Computes the Kronecker product two matrices, assuming batchdim(mat1)=1."""
  m1, n1 = mat1.get_shape().as_list()[1:]
  mat1_rsh = array_ops.reshape(mat1, [-1,m1, 1, n1, 1])
  m2, n2 = mat2.get_shape().as_list()
  mat2_rsh = array_ops.reshape(mat2, [1, m2, 1, n2])
  return array_ops.reshape(mat1_rsh * mat2_rsh, [-1,m1 * m2, n1 * n2])
def kronecker_product_b2(mat1, mat2):
  """Computes the Kronecker product two matrices, assuming batchdim(mat2)=1."""
  m1, n1 = mat1.get_shape().as_list()
  mat1_rsh = array_ops.reshape(mat1, [m1, 1, n1, 1])
  m2, n2 = mat2.get_shape().as_list()[1:]
  mat2_rsh = array_ops.reshape(mat2, [-1,1, m2, 1, n2])
  return array_ops.reshape(mat1_rsh * mat2_rsh, [-1,m1 * m2, n1 * n2])
def kronecker_product_bb(mat1, mat2):
  """Computes the Kronecker product two matrices, assuming batchdim(mat1/2)=1."""
  m1, n1 = mat1.get_shape().as_list()[1:]
  mat1_rsh = array_ops.reshape(mat1, [-1, m1, 1, n1, 1])
  m2, n2 = mat2.get_shape().as_list()[1:]
  mat2_rsh = array_ops.reshape(mat2, [-1, 1, m2, 1, n2])
  return array_ops.reshape(mat1_rsh * mat2_rsh, [-1,m1 * m2, n1 * n2])
def kronecker_product_b1fx1(mat1, mat2):
  """Computes the Kronecker product two matrices, assuming batchdim(mat1)=1."""
  f1, m1, n1 = mat1.get_shape().as_list()[1:]
  mat1_rsh = array_ops.reshape(mat1, [-1,f1,m1, 1, n1, 1])
  m2, n2 = mat2.get_shape().as_list()
  mat2_rsh = array_ops.reshape(mat2, [1, m2, 1, n2])
  return array_ops.reshape(mat1_rsh * mat2_rsh, [-1,f1,m1 * m2, n1 * n2])



#from (or based on)
#https://github.com/tensorflow/tensorflow/blob/r1.8/tensorflow/contrib/kfac/python/ops/utils.py

