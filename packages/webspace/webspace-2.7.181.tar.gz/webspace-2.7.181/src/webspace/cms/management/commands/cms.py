import json
from os import listdir
from os.path import isfile, join
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from wagtail.core.models import Page, Site
from wagtail.images.models import Image
from wagtail_feeds.models import RSSFeedsSettings

from webspace.cms import constants
from webspace.loader import get_model, get_class
from webspace.cms.blocks.mocker import Mocker
from webspace.account.utils import get_test_account

# Classes
ArticlesEntry = get_class('cms.blocks.entries', 'ArticlesEntry')
ButtonsEntry = get_class('cms.blocks.entries', 'ButtonsEntry')
CardsEntry = get_class('cms.blocks.entries', 'CardsEntry')
EmbedEntry = get_class('cms.blocks.entries', 'EmbedEntry')
GridInfoEntry = get_class('cms.blocks.entries', 'GridInfoEntry')
ImageEntry = get_class('cms.blocks.entries', 'ImageEntry')
ComponentTextEntry = get_class('cms.blocks.entries', 'ComponentTextEntry')
MediasLineEntry = get_class('cms.blocks.entries', 'MediasLineEntry')
SvgEntry = get_class('cms.blocks.entries', 'SvgEntry')
TextEntry = get_class('cms.blocks.entries', 'TextEntry')
TimeLineEntry = get_class('cms.blocks.entries', 'TimeLineEntry')
CalendlyEntry = get_class('cms.blocks.entries', 'CalendlyEntry')
TableEntry = get_class('cms.blocks.entries', 'TableEntry')
AccordionEntry = get_class('cms.blocks.entries', 'AccordionEntry')
NumbersEntry = get_class('cms.blocks.entries', 'NumbersEntry')
FormEntry = get_class('cms.blocks.entries', 'FormEntry')
GalleryEntry = get_class('cms.blocks.entries', 'GalleryEntry')
StreamContentEntry = get_class('cms.blocks.entries', 'StreamContentEntry')

SocialLinks = get_class('cms.blocks.static', 'SocialLinks')
SocialShare = get_class('cms.blocks.static', 'SocialShare')


# Models
MenuItem = get_model('cms', 'MenuItem')
Menu = get_model('cms', 'Menu')
IconSnippet = get_model('cms', 'IconSnippet')
Navigation = get_model('cms', 'Navigation')
Person = get_model('cms', 'Person')


HomePage = get_model('cms', 'HomePage')
ContentPage = get_model('cms', 'ContentPage')
BlogPage = get_model('cms', 'BlogPage')
BlogIndexPage = get_model('cms', 'BlogIndexPage')
PortfolioPage = get_model('cms', 'PortfolioPage')
PortfolioIndexPage = get_model('cms', 'PortfolioIndexPage')

WebspaceSettings = get_model('cms', 'WebspaceSettings')
MyDocument = get_model('cms', 'MyDocument')
Form = get_model('cms', 'Form')
FormField = get_model('cms', 'FormField')
Gallery = get_model('cms', 'Gallery')


