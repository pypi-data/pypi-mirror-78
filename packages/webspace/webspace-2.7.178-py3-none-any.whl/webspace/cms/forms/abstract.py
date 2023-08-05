import logging
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
import json
from django.core.serializers.json import DjangoJSONEncoder

from webspace.loader import get_model

Form = get_model('cms', 'Form')
FormSubmission = get_model('cms', 'FormSubmission')

logger = logging.getLogger('forms')


class FormMixin:

    def serve(self, request, *args, **kwargs):
        if request.method == 'POST' and 'form_id' in request.POST:
            try:
                form_instance = Form.objects.get(id=request.POST['form_id'])
                form = form_instance.get_form(request.POST, request.FILES, user=request.user)
                if form.is_valid():

                    logger.debug("Form is valid")

                    form_data = json.dumps(form.cleaned_data, cls=DjangoJSONEncoder)

                    for action in form_instance.actions:
                        action.value.run(request, form_instance, form_data)

                    fs = FormSubmission.objects.create(
                        form_data=form_data,
                        page=self,
                        form=form_instance
                    )
                    fs.save()

                    if form_instance.redirection_page:
                        url = form_instance.redirection_page.get_full_url()
                        logger.debug("Redirection page")
                        return HttpResponseRedirect(url)

                    if form_instance.redirection_url:
                        logger.debug("Redirection URL")
                        return HttpResponseRedirect(form_instance.redirection_url)
                else:

                    logger.debug("Form is not valid")

                    request.session['current_form_id'] = form_instance.id
                    return TemplateResponse(
                        request,
                        self.get_template(request, *args, **kwargs),
                        self.get_context(request, *args, **kwargs)
                    )
            except Form.DoesNotExist:
                pass

        logger.debug("Call super")
        request.session['current_form_id'] = None
        return super().serve(request, *args, **kwargs)

    class Meta:
        abstract = True
