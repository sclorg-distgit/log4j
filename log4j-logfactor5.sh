#!/bin/sh
# 
# LogFactor5 (log4j) startup script
#
# JPackage Project <http://www.jpackage.org/>
# $Id$

# Source functions library
if [ -f /usr/share/java-utils/java-functions ] ; then 
  . /usr/share/java-utils/java-functions
else
  echo "Can't find functions library, aborting"
  exit 1
fi

# Configuration
MAIN_CLASS=org.apache.log4j.lf5.StartLogFactor5
BASE_JARS="log4j xml-commons-apis jaxp_parser_impl"

# Set parameters
set_jvm
set_classpath $BASE_JARS
set_flags $BASE_FLAGS
set_options $BASE_OPTIONS

# Let's start
run "$@"
