## Synopsis

Table creator is a simple tool for creating tables in horizon. It is an alternative to using premade tables as it generates the basic html which can later be modified to fit any use. 

The tool basically creates a new panel using run_tests.sh and modifies the views.py and index.html files to create a table based on the json data supplied. The new template extends a premade one, which simply iterates through the given tables, creating specified columns for it. 

You can use your custom base views and templates if you want, either by modifying the source file or by supplying the --base_view and --base_template arguments. You can use a very basic tag system to describe what exactly needs to be substituted and where. 

The tables were originally designed to be used with salt stack modules. That's why some of the code might be wonky and you might notice a --use_salt argument. This is the first iteration of this program, and I might remove it when and if I keep updating it. 

## Example usage

generate\_table.py should reside in the same folder as run_tests.sh. In order to use it, you must have a .json file which contains the table columns and other information. You can see the example table_json.json file for an example. 

Then use 
```
$python generate_table.py --json_data path/to/json_file.json
```

You can add --verbose True, and the script will print out what it wrote to the views.py file as well as the specific commands it ran. 

You have to manually register the panel with the dashboard it's in, by editing the dashboards.py file. You can refer to openstack's documentation for this. 

If your view has buttons, the panel will define stub functions for them, but you still need to manually edit the urls.py file to enable them. 

The base template extends a premade template called vapour-base.html. This should go in openstack_dashboard/templates. 

After this, the panel should be visible. 

## Project files

**generate_table.py**

This file basically does all the work. Usage is explained in the previous part. 

**panel_creator/** 

Other files that have something to do with the script are located in this directory. Exceptions are vapour-base.html, salt_utils.py and salt_api.py . 

**vapour-base.html**

This is a base template that all the other views will use. It basicaly extends the base template used by openstack and adds the tables. This file should reside in openstack_dashboards/templates/
This template uses the following variables : 

* tables - this is a list of all the tables that are going to be shown in the panel. Tables have the following format : 
        tables = [{'name':'table1name', 
                   'columns':['col1', 'col2']},
                   'buttons':[{'name':'btnname', action:'btnaction', 'value':'btnvalue'}, ...], 
                   'index':'col1'}, 
                  {'name' : ... }
                 ]
* panel_header - this appears above all the tables
* panel_title - appears in the tab in the browser

**base_view.py**

When a new panel is created, its views.py file is replaced with this one, where the #tags# are replaced with generated values in from the generate_table.py and it supplies the afore-mentioned variables from the json file. 

**base_template.py**

This is the template that the new panel will have. As you can see, it's pretty basic, as it just specifies the blocks that are used by the vapour-base.html template. 

**base_action.py**

The base for the generated views that will be called for your buttons. 

**table_json.json**

A sample file containing a json file to explain the structure.

## Customizing

If you have a custom view, template or action that you would want to use instead of the default one, you can do so with : 
```
$python generate\_table.py --json\_data path/to/json --base\_view path/to/view --base\_template path/to/template --base\_action path/to/action
```
For the moment, base views use very rudimentary tags which basically look like #tag#. I am tempted to switch to jinja, but i kinda wanted to refrain from using other modules. 

The defaut view uses these tags. 
 * #Template\_Location# - which is the location of the template. This is calculated from the target value. 
 * #Tables\_Dictionary# - which is a list of all tables with their names and columns and looks like the following : 
  ```
    [{'name':'table1name', 'collumns':['col1', 'col2']},{'name':'table2name', 'columns':['col3', 'col4']}]
```
 * #Panel\_Header# - which is the same header as defined in the json data. 
 * #Panel\_Title# - which is the same title as in the json. 
 * #Actions# - which are the actions used by the buttons. 

I have pondered adding support for custom tags. The only problem is that there's barely any reason to use tags if you're not using them with variables. So for the moment, you may use custom tags by modifying the source file. Namely, find the line :

    replacement\_tags = {'#Template\_Location#' : template\_loc, '#Tables\_Dictionary#': str(tables), ...}

And add your tags as values in the dictionary like so : 

    replacement\_tags = {..., '#Tag\_Example#' : tag\_value , ...}

The source file is documented and should contain information about all the variables. 

The base template defines a few blocks that can be used and are left blank in the base template, and other than that, takes in the tables variable to create html tables as well as the panel header. If you are using the base template, you can edit the index.html to add stuff to the blocks supplied by the template. 

## Motivation

The history of this project is a very standard one. 
* Day 1 : "Boy I sure do like making panels with tables! But I would like to make it easier somehow."
* Day 2 : "Well all my templates look the same, might as well make a base template and have other templates extend it. "
* Day 3 : "Well now I'm copying other code. I can probably make a base view and have a script copy it to new panels when I make them. "
* Day 4 : "You know, this kinda works, but what if I wanted other types of views and templates, and I should also probably support custom tags and maybe one day I might make more customizations and..."
* Day 5 : "... great, almost done writing the readme. "

## Installation

Just download the source. generate\_table.py should be in the same folder as run\_tests.sh, while to use the default view and template, they should be put in a subdirectory panel\_creator. Your project structure should look like this : 
```
openstack_project/
    -generate_table.py
    panel_creator/
        -base_view.py 
        -base_template.py
        -base_action.py
        -table_json.json
    openstack_dashboards/
        -templates/
            -vapour-base.html
            ...
        ...
    ...
```

## TODO

There is no definitive way this project should go, but there are some issues. 

- Sometimes, openstack will generate the panel.py which will give an error 'Module has no <dashboard_name> attribute'. This happens at dashboard.<dashboard_name>.register(...). Now, this script doesn't touch the panel.py file at all, so I suspect it's an openstack thing, probably caused by bad project structuring. 

- More testing is needed - the script worked fine for all the panels I created with (barring the panel.py error) it but one can never know. 

- More of a design issue; maybe the 'target' and 'dashboard' values can be supplied as arguments instead of in the json file. 

## Contributors

Much like myself, this project is very simple. Any contributions are welcome. 

## License

Use it, modify it, spread it. 
