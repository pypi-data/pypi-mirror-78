import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler
from wagtail.core import hooks


@hooks.register('register_rich_text_features')
def register_read_more_feature(features):
    feature_name = 'read-more'
    type_ = 'READMORE'

    control = {
        'type': type_,
        'label': '♣',
        'description': 'Read More',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        'from_database_format': {'span[class="read-more"]': InlineStyleElementHandler(type_)},
        'to_database_format': {'style_map': {type_: {
            'element': 'span',
            'props': {'class': 'read-more'},
        }}},
    }

    features.register_converter_rule('contentstate', feature_name, db_conversion)
    features.default_features.append('read-more')
