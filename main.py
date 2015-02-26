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

#https://www.youtube.com/watch?v=R2qHKXL-_vw best of ipman 
#https://www.youtube.com/watch?v=jGoVzVCXCwU top 5 fight scenes
#https://www.youtube.com/watch?v=-W1qR80oOt4 the book of eli barfight scene
#
import webapp2
import os
import jinja2
import re
import random
import pickle
import string
import json
import movie_class
from google.appengine.ext import db

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
				display: inline;
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
				color: red;
				height: 5px;
			}
			img {
				width: 400px;
				height: 400px;
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
        input {
        	width: 300px;
        	height: 100px;
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
					<img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBwgHBgkIBwgKCgkLDRYPDQwMDRsUFRAWIB0iIiAdHx8kKDQsJCYxJx8fLT0tMTU3Ojo6Iys/RD84QzQ5OjcBCgoKDQwNGg8PGjclHyU3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3N//AABEIALoAugMBEQACEQEDEQH/xAAcAAEAAgIDAQAAAAAAAAAAAAAABgcBAwIEBQj/xABEEAABAwICBAkFDgYDAAAAAAAAAQIDBBEFBgcSITETQWFxgZGhwdEjUVKSsRQWMjM2QkNTVXJzgrLSREVjk6LCIiZi/8QAGwEBAAIDAQEAAAAAAAAAAAAAAAQFAQMGAgf/xAA2EQEAAQMBAwcLBAMBAAAAAAAAAQIDBBEFMVESFBUhQWGREyIzNEJTcYGh0eEGMrHBI1LwQ//aAAwDAQACEQMRAD8AvEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA01M8NPE+WokbHGxLuc5bIiGJmIjWXqiiquqKaY1mUGxbSPTQyPiwykdUaq/GyO1WrzJvXsIleZETpTC+x9gV1Ryr1WndG/7PEm0kY45fJQ0EacsT3L+o087udywp2DixvmqfnH2dV2f8xOW/D07fuwJ33Mc6utkbEwo9mfFwXPWY1/j0/sR/tMc5u8XrofCj2PrP3anZzzC7fiT05o2p3GOcXeL3GysOP8Az/n7uPvwzB9py9TfAxzi5xeui8P3f8sLm7MC/wA0m6m+A8vc4nReJ7uGPfbj/wBqT9ngPLXOJ0Zie7gTN2YE/mk3Z4Dy9zidGYnu4cvfhmD7Tl6k8B5e5xOi8P3cfVlucswpuxKTpY1e4zzi7xY6Kw/d/wA/dtbnnMabPd6dMLF/1M85ucXidj4U+x9Z+7Y3P2Ym/wAVE7ngb3DnN3i8zsXCn2Z8Zb49I2PttrtoZE5YHIvY7uPUZVzua52FiTu1j5/h6VDpMkR1sRw9qt43U7tqdC+JspzJ9qEW9+nqZj/FX4/hO8IxWixemSooJ2yN+cnG1fMqcRLorprjWlz+Rj3cerk3I0l37ntoZAAAAADCrYCp9JWOvrsTdhkL19y0y+UYm58nLzFdk3Jqq5MboddsTEi1a8tP7qt3dCGkVeag0NQaGoNDUGhqDQ1Boag0NQaGoNDUGhqDQ1Boag0NQaGr0suYxNgeKR1cTl4NVtMxF2Pbx3NluubdWqJm4tOVZm3Vv7O6V6U8rZ4mSxrdj2o5qpxopbxucDVTNM8mrfDaGAAAAAaKyZtNTSzv+DExz15kS5iZ0jVmmma6opjtfPck76iV88u2SVyvevKq3X2lNPXMy+jxTFHm07o6nG4ZLgLgLgLgLgLgLgLgLgLgLgLgLgLgL8gFy6OKxavK1M1yqrqdXQ7fM1dnYqFnj1cq3DidsW+RmVTHb1+O/wCqUG9WAAAAA8XOMvA5YxJ/9BydezvNd6dLcyl7Pp5WXbjvhRSrtKl3sMXAXAXAXAXAyiOXWsirZLrZL7BpO6CaoiNZnRjW2d5kLmAuAuAuAuAuAuAuBm4FpaI5dbCq2L0J79bU8CfiftmHKbfp0v0T3f2npLUQAAAAI1pEdq5SruVqJ2oaMn0VSx2TGuZQpMrXbwAAAAABKdGm3NcKf0pNnQb8f0iq216pPxhNMy5AocT16jD1Siq12rqt8m/nbxc6Eu5j019yhxNrX7Hm1edT3qyxfBMRwaZYq6nVtvnt2tXluQq7NdE7up0mLtLHydNJ0nhLzkU1J7IAAAAAAAFkaH33biTb8bF9qEzE7XNfqCOu3PxWSTXOAAAAAi2kpbZSqudn6kNOR6OVnsf1yn5qVTcVjtAAAAAAJVox+V0H4UnsJGP6RVbZ9Un4wulSxca61bRQVsKw1MTZGKm5U3AV3mTR+ketPh10ZvsxL6vO3wI9zHoq643rfF2xfs6U1+dH/dqB1uH1VC61REqN4nt2tXp4ukhV2qqN7pMbPsZMeZPXw7f++DqmtMAAAAAMixdDy+XxLmZ3kvE7XOfqDdb+azkJrmwAAAARXSZ8kqr7zP1Iacj0crPY/rlPzUmVrtC4C4C4C4C4Es0YL/2+D8GT2G/H9Iqts+qT8YXUWLjQDiq7QIfnSTAqKJz6ueOGrcl0iYms6Xnb3mu5coojzkvEw7+RV/ijq4/lUdbNBNUOfS0yU8a/NR178vIV1dUVTrEaOzxbVy1bim5Xypde54SS4C4C4C4FjaHvj8R5me1SZi9rnNv7rfzWehMc2yAAAAIppN+SNXyK1f8AJDTkejlZbI9cp+aklXaVrtC5ljUuDUuDUuDUuDVLNF3ywg/Bk9hux/SQq9s+qT8YXWq2QsXHPOxfG6DBqZZ8QqGRJa6N3udzJvU81100RrMt1jGu5E8m3Gv8K0zFpKra3XhweP3HCuzhnbZHcvmaQ7mRM9UOkxdiW7fnXp5U8Oz8oLJI+WR8kr3Pket3Pe5XOdzqpG39cruIiOqI6oYuYNS5k1Lg1Lg1Lg1LmDVY+hz4/EV5Gd5Mxe1z2391v5rRJjmwAAAARjSQxX5Rrv8Ay1HdqGm/6OVhsurTMoUYV+jtQAAAAAJLo+rqbDsyx1VbMyCFkMl3v2Ju2G2zMU1ayrtqWq7uNyKI1mZhIcx6TpJUdBl+NY27vdM7dq8rW+PUba8mZ6qFfi7EiPOyJ+Uf2r6qqairqHVFXNLPO/4UkrtZVI0zMzrK/oopojSiNIajD0AAAAAAADQWZoaatsSeqfOYidRLxY3ub2/V51uO6VnEtzwAAAAPDztDw+V8SjTjp39iX7jxcjWiUnCq5GTbq4TD5/vcrId5O8MsAAAAAGAAADIAAAAAAAXAtnQ5Fq4TWy2+HPbqRPEmY0ea5bbtWuRTTwj+1hklSAAAAA62IQtqKOWFyXR7FavSYmNepmmqaZiY7HzbUQPpKiWmkRUfC9Y1vyLYrNNJ0fQaK4rpiuO2NWu5h6LgLgLgLgLgLgLgLgLgLgLgLgLgLgL+cC89GdC6hytTI9qo+W8rr7/+S3TssWFmnSiHF7Uu+Uy65js6vBLDarwAAAAcXJfeBTmkzLs1LiTsSpo1dDL8bZNqKnGRL9uf3Q6TY+bRNHN656+xBCK6DrZDDAAAAAAAAAAAAAAFwPYytgc2OYnFE1irTtdeV9tlr7udTbaomqUHPzaca3PX507vu+gaOBtNTxxMRERrUQsOxxU9c6t4AAAAAAOtW0cVZCsUzUVFQCBYzo3paiR0lNeJVX6N1r9BpqsUVLOxtbIsxpM6x3o/UaN6xi+Smdblbc1TjcJTadvT7dDpv0f4m3c9F/Ipjm08W6NvWu2iWl2RcWTcrF/Kpjm1T1G3bM+zLguSMYTc2NevwHNq3vpzG7Yn6Na5Mxr6uH1neA5vU9dN4vCfD8uK5OxlPo4V/Ov7Rza4dNYnf4R93D3o419RF66+Bjm9w6axO/wj7splDGV+hi9dfAc3rOmsTv8ACPu5Jk3Gl+jh9d37Rze4dN4vf4flsbkrGF3si63eBnm9bz05i8J8Py2NyNiy/Vp0Ko5tU8ztyx2Uy2syDii73tT8imYxp4vE7dtf6S7Mejuvcqa0q9DDMY3e1zt6Oyj6vVw/RlrPR1XJI5qcV0ROzae6camN6Pc25fqiYoiI+srCwXBKXCYGx08bU1diWTcb4iI3Kiu5VcqmqudZl6hl4AAAAAAAAAGLIA1U8wDVb5kAxqM9FAHBs9FOoDHBM9BOoBwUfoJ1AOCj9BvUA4JnoJ1AZ4Nnop1AZ1W+ZAGqnmQBZAFgMgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB//9k=" />
				</div>
			</div>

			<div class="row text-center">
				<div class="col-md-12">

					<p class="lead">Want To Add a trailer To The List</p>
						<input type="text" id="title" placeholder="Movie Title" required >
						<input type="text" id="poster_image_link" placeholder="Poster Image Url" required >
						<input type="text" id="youtube_trailer_link" placeholder="Youtube Trailer Link" required >
						
						<br><input class="margin-top-2 btn btn-primary" id="submit_button" name="subm" value="Add To My Trailers">
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

		<div class="row text-center margin-top-2">

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

		#when we render the home_page we get our sample movie_objects from movie_class
		#iterate through each movie_object
		#store trailer_data
		#store the call to create_html_video on the trailer_data
		#add that html to the page

		#a note to the udacity reviewer. Before when I wrote the code
		#I didnt declare home_page global so imagine that line taken out
		#it gave me this unboundLocalError saying that home_page is being referenced before assignment
		#that is because in the get method, home_page was being declared
		#local to the get request

		global home_page
		titles_so_far = movie_class.titles_already
		sample_movies = movie_class.dylans_movies


		for m in sample_movies:
			if m.title not in titles_so_far:
				titles_so_far.append(m.title)
				html_video = m.create_html_video()
				home_page += html_video

		#add page closing tags
		home_page += page_closing_tags

		#display the awesome page we have dynamically created
		self.write(home_page)



	def post(self):
		#get our global home_page
		global home_page

		#grab the movie title the user is attempting to submit
		movie_title = self.request.get("title")

		#if the title is not in the list of titles uploaded so far
		#we add the title to the list and grab the poster image file and the youtube url
		if movie_title not in movie_class.titles_already:
			movie_class.titles_already.append(movie_title)
			poster_image_link = self.request.get("poster_image_link")
			youtube_trailer_link = self.request.get("youtube_trailer_link")

			#now that we have our data for our new movie object
			#we create a new movie object from our friend over in movie_class.py | pass in the data
			#get our html_video to add to our page
			#then add it to the page lol
			new_movie = movie_class.Movie(movie_title, poster_image_link, youtube_trailer_link)
			html_video = new_movie.create_html_video()
			home_page += html_video

			#since we are using an ajax request we use the json module to turn some text in json text
			#write the message in json to the success function of our ajax call
			json_man = json.dumps("reload")
			self.write(json_man)

		#if the title is in titles_already
		else:
			#write to the ajax function the json string exists
			#this will tell the client that the title they tried to submit already exists
			#and display an error to the user

			self.write(json.dumps("exists"));

app = webapp2.WSGIApplication([
    ('/', HomePage)
], debug=True)
