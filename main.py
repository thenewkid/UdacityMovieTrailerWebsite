#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import jinja2
import re
import random
# import movie_class

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), 
autoescape = True)

home_page = """
<!DOCTYPE html>
<html>
	<head>
		<style>

			#form_error {
				display: none;
			}
			
		</style>

		<title>Hello world</title>
		<meta http-equiv="Content-Type" content="text/html;charset=utf-8">
		<script src="/js/home_page.js"></script>
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
	</head>
	<body>
		<h1>The Youtube Trailer Profiler</h1>

		<form name="new_trailer_data" method="post">
			<input type="text" name="title" placeholder="Movie Title" required >
			<input type="text" name="poster_image_link" placeholder="Poster Image Url" required >
			<input type="text" name="youtube_trailer_link" placeholder="Youtube Trailer Link" required >
			
			<input type="submit" name="subm" value="Add To My Trailers">
		</form>
		<div id="form_error"></div>


	</body>
</html>
"""

class MainHandler(webapp2.RequestHandler):
	def write(self, *args, **kwargs):
		self.response.out.write(*args, **kwargs)
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)
	def render(self, template, **kwargs):
		self.write(self.render_str(template, **kwargs))

class HomePage(MainHandler):
	def get(self):
		self.write(home_page)
	def post(self):
		pass
# class MainHandler(webapp2.RequestHandler):

# 	def write(self, *args, **kwargs):
#   	 	self.response.out.write(*args, **kwargs)
        
#     def render_str(self, template, **params):
#     	t = jinja_env.get_template(template)
#        	return t.render(params)

#     def render(self, template, **kwargs):
#     	self.write(self.render_str(template, **kwargs))

# class HomePage(MainHandler):
# 	def get(self):
# 		self.response.out.write("<h1>Hello world</h1>")

# 	def post(self):
# 		pass

app = webapp2.WSGIApplication([
    ('/', HomePage)
], debug=True)
