# Program Name: To-Do List Manager (version 1.2)
# Authors:      Emily Huynh and Ugbad Arwo
# Date:         June 22, 2023
# Description:  This is an application that organizes and manages tasks

import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from datetime import datetime
import json 

# Initialize the Tkinter window
window = tk.Tk()
window.title("To-Do List Manager")
window.geometry("600x425")
window.configure(bg="#FFD1DC")

# Lists
dates_list, tasks, groups_list, events = [], [], [], []
time_int = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

# Definitions
def quit():
  tk.Label(text="Goodbye!", bg="#FFD1DC", font=("Georgia", 19)).pack(pady=180)
  window.quit()

def retrieve_saved_data():
  with open("tasks.json", "r") as file:
    try:
      data = json.load(file)
    except json.decoder.JSONDecodeError:
      return
    for task in data:
      task["date"]=datetime.date(datetime.strptime(task["date"], '%Y-%m-%d'))  
      tasks.append(task)

  with open("events.json", "r") as file:
    try:
      data = json.load(file)
    except json.decoder.JSONDecodeError:
      return
    for event in data:
      event["date"]=datetime.date(datetime.strptime(event["date"], '%Y-%m-%d')) 
      events.append(event)

  with open ("groups.json", "r") as file:
    try:
      data = json.load(file)
    except json.decoder.JSONDecodeError:
      return
    for group in data:
      groups_list.append(group)

def save_data():
  for task in tasks:
    task["date"]=str(task["date"])
  with open("tasks.json", "w") as file:
    json.dump(tasks, file, default=lambda o: o.__dict__, sort_keys=True, indent=4)

  for event in events:
    event["date"]=str(event["date"])
  with open("events.json", "w") as file:
    json.dump(events, file, default=lambda o: o.__dict__, sort_keys=True, indent=4)

  with open("groups.json", "w") as file:
    json.dump(groups_list, file)

  clear_screen(quit)

def clear_screen(window_to_show):
  for widget in window.winfo_children():
      widget.destroy()
  window.after(0, window_to_show)

def show_welcome_label():
  def save_date():
    current_date = current.get_date()
    dates_list.append(current_date)
    # Delete past events from event list
    for event in events:
      if str(event["date"])<str(current_date):
        events.remove(event)
    clear_screen(menu)

  welcome_frame = tk.Frame(window, bg="#FFB6C1")
  welcome_frame.pack(pady=25)
  tk.Label(welcome_frame, text="Welcome to the To-Do List Manager!", font=("Georgia", 21, "bold"), fg="white", bg="#FFD1DC").pack(pady=10)
  tk.Label(text="Use this app to organize your tasks,\n schedule, and deadlines.", font=("Georgia", 15, "bold"), fg="white", bg="light blue").pack()
  tk.Label(text="Enter today's date:", font=(10), bg="#FFD1DC").pack(pady=11)
  current = DateEntry(window, width=12, font=("Arial", 11), background='lightpink1', foreground='white', borderwidth=2)
  current.pack()
  tk.Button(text='Submit', font=("Georgia", 12), command=save_date).pack(pady=20)

# Displays menu page (with buttons)
def menu():
  menu_frame = tk.Frame(window, bg="white")
  menu_frame.pack(pady=30)
  tk.Label(menu_frame, text="Menu", font=("Georgia", 20, "bold"), fg="white", bg="#FFB6C1", width=80).pack(pady=10)
  tk.Button(text="+ Task", font=("Georgia", 12, "bold"), fg="white", bg="plum1", width=16, command=lambda: clear_screen(add_task)).pack(pady=3)
  tk.Button(text="+ Event", font=("Georgia", 12, "bold"), fg="white", bg="plum1", width=16, command=lambda: clear_screen(add_event)).pack(pady=3)
  tk.Button(text="Today", font=("Georgia", 12, "bold"), fg="white", bg="mediumOrchid1", width=16, command=lambda: clear_screen(today_section)).pack(pady=3)
  tk.Button(text="Low Priority Tasks", font=("Georgia", 12, "bold"), fg="white", bg="mediumOrchid1", width=16, command=lambda:
            clear_screen(low_priority_tasks)).pack(pady=3)
  tk.Button(text="High Priority Tasks", font=("Georgia", 12, "bold"), fg="white", bg="mediumOrchid1", width=16, command=lambda:
            clear_screen(high_priority_tasks)).pack(pady=3)
  tk.Button(text="Groups", font=("Georgia", 12, "bold"), fg="white", bg="mediumOrchid1", width=16, command=lambda: clear_screen(groups)).pack(pady=3)
  tk.Button(text="Save & Quit", width=16, font=("Georgia", 12, "bold"), fg="white", bg="mediumOrchid1", command=lambda:save_data()).pack(pady=3)

