#! /usr/bin/env python2


#The scheduler to use.
#To list them: for s in schedulers/*_scheduler.py ; do basename -s .py $s; done
scheduler = {
	"name":'easy_backfill_scheduler',
	"progressbar": False
	}

#Force the number of available processors in the simulated parallel machine
#num_processors = 80640

#should some stats have to be computed?
stats = False


