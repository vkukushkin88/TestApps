#!/bin/bash
coverage run -m unittest discover
coverage report -m | grep -v "site-packages"
