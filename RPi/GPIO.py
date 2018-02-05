# -*- coding: utf-8 -*-
"""
GPIO.setmode(GPIO.BCM)
# 输出模式
GPIO.setup(18,GPIO.OUT)
GPIO.output(18, GPIO.HIGH)
"""
import logging

print "\n YOU SHOULD NOT SEE THIS WHEN RUNNING\n"

BCM="BCM"
OUT="OUT"
HIGH="HIGH"

def use_logging(func):
	def wrapper(*args, **kwargs):
		#logging.warn("%s is running" % func.__name__)
		logging.warn("\n YOU SHOULD NOT SEE THIS IF NOT DEBUGING")
		return func(*args)
	return wrapper

@use_logging
def setmode(mode):
	print "set mode%s"%str(mode)


@use_logging
def setup(num,mode):
	print "setup %d %s"%(num,str(mode))


@use_logging
def output(num,mode):
	print "output %d %s"%(num,str(mode))



@use_logging
def cleanup():
	print "cleanup "