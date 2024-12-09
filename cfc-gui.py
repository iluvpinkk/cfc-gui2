# Program Developer Name:  Lacy Hartis

#

# Date Program Developed: 11/22/24

#

# Organization: CIS 202

#

# 1. Display menu bpard with GUI elements for the Calhoun Fried Chicken
# based on items from the board
# 2. Save the order to a data structure
# 3. Print orders (at least 5)

#

# Document your givens below this line

# Menu items/sizes & prices

#

# Document your inputs below this line

# User clicking buttons (if that counts)

#

# Document your outputs below this line

# Everything displayed in GUI; items and prices displayed

#

# Document your processes below this line

# Create listboxes with items; Radiobuttons with specifics (ie sizes or types of an item);
# Buttons to add to order and display subtotal; Quit button; Scrollbars

#

# Start your program code after this line

import tkinter as tk
import tkinter.messagebox
import sqlite3

def create_db():
    conn = sqlite3.connect('cfc_orders.db')
    cursor = conn.cursor()
    
    # create a table for storing orders
    cursor.execute('''CREATE TABLE IF NOT EXISTS Orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        combo_name TEXT,
        combo_type TEXT,
        combo_price REAL,
        drink_name TEXT,
        drink_size TEXT,
        drink_price REAL,
        main_name TEXT,
        chicken_type TEXT,
        chicken_price REAL,
        side_name TEXT,
        side_price REAL,
        dessert_name TEXT,
        dessert_price REAL,
        sauce_name TEXT,
        sauce_price REAL
            )''')

    conn.commit()
    conn.close()

create_db() 

def insert_order(item_name, item_type, price):
    conn = sqlite3.connect('cfc_orders.db')
    cursor = conn.cursor()
    global gcombo_name, gcombo_type, gcombo_price, gdrink_size, gdrink_name, gdrink_price, gmain_name, gchicken_type, gchicken_price, gside_name, gside_price, gdessert_name, gdessert_price, gsauce_name, gsauce_price

    # insert the selected item into the orders table
    cursor.execute('''
        INSERT INTO orders (combo_name, combo_type, combo_price,
        drink_name, drink_size, drink_price, main_name,
        chicken_type, chicken_price, 
        side_name, side_price,
        dessert_name, dessert_price,
        sauce_name, sauce_price)
        VALUES (?, ?, ?)
    ''', (item_name, item_type, price))
    conn.commit()

    order_id = cursor.lastrowid
    conn.close()


    return order_id
    
class Menu:
    global gcombo_name, gcombo_type, gcombo_price, gdrink_size, gdrink_name, gdrink_price, gmain_name, gchicken_type, gchicken_price, gside_name, gside_price, gdessert_name, gdessert_price, gsauce_name, gsauce_price
    def __init__(self):
        # create the main window widget
        self.main_window = tkinter.Tk()
        # display title
        self.main_window.title('CFC')

        # order list initialization
        self.order_list = []
        self.total_cost = 0.00

        # button that shows orders and price when clicked
        self.show_order_button = tkinter.Button(self.main_window,
                                              text = 'Display Order',
                                              command=self.show_order)
        
        self.show_all_orders_button = tkinter.Button(self.main_window, text='Show all Orders', command=self.show_all_orders)
        
        self.finish_order_button = tkinter.Button(self.main_window, text="Finish Order", command=self.finish_order)
        
        # packing display button
        self.show_order_button.pack(pady=10)
        self.show_all_orders_button.pack(pady=10)
        self.finish_order_button.pack(pady=20)

