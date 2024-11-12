# voter_analytics/models.py
# Definte the data objects for our application
from fileinput import filename
from xmlrpc.client import boolean
from django.db import models

class Voter(models.Model):
    last_name = models.TextField()
    first_name = models.TextField()
    addressStreetNumber = models.IntegerField()
    addressStreetName = models.TextField()
    addressAptNum = models.TextField()
    addressZipCode = models.IntegerField()
    dob = models.TextField()
    voterRegistration = models.TextField()
    partyAffiliation = models.TextField()
    voterScore = models.IntegerField()
    vote1 = models.BooleanField()
    vote2 = models.BooleanField()
    vote3 = models.BooleanField()
    vote4 = models.BooleanField()
    vote5 = models.BooleanField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.partyAffiliation}"


def load_data():
    Voter.objects.all().delete()

    filename = '/Users/awadkhawaja/Desktop/django/newton_voters.csv'
    f = open(filename)
    headers = f.readline() #read and discard headers
    print(headers)

    for line in f:
        try:
            fields = line.split(',')
            result = Voter(
                        last_name = fields[1],
                        first_name = fields[2],
                        addressStreetNumber = int(fields[3]),
                        addressStreetName = fields[4],
                        addressAptNum = fields[5],
                        addressZipCode = int(fields[6]),
                        dob = fields[7],
                        voterRegistration = fields[8],
                        partyAffiliation = fields[9].strip(),
                        voterScore = int(fields[16]),
                        vote1 = boolean(fields[11] == "TRUE"),
                        vote2 = boolean(fields[12] == "TRUE"),
                        vote3 = boolean(fields[13] == "TRUE"),
                        vote4 = boolean(fields[14] == "TRUE"),
                        vote5 = boolean(fields[15] == "TRUE"),
                    )
            result.save()
        except:
            print(f"Exception on {fields}")