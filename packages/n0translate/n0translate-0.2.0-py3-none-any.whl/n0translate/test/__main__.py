import sys
import os
mydir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, mydir)

import test_n0translate
test_n0translate.main()
