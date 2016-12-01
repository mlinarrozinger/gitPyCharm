#!/usr/bin/env python
import os
import jinja2
import webapp2

import random

from models import Sporocilo


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))

class RezultatHandler(BaseHandler):
    def post(self):
        besedilo = self.request.get("sporocilo")

        ime = self.request.get("ime")

        sporocilo = Sporocilo(besedilo_sporocila=besedilo, avtor=ime)
        sporocilo.put()

        izzrebane = []

        for j in range(7):
            izzrebane.append(random.randint(1, 37))

        params = {"name": ime, "besedilo": besedilo,
                  "izzrebane": izzrebane}

        return self.render_template("rezultat.html", params=params)

class MainHandler(BaseHandler):
    def get(self):

        return self.render_template("hello.html")

class OsnovnaStran(BaseHandler):
    def get(self):
        return self.render_template("base.html")

class AboutHandler(BaseHandler):
    def get(self):
        return self.render_template("about.html")

class ContactHandler(BaseHandler):
    def get(self):
        return self.render_template("contact.html")

class HelloHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")

class SporocilaHandler(BaseHandler):
    def get(self):

        sporocila = Sporocilo.query().fetch()

        params = {"sporocila": sporocila}

        return self.render_template("sporocila.html", params=params)

class PosameznoSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):

        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))

        params= {"sporocilo": sporocilo}

        return self.render_template("posamezno_sporocilo.html", params=params)

class EditHandler(BaseHandler):
    def get(self, sporocilo_id):

        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))

        params = {"sporocilo": sporocilo}

        return self.render_template("uredi_sporocilo.html", params=params)

    def post(self, sporocilo_id):

        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))

        sporocilo.besedilo_sporocila = self.request.get("text-sporocila")

        sporocilo.avtor = self.request.get("ime")

        sporocilo.put()

        return self.redirect_to("seznam_sporocil")









app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route("/mywebsite.html", OsnovnaStran),
    webapp2.Route("/about", AboutHandler),
    webapp2.Route("/contact", ContactHandler),
    webapp2.Route("/hello", HelloHandler),
    webapp2.Route('/rezultat', RezultatHandler),
    webapp2.Route('/sporocila', SporocilaHandler, name="seznam_sporocil"),
    webapp2.Route("/sporocila/<sporocilo_id:\d+>", PosameznoSporociloHandler),
    webapp2.Route("/sporocila/<sporocilo_id:\d+>/uredi", EditHandler)

], debug=True)
