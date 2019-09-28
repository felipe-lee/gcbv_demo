# -*- coding: utf-8 -*-
"""
Common Views
"""
from copy import deepcopy
from typing import Any, Dict, TypeVar

from django.db.models import ForeignKey, QuerySet
from django.forms import Form
from django.http import Http404, HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import ugettext_lazy as _
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import FormMixin
from six import iteritems


class HomeView(TemplateView):
    """
    Render home page
    """
    template_name = 'common/home.html'


def home_view(request: HttpRequest) -> HttpResponse:
    """
    Render todo home page
    :param request: user wsgi request
    :return: home page
    """
    return render(request=request, template_name='common/home.html')


class ProcessGetFormMixin(FormMixin):
    """
    Mixin to handle form GET submissions. Based on loosely on ProcessFormView.
    """
    http_method_names = ['get', 'head', 'options']

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Set up form and if data was passed in, validate it, otherwise render page with form.
        :param request: wsgi request
        :return: response for user
        """
        form = self.get_form()

        if request.GET:
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

        return self.render_to_response(self.get_context_data(form=form))

    def get_form_kwargs(self) -> Dict[str, Any]:
        """
        Get kwargs to instantiate form
        :return: form kwargs
        """
        kwargs = super().get_form_kwargs()

        if self.request.GET:
            kwargs['data'] = deepcopy(self.request.GET)

        return kwargs


class GetFormView(TemplateResponseMixin, ProcessGetFormMixin, View):
    """
    View to prepare a form, and either render it or process its submission data.
    """


TForm = TypeVar('TForm', bound=Form)


class FormListView(ProcessGetFormMixin, ListView):
    """
    View to render/process a form and list out model data.
    """
    # boolean indicating if queryset should be retrieved first-time through, i.e. form hasn't been submitted
    retrieve_queryset_first_time: bool = True

    def setup(self, request: HttpRequest, *args, **kwargs) -> None:
        """
        Add form to class variables that are easily accessible
        :param request: wsgi request
        """
        super().setup(request, *args, **kwargs)

        self.form: TForm

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Set up initial object list, which can be filtered later if need be.
        :param request: wsgi request
        :return: template with form, and possibly a queryset
        """
        if self.retrieve_queryset_first_time:
            self.object_list = self.get_queryset()

            self.check_for_empty_queryset()

        return super().get(request, *args, **kwargs)

    def form_valid(self, form: TForm) -> HttpResponse:
        """
        Retrieves/filters the object list upon successful form submission.
        :param form: validated form
        :return: template with form and list of data
        """
        if not self.retrieve_queryset_first_time:
            self.object_list = self.get_queryset()

        self.form = form
        self.object_list = self.filter_queryset()

        # Already checked this in get, but if we have filtered, need to check if the queryset is empty now.
        self.check_for_empty_queryset()

        context = self.get_context_data(form=form)

        return self.render_to_response(context)

    def filter_queryset(self) -> QuerySet:
        """
        Filters queryset based on form data. Really just a hook for children to modify and enable filtering.
        :return: filtered queryset
        """
        return self.object_list

    def check_for_empty_queryset(self) -> None:
        """
        Checks for an empty queryset and raises an error if appropriate (based on set attrs). Basically just re-doing
        what BaseListView does on GET.
        """
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset, it's better to do a cheap query than to load the
            # unpaginated queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list

            if is_empty:
                raise Http404(_(f'Empty list and "{self.__class__.__name__}.allow_empty" is False.'))


# Code below this is in py2, django 1.11. I didn't feel like converting it since it's not good code, and it's
# "understandable" in its current state.