class Command(BaseCommand):
    help = 'Cms commands : init'

    def add_arguments(self, parser):
        parser.add_argument('action', type=str)
        parser.add_argument('extra', type=str, nargs='?', default='')

    def handle(self, *args, **options):
        eval('self.' + options['action'] + '(' + options['extra'] + ')')

    def init(self):
        #  Delete all data
        Site.objects.all().delete()
        Page.objects.all().delete()
        #  Image.objects.all().delete()
        #  MyDocument.objects.all().delete()
        Menu.objects.all().delete()
        MenuItem.objects.all().delete()
        Navigation.objects.all().delete()
        Form.objects.all().delete()
        FormField.objects.all().delete()
        Person.objects.all().delete()
        Gallery.objects.all().delete()

        article_entry = ArticlesEntry()
        buttons_entry = ButtonsEntry()
        cards_entry = CardsEntry()
        embed_entry = EmbedEntry()
        grid_info_entry = GridInfoEntry()
        image_entry = ImageEntry()
        component_text_entry = ComponentTextEntry()
        medias_line_entry = MediasLineEntry()
        svg_entry = SvgEntry()
        text_entry = TextEntry()
        time_line_entry = TimeLineEntry()
        calendly_entry = CalendlyEntry()
        table_entry = TableEntry()
        accordion_entry = AccordionEntry()
        numbers_entry = NumbersEntry()
        form_entry = FormEntry()
        gallery_entry = GalleryEntry()
        stream_content_entry = StreamContentEntry()

        social_links = SocialLinks()
        social_share = SocialShare()

        account = get_test_account()

        mocker = Mocker()

        # Create page content type

        page_content_type, created = ContentType.objects.get_or_create(
            model='page',
            app_label='wagtailcore'
        )

        # Root page

        root = Page.objects.create(
            title="Root",
            slug='root',
            content_type=page_content_type,
            path='0001',
            depth=1,
            numchild=1,
            url_path='/',
        )
        root.save()

        # -------------------------------- HomePage --------------------------------

        home_page = HomePage.objects.create(
            title="Home Page",
            slug='home',
            path='00010001',
            depth=2,
            numchild=0,
            body=json.dumps([
                component_text_entry.mock(bg=True),
                cards_entry.mock(stop=3, carousel=False, container='regular', theme=constants.THEME_LIGHT),
                component_text_entry.mock(size_component='l', reverse=True, section=True),
                cards_entry.mock(container='full'),
                component_text_entry.mock(size_component='l', theme=constants.THEME_LIGHT, section=True),
                cards_entry.mock(container='full', theme=constants.THEME_LIGHT),
                component_text_entry.mock(size_component='l', reverse=True),
                component_text_entry.mock(theme=constants.THEME_LIGHT),
            ])
        )
        home_page.save()
        home_page_menu_id = mocker.menu(home_page)
        mocker.add_header_buttons(home_page)

        # Create default site

        site = Site.objects.create(
            hostname='localhost',
            port=8080,
            root_page_id=home_page.id,
            is_default_site=True
        )
        site.save()

        # -------------------------------- Content Pages --------------------------------

        content_page = ContentPage(
            title="Content Page",
            slug='content',
            body=json.dumps([
                component_text_entry.mock(),
                component_text_entry.mock(theme=constants.THEME_LIGHT),
                time_line_entry.mock(theme=constants.THEME_LIGHT),
                text_entry.mock(txt='<h2>Loreum</h2>', align='center', theme=constants.THEME_SPACE),
                component_text_entry.mock(reverse=True, theme=constants.THEME_SPACE),
                component_text_entry.mock(theme=constants.THEME_SPACE_INVERSE),
                component_text_entry.mock(theme=constants.THEME_LIGHT),
            ])
        )
        home_page.add_child(instance=content_page)
        content_menu_id = mocker.menu(content_page)
        mocker.add_menu(content_page, home_page_menu_id)
        mocker.add_menu(home_page, content_menu_id)

        # -------------------------------- Blog Pages --------------------------------

        articles_page = BlogIndexPage(
            title="Articles",
            slug='articles',
            bg_desktop=json.dumps([{
                'type': 'svg',
                'value': mocker.file(mocker.SVG_BG_DESKTOP_SPACE).id
            }]),
            bg_mobile=json.dumps([{
                'type': 'svg',
                'value': mocker.file(mocker.SVG_BG_MOBILE_SPACE).id
            }]),
            h1=mocker.h,
            first_text=mocker.text_first_content
        )
        home_page.add_child(instance=articles_page)
        articles_menu_id = mocker.menu(articles_page)
        mocker.add_menu(articles_page, home_page_menu_id)
        mocker.add_menu(home_page, articles_menu_id)

        article_list = []
        i = 1
        while i < 3:
            file_desktop = mocker.SVG_BG_DESKTOP_SPACE if i % 2 else mocker.IMG_BG_DESKTOP_SPACE
            file_mobile = mocker.SVG_BG_MOBILE_SPACE if i % 2 else mocker.IMG_BG_MOBILE_SPACE
            cover = mocker.SVG_BLOG_COVER_LIGHT if i % 2 else mocker.IMG_BLOG_COVER_LIGHT

            article_page = BlogPage(
                title="Article %s" % (str(i)),
                slug='article-%s' % (str(i)),
                body=json.dumps([
                    text_entry.mock(container='content', theme=constants.THEME_LIGHT),
                    svg_entry.mock(container='content', theme=constants.THEME_LIGHT),
                    text_entry.mock(container='content', theme=constants.THEME_LIGHT),
                    svg_entry.mock(force_file=mocker.SVG_CONTENT_HEIGHT_LIGHT, container='content',
                                   theme=constants.THEME_LIGHT),
                    text_entry.mock(container='content', theme=constants.THEME_LIGHT),
                    image_entry.mock(container='content', theme=constants.THEME_LIGHT),
                    text_entry.mock(container='content', theme=constants.THEME_LIGHT),
                    image_entry.mock(force_file=mocker.IMG_CONTENT_HEIGHT_LIGHT, container='content',
                                     theme=constants.THEME_LIGHT),
                    text_entry.mock(container='content', theme=constants.THEME_LIGHT),
                    embed_entry.mock(container='content', theme=constants.THEME_LIGHT),
                    text_entry.mock(container='content', theme=constants.THEME_LIGHT),
                ]),
                author=mocker.get_person(),
                bg_desktop=json.dumps([{
                    'type': ('svg' if i % 2 else 'image'),
                    'value': mocker.file(file_desktop).id
                }]),
                bg_mobile=json.dumps([{
                    'type': ('svg' if i % 2 else 'image'),
                    'value': mocker.file(file_mobile).id
                }]),
                cover=json.dumps([{
                    'type': ('svg' if i % 2 else 'image'),
                    'value': mocker.file(cover).id
                }]),
                intro=mocker.h,
                intro_page=mocker.text_first_content,
                h1=mocker.h,
            )
            article_page.tags.add('Foo' if i % 2 else 'Bar')
            articles_page.add_child(instance=article_page)
            mocker.menu(article_page, articles_menu_id)
            mocker.add_menu(article_page, home_page_menu_id)
            article_list.append(article_page)
            i += 1

        related = {
            'type': 'article',
            'value': article_list[0].id
        }
        for article in article_list:
            article.related_blogs = json.dumps([
                related, related, related
            ])
            article.save()

        # -------------------------------- Portfolio Pages --------------------------------

        portfolios_page = PortfolioIndexPage(
            title="Portfolio",
            slug='portfolio',
            bg_desktop=json.dumps([{
                'type': 'svg',
                'value': mocker.file(mocker.SVG_BG_DESKTOP_SPACE).id
            }]),
            bg_mobile=json.dumps([{
                'type': 'svg',
                'value': mocker.file(mocker.SVG_BG_MOBILE_SPACE).id
            }]),
            first_text=mocker.text_first_content
        )
        home_page.add_child(instance=portfolios_page)
        portfolios_menu_id = mocker.menu(portfolios_page)
        mocker.add_menu(portfolios_page, home_page_menu_id)
        mocker.add_menu(home_page, portfolios_menu_id)

        portfolio_list = []
        i = 1
        while i < 3:
            cover = mocker.SVG_BLOG_COVER_LIGHT if i % 2 else mocker.IMG_BLOG_COVER_LIGHT
            portfolio_page = PortfolioPage(
                title="Portfolio %s" % (str(i)),
                slug='portfolio-%s' % (str(i)),
                body=json.dumps([
                    text_entry.mock(container='content', theme=constants.THEME_LIGHT),
                    svg_entry.mock(container='content', theme=constants.THEME_LIGHT),
                    text_entry.mock(container='content', theme=constants.THEME_LIGHT),
                    svg_entry.mock(force_file=mocker.SVG_CONTENT_HEIGHT_LIGHT, container='content',
                                   theme=constants.THEME_LIGHT),
                    text_entry.mock(container='content', theme=constants.THEME_LIGHT),
                    image_entry.mock(container='content', theme=constants.THEME_LIGHT),
                    text_entry.mock(container='content', theme=constants.THEME_LIGHT),
                    image_entry.mock(force_file=mocker.IMG_CONTENT_HEIGHT_LIGHT, container='content',
                                     theme=constants.THEME_LIGHT),
                    text_entry.mock(container='content', theme=constants.THEME_LIGHT),
                    embed_entry.mock(container='content', theme=constants.THEME_LIGHT),
                    text_entry.mock(container='content', theme=constants.THEME_LIGHT),
                ]),
                cover=json.dumps([{
                    'type': ('svg' if i % 2 else 'image'),
                    'value': mocker.file(cover).id
                }]),
                intro=mocker.h,
            )
            portfolio_page.tags.add('Uks' if i % 2 else 'Kaks')
            portfolios_page.add_child(instance=portfolio_page)
            mocker.menu(portfolio_page, portfolios_menu_id)
            mocker.add_menu(portfolio_page, home_page_menu_id)
            portfolio_list.append(portfolio_page)
            i += 1

        related = {
            'type': 'portfolio',
            'value': portfolio_list[0].id
        }
        for portfolio in portfolio_list:
            portfolio.related_portfolio = json.dumps([
                related, related, related
            ])
            portfolio.save()

        # -------------------------------- Example --------------------------------

        # -------------------------------- Cards --------------------------------

        block_page = ContentPage(
            title="Blocks",
            slug='blocks',
        )
        home_page.add_child(instance=block_page)
        block_menu_id = mocker.menu(block_page)
        mocker.add_menu(block_page, home_page_menu_id)
        mocker.add_menu(home_page, block_menu_id)

        carousel_page = ContentPage(
            title="Cards",
            slug='cards',
            body=json.dumps([
                text_entry.mock(txt='<h2>Cards Custom</h2>', align='center'),
                cards_entry.mock(stop=1, carousel=False, container='content'),
                cards_entry.mock(stop=2, carousel=False, container='regular'),
                cards_entry.mock(stop=3, carousel=False, container='regular'),

                cards_entry.mock(stop=1, carousel=False, theme=constants.THEME_LIGHT, container='content'),
                cards_entry.mock(stop=2, carousel=False, theme=constants.THEME_LIGHT, container='regular'),
                cards_entry.mock(stop=3, carousel=False, theme=constants.THEME_LIGHT, container='regular'),

                text_entry.mock(txt='<h2>Carousel Custom</h2>', align='center'),
                cards_entry.mock(container='full'),
                cards_entry.mock(container='full', theme=constants.THEME_LIGHT),
            ])
        )
        block_page.add_child(instance=carousel_page)
        mocker.menu(carousel_page, block_menu_id)
        mocker.add_menu(carousel_page, home_page_menu_id)

        # -------------------------------- Component Text --------------------------------

        media_text_page = ContentPage(
            title="Component Text",
            slug='component-text',
            body=json.dumps([
                text_entry.mock(txt='<h2>Component Text Regular</h2>', align='center'),
                component_text_entry.mock(reverse=True),
                component_text_entry.mock(theme=constants.THEME_LIGHT),

                text_entry.mock(txt='<h2>Component Text Embed</h2>', align='center'),
                component_text_entry.mock(component='embed', size_component='xl'),

                text_entry.mock(txt='<h2>Component Text Form</h2>', align='center'),
                component_text_entry.mock(component='form'),

                text_entry.mock(txt='<h2>Component Text Size XL</h2>', align='center'),
                component_text_entry.mock(size_component='xl', reverse=True),
                component_text_entry.mock(size_component='xl', theme=constants.THEME_LIGHT),

                text_entry.mock(txt='<h2>Component Text Buttons</h2>', align='center'),
                component_text_entry.mock(
                    reverse=True,
                    button_1=constants.BUTTON_SECONDARY_FULL,
                    button_2=constants.BUTTON_SECONDARY
                ),
                component_text_entry.mock(
                    theme=constants.THEME_LIGHT,
                    button_1=constants.BUTTON_PRIMARY_FULL,
                    button_2=constants.BUTTON_PRIMARY
                ),

                text_entry.mock(txt='<h2>Component Text Background</h2>', align='center'),
                component_text_entry.mock(
                    reverse=True,
                    button_1=constants.BUTTON_TERTIARY_FULL,
                    button_2=constants.BUTTON_TERTIARY,
                    bg=True
                ),
                component_text_entry.mock(
                    theme=constants.THEME_LIGHT,
                    button_1=constants.BUTTON_SECONDARY_FULL,
                    button_2=constants.BUTTON_SECONDARY,
                    bg=True
                ),

                text_entry.mock(txt='<h2>Component Text Align</h2>', align='center'),
                component_text_entry.mock(
                    align='justify',
                    reverse=True,
                    button_1=constants.BUTTON_TERTIARY_FULL,
                    button_2=constants.BUTTON_TERTIARY,
                ),
                component_text_entry.mock(
                    theme=constants.THEME_LIGHT,
                    button_1=constants.BUTTON_SECONDARY_FULL,
                    button_2=constants.BUTTON_SECONDARY,
                    align='center'
                ),
            ])
        )
        block_page.add_child(instance=media_text_page)
        mocker.menu(media_text_page, block_menu_id)
        mocker.add_menu(media_text_page, home_page_menu_id)

        # -------------------------------- Text --------------------------------

        text_page = ContentPage(
            title="Text",
            slug='text',
            body=json.dumps([
                text_entry.mock(size='example', align='left'),
                text_entry.mock(size='example', align='left', theme=constants.THEME_LIGHT),

                text_entry.mock(size='normal', align='left'),
                text_entry.mock(size='normal', align='left', theme=constants.THEME_LIGHT),

                text_entry.mock(size='big', align='left'),
                text_entry.mock(size='big', align='left', theme=constants.THEME_LIGHT),
            ])
        )
        block_page.add_child(instance=text_page)
        mocker.menu(text_page, block_menu_id)
        mocker.add_menu(text_page, home_page_menu_id)

        # -------------------------------- Image --------------------------------

        image_page = ContentPage(
            title="Images",
            slug='images',
            body=json.dumps([
                text_entry.mock(txt='<h2>JPG</h2>', align='center', theme=constants.THEME_LIGHT),
                text_entry.mock(txt='<p>Size XS</p>', align='center', theme=constants.THEME_LIGHT),
                image_entry.mock(size='xs'),
                text_entry.mock(txt='<p>Size S</p>', align='center', theme=constants.THEME_LIGHT),
                image_entry.mock(size='s'),
                text_entry.mock(txt='<p>Size M</p>', align='center', theme=constants.THEME_LIGHT),
                image_entry.mock(size='m'),
                text_entry.mock(txt='<p>Size L</p>', align='center', theme=constants.THEME_LIGHT),
                image_entry.mock(size='l'),
                text_entry.mock(txt='<p>Size X</p>', align='center', theme=constants.THEME_LIGHT),
                image_entry.mock(size='x'),
                text_entry.mock(txt='<p>Size XL</p>', align='center', theme=constants.THEME_LIGHT),
                image_entry.mock(size='xl'),
                text_entry.mock(txt='<h2>SVG</h2>', align='center'),
                text_entry.mock(txt='<p>Size XS</p>', align='center'),
                svg_entry.mock(size='xs', theme=constants.THEME_LIGHT),
                text_entry.mock(txt='<p>Size S</p>', align='center'),
                svg_entry.mock(size='s', theme=constants.THEME_LIGHT),
                text_entry.mock(txt='<p>Size M</p>', align='center'),
                svg_entry.mock(size='m', theme=constants.THEME_LIGHT),
                text_entry.mock(txt='<p>Size L</p>', align='center'),
                svg_entry.mock(size='l', theme=constants.THEME_LIGHT),
                text_entry.mock(txt='<p>Size X</p>', align='center'),
                svg_entry.mock(size='x', theme=constants.THEME_LIGHT),
                text_entry.mock(txt='<p>Size XL</p>', align='center'),
                svg_entry.mock(size='xl', theme=constants.THEME_LIGHT),
            ])
        )
        block_page.add_child(instance=image_page)
        mocker.menu(image_page, block_menu_id)
        mocker.add_menu(image_page, home_page_menu_id)

        # -------------------------------- TimeLine --------------------------------

        timeline_page = ContentPage(
            title="Timeline",
            slug='timeline',
            body=json.dumps([
                text_entry.mock(txt='<h1>Timeline</h1>', align='center'),
                time_line_entry.mock(),
                time_line_entry.mock(theme=constants.THEME_SPACE_INVERSE),
                time_line_entry.mock(theme=constants.THEME_LIGHT),
            ])
        )
        block_page.add_child(instance=timeline_page)
        mocker.menu(timeline_page, block_menu_id)
        mocker.add_menu(timeline_page, home_page_menu_id)

        # -------------------------------- Line Medias --------------------------------

        medias_line_page = ContentPage(
            title="Medias Line",
            slug='medias-line',
            body=json.dumps([
                text_entry.mock(txt='<h1>Medias Line</h1>', align='center'),
                medias_line_entry.mock(2),
                medias_line_entry.mock(),
                medias_line_entry.mock(4),
            ])
        )
        block_page.add_child(instance=medias_line_page)
        mocker.menu(medias_line_page, block_menu_id)
        mocker.add_menu(medias_line_page, home_page_menu_id)

        # -------------------------------- Grid Info --------------------------------

        grid_info_page = ContentPage(
            title="Grid Info",
            slug='grid-info',
            body=json.dumps([
                text_entry.mock(txt='<h1>Grid Info</h1>', align='center'),
                grid_info_entry.mock(),
                grid_info_entry.mock(theme=constants.THEME_SPACE_INVERSE),
                grid_info_entry.mock(theme=constants.THEME_LIGHT),
            ])
        )
        block_page.add_child(instance=grid_info_page)
        mocker.menu(grid_info_page, block_menu_id)
        mocker.add_menu(grid_info_page, home_page_menu_id)

        # -------------------------------- Buttons --------------------------------

        buttons_page = ContentPage(
            title="Buttons",
            slug='buttons',
            body=json.dumps([
                text_entry.mock(txt='<h1>Buttons</h1>', align='center'),
                buttons_entry.mock(),
                buttons_entry.mock(align='center', theme=constants.THEME_SPACE_INVERSE),
                buttons_entry.mock(align='right', theme=constants.THEME_LIGHT),

                buttons_entry.mock(btn_one=constants.BUTTON_PRIMARY, btn_two=constants.BUTTON_PRIMARY_FULL),
                buttons_entry.mock(theme=constants.THEME_SPACE_INVERSE, btn_one=constants.BUTTON_PRIMARY,
                                   btn_two=constants.BUTTON_PRIMARY_FULL, align='center'),
                buttons_entry.mock(theme=constants.THEME_LIGHT, btn_one=constants.BUTTON_PRIMARY,
                                   btn_two=constants.BUTTON_PRIMARY_FULL, align='right'),

                buttons_entry.mock(btn_one=constants.BUTTON_TERTIARY, btn_two=constants.BUTTON_TERTIARY_FULL,
                                   theme=constants.THEME_LIGHT),
                buttons_entry.mock(theme=constants.THEME_SPACE_INVERSE, btn_one=constants.BUTTON_TERTIARY,
                                   btn_two=constants.BUTTON_TERTIARY_FULL, align='center'),
                buttons_entry.mock(theme=constants.THEME_LIGHT, btn_one=constants.BUTTON_TERTIARY,
                                   btn_two=constants.BUTTON_TERTIARY_FULL, align='right'),
            ])
        )
        block_page.add_child(instance=buttons_page)
        mocker.menu(buttons_page, block_menu_id)
        mocker.add_menu(buttons_page, home_page_menu_id)

        # -------------------------------- Calendly --------------------------------

        calendly_page = ContentPage(
            title="Calendly",
            slug='calendly',
            body=json.dumps([
                text_entry.mock(txt='<h1>Calendly</h1>', align='center'),
                calendly_entry.mock(),
            ])
        )
        block_page.add_child(instance=calendly_page)
        mocker.menu(calendly_page, block_menu_id)
        mocker.add_menu(calendly_page, home_page_menu_id)

        # -------------------------------- Table --------------------------------

        table_page = ContentPage(
            title="Table",
            slug='table',
            body=json.dumps([
                text_entry.mock(txt='<h1>Tables</h1>', align='center'),
                table_entry.mock(),
                table_entry.mock(theme=constants.THEME_SPACE_INVERSE),
                table_entry.mock(theme=constants.THEME_LIGHT),
            ])
        )
        block_page.add_child(instance=table_page)
        mocker.menu(table_page, block_menu_id)
        mocker.add_menu(table_page, home_page_menu_id)

        # -------------------------------- Accordion --------------------------------

        accordion_page = ContentPage(
            title="Accordion",
            slug='accordion',
            body=json.dumps([
                text_entry.mock(txt='<h1>Accordion</h1>', align='center'),
                accordion_entry.mock(),
                accordion_entry.mock(theme=constants.THEME_SPACE_INVERSE),
                accordion_entry.mock(theme=constants.THEME_LIGHT),
            ])
        )
        block_page.add_child(instance=accordion_page)
        mocker.menu(accordion_page, block_menu_id)
        mocker.add_menu(accordion_page, home_page_menu_id)

        # -------------------------------- Numbers --------------------------------

        numbers_page = ContentPage(
            title="Numbers",
            slug='numbers',
            body=json.dumps([
                text_entry.mock(txt='<h1>Numbers</h1>', align='center'),
                numbers_entry.mock(),
                numbers_entry.mock(theme=constants.THEME_SPACE_INVERSE),
                numbers_entry.mock(theme=constants.THEME_LIGHT),
            ])
        )
        block_page.add_child(instance=numbers_page)
        mocker.menu(numbers_page, block_menu_id)
        mocker.add_menu(numbers_page, home_page_menu_id)

        # -------------------------------- Forms --------------------------------

        forms_page = ContentPage(
            title="Forms",
            slug='forms',
            body=json.dumps([
                text_entry.mock(txt='<h1>Form</h1>', align='center'),
                form_entry.mock(),
                form_entry.mock(theme=constants.THEME_SPACE_INVERSE),
                form_entry.mock(theme=constants.THEME_LIGHT),
            ])
        )
        block_page.add_child(instance=forms_page)
        mocker.menu(forms_page, block_menu_id)
        mocker.add_menu(forms_page, home_page_menu_id)

        # -------------------------------- Social Media --------------------------------

        forms_page = ContentPage(
            title="Social Media",
            slug='social-media',
            body=json.dumps([
                text_entry.mock(txt='<h1>Social Media</h1>', align='center'),
                social_links.mock(),
                social_links.mock(theme=constants.THEME_SPACE_INVERSE),
                social_links.mock(theme=constants.THEME_LIGHT),
                social_share.mock(),
                social_share.mock(theme=constants.THEME_SPACE_INVERSE),
                social_share.mock(theme=constants.THEME_LIGHT),
            ])
        )
        block_page.add_child(instance=forms_page)
        mocker.menu(forms_page, block_menu_id)
        mocker.add_menu(forms_page, home_page_menu_id)

        # -------------------------------- Gallery --------------------------------

        gallery_page = ContentPage(
            title="Gallery",
            slug='gallery',
            body=json.dumps([
                text_entry.mock(txt='<h1>Gallery</h1>', align='center'),
                gallery_entry.mock(),
                gallery_entry.mock(theme=constants.THEME_SPACE_INVERSE),
                gallery_entry.mock(theme=constants.THEME_LIGHT),
            ])
        )
        block_page.add_child(instance=gallery_page)
        mocker.menu(gallery_page, block_menu_id)
        mocker.add_menu(gallery_page, home_page_menu_id)

        # -------------------------------- Stream Content --------------------------------

        stream_content_page = ContentPage(
            title="Stream Content",
            slug='stream-content',
            body=json.dumps([
                text_entry.mock(txt='<h1>Stream Content</h1>', align='center'),
                stream_content_entry.mock(),
                stream_content_entry.mock(theme=constants.THEME_SPACE_INVERSE),
                stream_content_entry.mock(theme=constants.THEME_LIGHT),
            ])
        )
        block_page.add_child(instance=stream_content_page)
        mocker.menu(stream_content_page, block_menu_id)
        mocker.add_menu(stream_content_page, home_page_menu_id)

        # -------------------------------- Settings --------------------------------

        ws_settings = WebspaceSettings.for_site(site)
        ws_settings.brand_name = "SpaceX"
        ws_settings.logo_header_primary = json.dumps([{
            'type': 'svg',
            'value': mocker.file(mocker.SVG_LOGO_SPACE).id
        }])
        ws_settings.logo_header_secondary = json.dumps([{
            'type': 'svg',
            'value': mocker.file(mocker.SVG_LOGO_LIGHT).id
        }])
        ws_settings.favicon = mocker.file(mocker.IMG_ICON_SPACE)
        ws_settings.language = 'fr'
        ws_settings.collect_text = "<p>En poursuivant votre navigation sur ce site, vous acceptez nos CGU ainsi que notre Politique de confidentialité</p>"
        ws_settings.social_share_text = """
        <h2>Partager cette page!</h2>
        <hr>
        <p>Chaque semaine dans votre boite mail, un condensé de conseils et de nouvelles entreprises qui
            recrutent.</p>
        """
        ws_settings.social_links_text = """
        <h2>Suivez-nous!</h2>
        <hr>
        <p>Chaque semaine dans votre boite mail, un condensé de conseils et de nouvelles entreprises qui
            recrutent.</p>
        """
        ws_settings.summary_text = """
        <h2>Sommaire</h2>
        <hr>
        """
        ws_settings.search_text = """
        <h2>Recherche</h2>
        <hr>
        """
        ws_settings.related_articles_text = """
        <h2>Articles related</h2>
        <hr>
        """

        ws_settings.related_portfolios_text = """
        <h2>Portfolios related</h2>
        <hr>
        """

        ws_settings.newsletter = Mocker.get_form('newsletter', nb_fields=1, head_text=False)

        ws_settings.facebook = mocker.URL_TEST
        ws_settings.instagram = mocker.URL_TEST
        ws_settings.linkedin = mocker.URL_TEST
        ws_settings.twitter = mocker.URL_TEST
        ws_settings.youtube = mocker.URL_TEST
        ws_settings.pinterest = mocker.URL_TEST
        ws_settings.save()

        rss = RSSFeedsSettings.for_site(site)
        rss.feed_app_label = 'cms'
        rss.feed_model_name = 'BlogPage'
        rss.feed_title = 'Change me'
        rss.feed_link = 'https://changeme.com'
        rss.feed_description = 'Change me'
        rss.feed_author_email = 'change@me.me'
        rss.feed_author_link = 'https://changeme.com'
        rss.feed_item_description_field = 'intro'
        rss.feed_item_content_field = 'body'
        rss.feed_image_in_content = True
        rss.feed_item_date_field = 'date'
        rss.is_feed_item_date_field_datetime = True
        rss.save()

    def icons(self):
        keys = [
            "user",
            "angle",
            "cross",
            "cross_red",
            "email",
            "facebook",
            "instagram",
            "linkedin",
            "twitter",
            "youtube",
            "pinterest",
            "info",
            "right",
            "left",
            "map_marker",
            "success",
            "pen",
            "phone",
            "help",
            "search",
            "tick",
            "time",
            "user",
            "accordion",
            "fr",
            "en",
            "star_enable",
            "star_disable",
        ]
        for key in keys:
            ico, created = IconSnippet.objects.get_or_create(
                key=key
            )
            if created:
                ico.save()

    def docs(self):
        MyDocument.objects.all().delete()
        doc_path = 'CHANGE_ME/cms/management/commands/files/documents'
        doc_files = [f for f in listdir(doc_path) if isfile(join(doc_path, f))]
        for doc_name in doc_files:
            file_title = doc_name.replace('.svg', '').replace('-', ' ').replace('_', ' ').title()
            file = ImageFile(
                open(doc_path + '/' + doc_name, "rb"),
                name=file_title + '.svg'
            )
            try:
                document = MyDocument.objects.get(title=file_title)
            except MyDocument.DoesNotExist:
                document = MyDocument(
                    title=file_title,
                    file=file
                )
                document.save()

            if 'icon_' in doc_name:
                doc_name_sp = doc_name.split('_')
                key_icon = doc_name_sp[1]
                theme = doc_name_sp[2]
                key_icon = key_icon.replace('-', '_')
                try:
                    icon = IconSnippet.objects.get(key=key_icon)
                    if theme == 'light.svg':
                        icon.light = document
                        icon.save()
                    if theme == 'space.svg':
                        icon.space = document
                        icon.save()
                except IconSnippet.DoesNotExist:
                    print("Error key icon does not exist")
                    import pdb
                    pdb.set_trace()

    def imgs(self):
        Image.objects.all().delete()
        doc_path = 'CHANGE_ME/cms/management/commands/files/images'
        doc_files = [f for f in listdir(doc_path) if isfile(join(doc_path, f))]
        for doc_name in doc_files:
            file_title = doc_name.replace('.png', '').replace('-', ' ').replace('_', ' ').title()
            file = ImageFile(
                open(doc_path + '/' + doc_name, "rb"),
                name=file_title + '.png'
            )
            try:
                document = Image.objects.get(title=file_title)
            except Image.DoesNotExist:
                document = Image(
                    title=file_title,
                    file=file
                )
                document.save()
