#!/bin/bash

if [ $# -eq 0 ]
then
	c=$(find . -maxdepth 3 -type f -name activate)
else
	c=$(find $1 -maxdepth 3 -type f -name activate)
fi

#split list with <space> and store each element in $1,$2 so on..
set -- $c

/bin/bash --rcfile $1