def back_to_menu_button():
  back_button = tk.Button(text="Back", font=("Georgia", 10, "bold"), bg="DarkTurquoise", fg="white", command=lambda: clear_screen(menu))
  back_button.place(x=520, y=380)

# Removes task from program once checked off 
def checkbox_checked(checkbox, task_name):
  for task in tasks:
    if task["name"] == task_name:
      tasks.remove(task)
      break
  checkbox.pack_forget()  

# Creates checkboxes for high priority and low priority pages
def priority_create_checkboxes(priority_lvl, frame):
  priority_tasks=[]
  for task in tasks:
    if task["priority"]==priority_lvl:
      priority_tasks.append(task)
      task_name = task["name"]
      checkbox = tk.Checkbutton(frame, text=task_name, font=("Georgia", 12), bg="#FFD1DC", highlightthickness=0)
      checkbox.deselect()
      checkbox.configure(command=lambda chkbox=checkbox, name=task_name: checkbox_checked(chkbox, name))
      checkbox.pack(anchor="w")
  if len(priority_tasks)==0:
    tk.Label(frame, text="No tasks added yet.", 
             font=("Georgia", 12, "bold"), 
             bg="#FFD1DC", fg="white").pack()

# Creates checkboxes on the side (for pages with table)
def chkbox_side(frame, chkbox_frame, key, compare_var):
  xframe, yframe = frame
  xchkbox_frame, ychkbox_frame = chkbox_frame
  task_frame = tk.Frame(bg="#FFD1DC")
  task_frame.place(x=xframe,y=yframe)
  chkbox_frame = tk.Frame(bg="#FFD1DC")
  chkbox_frame.place(x=xchkbox_frame, y=ychkbox_frame)
  tk.Label(task_frame, text="To-Do List", 
           font=("Georgia", 15), 
           bg="#FFD1DC").pack(side='left', pady=8)
  tasks_to_do=[]
  for task in tasks:
    if str(task[key])==str(compare_var):
      tasks_to_do.append(task)
      checkbox = tk.Checkbutton(chkbox_frame, text=task["name"], font=("Georgia", 12), bg='#FFD1DC', highlightthickness=0)
      checkbox.deselect()
      checkbox.configure(command=lambda chkbox=checkbox, name=task["name"]: checkbox_checked(chkbox, name))
      checkbox.pack(anchor="w")
  if len(tasks_to_do)==0:
    tk.Label(chkbox_frame, text="Nothing has been added yet.", font=("Georgia", 12), bg="#FFD1DC").pack()

# Creates popup window if invalid input occurs
def popup_msg(msg):
  popup = tk.Tk()
  popup.wm_title("!")
  popup.eval('tk::PlaceWindow . center')
  popup.attributes('-topmost',True)
  tk.Label(popup, text=msg, font=("Georgia", 12)).pack(padx=5, pady=5)
  tk.Button(popup, text="OK", command=popup.destroy).pack(padx=5, pady=5)
  popup.mainloop()

# Limits number of tasks and events
def max_num(group, priority, date, element, elist, max): 
  group_num=[]
  priority_num=[]
  date_num=[]
  error=0
  for item in elist:
    if element=="tasks":
      if item["priority"] == priority:
        priority_num.append(item)
    if item["group"] == group:
      group_num.append(item)
    if str(item["date"]) == str(date):
      date_num.append(item)
  if element=="tasks":
    if len(priority_num) > max:
      popup_msg(("Too many "+priority.lower()+" priority tasks."))
      error+=1
  if len(group_num) > max:
    popup_msg("Too many "+element+" in group")
    error+=1
  elif len(date_num) > max:
    popup_msg("Too many "+element+ f" on {date.strftime('%B %d, %Y')}")
    error+=1
  else:
    pass
  return error

