def setup(app):
    import os.path
    theme_path = os.path.join(os.path.dirname(__file__), 'themes')
    app.add_html_theme('yeen', os.path.join(theme_path, 'yeen'))
    app.connect("builder-inited", builder_inited)

def builder_inited(app):
    # unlimit field name size
    app.builder.env.settings['field_name_limit'] = None