# I tried to add a 'quit' button but it kept causing errors for some reason :(
# I'm painfully aware it looks ugly when fullscreened; I didn't have time to optimize
# it as well as I wanted due to health issues 
        
        # all the modules 
        self.__build_welcome_message()
        self.__build_combos()
        self.__combo_type_buttons()
        self.__build_main()
        self.__chicken_type_buttons()
        self.__build_sides()
        self.__side_button()
        self.__build_drinks()
        self.__build_desserts()
        self.__dessert_button()
        self.__build_sauces()
        self.__sauce_button()
        self.__drink_size_buttons()
        self.show_combo_choice()
        self.show_drink_choice()
        self.show_main_choice()
        self.show_side_choice()
        self.show_dessert_choice()
        self.show_sauce_choice()
        self.show_order()
        self.show_all_orders()
        self.finish_order()

        # enter the tkinter main loop
        tkinter.mainloop()

    # message that welcomes the user
    def __build_welcome_message(self):

        # labels and frames
        # I added a red color to make the welcome message pop;
        self.welcome_label = tkinter.Label(
            self.main_window, text='Welcome to Calhoun Fried Chicken!',
            fg='#FF004F')
        self.welcome_label.pack(padx=1, pady=1)

        self.order_label = tkinter.Label(
            self.main_window, text='Ready to order?',
            fg='#FF004F')
        self.order_label.pack(padx=1, pady=1)

    # section of the menu for combos
    def __build_combos(self):
        # frames for organization & packing
        self.combo_frame = tkinter.Frame(self.main_window)
        self.combo_frame.pack(side='left', fill='y', padx=5, pady=5)
        
        self.combo_label = tkinter.Label(
            self.combo_frame, text='Try our combos! Small drink included!')
        self.combo_label.pack()

        # combo listbox creation & packing
        self.combo_listbox = tkinter.Listbox(self.combo_frame)
        self.combo_listbox.pack(ipadx=75)

        # lists the combo items & prices in a dictionary
        self.combo = {
            'Combo #1 - Fried Chicken & 1 Side': 7.00,
            'Combo #2 - Fried Chicken & 2 Sides': 9.00,
            'Combo #3 - Chicken Sandwhich & 1 Side': 7.00,
            'Combo #4 - Chicken Sandwhich & 2 Sides': 9.00,
            'Combo #5 - Popcorn Chicken & 2 Sides': 9.00,
            'Combo #6 - Popcorn Chicken & 3 Sides': 11.00
            }

        # general format for adding items into the listboxes; repeated throughout code
        for combo_name, price in self.combo.items():
            self.combo_listbox.insert(tk.END, f'{combo_name} ... ${price:.2f}')

    # buttons for options such as 'Spicy', 'Saucy', and 'Grilled'
    def __combo_type_buttons(self):
        self.top_frame = tkinter.Frame(self.combo_frame)
        self.bottom_frame = tkinter.Frame(self.combo_frame)


        self.radio_var1 = tkinter.StringVar()
        self.radio_var1.set('Spicy')

        self.rb1 = tkinter.Radiobutton(self.combo_frame,
                                       text='Make it Spicy!', 
                                       variable=self.radio_var1,
                                       value='Spicy')

        self.rb2 = tkinter.Radiobutton(self.combo_frame,
                                       text='Make it Saucy!',
                                       variable=self.radio_var1,
                                       value='Saucy')

        self.rb3 = tkinter.Radiobutton(self.combo_frame,
                                       text='Grill it!',
                                       variable=self.radio_var1,
                                       value='Grilled')

        self.rb1.pack()
        self.rb2.pack()
        self.rb3.pack()

        # button to add combo(s) to order
        self.ok_button = tkinter.Button(self.bottom_frame,
                                        text='Add to order',
                                        command=self.show_combo_choice)
        self.ok_button.pack(side='left')

        self.top_frame.pack()
        self.bottom_frame.pack()
        

    # Virtually the same to the combo module
    def __build_main(self):
        self.main_frame = tkinter.Frame(self.main_window)
        self.main_frame.pack(side='left', fill='y', padx=5, pady=5)

        self.main_label = tkinter.Label(
            self.main_frame, text='Get started with delicious chicken!' +
            ' (and your choice of sauce)')
        self.main_label.pack()

        self.main_listbox = tkinter.Listbox(self.main_frame)
        self.main_listbox.pack(ipadx=20)

        # add main options via dictionary
        self.main = {
            'Fried Chicken': 6.00,
            'Grilled Chicken': 5.00,
            'Popcorn Chicken': 5.00,
            'Chicken Sandwhich': 6.00,
            'Chicken - White Meat': 6.00,
            'Chicken - Dark Meat': 6.00
            }

        for main_name, price in self.main.items():
            self.main_listbox.insert(tk.END, f'{main_name} ... ${price:.2f}')

        
    def __chicken_type_buttons(self):
        self.top_frame = tkinter.Frame(self.main_frame)
        self.bottom_frame = tkinter.Frame(self.main_frame)

        self.radio_var2 = tkinter.StringVar()
        self.radio_var2.set('Spicy')

        self.rb1 = tkinter.Radiobutton(self.main_frame,
                                       text='Make it Spicy!',
                                       variable=self.radio_var2,
                                       value='Spicy')

        self.rb2 = tkinter.Radiobutton(self.main_frame,
                                       text='Make it Saucy!',
                                       variable=self.radio_var2,
                                       value='Saucy')

        self.rb3 = tkinter.Radiobutton(self.main_frame,
                                       text='Grill it!',
                                       variable=self.radio_var2,
                                       value='Grilled')

        self.rb1.pack()
        self.rb2.pack()
        self.rb3.pack()

        # button to add main(s) to order
        self.ok_button = tkinter.Button(self.bottom_frame,
                                        text='Add to order',
                                        command=self.show_main_choice)
        self.ok_button.pack(side='left')

        self.top_frame.pack()
        self.bottom_frame.pack()
        
    # module for the sides
    def __build_sides(self):
        self.side_frame = tkinter.Frame(self.main_window)
        self.side_frame.pack(side='left', fill='y', padx=5, pady=5)
        
        # label to inform customer all sides are $3.00
        self.side_label = tkinter.Label(
            self.side_frame, text='Pick a $3.00 side!')
        self.side_label.pack()

        # add side options via dictionary
        self.side_listbox = tkinter.Listbox(self.side_frame)
        self.side_listbox.pack()

        self.side = {
            'Fries': '$3.00', 'Mashed Potatoes': '$3.00',
            'Fried Okra': '$3.00', 'Mixed Fruit': '$3.00',
            'Mac & Cheese': '$3.00', 'Green Beans': '$3.00',
            'Chicken Noodle Soup': '$3.00', 'Biscuits & Gravy': '$3.00'
            }

        for side_name, price in self.side.items():
            self.side_listbox.insert(tk.END, f' {side_name}')


    def __side_button(self):
        self.top_frame = tkinter.Frame(self.side_frame)
        self.bottom_frame = tkinter.Frame(self.side_frame)

        # button to add side(s) to order
        self.ok_button = tkinter.Button(self.bottom_frame,
                                        text='Add to order',
                                        command=self.show_side_choice)


        self.ok_button.pack(side='left')        

        self.top_frame.pack()
        self.bottom_frame.pack()

    # module for drinks
    def __build_drinks(self):
        self.drink_frame = tkinter.Frame(self.main_window)
        self.drink_frame.pack(side='left', fill='y', padx=5, pady=5)
        
        self.drink_label = tkinter.Label(
            self.drink_frame, text='Choose a refreshing drink!')
        self.drink_label.pack()

        # add drink options via dictionary
        self.drink_listbox = tkinter.Listbox(self.drink_frame)
        self.drink_listbox.pack()


        # prices listed as N/A since the price is determined by the size
        self.drink = {
            'Dr Pepper': 'N/A', 'Tea - Sweet': 'N/A', 'Tea - Unsweetened': 'N/A',
            'Decaf Tea': 'N/A', 'Coke': 'N/A', 'Diet Coke': 'N/A', 'Coke Zero': 'N/A',
            'Lemonade': 'N/A', 'Pink Lemonade': 'N/A', 'Bug Juice': 'N/A',
            'Bottled Water': 'N/A'
            }

        for drink_name, price in self.drink.items():
            self.drink_listbox.insert(tk.END, f' {drink_name}')
   
        
    def __drink_size_buttons(self):
        # add radiobuttons for size
        self.top_frame = tkinter.Frame(self.drink_frame)
        self.bottom_frame = tkinter.Frame(self.drink_frame)

        self.radio_var3 = tkinter.StringVar()

        self.radio_var3.set('Small') # default size set to small

        # adding size options in radiobutton form; packing buttons
        self.rb1 = tkinter.Radiobutton(self.drink_frame,
                                       text='Small - $2.00',
                                       variable=self.radio_var3,
                                       value='Small')

        self.rb2 = tkinter.Radiobutton(self.drink_frame,
                                       text='Medium - $3.00',
                                       variable=self.radio_var3,
                                       value='Medium')
        self.rb3 = tkinter.Radiobutton(self.drink_frame,
                                       text='Large - $4.00',
                                       variable=self.radio_var3,
                                       value='Large')
        
        self.rb4 = tkinter.Radiobutton(self.drink_frame,
                                       text='Extra-Large - $5.00',
                                       variable=self.radio_var3,
                                       value='Extra-Large')        
        self.rb1.pack()
        self.rb2.pack()
        self.rb3.pack()
        self.rb4.pack()

        # button to add drink(s) to order
        self.ok_button = tkinter.Button(self.bottom_frame,
                                        text='Add to order',
                                        command=self.show_drink_choice)


        self.ok_button.pack(side='left')



        self.top_frame.pack()
        self.bottom_frame.pack()

        # requires this tkinter.mainloop() or else it crashes
        tkinter.mainloop()

    # desset module
    def __build_desserts(self):
        self.dessert_frame = tkinter.Frame(self.main_window)
        self.dessert_frame.pack(side='left', fill='y', padx=5, pady=5)

        self.dessert_label = tkinter.Label(
            self.dessert_frame, text='Choose a dessert!')
        self.dessert_label.pack()

        # adding dessert options via dictionary
        self.dessert_listbox = tkinter.Listbox(self.dessert_frame)
        self.dessert_listbox.pack(ipadx = 75) # large internal padding for full visibility

        self.dessert = {
            'Icecream': '$3.00', 'Apple Cobbler': '$4.50', 'Peach Cobbler': '$4.50',
            'Chocolate Cobbler': '$4.50', 'Blueberry Cobbler': '$4.50',
            'Chocolate Chip Cookie': '$2.50',
            'Peanutbutter Cookie': '$2.50', 'Triple Chocolate Cookie': '$2.50',
            'Sugar Cookie': '$2.50', 'White Chocolate Macadenia Nut Cookie': '$2.50',
            'Brownies': '$3.00', 'Banana Pudding': '$3.00'
            }
        for dessert_name, price in self.dessert.items():
            self.dessert_listbox.insert(tk.END, f' {dessert_name} ... {price}')

        # vertical scrollbar 
        self.scrollbar1 = tkinter.Scrollbar(
            self.dessert_frame, orient=tkinter.VERTICAL)
        self.scrollbar1.pack(side='right', fill=tkinter.Y)

        self.scrollbar1.config(command=self.dessert_listbox.yview)
        self.dessert_listbox.config(yscrollcommand=self.scrollbar1.set)

    # button to add dessert(s) to order
    def __dessert_button(self):
        self.top_frame = tkinter.Frame(self.dessert_frame)
        self.bottom_frame = tkinter.Frame(self.dessert_frame)

        self.ok_button = tkinter.Button(self.bottom_frame,
                                        text='Add to order',
                                        command=self.show_dessert_choice)


        self.ok_button.pack(side='left')        

        self.top_frame.pack()
        self.bottom_frame.pack()        

