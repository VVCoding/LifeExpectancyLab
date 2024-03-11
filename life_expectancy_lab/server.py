# flask --app data_server run
from flask import Flask
from flask import request
from flask import render_template
import json


app = Flask(__name__, static_url_path='', static_folder='static')

# Gets the endpoints given a country
def endpoints(country):
    
    f = open("data/life_expectancy.json", "r")
    data = json.load(f)
    f.close()
    
     #Filter and reformat data for ease of access in the template
    requested_data = data[country]
    years = sorted(list(requested_data.keys()))
    line_endpoints =[]
    for i in range(len(years)-1): # make it easy to dynamically generate a line graph
        start_x = years[i] #generate endpoints for each line segment
        stop_x = years[i+1]
        line_endpoints.append([requested_data[start_x],requested_data[stop_x]] )
    
    return line_endpoints

# Returns the value of the universal average
def avgval():
    f = open("data/life_expectancy.json", "r")
    data = json.load(f)
    f.close()
    
    count = 0;
    countries = list(data.keys())
    all_years = sorted(list(data[countries[0]].keys()))
    era = 3*(int(all_years[-1])-int(all_years[0])+1)
    for country in countries:
        for lifexpect in data[country].values():
            count += int(lifexpect)
    
    average  = count/era
    return average



@app.route('/')
def index():
    f = open("data/life_expectancy.json", "r")
    data = json.load(f)
    f.close()

    #Filter and reformat data for ease of access in the template
    countries = list(data.keys())
    all_years = sorted(list(data[countries[0]].keys()))

    return render_template('index.html', all_years=all_years, cendpoints = endpoints("Canada"), mendpoints = endpoints("Mexico"), uendpoints = endpoints("UnitedStates"), avgval = avgval())
    

@app.route('/year')
def year():
    f = open("data/life_expectancy.json", "r")
    data = json.load(f)
    f.close()
    
    
    #check to see if year is in the query string portion of the URL
    requested_year = request.args.get('year')
    if requested_year == None:
        requested_year = list(data[0])[0] #just in case
        
    countries = list(data.keys())
    requested_data = {}
    for country in countries:
        requested_data[country] = data[country][requested_year]
    
    #represent all variables needed in render template
    # round values of life expectancy
    roundedu = round(requested_data["UnitedStates"],2)
    roundedc = round(requested_data["Canada"],2)  
    roundedm = round(requested_data["Mexico"],2) 
    
    # rounded values of percent of North American Average
    avgMex = round(((roundedm)/((roundedc+roundedm+roundedu)/3)*100),2)
    avgUSA = round(((roundedu)/((roundedc+roundedm+roundedu)/3)*100),2) 
    avgCanada = round(((roundedc)/((roundedc+roundedm+roundedu)/3)*100),2)  
    
    return render_template('year.html', requested_year= requested_year, data = requested_data, countries = countries, roundedu = roundedu, roundedm = roundedm, roundedc = roundedc, avgMex = avgMex, avgUSA = avgUSA, avgCanada = avgCanada)

app.run(debug=True)
