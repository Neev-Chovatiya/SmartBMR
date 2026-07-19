app_name = "smart_bmr"
app_title = "SmartBMR"
app_publisher = "Neev Chovatiya"
app_description = "AI-Powered Batch Manufacturing Records"
app_email = "neevchovatiya23@gmail.com"
app_license = "mit"

# Apps
# ------------------

# Print Formats
# -------------
# Automatically register standard app print formats with the framework
standard_print_formats = ["Batch Manufacturing Record"]

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "smart_bmr",
# 		"logo": "/assets/smart_bmr/logo.png",
# 		"title": "SmartBMR",
# 		"route": "/smart_bmr",
# 		"has_permission": "smart_bmr.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/smart_bmr/css/smart_bmr.css"
# app_include_js = "/assets/smart_bmr/js/smart_bmr.js"

# include js, css files in header of web template
# web_include_css = "/assets/smart_bmr/css/smart_bmr.css"
# web_include_js = "/assets/smart_bmr/js/smart_bmr.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "smart_bmr/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "smart_bmr/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "smart_bmr.utils.jinja_methods",
# 	"filters": "smart_bmr.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "smart_bmr.install.before_install"
# after_install = "smart_bmr.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "smart_bmr.uninstall.before_uninstall"
# after_uninstall = "smart_bmr.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "smart_bmr.utils.before_app_install"
# after_app_install = "smart_bmr.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "smart_bmr.utils.before_app_uninstall"
# after_app_uninstall = "smart_bmr.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "smart_bmr.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"smart_bmr.tasks.all"
# 	],
# 	"daily": [
# 		"smart_bmr.tasks.daily"
# 	],
# 	"hourly": [
# 		"smart_bmr.tasks.hourly"
# 	],
# 	"weekly": [
# 		"smart_bmr.tasks.weekly"
# 	],
# 	"monthly": [
# 		"smart_bmr.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "smart_bmr.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "smart_bmr.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "smart_bmr.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["smart_bmr.utils.before_request"]
# after_request = ["smart_bmr.utils.after_request"]

# Job Events
# ----------
# before_job = ["smart_bmr.utils.before_job"]
# after_job = ["smart_bmr.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"smart_bmr.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

