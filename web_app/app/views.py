from app import app
import os
from flask import Flask, flash, render_template, json, request, redirect, session, url_for
from app.queries import sayHello, getGameInformation, getClassProperties, getDevelopers, getGenres
from app.queries import generate_visualization_data

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/storeConfig')
def storeConfig():
    pass

@app.route('/query')
def queryPage():
    developer_list = getDevelopers()
    genre_list = getGenres()
    return render_template('query.html', developer_list=developer_list, genre_list=genre_list)

@app.route('/game', methods=['GET'])
def gamePage():
    '''
    pass game_id as 'mig_0'. do not pass the namespace -> mgns
    :return: game_info ---> dictionary (key, value pair with values being string)
                    keys are:
                    1. game_summary
                    2. name
                    3. released_year
                    4. platform_name
                    5. developer_name
                    6. publisher_name
                    7. game_mode_label
                    8. genre_label
                    9. theme_label
                    10. rating
                    11. seller_name
                    12. price
                    13. discount
                    14. url
             Note:
    '''
    game_id = request.args.get("game_id")
    game_info, recommended_games_info = getGameInformation(game_id)
    print(game_info)
    return render_template('game.html', game_info=game_info, rec_games_info=recommended_games_info)

@app.route('/getPropertiesForClass', methods=['GET', 'POST'])
def getPropertiesForClass():
    cur_class_name = request.args.get("class_name")
    class_properties_dict = getClassProperties()
    cur_prop_list = class_properties_dict[cur_class_name]
    result = {}
    result["vals"] = cur_prop_list
    return result

@app.route('/visualize')
def visualizationPage():
    class_properties_dict = getClassProperties()
    class_list = list(class_properties_dict.keys())
    return render_template('visualization.html', class_list=class_list)

@app.route('/getVisualizationData', methods=['GET', 'POST'])
def getVisualizationData():
    class_name = request.args.get("class_name")
    property_name = request.args.get("property_name")
    result = generate_visualization_data(class_name, property_name)
    result_dict = {}

    if not isinstance(result[0], tuple):
        result_dict["data_type"] = "continuous"
        result_dict["x_vals"] = result
    else:
        x_vals = []
        y_vals = []
        for key, val in result:
            x_vals.append(key)
            y_vals.append(val)

        result_dict = {}
        result_dict["data_type"] = "discrete"
        result_dict["x_vals"] = x_vals
        result_dict["y_vals"] = y_vals

    return result_dict
