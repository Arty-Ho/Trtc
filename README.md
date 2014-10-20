# coverage
coverage run trtc_check.py trtc_file 1000 2000 500 1000

coverage report -m
Name         Stmts   Miss  Cover   Missing
------------------------------------------
trtc_check      90     16    82%   43, 48, 56, 73, 80-81, 85-86, 89-95, 120


# add unit test
# coverage
coverage run trtc_unit_test.py
.color not match
trtc:  red
check: green
trtc_tp:  1920
check_tp: 1920
trtc_tc:  920
check_tc: 920
.color not match
trtc:  yellow
check: green
trtc_tp:  1920
check_tp: 1920
trtc_tc:  920
check_tc: 920
..token buckets not match
trtc:  green
check: green
trtc_tp:  1920
check_tp: 1920
trtc_tc:  980
check_tc: 920
.token buckets not match
trtc:  green
check: green
trtc_tp:  1980
check_tp: 1920
trtc_tc:  920
check_tc: 920
........
----------------------------------------------------------------------
Ran 13 tests in 0.002s

OK

# report
coverage report -m
Name             Stmts   Miss  Cover   Missing
----------------------------------------------
trtc_check          91     29    68%   100-122, 126-142, 146-149
trtc_unit_test      55      0   100%
----------------------------------------------
TOTAL              146     29    80%