def add_task():
  back_to_menu_button()

  # Changes priority button colour when pressed
  def priority_button_colour(button):
    if button==set_high:
      set_high.configure(bg="blue")
      set_low.configure(bg="dark turquoise")
    else:
      set_low.configure(bg="blue")
      set_high.configure(bg='dark turquoise')

  # Sets priority according to button pressed
  def get_task_input():
    if set_high['bg'] != 'dark turquoise':
      task_priority="High"
    elif set_low['bg'] != 'dark turquoise':
      task_priority = "Low"
    else:
      task_priority=""

    task = {
      "name": task_name_entry.get(),
      "priority": task_priority,
      "group": set_group_entry.get(),
      "date": task_date_entry.get_date()
      }

    # Bulletproofing for task input
    errors = max_num(task["group"], task["priority"], task["date"], "tasks", tasks, 9)
    if errors > 0:
      return
    elif len(groups_list) == 0:
      popup_msg("Please create a group first.")
      return
    elif len(task["name"])==0 or len(task["group"])==0 or task_priority=="":
      popup_msg("Please enter all required fields.")
      return
    elif len(task["name"])>16:
      popup_msg("Too many characters")
      return
    elif task["group"] not in groups_list:
      popup_msg("Group does not exist.")
      return
    else:
      pass

    # Adds task to task list
    tasks.append(task)
    clear_screen(menu)

  # Displays entries and labels needed to get task input
  task_frame = tk.Frame(window, bg="white")
  task_frame.pack(pady=20)
  tk.Label(task_frame, text="Add Task", font=("Georgia", 15, "bold"), fg="black", bg="white").pack()
  tk.Label(text="Task Name: ", font=("Georgia", 12, "bold"), bg="#FFD1DC").place(x=150, y=80)
  task_name_entry = tk.Entry()
  task_name_entry.place(x=275, y=80)
  tk.Label(text="Priority Level:", font=("Georgia", 12, "bold"), bg="#FFD1DC").place(x=150, y=120)
  set_high = tk.Button(text="High", font=("Georgia", 10, "bold"), bg="dark turquoise", fg="white", width=4, command=lambda:priority_button_colour(set_high))
  set_high.place(x=290, y=115)
  set_low = tk.Button(text="Low", font=("Georgia", 10, "bold"), bg="dark turquoise", fg="white", width=4, command=lambda:priority_button_colour(set_low))
  set_low.place(x=370, y=115)
  tk.Label(text="Group:", font=("Georgia", 12, "bold"), bg="#FFD1DC").place(x=150, y=160)

  # Drop down menu for groups 
  set_group_entry = ttk.Combobox(values=groups_list, width=26)
  set_group_entry.place(x=280, y=160)
  if len(groups_list) == 0:
    set_group_entry.set("No group added")
  else:
    set_group_entry.set(groups_list[0])

  tk.Label(text="Date of task:", font=("Georgia", 12, "bold"), bg="#FFD1DC").place(x=150, y=200)
  task_date_entry = DateEntry(window, width=16, font=("Arial", 11), mindate=dates_list[0], foreground='white', background='lightpink1', borderwidth=2)
  task_date_entry.place(x=280, y=200)
  confirm_add_task = tk.Button(text="Create task", font=("Georgia", 12, "bold"), fg="white", bg="lightBlue", command=get_task_input)
  confirm_add_task.place(x=240, y=260)

