from django.templatetags.static import static


class KeenConfig(object):

    @staticmethod
    def get_app_info(request):
        data = {
            'logo': static('src/assets/media/logos/logo-4.png'),
            'logo_url': '/',
            'logo_sticky': static('src/assets/media/logos/logo-4.png'),
            'title': 'Foo Bar',
            'fluid': True,
            'display_footer': False,
        }
        return data

    @staticmethod
    def get_header_menu(request):
        data = {
            'menus': [
                ('Dobra', {
                    'icon': 'fas fa-adjust',
                    'url': '#',
                    'has_perm': True,
                    'children': (
                        ('Menu 1', {
                            'icon': 'fas fa-file',
                            'url': 'teste',
                            'has_perm': True
                        }),
                        ('Menu 2', {
                            'icon': 'fas fa-circle',
                            'url': '#',
                            'has_perm': True
                        }),
                    )
                }),
                ('Menu 2', {
                    'icon': 'flaticon-map',
                    'url': '#',
                    'has_perm': True,
                })
            ]
        }
        return data

    @staticmethod
    def get_user_menu(request):
        data = {
            'user_name': 'Jon Doe',
            'user_subtitle': 'Admin',
            'user_avatar': None,
            'user_avatar_color': 'primary',
            'user_initials': 'JD',
            'user_menus': (
                ('My Profile', {
                    'icon': 'fas fa-search',
                    'url': '#',
                    'has_perm': True
                }
                 ),
            ),
            'signout_url': '#',
        }
        return data

    @staticmethod
    def get_user_apps(request):
        apps = {
            'user_apps': [
                ('Separar PDF', {
                    'label': 'Separa um pdf contendo vários CAMS, em vários PDFs menores. Divididos por bitola.',
                    'url': '/extrator/pdf/add/',
                    'image': static('dist/assets/media/users/300_16.jpg'),
                    'has_perm': True,
                }),
                ('Separar PDF', {
                    'label': 'Separa um pdf contendo vários CAMS, em vários PDFs menores. Divididos por bitola.',
                    'url': '/extrator/pdf/add/',
                    'image': static('dist/assets/media/users/300_16.jpg'),
                    'has_perm': True,
                }),
                ('Separar PDF', {
                    'label': 'Separa um pdf contendo vários CAMS, em vários PDFs menores. Divididos por bitola.',
                    'url': '/extrator/pdf/add/',
                    'image': static('dist/assets/media/users/300_16.jpg'),
                    'has_perm': True,
                }),
                ('Separar PDF', {
                    'label': 'Separa um pdf contendo vários CAMS, em vários PDFs menores. Divididos por bitola.',
                    'url': '/extrator/pdf/add/',
                    'image': static('dist/assets/media/users/300_16.jpg'),
                    'has_perm': True,
                }),
            ],
        }
        return apps
