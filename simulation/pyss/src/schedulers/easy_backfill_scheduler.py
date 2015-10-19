from common import Scheduler, CpuSnapshot, list_copy 
from base.prototype import JobStartEvent

class EasyBackfillScheduler(Scheduler):

    def __init__(self, options):
        super(EasyBackfillScheduler, self).__init__(options)
        self.cpu_snapshot = CpuSnapshot(self.num_processors, options["stats"])
        self.unscheduled_jobs = []

    def new_events_on_job_submission(self, just_submitted_job, current_time):
        """ Here we first add the new job to the waiting list. We then try to schedule
        the jobs in the waiting list, returning a collection of new termination events """
        # TODO: a probable performance bottleneck because we reschedule all the
        # jobs. Knowing that only one new job is added allows more efficient
        # scheduling here.
        self.cpu_snapshot.archive_old_slices(current_time)
        self.unscheduled_jobs.append(just_submitted_job)
        
        retl = []
        
        if (self.cpu_snapshot.free_processors_available_at(current_time) >= just_submitted_job.num_required_processors):
		for job in self._schedule_jobs(current_time):
			retl.append(JobStartEvent(current_time, job))
        
        return retl

    def new_events_on_job_termination(self, job, current_time):
        """ Here we first delete the tail of the just terminated job (in case it's
        done before user estimation time). We then try to schedule the jobs in the waiting list,
        returning a collection of new termination events """
        self.cpu_snapshot.archive_old_slices(current_time)
        self.cpu_snapshot.delTailofJobFromCpuSlices(job)
        return [
            JobStartEvent(current_time, job)
            for job in self._schedule_jobs(current_time)
        ]

    def _schedule_jobs(self, current_time):
        "Schedules jobs that can run right now, and returns them"
        jobs = self._schedule_head_of_list(current_time)
        jobs += self._backfill_jobs(current_time)
        return jobs

    def _schedule_head_of_list(self, current_time):     
        result = []
        while True:
            if len(self.unscheduled_jobs) == 0:
                break
            # Try to schedule the first job
            if self.cpu_snapshot.free_processors_available_at(current_time) >= self.unscheduled_jobs[0].num_required_processors:
                job = self.unscheduled_jobs.pop(0)
                self.cpu_snapshot.assignJob(job, current_time)
                result.append(job)
            else:
                # first job can't be scheduled
                break
        return result

    def _backfill_jobs(self, current_time):
        """
        Find jobs that can be backfilled and update the cpu snapshot.
        """
        if len(self.unscheduled_jobs) <= 1:
            return []
        
        result = []
        first_job = self.unscheduled_jobs[0]
        shadow_time = self.cpu_snapshot.jobEarliestAssignment(first_job, current_time)
        shadow_len = shadow_time - current_time
        #this can be done at the same time as jobEarliestAssignment
        extra_cpu = self.cpu_snapshot.free_processors_available_at(shadow_time)-first_job.num_required_processors
        nonextra_cpu = self.cpu_snapshot.free_processors_available_at(current_time)-extra_cpu
        if nonextra_cpu < 0:
            extra_cpu += nonextra_cpu#<=> =self.cpu_snapshot.free_processors_available_at(current_time)
            nonextra_cpu = 0

        for job in self.unscheduled_jobs[1:]:
            if job.predicted_run_time > shadow_len:
                if job.num_required_processors <= extra_cpu:
                    result.append(job)
                    self.cpu_snapshot.assignJob(job, current_time)
                    extra_cpu -= job.num_required_processors
            else:
                if job.num_required_processors <= extra_cpu+nonextra_cpu:
                    result.append(job)
                    self.cpu_snapshot.assignJob(job, current_time)
                    nonextra_cpu -= job.num_required_processors
                    if nonextra_cpu < 0:
                        extra_cpu += nonextra_cpu
                        nonextra_cpu = 0

        for job in result:
            self.unscheduled_jobs.remove(job)

        return result