def add_event():
  back_to_menu_button()

  def get_event_input():
    event_name = event_name_entry.get()
    event_date = event_date_entry.get_date() 
    event_time = time_combobox.get()
    event_group = set_group_entry.get()

    # Bulletproofing for event input
    errors = max_num(event_group, "no priority", event_date, "events", events, 13)
    if errors > 0:
      return
    elif len(groups_list) == 0:
      popup_msg("Please create a group first.")
      return
    elif len(event_name) == 0 or len(event_group) == 0 or len(event_time) == 0:
      popup_msg("Please enter all required fields.")
      return
    elif event_group not in groups_list:
      popup_msg("Group does not exist.")
      return
    elif event_time not in time_values or event_time=="":
      popup_msg("Please select a valid time.")
      return
    elif len(event_name)>20:
      popup_msg("Too many characters.")
      return
    else:
      pass

    # Assigns a comparable time value (integer) to variable
    # integer is related to actual time (has same index) to help organize events chronologically
    new_time = time_int[time_values.index(event_time)]
    event = {
      "name": event_name,
      "date": event_date,
      "time": event_time,
      "int time": new_time,
      "group": event_group
      }
    events.append(event)
    clear_screen(menu)

  # Displays entries and labels needed to get event input
  event_frame = tk.Frame(window, bg="#FFD1DC")
  event_frame.pack(pady=20)
  event_label = tk.Label(event_frame, text="Add Event", font=("Georgia", 15, "bold"), fg="black", bg="#FFD1DC")
  event_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
  event_name_label = tk.Label(event_frame, text="Event Name:", font=("Georgia", 12, "bold"), bg="#FFD1DC")
  event_name_label.grid(row=1, column=0, padx=10, pady=10)
  event_name_entry = tk.Entry(event_frame, bg="white")
  event_name_entry.grid(row=1, column=1, padx=10, pady=10)
  event_date_label = tk.Label(event_frame, text="Date of Event:", font=("Georgia", 12, "bold"), bg="#FFD1DC")
  event_date_label.grid(row=2, column=0, padx=10, pady=10)
  event_date_entry = DateEntry(event_frame, width=16, font=("Arial", 11), mindate=dates_list[0], background='lightpink1', foreground='white', borderwidth=2)
  event_date_entry.grid(row=2, column=1, padx=10, pady=10)
  time_label = tk.Label(event_frame, text="Time:", font=("Georgia", 12, "bold"), bg="#FFD1DC")
  time_label.grid(row=3, column=0, padx=10, pady=10)
  time_values = ['1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM','12:00 AM']
  time_combobox = ttk.Combobox(event_frame, values=time_values, width=12)
  time_combobox.grid(row=3, column=1, padx=10, pady=10)
  set_group_label = tk.Label(event_frame, text="Group:", font=("Georgia", 12, "bold"), bg="#FFD1DC")

  # Drop group down menu for groups
  set_group_label.grid(row=4, column=0, padx=10, pady=10)
  set_group_entry = ttk.Combobox(event_frame, values=groups_list, width=26)
  set_group_entry.grid(row=4, column=1, padx=10, pady=10)
  if len(groups_list) == 0:
    set_group_entry.set("No group added")
  else:
    set_group_entry.set(groups_list[0])
  confirm_add_event = tk.Button(event_frame, text="Create Event", font=("Georgia", 12, "bold"), fg="white", bg="lightBlue", command=get_event_input)
  confirm_add_event.grid(row=5, column=0, columnspan=2, pady=10)

def today_section():
  back_to_menu_button()

  # Sorts events by date and time
  sorted_events = sorted(events, key=lambda event: (event["date"], event["int time"])) 
  today_box = tk.Frame(bg="lightblue", bd=0, relief="solid")
  today_box.pack(padx=10, pady=10)
  tk.Label(today_box, text=f"Today, {dates_list[0].strftime('%A %B %d, %Y')}", font=("Georgia", 18, "bold"), fg="white", bg="lightblue").pack(padx=10, pady=8)

  # Creates event table
  treeview_widget = ttk.Treeview(window, selectmode="browse", height=15)
  treeview_widget.pack(anchor="nw", padx=10, pady=10)
  treeview_widget["columns"]=(1, 2)
  treeview_widget["show"]="headings"
  treeview_widget.column("1", width=70, anchor="c")
  treeview_widget.column("2", width=200, anchor="c")
  treeview_widget.heading("1", text="Time")
  treeview_widget.heading("2", text="Event")
  i=0
  for event in sorted_events:
    if str(event["date"])==str(dates_list[0]):
      treeview_widget.insert("", "end", text=f"L{i+1}", values=(event["time"], event["name"]))

  # Creates to-do list for current date
  chkbox_side((310, 80), (310, 130), "date", dates_list[0])

def low_priority_tasks():
  back_to_menu_button()
  low_priority_frame = tk.Frame(window, bg="#FFD1DC")
  low_priority_frame.pack(pady=30)
  tk.Label(low_priority_frame, text="Low Priority Tasks", font=("Georgia", 20, "bold"), fg="white", bg='lightblue').pack()
  current_date = dates_list[0] 
  date_label = tk.Label(low_priority_frame, text=f"Date: {current_date}", font=("Georgia", 12, "bold"), bg="#FFD1DC", fg="white")
  date_label.pack(pady=10)
  priority_create_checkboxes("Low", low_priority_frame)

def high_priority_tasks():
  back_to_menu_button()
  high_priority_frame = tk.Frame(window, bg="#FFD1DC")
  high_priority_frame.pack(pady=30)
  tk.Label(high_priority_frame, text="High Priority Tasks", font=("Georgia", 20, "bold"), fg="white", bg='lightblue').pack()
  current_date = dates_list[0]
  date_label = tk.Label(high_priority_frame, text=f"Date: {current_date}", font=("Georgia", 12, "bold"), bg="#FFD1DC", fg="white")
  date_label.pack(pady=10)
  priority_create_checkboxes("High", high_priority_frame)

