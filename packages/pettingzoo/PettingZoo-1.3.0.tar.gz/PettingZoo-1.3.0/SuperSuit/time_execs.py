import timeit
import numpy as np
print(timeit.timeit('np.array(a)', "import numpy as np; a = [1,2,3,4,5,6,7,8,9,10]*10", number=10000))
print(timeit.timeit('np.array(a,dtype=np.float64)', "import numpy as np; a = [1,2,3,4,5,6,7,8,9,10]*10", number=10000))
print(timeit.timeit('np.stack(a)', "import numpy as np; a = [1,2,3,4,5,6,7,8,9,10]*10", number=10000))
