from django.db import models

# Create your models here.


class User(models.Model):
    accountname = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    accepted = models.PositiveIntegerField(default=0)
    submitted = models.PositiveIntegerField(default=0)

    def __unicode__(self):  # __str__ in py3
        return self.accountname


class OnlineOJ(models.Model):
    name = models.CharField(max_length=50)
    link = models.URLField()

    def __unicode__(self):
        return self.name


class Problem(models.Model):
    oj = models.ForeignKey(OnlineOJ, on_delete=models.CASCADE)
    id = models.PositiveIntegerField(primary_key=True)
    number = models.PositiveIntegerField()
    submitted = models.PositiveIntegerField(default=0)
    accepted = models.PositiveIntegerField(default=0)
    submitted_on_oringin = models.PositiveIntegerField(default=0)
    accepted_on_oringin = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=50)
    time_limit = models.CharField(max_length=20, blank=True)
    mem_limit = models.CharField(max_length=20, blank=True)
    detail = models.CharField(max_length=2000)
    sample = models.CharField(max_length=1000, blank=True)
    sampleinput = models.CharField(max_length=500, default='')
    sampleoutput = models.CharField(max_length=500, default='')
    source = models.CharField(max_length=200, default='')

    def __unicode__(self):
        return str(self.id)


class Status(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    subtime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100)
    time = models.PositiveIntegerField(default=0)
    mem = models.PositiveIntegerField(default=0)
    lan = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    codelength = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return str(id) + ':' + self.problem.title


class Contest(models.Model):
    title = models.CharField(max_length=200)
    assignlimit = models.DateTimeField()
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    candidates = models.ManyToManyField(User, through="ContestLog",
                                        through_fields=(
                                            "contest", "candidate"),
                                        )

    def __unicode__(self):
        return self.title


class ContestProblem(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    point = models.IntegerField()
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.contest.title + self.problem.title


class ContestProblemStatus(models.Model):
    problem = models.ForeignKey(ContestProblem, on_delete=models.CASCADE)
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)
    laststatus = models.CharField(max_length=100, default="Unsubmitted")
    starttime = models.DateTimeField(auto_now_add=True)
    endtime = models.DateTimeField(blank=True)

    def __unicode__(self):
        return self.problem.problem.title + str(self.status)


class ContestLog(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    point = models.IntegerField(default=0)
    problemsolved = models.ManyToManyField(ContestProblem, blank=True)

    def __unicode__(self):
        return self.contest.title + self.candidate.accountname