def groups():

  # Goes to selected group page (after button is pressed))
  def group_clear_screen(group_name):
    for widget in window.winfo_children():
      widget.destroy()
    display_group(group_name)

  back_to_menu_button()
  view_group_label=tk.Label(text="Groups", font=("Georgia", 20, "bold"),fg="white", bg='lightblue')
  view_group_label.grid(row=0, column=0, columnspan=4, padx=240, pady=20)
  tk.Button(text="+ Group", font=("Georgia", 12, "bold"),fg="white", bg='DarkTurquoise', command=lambda: clear_screen(add_group)).place(x=15, y=375)

  # Displays group buttons
  a,b=0,0
  for group in groups_list:
    i = groups_list.index(group)
    group_button = tk.Button(text=group, width=10, font=("Georgia", 12,"bold"), bg="plum1",fg="white", command=lambda group=group:group_clear_screen(group))
    if i%4==0:
      a+=1
      b=0
    group_button.grid(column=b, row=a+2, pady=10)
    b+=1

def back_to_groups_button():
  back_to_group= tk.Button(text="Back", font=("Georgia", 10, "bold"), bg="DarkTurquoise", fg="white", command=lambda: clear_screen(groups))
  back_to_group.place(x=520, y=380)

def add_group():
  back_to_groups_button()

  # Gets group input and bulletproofs for group input
  def get_group_input():
    group = group_name_entry.get()
    if group=="":
      popup_msg("Please enter the group name.")
      return
    if len(group)>12:
      popup_msg("Too many characters.")
      return
    elif group in groups_list:
      popup_msg("Group already exists.")
      return
    elif len(groups_list)>19:
      popup_msg("Maximum number of groups reached.")
      return
    else:
      pass
    # Adds group to group list
    groups_list.append(group)
    clear_screen(groups)

  tk.Label(text="Add Group", font=("Georgia", 20, "bold"), fg="white", bg="lightblue").pack(pady=30)
  tk.Label(text="Group Name: ", font=("Georgia", 12, "bold"), bg='#FFD1DC').place(x=140, y=100)
  group_name_entry=tk.Entry(font="Georgia", width=22)
  group_name_entry.place(x=270, y=100)
  tk.Button(text="Create Group", font=("Georgia", 12, "bold"),fg="white",bg="lightblue", command=lambda: get_group_input()).pack(pady=70)

def display_group(group): 
  back_to_groups_button()
  # Sorts all events by date and time
  sorted_events = sorted(events, key=lambda event: (event['date'], event['int time']))
  tk.Label(text=group, font=("Georgia", 18, "bold"),bg="lightblue",fg="white").pack(pady=8)

  # Creates event table
  treeview_widget = ttk.Treeview(window, selectmode="browse", height=15)
  treeview_widget.pack(anchor="nw", padx=10, pady=10)
  treeview_widget["columns"] = ("1", "2", "3")
  treeview_widget["show"] = "headings"
  treeview_widget.column("1", width=115, anchor="c")
  treeview_widget.column("2", width=70, anchor="c")
  treeview_widget.column("3", width=190, anchor="c")
  treeview_widget.heading("1", text="Date")
  treeview_widget.heading("2", text="Time")
  treeview_widget.heading("3", text="Event")
  group_events=[]
  for event in sorted_events: 
    if event["group"]==group:
      group_events.append(event)
      event_date = event["date"].strftime("%b. %d. %Y")
      treeview_widget.insert("", "end", text=f"L{group_events.index(event)+1}", values=(event_date, event["time"], event["name"]))
  # Creates task list for group
  chkbox_side((400, 80), (400, 130), "group", group)

# Title (first page)
retrieve_saved_data()
title_frame = tk.Frame(window, bg="#FFB6C1", width=600, height=400)
title_frame.place(y=90)
title_frame.pack(pady=75, padx=35)
tk.Label(title_frame, text="To-Do List Manager", font=("Georgia", 35, "bold"), fg="white", bg="#FFD1DC").pack(pady=50)
tk.Button(window, text="Continue", command=lambda: clear_screen(show_welcome_label), bg='light blue', font=("Georgia", 15, "bold"), fg='white').pack()

window.mainloop()