from typing import Dict

import os

from jinja2 import Environment, FileSystemLoader

from arpoc.base import ServiceProxy



env = Environment(loader=FileSystemLoader(os.path.join(
    os.path.dirname(__file__),
    'resources',
    'templates')))


class Userinfo(ServiceProxy):
    """
        Class of the special page Userinfo.

        Displays the userinfo of a logged-in user.
        If the user is not logged-in, an empty dictionary is displayed.
        You can force the user to be logged in by setting the right access control policies.
    """
    def _proxy(self, url: str, access: Dict) -> str:
        _, userinfo = self._oidc_handler.get_userinfo()

        tmpl = env.get_template("userinfo.html")
        return tmpl.render(userinfo=userinfo)
