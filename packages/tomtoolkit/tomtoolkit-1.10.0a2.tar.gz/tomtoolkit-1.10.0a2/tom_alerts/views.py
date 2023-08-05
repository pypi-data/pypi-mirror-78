import json

from django.views.generic.edit import FormView, DeleteView
from django.views.generic.base import TemplateView, View
from django.db import IntegrityError
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.cache import cache
from guardian.shortcuts import assign_perm
from django_filters.views import FilterView
from django_filters import FilterSet, ChoiceFilter, CharFilter

from tom_alerts.models import BrokerQuery
from tom_alerts.alerts import get_service_class, get_service_classes


class BrokerQueryCreateView(LoginRequiredMixin, FormView):
    """
    View for creating a new query to a broker. Requires authentication.
    """
    template_name = 'tom_alerts/query_form.html'

    def get_broker_name(self):
        """
        Returns the broker specified in the request

        :returns: Broker name
        :rtype: str
        """
        if self.request.method == 'GET':
            return self.request.GET.get('broker')
        elif self.request.method == 'POST':
            return self.request.POST.get('broker')

    def get_form_class(self):
        """
        Returns the form class to use in this view. The form class will be the one defined in the specific broker
        module for which a new query is being created.
        """
        broker_name = self.get_broker_name()

        if not broker_name:
            raise ValueError('Must provide a broker name')

        return get_service_class(broker_name).form

    def get_form(self):
        """
        Returns an instance of the form to be used in this view.

        :returns: Form instance
        :rtype: django.forms.Form
        """
        form = super().get_form()
        form.helper.form_action = reverse('tom_alerts:create')
        return form

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.

        :returns: dict of initial values
        :rtype: dict
        """
        initial = super().get_initial()
        initial['broker'] = self.get_broker_name()
        return initial

    def form_valid(self, form):
        """
        Saves the associated ``BrokerQuery`` and redirects to the ``BrokerQuery`` list.
        """
        form.save()
        return redirect(reverse('tom_alerts:list'))


class BrokerQueryUpdateView(LoginRequiredMixin, FormView):
    """
    View that handles the modification of a previously saved ``BrokerQuery``. Requires authentication.
    """
    template_name = 'tom_alerts/query_form.html'

    def get_object(self):
        """
        Returns the ``BrokerQuery`` object that corresponds with the ID in the query path.

        :returns: ``BrokerQuery`` object
        :rtype: ``BrokerQuery``
        """
        return BrokerQuery.objects.get(pk=self.kwargs['pk'])

    def get_form_class(self):
        """
        Returns the form class to use in this view. The form class will be the one defined in the specific broker
        module for which the query is being updated.
        """
        self.object = self.get_object()
        return get_service_class(self.object.broker).form

    def get_form(self):
        """
        Returns an instance of the form to be used in this view.

        :returns: Form instance
        :rtype: django.forms.Form
        """
        form = super().get_form()
        form.helper.form_action = reverse(
            'tom_alerts:update', kwargs={'pk': self.object.id}
        )
        return form

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view. Initial data for this form consists of the name of
        the broker that the query is for.

        :returns: dict of initial values
        :rtype: dict
        """
        initial = super().get_initial()
        initial.update(self.object.parameters_as_dict)
        initial['broker'] = self.object.broker
        return initial

    def form_valid(self, form):
        """
        Saves the associated ``BrokerQuery`` and redirects to the ``BrokerQuery`` list.
        """
        form.save(query_id=self.object.id)
        return redirect(reverse('tom_alerts:list'))


class BrokerQueryFilter(FilterSet):
    """
    Defines the available fields for filtering the list of broker queries.
    """
    broker = ChoiceFilter(
        choices=[(k, k) for k in get_service_classes().keys()]
    )
    name = CharFilter(lookup_expr='icontains')

    class Meta:
        model = BrokerQuery
        fields = ['broker', 'name']