# sauce module 
    def __build_sauces(self):
        self.sauce_frame = tkinter.Frame(self.main_window)
        self.sauce_frame.pack(side='left', fill='y', padx=5, pady=5)

        # letting customer know all sauces are $1.00
        self.sauce_label = tkinter.Label(
            self.sauce_frame, text='Pick from our $1.00 sauces!') 
        self.sauce_label.pack()

        # adding sauce options via dictionary
        self.sauce_listbox = tkinter.Listbox(self.sauce_frame)
        self.sauce_listbox.pack()
        
        self.sauce = {
            'St. Louis BBQ': '$1.00', 'Memphis BBQ': '$1.00',
            'North Carolina BBQ': '$1.00', 'Texas BBQ': '$1.00',
            'Soy Sauce': '$1.00', 'Honey Mustard': '$1.00',
            'Ranch': '$1.00','Ranch w/ Jalepeno': '$1.00', 'Hot (Mild)': '$1.00',
            'Hot (Medium)': '$1.00', 'Hot (Hot!)': '$1.00', 'Hot (Suicide!!)': '$1.00',
            }
        for sauce_name, price in self.sauce.items():
            self.sauce_listbox.insert(tk.END, f' {sauce_name}')

        # second scrollbar
        self.scrollbar2 = tkinter.Scrollbar(
            self.sauce_frame, orient=tkinter.VERTICAL)
        self.scrollbar2.pack(side='right', fill=tkinter.Y)

        self.scrollbar2.config(command=self.sauce_listbox.yview)
        self.sauce_listbox.config(yscrollcommand=self.scrollbar2.set)

    # button to add sauce(s) to order
    def __sauce_button(self):
        self.top_frame = tkinter.Frame(self.sauce_frame)
        self.bottom_frame = tkinter.Frame(self.sauce_frame)

        self.ok_button = tkinter.Button(self.bottom_frame,
                                        text='Add to order',
                                        command=self.show_sauce_choice)
        
        
        self.ok_button.pack(side='left')        

        self.top_frame.pack()
        self.bottom_frame.pack() 

    # module to display a confirmation message
    # and append it to the order_list.
    # The other modules are similar with slight differences that will be mentioned
    def show_combo_choice(self):
        combo_index = self.combo_listbox.curselection()
        
        if combo_index:
            combo_name = self.combo_listbox.get(combo_index[0])
            
            # When items' prices are dynamic/not determined by radiobuttons,
            # they need to be split and stripped to avoid errors
            combo_name_cleaned = combo_name.split('...')[0].strip()
            combo_type = self.radio_var1.get() # retrieves radiobutton info for preference

            # relists the prices in dictionary form
            combo_prices = {
                'Combo #1 - Fried Chicken & 1 Side': 7.00,
                'Combo #2 - Fried Chicken & 2 Sides': 9.00,
                'Combo #3 - Chicken Sandwhich & 1 Side': 7.00,
                'Combo #4 - Chicken Sandwhich & 2 Sides': 9.00,
                'Combo #5 - Popcorn Chicken & 2 Sides': 9.00,
                'Combo #6 - Popcorn Chicken & 3 Sides': 11.00
                }


            price = combo_prices.get(combo_name_cleaned, 0.00)
            # appending to order_list
            self.order_list.append(f'{combo_name_cleaned} ({combo_type}) - ${price:.2f}')
            # updating total_cost
            self.total_cost += price

            #order_id = insert_order(combo_name_cleaned, combo_type, price)

            #insert_order(combo_name_cleaned, combo_type, price)

            self.gcombo_name = combo_name_cleaned
            self.gcombo_type = combo_type
            self.gcombo_price = price

            # general format for confirmation message
            message = f'Order ID: {"order_id"}\n1 {combo_name_cleaned} ({combo_type}) added to order! Price: ${price:.2f}'
            tkinter.messagebox.showinfo('CFC Combo Meal Selection', message)


    
    def show_drink_choice(self):
        drink_index = self.drink_listbox.curselection()

        if drink_index:
            # doesn't require splitting/stripping 
            drink_name = self.drink_listbox.get(drink_index[0])
            drink_size = self.radio_var3.get() # retrieves size/price info from radiobuttons

            # drink prices determined by size/radiobuttons
            drink_prices = {
                'Small': 2.00,
                'Medium': 3.00,
                'Large': 4.00,
                'Extra-Large': 5.00
                }
            price = drink_prices.get(drink_size, 2.00)
            self.order_list.append(f'{drink_size} {drink_name} - ${price:.2f}')
            self.total_cost += price

            self.gdrink_size = drink_size
            self.gdrink_name = drink_name
            self.gdrink_price = price

            message = f'1 {drink_size} {drink_name} added to order! Price: ${price:.2f}'
            tkinter.messagebox.showinfo('CFC Drink Selection', message)


    def show_main_choice(self):
        main_index = self.main_listbox.curselection()
        
        if main_index:
            main_name = self.main_listbox.get(main_index[0])
            # requires splitting/stripping for the same reasons as the combos
            main_name_cleaned = main_name.split('...')[0].strip()
            chicken_type = self.radio_var2.get() # retrieves radiobutton info for preference
        # prices listed in dictionary form
        main_prices = {
            'Fried Chicken': 6.00,
            'Grilled Chicken': 5.00,
            'Popcorn Chicken': 5.00,
            'Chicken Sandwhich': 6.00,
            'Chicken - White Meat': 6.00,
            'Chicken - Dark Meat': 6.00
            }
        price = main_prices.get(main_name_cleaned, 0.00)

        self.order_list.append(f'{main_name_cleaned} ({chicken_type}) - ${price:.2f}')
        self.total_cost += price

        self.gmain_name = main_name_cleaned
        self.gchicken_type = chicken_type
        self.gchicken_price = price

        message = f'1 {main_name_cleaned} ({chicken_type}) added to order! Price: ${price:.2f}'
        tkinter.messagebox.showinfo('CFC Main Item Selection', message)


        
    def show_side_choice(self):
        side_index = self.side_listbox.curselection()

        if side_index:
            side_name = self.side_listbox.get(side_index[0])
            price = 3.00 # each side is the same price
        self.order_list.append(f'{side_name} - ${price:.2f}')
        self.total_cost += price
        
        self.gside_name = side_name
        self.gside_price = price

        message = f'1 {side_name} added to order! Price: ${price:.2f}'
        tkinter.messagebox.showinfo('CFC Side Item Selection', message)

    def show_dessert_choice(self):
        dessert_index = self.dessert_listbox.curselection()

        if dessert_index:
            dessert_name = self.dessert_listbox.get(dessert_index[0])
            # dessert also needs to be split/stripped
            dessert_name_cleaned = dessert_name.split('...')[0].strip()
            # prices listed in dictionary form
            dessert_prices = {
                'Icecream': 3.00,
                'Apple Cobbler': 4.50,
                'Peach Cobbler': 4.50,
                'Chocolate Cobbler': 4.50,
                'Blueberry Cobbler': 4.50,
                'Chocolate Chip Cookie': 2.50,
                'Peanutbutter Cookie': 2.50,
                'Triple Chocolate Cookie': 2.50,
                'Sugar Cookie': 2.50,
                'White Chocolate Macadenia Nut Cookie': 2.50
                }
            
            price = dessert_prices.get(dessert_name_cleaned, 0.00)

            self.order_list.append(f'{dessert_name_cleaned} - ${price:.2f}')
            self.total_cost += price

            self.gdessert_name = dessert_name_cleaned
            self.gdessert_price = price

            message = f'1 {dessert_name_cleaned} added to order! Price: ${price:.2f}'
            tkinter.messagebox.showinfo('CFC Dessert Item Selection', message)
                
 
    def show_sauce_choice(self):
        sauce_index = self.sauce_listbox.curselection()

        if sauce_index:
            sauce_name = self.sauce_listbox.get(sauce_index[0])
            price = 1.00 # all sauces are 1.00
        self.order_list.append(f'{sauce_name} - ${price:.2f}')
        self.total_cost += price
        
        self.gsauce_name = sauce_name
        self.gsauce_price = price
        message = f'1 {sauce_name} added to order! Price: ${price:.2f}'
        tkinter.messagebox.showinfo('CFC Sauce Selection', message)            
     

    # module that connects to the 'display order' button;
    # displays order(s) and total price
    def show_order(self):
        conn = sqlite3.connect('cfc_orders.db')
        cursor = conn.cursor()
        print("show_order")
        #### ORDER_ID not ID ----\/
        order_id = 6
        cursor.execute('SELECT order_id, combo_name, combo_type, combo_price FROM orders')
        orders = cursor.fetchall()

        #print('orders fetched from database:', orders)

        if not orders:
            print('no orders found')
            #tkinter.messagebox.showinfo('Your Order', 'No items have been added to your order yet!')
            return

        # this part has been hashtagged b/c of the database stuff. just keeping it temporarily
        # error message in case it's pressed before any orders are added
        #if not self.order_list:
         #   tkinter.messagebox.showinfo('Your Order', 'No items have been added to your order yet!')
          #  return
        #order_details = '\n'.join(self.order_list) # adds everything into one list

        #### DISPLAY ALL ORDERS FROM DATABASE
        #### order_details = '\n'.join([f'Order ID: {item[0]} - {item[1]} ({item[2]}) - ${item[3]:.2f}' for item in orders])
        
        print(orders[-1])
        lastOrder = orders[-1]
        print("lastOrder: ", lastOrder)
        #lastOrderJoined = ','.join(str(lastOrder))
        #print("lastOrderJoined: ", lastOrderJoined)
        #lastOrderList = lastOrderJoined.split(',')
        #print("lastOrderList: ", lastOrderList)
        lastOrderPretty = str(lastOrder[0]) + " " + str(lastOrder[1]) + " " + str(lastOrder[2]) + " " + str(lastOrder[3])
        
        #### print("order_details: ", order_details)
        order_summary = f'Total Cost: ${self.total_cost:.2f}' # displays total cost
        print("order_summary: ", order_summary)

        # displays a summary of the orders and the total cost
        tkinter.messagebox.showinfo('Your Order', f'{lastOrderPretty}\n\n{order_summary}')

        conn.close()
    
    def show_all_orders(self):
        
        conn = sqlite3.connect('cfc_orders.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT order_id, item_name, item_type, price FROM orders')
        orders = cursor.fetchall()

        order_details = '\n'.join([f'Order ID: {item[0]} - {item[1]} ({item[2]}) - ${item[3]:.2f}' for item in orders])
        
        tkinter.messagebox.showinfo('Your Order', f'{order_details}')
        conn.close()



    def finish_order(self):
        print(self.gcombo_name, 
              self.gcombo_type, 
              self.gcombo_price, 
              self.gdrink_size, 
              self.gdrink_name, 
              self.gdrink_price, 
              self.gmain_name, 
              self.gchicken_type, 
              self.gchicken_price, 
              self.gside_name, 
              self.gside_price, 
              self.gdessert_name, 
              self.gdessert_price, 
              self.gsauce_name, 
              self.gsauce_price)
        insert_order(self.gcombo_name, self.gcombo_type, self.gcombo_price,
                     self.gdrink_size, self.gdrink_name, self.gdrink_price,
                     self.gmain_name, self.gchicken_type, self.gchicken_price,
                     self.gside_name, self.gside_price, self.gdessert_name,
                     self.gdessert_price, self.gsauce_name, self.gsauce_price
                     )

if __name__ == "__main__":
    menu = Menu()
#

#This is the end of the program
