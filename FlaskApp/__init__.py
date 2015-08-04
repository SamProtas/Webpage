from flask import Flask, render_template, session, request, jsonify, json
from get_locations import *
from stats_HG import *
import requests
import os, sys

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(PROJECT_ROOT, 'Yahoo_Fantasy'))

from stats_fantasy import *
from winnings_fantasy import * 

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home_skeleton.html", title="Home")

@app.route('/about')
def contact():
	return render_template("about_skeleton.html", title="About")

@app.route('/contact', methods=['GET', 'POST'])
def about():
	return render_template("contact_skeleton.html", title="Contact" )

@app.route('/construction')
def construction():
	return render_template("construction.html", title="Coming Soon")
	
@app.route('/projects')
def datascrape():
	return render_template("projects_skeleton.html", title="Projects")

@app.route('/instagram')
def chart1():
	return render_template("instagram_skeleton.html", title="Datascrape-Instagram")

@app.route('/stubhub')
def stubhub():
	return render_template("construction.html", title="Stubhub")

@app.route('/fantasy_football', methods=['GET', 'POST'])
def fantasy_football():
	return render_template("fantasy.html", title="Fantasy_Football")

@app.route('/LowerMerion')
def LowerMerion():
	x = points_above_average_LM()
	df_points = x[0] 
	num_of_dfs = len(df_points)
	names = x[1]
	df_length = len(names)
	totals = counting_stats_LM() #y is entire set of lists
	len_managers = len(totals)
 	averages = averages_LM()
 	draft_pos = draft_pos_LM()
 	z=pick_vs_place_LM()
	length_pick_vs_place = len(z)
	draft_year=z['year'].tolist()
	draft_name=z['manager_name'].tolist()
	draft_team=z['manager_team'].tolist()
	draft_pick=z['pick'].tolist()
	draft_place=z['place'].tolist()
	champions=champions_lm()
	first_place=champions[0]
	reg_season_champs=champions[1]
	length_champions = len(champions[0])

	n = points_vs_pick_LM()
	length_n=len(n[3])

	earnings=earnings_lm()
	total_buyin = sum(earnings['buyin'])
	total_earned = sum(earnings['weekly']) + sum(earnings['yearly']) + sum(earnings['mostpoints']) + sum(earnings['regseason'])


	return render_template("LowerMerion.html", title="Extraordinary_Jackasses", df_points=df_points, num_of_dfs=num_of_dfs, names=names, 
												df_length=df_length, len_managers = len_managers, totals=totals, averages=averages, 
												draft_pos=draft_pos,#length_totals=length_totals, 
												draft_year=draft_year, draft_name=draft_name, draft_team=draft_team, draft_pick=draft_pick, 
												draft_place=draft_place, length_pick_vs_place=length_pick_vs_place, n=n, length_n=length_n,
												first_place=first_place, reg_season_champs=reg_season_champs, length_champions=length_champions,
												earnings=earnings, total_buyin=total_buyin, total_earned=total_earned)

@app.route('/SigmaChi')
def SimgaChi():
	x = points_above_average_EX()
	df_points = x[0] 
	num_of_dfs = len(df_points)
	names = x[1]
	df_length = len(names)
	totals = counting_stats_EX() 
	len_managers = len(totals)
 	averages_ex = averages_EX()  #Why is this not returning correctly on server?
 	
 	draft_pos = draft_pos_EX()
	z=pick_vs_place_ex()
	length_pick_vs_place = len(z)
	draft_year=z['year'].tolist()
	draft_name=z['manager_name'].tolist()
	draft_team=z['manager_team'].tolist()
	draft_pick=z['pick'].tolist()
	draft_place=z['place'].tolist()
	n = points_vs_pick_ex()
	length_n=len(n[3])
	######### TABLES ##########
	champions=champions_ex()
	first_place=champions[0]
	reg_season_champs=champions[1]
	length_champions = len(champions[0])

	earnings=earnings_ex()
	total_buyin = sum(earnings['buyin'])
	total_earned = sum(earnings['weekly']) + sum(earnings['yearly']) + sum(earnings['mostpoints']) + sum(earnings['regseason'])


	return render_template("SigmaChi.html", title="SigmaChi Fantasy Football",df_points=df_points, num_of_dfs=num_of_dfs, names=names, 
												df_length=df_length, len_managers = len_managers, totals=totals, averages_ex=averages_ex, 
												draft_pos=draft_pos,#length_totals=length_totals, 
												draft_year=draft_year, draft_name=draft_name, draft_team=draft_team, draft_pick=draft_pick, 
												draft_place=draft_place, length_pick_vs_place=length_pick_vs_place, n=n, length_n=length_n,
												first_place=first_place, reg_season_champs=reg_season_champs, length_champions=length_champions,
												earnings=earnings, total_buyin=total_buyin, total_earned=total_earned)


	
@app.route('/statistics_followers', methods=['GET', 'POST'])
def stats():
 	x = Followers_per_hour()
 	follower_rate = x[0]
 	length = x[1]
 	followers = x[2]
 	Pos_vs_Neg = x[3]
 	Time_of_post = x[4]
  	Likes_per_post = x[5]
  	length2 = x[6]
  	yaxis=x[7]
 	df_city=post_by_long_lat()
 	length_df_city = len(df_city['Cities'])

 	if request.method=="POST":
 		prediction=int(request.form['Submission'])
 		y = date_predict(prediction)
 		r2=y[1]
 		enddate=y[0]
 		return render_template("statistics_followerrate_skeleton.html", title="stats", data = follower_rate, length= length, data2=followers, pos_neg=Pos_vs_Neg, enddate=enddate, r2=r2, df_city=df_city, length_df_city=length_df_city, Time_of_post=Time_of_post, Likes_per_post = Likes_per_post, length2=length2, yaxis=yaxis)
	
 	else:
 		return render_template("statistics_followerrate_skeleton.html", title="stats", data = follower_rate, length= length, data2=followers, pos_neg=Pos_vs_Neg, df_city=df_city, length_df_city=length_df_city, Time_of_post=Time_of_post, Likes_per_post = Likes_per_post, length2=length2, yaxis=yaxis)


@app.route('/Likes_per_post', methods=['GET', 'POST'])
def instagramtest():
  	x = Followers_per_hour()
  	Time_of_post = x[4]
  	Likes_per_post = x[5]
  	length = x[6]
  	yaxis=x[7]
 	return render_template("Likes_per_post.html", title="instagramtest", Time_of_post=Time_of_post, Likes_per_post = Likes_per_post, length=length, yaxis=yaxis) 


#@app.route('/locations', methods=['GET', 'POST'])
# #def googlemap():
# 	#z=request.form["yourname"]
# #	y=request.form["youremail"]
#  #	x = get_locations('54500086', '33', 33)
# #	return render_template("locations.html", title="location", data3 = x, posts_display = int(y))

@app.route('/test', methods=['GET', 'POST'])
def test():

	averages = averages_EX()
	len_managers = len(averages['manager_name'])

	return render_template("testt.html", title="test", averages = averages, len_managers=len_managers)


if __name__ == "__main__":
	
    app.run(debug=True)