class BrokerQueryListView(FilterView):
    """
    View that displays all saved ``BrokerQuery`` objects.
    """
    model = BrokerQuery
    template_name = 'tom_alerts/brokerquery_list.html'
    filterset_class = BrokerQueryFilter

    def get_context_data(self, *args, **kwargs):
        """
        Adds the brokers available to the TOM to the context dictionary.

        :returns: context
        :rtype: dict
        """
        context = super().get_context_data(*args, **kwargs)
        context['installed_brokers'] = get_service_classes()
        return context


class BrokerQueryDeleteView(LoginRequiredMixin, DeleteView):
    """
    View that handles the deletion of a saved ``BrokerQuery``. Requires authentication.
    """
    model = BrokerQuery
    success_url = reverse_lazy('tom_alerts:list')


class RunQueryView(TemplateView):
    """
    View that handles the running of a specific ``BrokerQuery``.
    """
    template_name = 'tom_alerts/query_result.html'

    def get_context_data(self, *args, **kwargs):
        """
        Runs the ``fetch_alerts`` method specific to the given ``BrokerQuery`` and adds the matching alerts to the
        context dictionary.

        :returns: context
        :rtype: dict
        """
        context = super().get_context_data()
        query = get_object_or_404(BrokerQuery, pk=self.kwargs['pk'])
        broker_class = get_service_class(query.broker)()
        alerts = broker_class.fetch_alerts(query.parameters_as_dict)
        context['alerts'] = []
        query.last_run = timezone.now()
        query.save()
        context['query'] = query
        try:
            while len(context['alerts']) < 20:
                alert = next(alerts)
                generic_alert = broker_class.to_generic_alert(alert)
                cache.set('alert_{}'.format(generic_alert.id), json.dumps(alert), 3600)
                context['alerts'].append(generic_alert)
        except StopIteration:
            pass
        return context


class CreateTargetFromAlertView(LoginRequiredMixin, View):
    """
    View that handles the creation of ``Target`` objects from a ``BrokerQuery`` result. Requires authentication.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles the POST requests to this view. Creates a ``Target`` for each alert sent in the POST. Redirects to the
        ``TargetListView`` if multiple targets were created, and the ``TargetUpdateView`` if only one was created.
        Redirects to the ``RunQueryView`` if no ``Target`` objects. were successfully created.
        """
        query_id = self.request.POST['query_id']
        broker_name = self.request.POST['broker']
        broker_class = get_service_class(broker_name)
        alerts = self.request.POST.getlist('alerts')
        errors = []
        if not alerts:
            messages.warning(request, 'Please select at least one alert from which to create a target.')
            return redirect(reverse('tom_alerts:run', kwargs={'pk': query_id}))
        for alert_id in alerts:
            cached_alert = cache.get('alert_{}'.format(alert_id))
            if not cached_alert:
                messages.error(request, 'Could not create targets. Try re running the query again.')
                return redirect(reverse('tom_alerts:run', kwargs={'pk': query_id}))
            generic_alert = broker_class().to_generic_alert(json.loads(cached_alert))
            target = generic_alert.to_target()
            try:
                target.save()
                broker_class().process_reduced_data(target, json.loads(cached_alert))
                for group in request.user.groups.all().exclude(name='Public'):
                    assign_perm('tom_targets.view_target', group, target)
                    assign_perm('tom_targets.change_target', group, target)
                    assign_perm('tom_targets.delete_target', group, target)
            except IntegrityError:
                messages.warning(request, f'Unable to save {target.name}, target with that name already exists.')
                errors.append(target.name)
        if (len(alerts) == len(errors)):
            return redirect(reverse('tom_alerts:run', kwargs={'pk': query_id}))
        elif (len(alerts) == 1):
            return redirect(reverse(
                'tom_targets:update', kwargs={'pk': target.id})
            )
        else:
            return redirect(reverse(
                'tom_targets:list')
            )
