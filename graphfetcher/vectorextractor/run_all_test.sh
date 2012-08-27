#!/bin/bash
# Run all test
# Copyright (C) 2012 Hitoshi Yamauchi
#

TEST_PY="test_linkvectorextractor_en_en_0.py \
test_linkvectorextractor_en_en_1.py \
test_linkvectorextractor_ja_en_0.py \
"


for tpy in ${TEST_PY}
do
    python ${tpy}
done




