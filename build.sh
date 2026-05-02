#!/bin/bash

nuitka \
    --standalone \
    --enable-plugin=pyside6 \
    --include-qt-plugins=sensible,imageformats,platforms,multimedia,iconengines \
    --include-data-dir=images=images \
    --include-data-dir=sounds=sounds \
    --include-data-dir=databases=databases \
    --include-data-dir=reports=reports \
    --output-dir=builds \
    main.py