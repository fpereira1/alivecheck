#!/usr/bin/env python

import os, sys, time, urllib2, smtplib

smtp = 'localhost'
sender = os.getlogin() + '@' + smtp
admin_email = 'youremail@example.com'

verbose = False

def check(url, string_to_check):
	if 'http://' not in url:
		url = 'http://' + url

	data = urllib2.urlopen(url).read()
	if string_to_check in data:
		status = 1
		print string_to_check + ' found in ' + url
	else:
		status = 0
		msg = "Error finding " + string_to_check + " in " + url
		# data = data.replace('</body>', signature + '</body>')
		d = open('debug.html', 'w')
		d.write(data)
		d.close()
		if verbose:
			print "Debug file created, please check it for more details"
		try:
			server = smtplib.SMTP(smtp)
			server.sendmail(sender, admin_email, msg)
			server.quit()
		except Exception, e:
			if verbose:
				print "Unable to send email using " + smtp + ": " + e.strerror
		print msg

	print '[OK]' if status else '[ERROR]'
	
	log(url, status)

def log(url, status):
	logfile =  'alivecheck.log'
	log = open(logfile, 'a')
	log.write(str(status) + ',' + url + ',' + str(int(time.time())) + os.linesep)
	log.close()
	if verbose:
		print logfile + " saved"

def usage():
	print sys.argv[0] + ' url string_to_check'

def main():
	if sys.argv[1] and sys.argv[2]:
		url = sys.argv[1]
		string_to_check = sys.argv[2]
		check(url, string_to_check);
	else:
		usage()


if verbose:
	# print os.linesep
	print 'Verbose enabled' + os.linesep


main();