class MultiFormCreateView(CreateView):
    """
    This allows you to handle multiple forms on one page. It can handle forms that each have their own submit button
    and multiple forms being submitted by one button. You just have to define the attributes accordingly.

    The context names of the forms in the template will be the form class name (lowercase). All the forms will
    also be in 'forms' which is a list.

    form_classes needs to be a list of the forms (classes) you want to use.

    initial needs to be a dict, where the key is the form class and the value is a dict mapping field names to initial
    values. Ex: initial = {ForClsOne: {'field_one': 'value_one'}, FormClsTwo: {'state': 'TX}}

    prefix needs to be a dict mapping form classes to prefixes. If one is not provided for a specific form class, it
    defaults to the form class name (lowercase).

    if relative_url needs args or kwargs, you should set it in one of your methods. dispatch, post, form_valid, or a
    custom method are probably best.

    submit_names needs to be a dict mapping form classes to the 'name' of the submit button you want to use on the
    template for that form.

    submit_multiple needs to be a dict mapping the 'name' of the submit button to a list of the form classes whose forms
    would be submitted with that button. Ex: submit_multiple = {'submit_student_info': [BiographicalInfo, ClassInfo]
    """

    form_classes = []  # Required
    initial = {}  # Optional
    prefix = {}  # Optional
    relative_url = None  # Either this or success_url is required.
    submit_names = {}  # Either this one or submit_multiple are required. Both can be used.
    submit_multiple = {}  # Either this one or submit_names are required. Both can be used.

    def __init__(self, *args, **kwargs):
        """
        Sets some self attributes that will be used in the class. Checks to make sure the appropriate attributes have
        been set.
        """
        super(MultiFormCreateView, self).__init__(**kwargs)
        self.submitted_forms = []
        self.not_submitted_forms = []
        self.forms = {}
        self.instances = []
        self.use_post_data = False

        if not self.form_classes or \
            (not isinstance(self.form_classes, list) and not isinstance(self.form_classes, tuple)):
            raise NotImplementedError('form_classes must be a list or tuple.')

        if not self.submit_names and not self.submit_multiple:
            raise NotImplementedError('Either "submit_names" or "submit_multiple" must be used. Both can be used as '
                                      'well')

    def form_invalid(self, *args, **kwargs):
        """
        Super sent form but forms are self.forms now so they don't need to be passed to self.get_context_data.
        :return: Returns an http response with the context data.
        """
        return self.render_to_response(self.get_context_data())

    def form_valid(self, *args, **kwargs):
        """
        Calls save_forms method. Checks to make sure a success_url or relative_url have been provided. Then can redirect
        to the provided url.
        :return: Returns a redirect to the provided url.
        """
        self.save_forms()

        if self.relative_url:
            return redirect(self.relative_url)
        elif self.success_url:
            return redirect(self.get_success_url())
        else:
            raise NotImplementedError('Either a relative_url or a success_url need to be set.')

    def get_context_data(self, **kwargs):
        """
        Adds each form to the context.
        :return: Returns all the kwargs for the template.
        """
        kwargs['forms'] = []
        if self.forms:
            for cls, form in iteritems(self.forms):
                kwargs[cls] = form
                kwargs.get('forms').append(form)
        else:
            for form_cls in self.form_classes:
                form = self.get_form(form_class=form_cls)
                kwargs['{0}'.format(form_cls.__name__.lower())] = form
                kwargs.get('forms').append(form)

        # because we are not declaring a specific form, pulled super's super's (yes that is repeated intentionally) code
        # here to avoid conflicts.
        if self.object:
            kwargs['object'] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                kwargs[context_object_name] = self.object

        if 'view' not in kwargs:
            kwargs['view'] = self

        return kwargs

    def get_form(self, form_class=None):
        """
        :param form_class: The class of the form that is being retrieved.
        :return: Returns a form instantiated with the kwargs for the passed form_class.
        """
        return form_class(**self.get_form_kwargs(form_class=form_class))

    def get_form_kwargs(self, form_class=None, initial_data=None, model_data=None):
        """
        Gets all the kwargs that have been provided for the form_class passed.
        :param form_class: The class of the form whose kwargs are being retrieved.
        :param initial_data: Initial data that can be passed in to add more initial data.
        :param model_data: Model data that can be passed in to initialize the model instance.
        :return: Returns kwargs for the form_class passed.
        """
        kwargs = {
            'initial': self.get_initial(form_class=form_class, initial_data=initial_data),
            'prefix': self.get_prefix(form_class=form_class),
            'instance': self.get_model_instance(form_class=form_class, model_data=model_data)
        }

        if self.use_post_data:
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })

        return kwargs

    def get_initial(self, form_class=None, initial_data=None):
        """
        Checks to see if any initial data was provided for the passed form_class, either as an argument and/or in the
        'initial' attribute.
        :param form_class: The class of the form whose initial data is being retrieved.
        :param initial_data: Allows to pass in initial data to update the attribute initial data (if any).
        :return: Returns either the dict of initial data provided for the form_class passed or an empty dict.
        """
        initial = {}
        if form_class.__name__ in self.initial:
            initial_attrib_data = self.initial.get(form_class.__name__)
            if isinstance(initial_attrib_data, dict):
                initial.update(initial_attrib_data)
            else:
                raise NotImplementedError("Initial data set in the attribute needs to be in a dictionary. The data set "
                                          "for {form_class} is not a dict.".format(form_class=form_class))

        if initial_data is not None:
            if isinstance(initial_data, dict):
                initial.update(initial_data)
            else:
                raise NotImplementedError("Initial data passed in must be in a dictionary. The data for {form_class} "
                                          "is not a dict.".format(form_class=form_class))

        return initial

    def get_model_instance(self, form_class, model_data=None):
        """
        Checks to see if the model data passed in is a dict. If so, it instantiates the model with that data.
        :param form_class: The class of the form whose instance data is being retrieved.
        :param model_data: If this view is sub-classed, this param allows one to pass model_data for a specific model to
        this method without having to rewrite this logic.
        :return: Returns the instance of the model for the form_class passed.
        """
        model = form_class._meta.model

        data = {}
        if model_data is not None:
            if isinstance(model_data, dict):
                data = model_data
            else:
                raise NotImplementedError("Model data passed in must be in a dictionary. The data for {form_class} "
                                          "(model={model}) is not a dict.".format(form_class=form_class, model=model))

        return model(**data)

    def get_prefix(self, form_class=None):
        """
        Checks to see if any prefix was provided for the passed form_class.
        :param form_class: The class of the form whose prefix is being retrieved.
        :return: Returns the prefix that was provided for the passed form_class, or returns the form_class name
        (lowercase) as a prefix.
        """
        if form_class.__name__ in self.prefix:
            prefix = self.prefix.get(form_class.__name__)
        else:
            prefix = form_class.__name__.lower()

        return prefix

    def post(self, request, *args, **kwargs):
        """
        Calls method to figure out which forms need to be validated. Validates all the forms and adds them to
        self.forms. If all the forms were not valid, it adds the rest of the forms (the ones that were not submitted)
        to self.forms as well (so that they can all be passed to template again). Then calls appropriate method
        depending on whether all the forms were valid or not.
        :return: Returns the appropriate method depending on the validity of the submitted forms.
        """
        self.use_post_data = True
        self.select_forms()
        all_forms_valid = True
        for form_cls in self.submitted_forms:
            form = self.get_form(form_class=form_cls)
            if not form.is_valid():
                all_forms_valid = False
            self.forms['{0}'.format(form_cls.__name__.lower())] = form

        if all_forms_valid:
            return self.form_valid()
        else:
            self.use_post_data = False
            for form_cls in self.not_submitted_forms:
                form = self.get_form(form_class=form_cls)
                self.forms['{0}'.format(form_cls.__name__.lower())] = form

            return self.form_invalid()

    def save_forms(self, *args, **kwargs):
        """
        Saves each form. Separated into its own method to make it easier to override if special processing is needed.
        """
        for cls, form in self.forms:
            self.instances.append(form.save())  # form.save() returns the instance of the model with the data

    def select_forms(self):
        """
        New method that finds the list of forms that should be validated. Doesn't return anything. Sets the form lists
        as attributes of this cbv.
        """
        for s_key, form_list in iteritems(self.submit_multiple):
            if s_key in self.request.POST:
                self.submitted_forms = form_list

        for form_cls in self.form_classes:
            if form_cls.__name__ in self.submit_names:
                if self.submit_names.get(form_cls.__name__) in self.request.POST:
                    self.submitted_forms = [form_cls]

        for form in self.form_classes:
            if form not in self.submitted_forms:
                self.not_submitted_forms.append(form)


