import requests
import json
from datetime import datetime
from django.conf import settings
from wagtail.core.models import Site

import logging
from wagtail.core import blocks
from webspace.cms import constants

logger = logging.getLogger('email')


class SendGrid(object):

    @staticmethod
    def send_email_data(receiver_email, data, hostname):
        now = datetime.now()
        res = requests.post(
            "https://api.sendgrid.com/v3/mail/send",
            data=json.dumps({
                "from": {
                    "email": constants.STUDIO_EMAIL,
                    "name": "Notification %s" % constants.STUDIO_NAME
                },
                "personalizations": [
                    {
                        "to": [{"email": receiver_email}],
                        "custom_args": data,
                        "send_at": int(datetime.timestamp(now)),
                        "dynamic_template_data": {
                            "subject": "Notification %s" % hostname,
                            "data": data
                        }
                    }
                ],
                "template_id": "d-8cbd3714e87f4075a193b4c8fc0c8c78"
            }),
            headers={
                "Authorization": "Bearer " + settings.SENDGRID_SK,
                "Content-Type": "application/json",
            }
        )
        if res.status_code >= 400:
            logger.error('Email not send')
            logger.error(str(res.content))
        else:
            logger.debug('Email send')


class EmailActionValue(blocks.StructValue):
    def run(self, request, form_instance, form_data):
        email_receiver = self.get('email_receiver')
        site = Site.find_for_request(request)

        SendGrid.send_email_data(
            email_receiver,
            {'data': form_data},
            site.hostname
        )


class EmailAction(blocks.StructBlock):
    email_receiver = blocks.CharBlock(required=False)

    class Meta:
        value_class = EmailActionValue
