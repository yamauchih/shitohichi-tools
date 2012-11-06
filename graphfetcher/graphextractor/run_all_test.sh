#!/bin/bash
#
# Run all the tests
# Copyright (C) 2012 Yamauchi, Hitoshi
# For Rebecca from Hitoshi the fool
#

# test_00_decompose_element.py
# test_00_pretty_print_html.py
TEST_PY="test_graphextractor_de_de_0.py \
test_graphextractor_de_en_0.py \
test_graphextractor_de_ja_0.py \
test_graphextractor_en_de_0.py \
test_graphextractor_en_en_0.py \
test_graphextractor_en_ja_0.py \
test_graphextractor_ja_de_0.py \
test_graphextractor_ja_en_0.py \
test_graphextractor_ja_ja_0.py \
test_graphextractor_ja_ja_1.py \
"

for tpy in ${TEST_PY}
do
    python ${tpy}
done