class MultiFormUpdateView(MultiFormCreateView):
    """
    model will be the model that is updated (alternatively you can define a queryset). The form that is form the model
    will be updated while any other form in form_classes will be creating a new object. If a form is related to the
    target model via a foreignkey, an instance of the target model will be used to instantiate the form. If none of the
    forms are for or related to the target model, you should use MultiFormCreateView.
    """
    form_classes = []  # Required
    initial = {}  # Optional
    model = None  # Required
    prefix = {}  # Optional
    relative_url = None  # Either this or success_url is required.
    submit_names = {}  # Either this one or submit_multiple are required. Both can be used.
    submit_multiple = {}  # Either this one or submit_names are required. Both can be used.

    def dispatch(self, request, *args, **kwargs):
        """
        Sets self.object since it is needed for both get and post methods.
        :return: Returns super's dispatch.
        """
        self.object = self.get_object()
        return super(MultiFormUpdateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Skips super's get method since this cbv needs self.object and the super sets self.object = None in its get
        method.
        :return: Returns an http response with the context data.
        """
        return self.render_to_response(self.get_context_data())

    def get_model_instance(self, form_class, model_data=None):
        """
        Overwrites super's method since one of the instances is already set and it would make the logic strange to call
        the super when it isn't necessary.
        :param form_class: The class of the form whose instance data is being retrieved.
        :param model_data: If this view is sub-classed, this param allows one to pass model_data for a specific model to
        this method without having to rewrite this logic.
        :return: Returns the instance of the model for the form_class passed.
        """
        model = form_class._meta.model

        if model == self.model:
            instance = self.object
        else:
            all_fields = model._meta.get_fields()

            related_field_name = None
            for field in all_fields:
                if isinstance(field, ForeignKey) and field.related_model == self.model:
                    related_field_name = field.name

            data = {}
            if model_data is not None:
                if isinstance(model_data, dict):
                    data = model_data
                else:
                    raise NotImplementedError("Model data passed in must be in a dictionary. The data for {form_class} "
                                              "(model={model}) is not a dict.".format(form_class=form_class,
                                                                                      model=model))

            if related_field_name:
                data.update({
                    '{0}'.format(related_field_name): self.object,
                })

            instance = model(**data)

        return instance
