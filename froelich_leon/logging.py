# https://adamj.eu/tech/2022/03/30/how-to-make-django-error-for-undefined-template-variables/#with-a-logging-filter-that-raises-exceptions
import logging


class MissingVariableError(Exception):
    """
    A variable was missing from a template. Used as an alternative to
    django.template.base.VariableDoesNotExist, because that exception has some
    meaning within the template engine.
    """


class MissingVariableErrorFilter(logging.Filter):
    """
    Take log messages from Django for missing template variables and turn them
    into exceptions.
    """

    ignored_prefixes = (
        "admin/",
        "auth/",
        "debug_toolbar/",
        "django/",
        "wagtail/",
        "wagtailadmin/",
        "wagtailblog/",
        "wagtailembeds/",
        "wagtailimages/",
        "wagtailsites/",
        "wagtailusers/",
    )

    def filter(self, record):
        if record.msg.startswith("Exception while resolving variable "):
            variable_name, template_name = record.args
            if not template_name.startswith(self.ignored_prefixes):
                raise MissingVariableError(
                    f"{variable_name!r} missing in {template_name!r}"
                ) from None # suppress context and cause
        return False
