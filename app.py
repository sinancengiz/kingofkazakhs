#Dependencies
from flask import Flask , g, render_template, flash, redirect , url_for, request, jsonify
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user , logout_user, login_required, current_user
import models
import forms

DEBUG =True
PORT = 8000

app = Flask(__name__)
app.secret_key = "justrandomstuff"

#set up  login mananager
login_manager = LoginManager()
login_manager.init_app(app) # just makes connection to our app
login_manager.login_view = "login" # where we direct when user is not login yet

@login_manager.user_loader
def load_player(player_id):
    try:
        return models.Player.get(models.Player.id == player_id)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    '''Connect to the database before each request'''
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user

@app.after_request
def after_request(response):  
    '''close the database connection after each request'''
    g.db.close()
    return response

# This hook ensures that the connection is closed when we've finished
# processing the request.
@app.teardown_request
def _db_close(response):
    if not g.db.is_closed():
        g.db.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Yay, you registered to the game start playing!", "success")
        models.Player.create_player(
            player_name=form.player_name.data,
            email=form.email.data,
            password=form.password.data
        )

        models.City.create_city(
          city_name = f"{form.player_name.data}polis",
          king_of_city = form.player_name.data
        )
        models.Population.create_population(
          king_name = form.player_name.data,
        )
        return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            player = models.Player.get(models.Player.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match!", "error")
            
        else:
            if check_password_hash(player.password, form.password.data):
                login_user(player)
                flash("You've been logged in!", "success")
                return redirect(url_for('game_main'))
            else:
                flash("Your email or password doesn't match!", "error")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/game_main')
@login_required
def game_main():
    village_data = models.City.get(models.City.king_of_city == g.user.player_name)
    population_data = models.Population.get(models.Population.king_name == g.user.player_name)
    player = models.Player.get(models.Player.email == g.user.email)
    return render_template('game_main.html', village_data = village_data, population_data= population_data,player=player)

@app.route('/village')
@login_required
def village():
    village_data = models.City.get(models.City.king_of_city == g.user.player_name)
    population_data = models.Population.get(models.Population.king_name == g.user.player_name)
    player = models.Player.get(models.Player.email == g.user.email)
    return render_template("village.html", village_data = village_data, population_data= population_data,player=player)

@app.route('/castle')
@login_required
def castle():
    village_data = models.City.get(models.City.king_of_city == g.user.player_name)
    population_data = models.Population.get(models.Population.king_name == g.user.player_name)
    player = models.Player.get(models.Player.email == g.user.email)
    return render_template("castle.html", village_data = village_data, population_data= population_data,player=player)

@app.route('/farm')
@login_required
def farm():
    village_data = models.City.get(models.City.king_of_city == g.user.player_name)
    population_data = models.Population.get(models.Population.king_name == g.user.player_name)
    player = models.Player.get(models.Player.email == g.user.email)
    return render_template("farm.html", village_data = village_data, population_data= population_data,player=player)

@app.route('/gold_mine')
@login_required
def gold_mine():
    village_data = models.City.get(models.City.king_of_city == g.user.player_name)
    population_data = models.Population.get(models.Population.king_name == g.user.player_name)
    player = models.Player.get(models.Player.email == g.user.email)
    return render_template("gold_mine.html", village_data = village_data, population_data= population_data,player=player)

@app.route('/stone_quarry')
@login_required
def stone_quarry():
    village_data = models.City.get(models.City.king_of_city == g.user.player_name)
    population_data = models.Population.get(models.Population.king_name == g.user.player_name)
    player = models.Player.get(models.Player.email == g.user.email)
    return render_template("stone_quarry.html", village_data = village_data, population_data= population_data,player=player)

@app.route('/lumberjack')
@login_required
def lumberjack():
    village_data = models.City.get(models.City.king_of_city == g.user.player_name)
    population_data = models.Population.get(models.Population.king_name == g.user.player_name)
    player = models.Player.get(models.Player.email == g.user.email)
    return render_template("lumberjack.html", village_data = village_data, population_data= population_data,player=player)

@app.route('/wall')
@login_required
def wall():
    village_data = models.City.get(models.City.king_of_city == g.user.player_name)
    population_data = models.Population.get(models.Population.king_name == g.user.player_name)
    player = models.Player.get(models.Player.email == g.user.email)
    return render_template("wall.html", village_data = village_data, population_data= population_data,player=player)


@app.route('/next_year')
@login_required
def next_year():
    player = models.Player.get(models.Player.email == g.user.email)
    population = models.Population.get(models.Population.king_name == g.user.player_name)
    city = models.City.get(models.City.king_of_city == g.user.player_name)
    population_max = city.population_max
    # increase population each year
    total_population = population.total_population
    total_population = total_population * 1.05
    total_population = int(total_population)
    
    if player.food > 0:
        if population_max > total_population :
            new_population = total_population - population.total_population
            population.unassingned_population += new_population
            population.total_population += new_population
            population.save()

        else:
            new_population = population_max - population.total_population
            population.unassingned_population += new_population
            population.total_population += new_population
            population.save()
    #increase stone, gold and wood and food each year
    player.food += population.farmer * 10
    player.wood += population.lumberjack * 5
    player.stone += population.stone_worker * 3
    player.gold += population.gold_miner * 1
    player.save()
    #subtract soldiers spendings
    if player.food >= 0:
        player.food -= (((population.spearman + population.swordsman + population.archers) * 2)
                        + ((population.ligth_cavalry + population.heavy_cavalry + population.mounted_archer) * 3) 
                        + population.total_population)
        if player.food <= 0:
            player.food = 0
    
    if player.food <= 0:
        population.spearman -= int(population.spearman * 0.1)
        population.swordsman -= int(population.swordsman * 0.1)
        population.archers -= int(population.archers * 0.1)
        population.ligth_cavalry -= int(population.ligth_cavalry * 0.1)
        population.heavy_cavalry -= int(population.heavy_cavalry * 0.1)
        population.mounted_archer -= int(population.mounted_archer * 0.1)
        population.farmer -= int(population.farmer * 0.02)
        population.stone_worker -= int(population.stone_worker * 0.1)
        population.lumberjack -= int(population.lumberjack * 0.1)
        population.gold_miner -= int(population.gold_miner * 0.1)
        population.unassingned_population -= int(population.unassingned_population * 0.1)
        population.total_population -= int(population.total_population * 0.1)

        population.save()

    if player.gold >= 0:
        player.gold -= ((population.spearman ) + (population.swordsman + population.archers) *2 +
                        (population.ligth_cavalry  + population.mounted_archer) * 3 + (population.heavy_cavalry * 5))
        if player.gold <= 0:
            player.gold = 0
    
    if player.gold <= 0:
        population.total_population -= int(population.spearman * 0.1)
        population.spearman -= int(population.spearman * 0.1)
        population.total_population -= int(population.swordsman * 0.1)
        population.swordsman -= int(population.swordsman * 0.1)
        population.total_population -= int(population.archers * 0.1)
        population.archers -= int(population.archers * 0.1)
        population.total_population -= int(population.ligth_cavalry * 0.1)
        population.ligth_cavalry -= int(population.ligth_cavalry * 0.1)
        population.total_population -= int(population.heavy_cavalry * 0.1)
        population.heavy_cavalry -= int(population.heavy_cavalry * 0.1)
        population.total_population -= int(population.mounted_archer * 0.1)
        population.mounted_archer -= int(population.mounted_archer * 0.1)
        
        population.save()
    # increae game year each year
    player.game_year = player.game_year + 1
    player.save()
    
    return redirect(url_for('game_main'))

@app.route('/city_level_up')
@login_required
def city_level_up():
    city = models.City.get(models.City.king_of_city == g.user.player_name)
    player = models.Player.get(models.Player.email == g.user.email)
    if player.gold >= (50 * (2 ** city.city_level)) and player.stone > (100 * (2 ** city.city_level)):
        city.city_level += 1
        city.population_max = city.population_max * 1.5
        city.save()
        player.gold -= 50 * (2 ** city.city_level) 
        player.stone -= 100 *  (2 ** city.city_level)
        player.save()

    return redirect(url_for('game_main'))

@app.route('/farm_level_up')
@login_required
def farm_level_up():
    city = models.City.get(models.City.king_of_city == g.user.player_name)
    player = models.Player.get(models.Player.email == g.user.email)
    if player.gold >= (20 * (2 ** city.farm)) and player.wood >= (50 * (2 ** city.farm)):
        player.gold -= 20 * (2 ** city.farm) 
        player.wood -= 50 *  (2 ** city.farm)
        city.farm += 1
        city.save()
        player.save()

    return redirect(url_for('farm'))

@app.route('/gold_mine_level_up')
@login_required
def gold_mine_level_up():
    city = models.City.get(models.City.king_of_city == g.user.player_name)
    player = models.Player.get(models.Player.email == g.user.email)
    if player.stone >= (40 * (2 ** city.gold_mine)) and player.wood >= (80 * (2 ** city.gold_mine)):
        player.stone -= (40 * (2 ** city.gold_mine)) 
        player.wood -= (80 * (2 ** city.gold_mine))
        city.gold_mine += 1
        city.save()
        player.save()

    return redirect(url_for('gold_mine'))

@app.route('/stone_quarry_level_up')
@login_required
def stone_quarry_level_up():
    city = models.City.get(models.City.king_of_city == g.user.player_name)
    player = models.Player.get(models.Player.email == g.user.email)
    if player.gold >= (30 * (2 ** city.stone_quary)) and player.wood >= (50 * (2 ** city.stone_quary)):
        player.gold -= (30 * (2 ** city.stone_quary)) 
        player.wood -= (50 * (2 ** city.stone_quary))
        city.stone_quary += 1
        city.save()
        player.save()

    return redirect(url_for('stone_quarry'))

@app.route('/lumberjack_level_up')
@login_required
def lumberjack_level_up():
    city = models.City.get(models.City.king_of_city == g.user.player_name)
    player = models.Player.get(models.Player.email == g.user.email)
    if player.gold >= (30 * (2 ** city.lumberjack)) and player.stone >= (50 * (2 ** city.lumberjack)):
        player.gold -= (30 * (2 ** city.lumberjack)) 
        player.stone -= (50 * (2 ** city.lumberjack))
        city.lumberjack += 1
        city.save()
        player.save()

    return redirect(url_for('lumberjack'))


@app.route('/wall_level_up')
@login_required
def wall_level_up():
    city = models.City.get(models.City.king_of_city == g.user.player_name)
    player = models.Player.get(models.Player.email == g.user.email)
    if player.gold >= (3000 * (2 ** city.wall_level)) and player.stone >= (25000 * (2 ** city.wall_level)):
        player.gold -= (3000 * (2 ** city.wall_level)) 
        player.stone -= (25000 * (2 ** city.wall_level))
        city.wall_level += 1
        city.save()
        player.save()

    return redirect(url_for('wall'))


@app.route('/assin_farmers' , methods=['POST'])
def assin_farmers():
    city = models.City.get(models.City.king_of_city == g.user.player_name)
    population = models.Population.get(models.Population.king_name == g.user.player_name)
    if request.form['assin_farmers']:
        number = request.form["assin_farmers"]
        number = int(number)
        if population.unassingned_population >= number and (city.farm * 1000) >= (population.farmer + number):
            population.farmer += number
            population.unassingned_population -= number
        population.save()
    return redirect(url_for('farm'))

@app.route('/unassin_farmers', methods=['POST'])
def unassin_farmers():
    if request.form['unas_farmer']:
        unassin_farmer_number = request.form['unas_farmer']
        unassin_farmer_number = int(unassin_farmer_number)
        population = models.Population.get(models.Population.king_name == g.user.player_name)
        if population.farmer >= unassin_farmer_number:
            population.farmer -= unassin_farmer_number
            population.unassingned_population += unassin_farmer_number
        population.save()
    return redirect(url_for('farm'))

@app.route('/assin_gold_miners', methods=['POST'])
def assin_gold_miners():
    city = models.City.get(models.City.king_of_city == g.user.player_name)
    if request.form['assin_gold_miners']:
        assin_gold_miners_number = request.form['assin_gold_miners']
        assin_gold_miners_number = int(assin_gold_miners_number)
        population = models.Population.get(models.Population.king_name == g.user.player_name)
        if population.unassingned_population >= assin_gold_miners_number and (city.gold_mine * 500) >= (population.gold_miner + assin_gold_miners_number):
            population.gold_miner += assin_gold_miners_number
            population.unassingned_population -= assin_gold_miners_number
        population.save()
    return redirect(url_for('gold_mine'))


@app.route('/unassin_gold_miners', methods=['POST'])
def unassin_gold_miners():
    if request.form['unassin_gold_miners']:
        unassin_gold_miners_number = request.form['unassin_gold_miners']
        unassin_gold_miners_number = int(unassin_gold_miners_number)
        population = models.Population.get(models.Population.king_name == g.user.player_name)
        if population.gold_miner >= unassin_gold_miners_number:
            population.gold_miner -= unassin_gold_miners_number
            population.unassingned_population += unassin_gold_miners_number
        population.save()
    return redirect(url_for('gold_mine'))

@app.route('/assin_stone_workers', methods=['POST'])
def assin_stone_workers():
    city = models.City.get(models.City.king_of_city == g.user.player_name)
    if request.form['assin_stone_workers']:
        assin_stone_workers_number = request.form['assin_stone_workers']
        assin_stone_workers_number = int(assin_stone_workers_number)
        population = models.Population.get(models.Population.king_name == g.user.player_name)
        if population.unassingned_population >= assin_stone_workers_number and (city.stone_quary * 500) >= (population.stone_worker + assin_stone_workers_number):
            population.stone_worker += assin_stone_workers_number
            population.unassingned_population -= assin_stone_workers_number
        population.save()
    return redirect(url_for('stone_quarry'))

@app.route('/unassin_stone_workers', methods=['POST'])
def unassin_stone_workers():
    if request.form['unassin_stone_workers']:
        unassin_stone_workers_number = request.form['unassin_stone_workers']
        unassin_stone_workers_number = int(unassin_stone_workers_number)
        population = models.Population.get(models.Population.king_name == g.user.player_name)
        if population.stone_worker >= unassin_stone_workers_number:
            population.stone_worker -= unassin_stone_workers_number
            population.unassingned_population += unassin_stone_workers_number
        population.save()
    return redirect(url_for('stone_quarry'))

@app.route('/assin_lumber_workers', methods=['POST'])
def assin_lumber_workers():
    city = models.City.get(models.City.king_of_city == g.user.player_name)
    population = models.Population.get(models.Population.king_name == g.user.player_name)
    if request.form['assin_lumber_workers']:
        assin_lumber_workers_number = request.form['assin_lumber_workers']
        assin_lumber_workers_number = int(assin_lumber_workers_number)
        if population.unassingned_population >= assin_lumber_workers_number and (city.lumberjack * 500) >= (population.lumberjack + assin_lumber_workers_number):
            population.lumberjack += assin_lumber_workers_number
            population.unassingned_population -= assin_lumber_workers_number
        population.save()
    return redirect(url_for('lumberjack'))

@app.route('/unassin_lumber_workers', methods=['POST'])
def unassin_lumber_workers():
    if request.form['unassin_lumber_workers']:
        unassin_lumber_workers_number = request.form['unassin_lumber_workers']
        unassin_lumber_workers_number = int(unassin_lumber_workers_number)
        population = models.Population.get(models.Population.king_name == g.user.player_name)
        if population.lumberjack >= unassin_lumber_workers_number:
            population.lumberjack -= unassin_lumber_workers_number
            population.unassingned_population += unassin_lumber_workers_number
        population.save()
    return redirect(url_for('lumberjack'))

@app.route('/assin_spearman', methods=['POST'])
def assin_spearman():
    if request.form['assin_spearman']:
        amount = request.form['assin_spearman']
        amount = int(amount)
        population = models.Population.get(models.Population.king_name == g.user.player_name)
        if population.unassingned_population >= amount:
            population.spearman += amount
            population.unassingned_population -= amount
        population.save()
    return redirect(url_for('castle'))

@app.route('/unassin_spearman', methods=['POST'])
def unassin_spearman():
    if request.form['unassin_spearman']:
        amount = request.form['unassin_spearman']
        amount = int(amount)
        population = models.Population.get(models.Population.king_name == g.user.player_name)
        if population.spearman >= amount:
            population.spearman -= amount
            population.unassingned_population += amount
        population.save()
    return redirect(url_for('castle'))

@app.route('/assin_swordsman', methods=['POST'])
def assin_swordsman():
    if request.form['assin_swordsman']:
        amount = request.form['assin_swordsman']
        amount = int(amount)
        population = models.Population.get(models.Population.king_name == g.user.player_name)
        if population.unassingned_population >= amount:
            population.swordsman += amount
            population.unassingned_population -= amount
        population.save()
    return redirect(url_for('castle'))

@app.route('/unassin_swordsman', methods=['POST'])
def unassin_swordsman():
    if request.form['unassin_swordsman']:
        amount = request.form['unassin_swordsman']
        amount = int(amount)
        population = models.Population.get(models.Population.king_name == g.user.player_name)
        if population.swordsman >= amount:
            population.swordsman -= amount
            population.unassingned_population += amount
        population.save()
    return redirect(url_for('castle'))

@app.route('/assin_archers', methods=['POST'])
def assin_archers():
    if request.form['assin_archers']:
        amount = request.form['assin_archers']
        amount = int(amount)
        population = models.Population.get(models.Population.king_name == g.user.player_name)
        if population.unassingned_population >= amount:
            population.archers += amount
            population.unassingned_population -= amount
        population.save()
    return redirect(url_for('castle'))

@app.route('/unassin_archers', methods=['POST'])
def unassin_archers():
    if request.form['unassin_archers']:
        amount = request.form['unassin_archers']
        amount = int(amount)
        population = models.Population.get(models.Population.king_name == g.user.player_name)
        if population.archers >= amount:
            population.archers -= amount
            population.unassingned_population += amount
        population.save()
    return redirect(url_for('castle'))

@app.route('/assin_ligth_cavalry', methods=['POST'])
def assin_ligth_cavalry():
    if request.form['assin_ligth_cavalry']:
        amount = request.form['assin_ligth_cavalry']
        amount = int(amount)
        population = models.Population.get(models.Population.king_name == g.user.player_name)
        if population.unassingned_population >= amount:
            population.ligth_cavalry += amount
            population.unassingned_population -= amount
        population.save()
    return redirect(url_for('castle'))

@app.route('/unassin_ligth_cavalry', methods=['POST'])
def unassin_ligth_cavalry():
    if request.form['unassin_ligth_cavalry']:
        amount = request.form['unassin_ligth_cavalry']
        amount = int(amount)
        population = models.Population.get(models.Population.king_name == g.user.player_name)
        if population.ligth_cavalry >= amount:
            population.ligth_cavalry-= amount
            population.unassingned_population += amount
        population.save()
    return redirect(url_for('castle'))

@app.route('/assin_heavy_cavalry', methods=['POST'])
def assin_heavy_cavalry():
    if request.form['assin_heavy_cavalry']:
        amount = request.form['assin_heavy_cavalry']
        amount = int(amount)
        population = models.Population.get(models.Population.king_name == g.user.player_name)
        if population.unassingned_population >= amount:
            population.heavy_cavalry += amount
            population.unassingned_population -= amount
        population.save()
    return redirect(url_for('castle'))

@app.route('/unassin_heavy_cavalry', methods=['POST'])
def unassin_heavy_cavalry():
    if request.form['unassin_heavy_cavalry']:
        amount = request.form['unassin_heavy_cavalry']
        amount = int(amount)
        population = models.Population.get(models.Population.king_name == g.user.player_name)
        if population.heavy_cavalry >= amount:
            population.heavy_cavalry -= amount
            population.unassingned_population += amount
        population.save()
    return redirect(url_for('castle'))

@app.route('/assin_mounted_archer', methods=['POST'])
def assin_mounted_archer():
    if request.form['assin_mounted_archer']:
        amount = request.form['assin_mounted_archer']
        amount = int(amount)
        population = models.Population.get(models.Population.king_name == g.user.player_name)
        if population.unassingned_population >= amount:
            population.mounted_archer+= amount
            population.unassingned_population -= amount
        population.save()
    return redirect(url_for('castle'))

@app.route('/unassin_mounted_archer', methods=['POST'])
def unassin_mounted_archer():
    if request.form['unassin_mounted_archer']:
        amount = request.form['unassin_mounted_archer']
        amount = int(amount)
        population = models.Population.get(models.Population.king_name == g.user.player_name)
        if population.mounted_archer >= amount:
            population.mounted_archer-= amount
            population.unassingned_population += amount
        population.save()
    return redirect(url_for('castle'))


@app.route("/map")
def map():
    return render_template("map.html")



@app.route('/restart_game')
@login_required
def restart_game():
    #reset population table
    population = models.Population.get(models.Population.king_name == g.user.player_name)
    population.total_population = 1000
    population.unassingned_population = 200
    population.farmer = 300
    population.gold_miner = 50
    population.stone_worker = 100
    population.lumberjack = 150
    population.spearman = 60
    population.swordsman = 30
    population.archers = 30
    population.ligth_cavalry =30
    population.heavy_cavalry = 20
    population.mounted_archer = 30
    population.save()
    # reset city table
    city = models.City.get(models.City.king_of_city == g.user.player_name)
    city.city_level = 1
    city.farm = 1
    city.stone_quary = 1
    city.academy = 1
    city.wall_level = 1
    city.barracks = 1
    city.gold_mine = 1
    city.lumberjack = 1
    city.stable_level = 1
    city.population_max = 5000
    city.save()
    #reset player table
    player = models.Player.get(models.Player.email == g.user.email)
    player.gold = 1000
    player.wood = 1000
    player.stone = 1000
    player.food = 1000
    player.game_year = 650
    player.save()

    return redirect(url_for('game_main'))

if __name__ == "__main__":
    models.initialize()
    app.run(debug=True)