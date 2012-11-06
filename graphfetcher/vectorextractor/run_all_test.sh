#!/bin/bash
#
# Run all the tests
# Copyright (C) 2012 Yamauchi, Hitoshi
# For Rebecca from Hitoshi the fool
#

# English Writer
#   test_linkvectorextractor_en_en_0.py
#   test_linkvectorextractor_en_de_0.py
#   test_linkvectorextractor_en_ja_0.py

# German Writer
#   test_linkvectorextractor_de_en_0.py
#   test_linkvectorextractor_de_de_0.py
#   test_linkvectorextractor_de_ja_0.py

# Japanese Writer
#   test_linkvectorextractor_ja_en_0.py
#   test_linkvectorextractor_ja_de_0.py
#   test_linkvectorextractor_ja_ja_0.py


TEST_PY="test_linkvectorextractor_en_en_0.py 	\
test_linkvectorextractor_en_en_2.py 		\
test_linkvectorextractor_en_de_0.py		\
test_linkvectorextractor_en_ja_0.py		\
test_linkvectorextractor_de_en_0.py		\
test_linkvectorextractor_de_de_0.py		\
test_linkvectorextractor_de_ja_0.py		\
test_linkvectorextractor_ja_en_0.py		\
test_linkvectorextractor_ja_de_0.py		\
test_linkvectorextractor_ja_ja_0.py		\
"

for tpy in ${TEST_PY}
do
    python ${tpy}
done
