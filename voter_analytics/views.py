from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter  # Ensure you import the Voter model
import plotly
import plotly.express as px

class VoterListView(ListView):
    '''View to show a list of voters.'''

    template_name = 'voter_analytics/voter_list.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100  # Show 100 voters per page

    def get_queryset(self):
        '''Limit the results based on filtering criteria.'''

        # Default query set is all of the records:
        qs = super().get_queryset()

        # Handle search form/URL parameters:
        if 'party' in self.request.GET:
            party = self.request.GET['party']
            qs = qs.filter(partyAffiliation__icontains=party)

        if 'min_dob' in self.request.GET and self.request.GET['min_dob']:
            min_dob = self.request.GET['min_dob']
            qs = qs.filter(dob__gte=f"{min_dob}-01-01")

        if 'max_dob' in self.request.GET and self.request.GET['max_dob']:
            max_dob = self.request.GET['max_dob']
            qs = qs.filter(dob__lte=f"{max_dob}-12-31")

        if 'voter_score' in self.request.GET and self.request.GET['voter_score']:
            voter_score = self.request.GET['voter_score']
            qs = qs.filter(voterScore=voter_score)

        elections = self.request.GET.getlist('elections')
        if elections:
            if 'election1' in elections:
                qs = qs.filter(vote1=True)
            if 'election2' in elections:
                qs = qs.filter(vote2=True)
            if 'election3' in elections:
                qs = qs.filter(vote3=True)
            if 'election4' in elections:
                qs = qs.filter(vote4=True)
            if 'election5' in elections:
                qs = qs.filter(vote5=True)
        return qs.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['years'] = list(range(1900, 2024))
        context['voterscores'] = list(range(0, 6))
        context['selected_elections'] = self.request.GET.getlist('elections')
        context['form_action'] = self.request.path
        return context

class VoterDetailView(DetailView):
    model = Voter
    template_name = "voter_analytics/voter_details.html"
    context_object_name = "voter"

class GraphsView(ListView):
    template_name="voter_analytics/graphs.html"
    model = Voter
    context_object_name = "voters"

    def get_queryset(self):
        '''Limit the results based on filtering criteria.'''

        # Default query set is all of the records:
        qs = super().get_queryset()

        # Handle search form/URL parameters:
        if 'party' in self.request.GET:
            party = self.request.GET['party']
            qs = qs.filter(partyAffiliation__icontains=party)

        if 'min_dob' in self.request.GET and self.request.GET['min_dob']:
            min_dob = self.request.GET['min_dob']
            qs = qs.filter(dob__gte=f"{min_dob}-01-01")

        if 'max_dob' in self.request.GET and self.request.GET['max_dob']:
            max_dob = self.request.GET['max_dob']
            qs = qs.filter(dob__lte=f"{max_dob}-12-31")

        if 'voter_score' in self.request.GET and self.request.GET['voter_score']:
            voter_score = self.request.GET['voter_score']
            qs = qs.filter(voterScore=voter_score)

        elections = self.request.GET.getlist('elections')
        if elections:
            if 'election1' in elections:
                qs = qs.filter(vote1=True)
            if 'election2' in elections:
                qs = qs.filter(vote2=True)
            if 'election3' in elections:
                qs = qs.filter(vote3=True)
            if 'election4' in elections:
                qs = qs.filter(vote4=True)
            if 'election5' in elections:
                qs = qs.filter(vote5=True)
        return qs.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()
        
        if voters:
            dobs = [int(voter.dob.split('-')[0]) for voter in voters]
            fig1 = px.histogram(x=dobs, title='Distribution of Voters by Year of Birth', width=900, height=750)
            BirthYearBarGraph_div = plotly.offline.plot(fig1, auto_open=False, output_type='div')
            context["BirthYearBarGraph"] = BirthYearBarGraph_div

            party_counts = {}
            for voter in voters:
                if voter.partyAffiliation not in party_counts:
                    party_counts[voter.partyAffiliation] = 1
                else:
                    party_counts[voter.partyAffiliation] += 1
            fig2 = px.pie(names=list(party_counts.keys()), values=list(party_counts.values()), title='Distribution of Voters by Party Affiliation', width=900, height=750)
            PartyDistributionPieChart_div = plotly.offline.plot(fig2, auto_open=False, output_type='div')
            context["PartyDistributionPieChart"] = PartyDistributionPieChart_div

            election_data = ["v20state", "v21town", "v21primary", "v22general", "v23town"]
            election_counts = [0,0,0,0,0]
            for voter in voters:
                if voter.vote1:
                    election_counts[0] += 1
                if voter.vote2:
                    election_counts[1] += 1
                if voter.vote3:
                    election_counts[2] += 1
                if voter.vote4:
                    election_counts[3] += 1
                if voter.vote5:
                    election_counts[4] += 1
            print(election_counts)
            fig3 = px.bar(x=election_data, y=election_counts, title='Distribution of Voters by Participation in Elections', labels={'x': "Elections", "y": "Number of votes"}, width=900, height=750)
            ElectionParticipationChar = plotly.offline.plot(fig3, auto_open=False, output_type='div')
            context['ElectionParticipationChar'] = ElectionParticipationChar

            
            context['years'] = list(range(1900, 2024))
            context['voterscores'] = list(range(0, 6))
            context['selected_elections'] = self.request.GET.getlist('elections')
            context['form_action'] = self.request.path
            return context
