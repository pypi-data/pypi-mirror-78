from wagtail.contrib.settings.models import register_setting
from wagtail.snippets.models import register_snippet

from webspace.loader import is_model_registered

__all__ = []

from .document.abstract import AMyDocument

if not is_model_registered('cms', 'MyDocument'):
    class MyDocument(AMyDocument):
        pass


    __all__.append('MyDocument')

# Snippets

from .snippets.icon import AIconSnippet

if not is_model_registered('cms', 'IconSnippet'):
    @register_snippet
    class IconSnippet(AIconSnippet):
        pass


    __all__.append('IconSnippet')

from .snippets.menu import AMenu, AMenuItem

if not is_model_registered('cms', 'Menu'):
    @register_snippet
    class Menu(AMenu):
        pass


    __all__.append('Menu')

if not is_model_registered('cms', 'MenuItem'):
    class MenuItem(AMenuItem):
        pass


    __all__.append('MenuItem')

from .snippets.navigation import ANavigation

if not is_model_registered('cms', 'Navigation'):
    @register_snippet
    class Navigation(ANavigation):
        pass


    __all__.append('Navigation')

from .snippets.form import AForm, AFormField, AFormSubmission

if not is_model_registered('cms', 'Form'):
    @register_snippet
    class Form(AForm):
        pass


    __all__.append('Form')

if not is_model_registered('cms', 'FormField'):
    class FormField(AFormField):
        pass


    __all__.append('FormField')

if not is_model_registered('cms', 'FormSubmission'):
    class FormSubmission(AFormSubmission):
        pass


    __all__.append('FormSubmission')

from .snippets.person import APerson

if not is_model_registered('cms', 'Person'):
    @register_snippet
    class Person(APerson):
        pass


    __all__.append('Person')


from .snippets.gallery import AGallery

if not is_model_registered('cms', 'Gallery'):
    @register_snippet
    class Gallery(AGallery):
        pass


    __all__.append('Gallery')


#  Pages


from .pages._generic import AGenericPage

if not is_model_registered('cms', 'GenericPage'):
    class GenericPage(AGenericPage):
        pass


    __all__.append('GenericPage')

from .pages.blog import ABlogIndexPage, ABlogPage, ABlogPageTag

if not is_model_registered('cms', 'BlogPageTag'):
    class BlogPageTag(ABlogPageTag):
        pass


    __all__.append('BlogPageTag')

if not is_model_registered('cms', 'BlogIndexPage'):
    class BlogIndexPage(ABlogIndexPage):
        pass


    __all__.append('BlogIndexPage')

if not is_model_registered('cms', 'BlogPage'):
    class BlogPage(ABlogPage):
        pass


    __all__.append('BlogPage')

from .pages.content import AContentPage

if not is_model_registered('cms', 'ContentPage'):
    class ContentPage(AContentPage):
        pass


    __all__.append('ContentPage')

from .pages.home import AHomePage

if not is_model_registered('cms', 'HomePage'):
    class HomePage(AHomePage):
        pass


    __all__.append('HomePage')

from .pages.document import ADocumentPage

if not is_model_registered('cms', 'DocumentPage'):
    class DocumentPage(ADocumentPage):
        pass


    __all__.append('DocumentPage')

from .pages._generic import AMultiLanguagePage

if not is_model_registered('cms', 'MultiLanguagePage'):
    class MultiLanguagePage(AMultiLanguagePage):
        pass


    __all__.append('MultiLanguagePage')

from .pages.portfolio import APortfolioIndexPage, APortfolioPage, APortfolioPageTag

if not is_model_registered('cms', 'PortfolioPageTag'):
    class PortfolioPageTag(APortfolioPageTag):
        pass


    __all__.append('PortfolioPageTag')

if not is_model_registered('cms', 'PortfolioIndexPage'):
    class PortfolioIndexPage(APortfolioIndexPage):
        pass


    __all__.append('PortfolioIndexPage')

if not is_model_registered('cms', 'PortfolioPage'):
    class PortfolioPage(APortfolioPage):
        pass


    __all__.append('PortfolioPage')

#  Settings

from .settings.webspace import AWebspaceSettings, AFounders

if not is_model_registered('cms', 'WebspaceSettings'):
    @register_setting
    class WebspaceSettings(AWebspaceSettings):
        pass


    __all__.append('WebspaceSettings')

if not is_model_registered('cms', 'Founders'):
    class Founders(AFounders):
        pass


    __all__.append('Founders')
