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
import pickle
import string
from google.appengine.ext import db
# import movie_class

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), 
autoescape = True)

home_page = """
<!DOCTYPE html>
<html>
	<head>
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
		<script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    	<script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    	<link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    	<link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
		
		<title>Hello world</title>
		<meta http-equiv="Content-Type" content="text/html;charset=utf-8">
		<script src="/js/home_page.js"></script>	
		<style>

			
			#form_error {
				display: none;
			}
			.margin-top-4 {
				margin-top: 4%;
			}
			.margin-top-2 {
				margin-top: 2%;
			}
			.border-blue {
				border: 3px solid #0066ff;
			}
			.err_msg {
				border: 2px groove #660000;
				background-color: #993333;
			}
			#form_error p {
				color: white;
				text-shadow: 1px 1px 1px black;
				width: 50%;
				margin: 0px auto;
			}
			hr {
				color: black;
			}

			.scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
			.scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
		</style>

	</head>
	<body>

		<div class="container-fluid">
			<div class="row">
				<div class="col-md-5">
					<h1>Everybody's Favorite Trailers</h1>
				</div>
				<div class="col-md-2">
					<img src="data:image/jpeg;base64,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" />
				</div>
			</div>

			<div class="row text-center">
				<div class="col-md-12">

					<p class="lead">Want To Add a trailer To The List</p>
					<form name="new_trailer_data" method="post">
						<input type="text" name="title" placeholder="Movie Title" required >
						<input type="text" name="poster_image_link" placeholder="Poster Image Url" required >
						<input type="text" name="youtube_trailer_link" placeholder="Youtube Trailer Link" required >
						
						<br><input class="margin-top-2 btn btn-primary" type="submit" name="subm" value="Add To My Trailers">
					</form>
				</div>

			</div>

			<div class="row">
				<div class="col-md-12">
					<div><hr style="color:black"></div>
				</div>
			</div>

			<div class="row text-center">
				<div class="col-md-12">
					<div id="form_error" class="margin-top-4"></div>
				</div>
			</div>
		</div>
"""
page_closing_tags = """

	</body>
</html>

"""
modal = """
<div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>
"""
class Trailers(db.Model):
	#trailer_data will be a pickled string prepresentation of a hash
	#the hash will contain the keys movie_title, poster_image_link, youtube_trailer_link and the user_key
	trailer_data = db.TextProperty(required=True)
	trailer_submit_date = db.DateTimeProperty(auto_now_add=True)

	#Trailers.is_key_present(user_key) returns true if the user_key has already made it to the list
	#when a user adds a trailer to the list we will generate a random key for our user, we have to make sure
	#that the generated key isnt already in our database
	@classmethod
	def is_user_present(cls, user_key):
		all_trailers = Trailers.all()
		for t in all_trailers:
			trailer_d = pickle.loads(t.trailer_data)
			if trailer_d['User'] == user_key:
				return True
		return False

	@classmethod
	def store_trailer(cls, uk, title, poster_image_link, youtube_trailer_link):
		data = {'User':uk, 'Title':title, 'poster_image_link':poster_image_link, 'youtube_trailer_link': youtube_trailer_link}
		new_trailer = Trailers(
			trailer_data = pickle.dumps(data)
		)
		new_trailer.put()

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
		#here we get all trailer objects from our Trailers DB and create our trailer html page
		#then we render home_page + trailer_page
		#db.delete(Trailers.all())
		trailer_html = create_trailer_page()

		self.write(home_page + trailer_html + page_closing_tags)

	def post(self):
		movie_title = self.request.get("title")
		poster_image_link = self.request.get("poster_image_link")
		youtube_trailer_link = self.request.get("youtube_trailer_link")
		
		user_key_gen = create_user_key()

		Trailers.store_trailer(user_key_gen, movie_title, poster_image_link, youtube_trailer_link)

		trailer_html = create_trailer_page()

		self.write(home_page + trailer_html + page_closing_tags)

def create_trailer_page():
	trailer_html = """
	"""
	#get all trailer objects
	#iterate throuhg them
	#for each trailer element we call a function called create_html_video 
	#passing in current element.trailer_data
	all_trailer_objects = Trailers.all()
	for t in all_trailer_objects:
		trailer_html += create_html_video(pickle.loads(t.trailer_data))
	return trailer_html

def create_html_video(trailer_data):
	youtube_link = trailer_data["youtube_trailer_link"]
	index = youtube_link.index("v=")+2
	youtube_id = youtube_link[index:]
	html_video = """
	<div class="row text-center margin-top-2">
		<div class="col-md-12">
			<div class='user lead'>User -%s-</div>
			<div class="lead title">Title -%s-</div>
			<div class="video-pic">
				<img src="%s" data-toggle='modal' data-target='#%s' />
			</div>
		</div>
	</div>
	<hr>

	<div class="modal" id="%s">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          	<iframe width="854" height="510" src="https://www.youtube.com/embed/%s" frameborder="0" allowfullscreen></iframe>
          </div>
        </div>
      </div>
    </div>
	""" % (

		trailer_data["User"],
		trailer_data["Title"],
		trailer_data["poster_image_link"],
		trailer_data["User"],
		trailer_data["User"],
		youtube_id
		# trailer_data["youtube_trailer_link"],
		# trailer_data["youtube_trailer_link"]
	)
	return html_video
#	""" % (trailer_data["User"], trailer_data["Title"], trailer_data["poster_image_link"], trailer_data["youtube_trailer_link"])

#<video width="320" height="240"  poster="%s" source="%s"></video>
def get_hash():
	return string.letters+string.digits+string.letters+string.digits

def create_player_key():
    return "".join([get_hash()[random.randrange(0, len(get_hash()))] for n in range(10)])

def create_user_key():
	key = create_player_key()
	while Trailers.is_user_present(key):
		key = create_player_key()
	return key
	#create random key
	#while random key is present in db
		#create random key
	#return key


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
