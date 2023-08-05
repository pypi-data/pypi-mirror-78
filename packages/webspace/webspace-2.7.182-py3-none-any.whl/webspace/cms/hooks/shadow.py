import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler
from wagtail.core import hooks


#  Shadow

@hooks.register('register_rich_text_features')
def register_shadow_feature(features):
    feature_name = 'shadow'
    type_ = 'SHADOW'

    control = {
        'type': type_,
        'label': '≈',
        'description': 'Shadow',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        'from_database_format': {'span[class="shadow"]': InlineStyleElementHandler(type_)},
        'to_database_format': {'style_map': {type_: {
            'element': 'span',
            'props': {'class': 'shadow'},
        }}},
    }

    features.register_converter_rule('contentstate', feature_name, db_conversion)
    features.default_features.append('shadow')
