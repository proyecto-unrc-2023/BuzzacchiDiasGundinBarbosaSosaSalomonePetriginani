
#from features.environment import table_from_string
from logic.game_state import GameMode
from selenium import webdriver
from selenium.webdriver.common.by import By


###Scenario: Start a new game
@given(u'the game is not started')
def step_impl(context):
    pass

@when(u'we create a new game with an {rows:d}x{columns:d} board')
def step_impl(context, rows, columns):
    context.state.new_game(rows, columns)

@then(u'the game should be in spawn placement mode')
def step_impl(context):
    assert context.state.mode == GameMode.SPAWN_PLACEMENT

@then(u'the state of the board should be a 50x50 empty board')
def step_impl(context):
    emptyboard_50x50 = (' |'*49 + ' \n')*49 + ' |'*49 + ' '
    assert context.state.board.__str__() == emptyboard_50x50


###Scenario: Team Selection
@given(u'that I am on the game start screen')
def step_impl(context):
    context.driver = webdriver.Chrome()
    context.driver.get('http://localhost:5000/')

@given(u'I have already typed the username "{username}"')
def step_impl(context, username):
    context.username = username
    username_input = context.driver.find_element(By.ID, 'username')
    username_input.send_keys(username)

@when(u'I choose the team "{team}"')
def step_impl(context, team):
    context.team = team

@when(u'I click the "Start Game" button')
def step_impl(context):
    start_button = context.driver.find_element(By.XPATH, '//button[@type="submit"]')
    start_button.click()

@then(u'I should see the game screen with the "{team}"')
def step_impl(context, team):
    assert f'Welcome, {context.username}!' in context.driver.page_source
    assert f'You are part of the {team}.' in context.driver.page_source
    context.driver.quit()







