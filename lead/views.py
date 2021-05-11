from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Lead, Agent, Category
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateForm, CreateFormModel, CustomUserCreationForm, AssignAgentForm, LeadCategoryUpdateForm
from django.views import generic
from django.core.mail import send_mail
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganiserAndLoginRequiredMixin

# Create your views here.

class SignupView(generic.CreateView):
  template_name = 'registration/signup.html'
  form_class = CustomUserCreationForm

  def get_success_url(self):
    return reverse('login')


class LandingTemplateView(generic.TemplateView):
  template_name = 'landing.html'


class LeadListView(LoginRequiredMixin, generic.ListView):
  
  template_name = 'lead/lead_list.html'
  context_object_name = 'leads'

  def get_queryset(self):
    user = self.request.user
    if user.is_organiser:
      queryset = Lead.objects.filter(organisation=user.userprofile, agent__isnull=False)
    else:
      queryset = Lead.objects.filter(
          organisation=user.agent.organisation, agent__isnull=False)
      # filter for the agent that is logged in
      queryset = queryset.filter(agent__user=user)
    return queryset
  
  def get__context_data(self, **kwargs):
    context = super(LeadListView, self).get__context_data(**kwargs)
    user = self.request.user
    if user.is_organiser:
      queryset = Lead.objects.filter(
        organisation=user.userprofile,agent__isnull=True
      )
      context.update({
          "unassigned_leads": queryset
      })
    return context


class CategoryListView(LoginRequiredMixin, generic.ListView):
  template_name = 'lead/category_list.html'
  context_object_name = 'category_list'

  # def get_context_data(self, **kwargs):
  #   context = super(CategoryListView, self).get_context_data(**kwargs)
  #   user = self.request.user
  #   if user.is_organiser:
  #     queryset = Category.objects.filter(
  #         organisation=user.userprofile)
  #   else:
  #     queryset = Category.objects.filter(
  #         organisation=user.agent.organisation
  #     )

  #   context.update({
  #     "unassigned_lead_count": queryset.filter(category__isnull=True).count()
  #   })
  #   return context

  def get_queryset(self):
    user = self.request.user
    if user.is_organiser:
      queryset = Category.objects.filter(
          organisation=user.userprofile)
    else:
      queryset = Category.objects.filter(
          organisation=user.agent.organisation
          )
    return queryset


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
  template_name = 'lead/category_detail.html'
  context_object_name = 'category'

  def get_queryset(self):
    user = self.request.user
    if user.is_organiser:
      queryset = Category.objects.filter(
          organisation=user.userprofile)
    else:
      queryset = Category.objects.filter(
          organisation=user.agent.organisation
      )
    return queryset


class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
  template_name = 'lead/lead_category_update.html'
  form_class = LeadCategoryUpdateForm

  def get_queryset(self):
    user = self.request.user
    if user.is_organiser:
      queryset = Lead.objects.filter(organisation=user.userprofile)
    else:
      queryset = Lead.objects.filter(organisation=user.agent.organisation)
      # filter for the agent that is logged in
      queryset = queryset.filter(agent__user=user)
    return queryset

  def get_success_url(self):
    return reverse('lead:lead-detail', kwargs={"pk":self.get_object().id})




class AssignAgentView(OrganiserAndLoginRequiredMixin, generic.FormView):
  template_name = 'lead/assign_lead.html'
  form_class = AssignAgentForm

  def get_form_kwargs(self):
    return {
      "request": self.request
    }

  def get_success_url(self):
    return reverse('lead:lead-list')

  def form_valid(self, form):
    agent = form.cleaned_data['agent']
    lead = Lead.objects.get(id=self.kwargs['pk'])
    lead.agent = agent
    lead.save()
    return super(AssignAgentView, self).form_valid(form)




class LeadDetailView(LoginRequiredMixin, generic.DetailView):
  template_name = 'lead/lead_detail.html'
  context_object_name = 'lead'

  def get_queryset(self):
    user = self.request.user
    if user.is_organiser:
      queryset = Lead.objects.filter(organisation=user.userprofile)
    else:
      queryset = Lead.objects.filter(organisation=user.agent.organisation)
      # filter for the agent that is logged in
      queryset = queryset.filter(agent__user=user)
    return queryset


class LeadCreateView(OrganiserAndLoginRequiredMixin, generic.CreateView):
  template_name = 'lead/create_lead.html'
  form_class = CreateFormModel

  def get_success_url(self):
    return reverse('lead:lead-list')

  def form_valid(self, form):
    lead = form.save(commit=False)
    lead.organisation = self.request.user.userprofile
    lead.save()
    send_mail(
      subject="A lead has been created",
      message="Go to the site to see the new lead",
      from_email="test@example.com",
      recipient_list= ['test2@example.com']
    )
    return super(LeadCreateView, self).form_valid(form)


class LeadUpdateView(OrganiserAndLoginRequiredMixin, generic.UpdateView):
  template_name = 'lead/update_lead.html'
  form_class = CreateFormModel

  def get_queryset(self):
    user = self.request.user
    if user.is_organiser:
      queryset = Lead.objects.filter(organisation=user.userprofile)
    else:
      queryset = Lead.objects.filter(organisation=user.agent.organisation)
      # filter for the agent that is logged in
      queryset = queryset.filter(agent__user=user)
    return queryset
    
  def get_success_url(self):
    return reverse('lead:lead-list')




  
  



class LeadDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
  template_name = 'lead/delete_lead.html'

  def get_queryset(self):
    user = self.request.user
    if user.is_organiser:
      queryset = Lead.objects.filter(organisation=user.userprofile)
    else:
      queryset = Lead.objects.filter(organisation=user.agent.organisation)
      # filter for the agent that is logged in
      queryset = queryset.filter(agent__user=user)
    return queryset

  def get_success_url(self):
    return reverse('lead:lead-list')

  

