import sys, argparse, json, pprint, subprocess, os
from django import template

#Creates a new view by generating stub functions for all the buttons and generating the panel context. The urls.py file still needs to manually be edited. 
def create_new_view(tables, base_view, replacement_tags, base_action):
    actions = ''
    for table in tables:
        for button in table['buttons']:
            actions = actions + substitute_tags(base_action, {'#Action_Name#': button['action']}) + '\n'
    replacement_tags['#Actions#'] = actions
    return substitute_tags(base_view, replacement_tags)

#Takes the base view as an argument and returns the view with all the tags substituted. 
def substitute_tags(base_view, replacement_tags):
    for tag in replacement_tags:
        base_view = base_view.replace(tag, str(replacement_tags[tag]))
    return base_view

def main():
    #Read arguments. Arguments are mostly self-explanatory, but you can refer to the help attribute for, well, help. 
    parser = argparse.ArgumentParser(prog = 'generate_table')
    parser.add_argument('--json_data', required = True, help = 'A json file containing data for the table. Consult the sample_json.json file.')
    parser.add_argument('--base_view', help = 'Optional. A file containing a base view. Consult the readme for how to write the base files.', default = 'panel_creator/base_view.py')
    parser.add_argument('--base_template', help = 'Optional. A file containing a base template. ', default = 'panel_creator/base_template.html')
    parser.add_argument('--base_action', help = 'Optional. A file containing a base action. ', default = 'panel_creator/base_action.py')
    parser.add_argument('--verbose', help = 'Optional. Set to True for a verbose output. ', default = False)


    args = parser.parse_args()
    json_data, base_view, base_template, base_action, verbose = args.json_data, args.base_view, args.base_template, args.base_action, args.verbose
    json_data = json.loads(open(json_data, 'r').read())

    #Open the base files that will be used to generate the new view and template. 
    base_view = open(base_view, 'r').read()
    base_template = open(base_template, 'r').read()
    base_action = open(base_action, 'r').read()

    #Extract all panel information from the json. 
    #panel_name is used when registering the panel to a dashboard. panel_header is the header that appears above all tables. panel_title is the text that is shown on the tab of the browser. 
    #target and dashboard are used when creating the panel via horizon. template_loc is the location of the index.html file. 
    panel_name = json_data['panel_name']
    panel_header = json_data['panel_header']
    panel_title = json_data['panel_title']
    target = json_data['target'] + panel_name
    dashboard = json_data['dashboard'] if 'dashboard' in json_data.keys() else '/'.join(target.split('/')[0:-1]).replace('/','.')
    template_loc = dashboard.split('.')[-1] + '/' + panel_name

    #Convert the table into a manageable format. 
    #Example : tables = [{'name':'table1name',
    #'columns':['col1', 'col2']},
    #'buttons':[{'name':'btnname', action:'btnaction', 'value':'btnvalue'}, ...]
    #'index':'col1'}, {... ]
    tables = json_data['tables']
    if verbose:
        print 'Loaded JSON data : ', tables
    tables = [{'name':table['name'], 'columns' : table['columns'] + [button['name'] for button in table['action-buttons']], 'buttons' : table['action-buttons']} for table in tables]

    #Modify the original views.py so that the context returns a tables array with the values described above. 
    replacement_tags = {'#Template_Location#' : template_loc, '#Tables_Dictionary#': str(tables), '#Panel_Header#': panel_header, '#Panel_Title#' : panel_title, '#Actions#' : ''}
    base_view = create_new_view(tables, base_view, replacement_tags, base_action)

    #Create panel directory and start the panel. 
    create_dir = 'mkdir ' + target
    create_app = './run_tests.sh -m startpanel ' + panel_name + ' --dashboard=' + dashboard + ' --target=' + target

    if verbose:
        print 'Creating dir : ', create_dir
    os.system(create_dir)

    if verbose:
        print 'Creating app : ', create_app
    os.system(create_app)

    #Replace the view and template. 
    #The template will use the tables array created earlier to create an actual table. 
    new_view = open(target + '/views.py', 'w')
    if verbose:
        print 'New view : \n', base_view
    new_view.write(base_view)

    new_template = open(target + '/templates/' + panel_name + '/index.html', 'w')
    new_template.write(base_template)


main()
