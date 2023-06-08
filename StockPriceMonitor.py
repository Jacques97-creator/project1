import tkinter as tk
import requests
import time
import threading
from datetime import datetime

# Global variables
current_price = 0
previous_price = 0
alarm_threshold = 3
stock_name = ""  # New global variable for stock name
#index_counter = 0

def update_clock():
    if show_clock:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        clock_label.config(text=current_time)
    clock_label.after(1000, update_clock)


def toggle_clock():
    global show_clock
    show_clock = not show_clock
    if show_clock:
        clock_label.pack()
    else:
        clock_label.pack_forget()


def get_stock_price(stock_name, start_date, end_date):
    url = f'https://api.marketdata.app/v1/stocks/candles/D/{stock_name}?from={start_date}&to={end_date}'
    print("URL:", url)

    response = requests.get(url)

    print(response)

    if response.status_code == 200:
        data = response.json()
        if 'c' in data:
            return data['c'][0]
    return None


def store_stock_value():
    global current_price, previous_price
    stock_name = entry_stock.get()
    start_date = entry_start_date.get()
    end_date = entry_end_date.get()

    price = get_stock_price(stock_name, start_date, end_date)
    if price is not None:
        previous_price = current_price
        current_price = price
        console_message = f"Date: {start_date}, Volume: {end_date}, Stock value stored: {price}"
        print(console_message)
        label_price.config(text=str(price))


def check_price_alarm():
    global current_price, previous_price, alarm_threshold
    if current_price > previous_price * (1 + alarm_threshold / 100):
        print("ALARM! Stock price increased by", alarm_threshold, "%")


def start_flow_of_information():
    global stock_name
    stock_name = "GOOG"
    threading.Thread(target=continuous_price_update, args=(stock_name,)).start()


def get_realtime_price(stock_name, data_corrector):
    #global index_counter  # Declare index_counter as global
    url = f'https://serpapi.com/search.json?engine=google_finance&q={stock_name}:NASDAQ&api_key=b04a2d0bd225550d77b800c052bc164d4e0521d93780b268d2e8df95a71ffb8a'

    response = requests.get(url)

    print(response)
    if response.status_code == 200:
        data = response.json()
        if 'graph' in data:
            current_time = datetime.now().time()
            market_open_time = datetime.strptime("09:30", "%H:%M").time()  # Market open time: 9:30 AM
            time_diff = datetime.combine(datetime.today(), current_time) - datetime.combine(datetime.today(), market_open_time)
            index = int(time_diff.total_seconds() // 60)
            print("Index currently equals to:", str(index))
            #index_counter = int(index) - data_corrector[0]
            #if index_counter + 1 == int(index):
                #index_counter = int(index) - data_corrector[-1]
            if index < len(data['graph']):
                return data['graph'][int(index) - data_corrector[0]]
            else:
                data_corrector[0] += 1
                print("Current number of iterations with no value:", str(data_corrector[0]))

                return data['graph'][int(index) - data_corrector[0]]
    return None


def continuous_price_update(stock_name):
    data_corrector = [0]
    while True:
        price = get_realtime_price(stock_name, data_corrector)
        if price is not None:
            formatted_price = f"Price: {price['price']}, Currency: {price['currency']}"
            console_message = f"Date: {price['date']}, Volume: {price['volume']}, {formatted_price}"
            print("Real-time price:", console_message)
            label_price_test.config(text=str(formatted_price))
        time.sleep(60)


window = tk.Tk()
window.title("Stock Price Monitor")

clock_label = tk.Label(window, font=("Arial", 14), bg="white", fg="black")
clock_label.pack()

show_clock = True
update_clock()

button_toggle_clock = tk.Button(window, text="Toggle Clock", command=toggle_clock)
button_toggle_clock.pack()

label_stock = tk.Label(window, text="Enter the stock name:")
label_stock.pack()
entry_stock = tk.Entry(window)
entry_stock.pack()

label_start_date = tk.Label(window, text="Enter the start date (YYYY-MM-DD):")
label_start_date.pack()
entry_start_date = tk.Entry(window)
entry_start_date.pack()

label_end_date = tk.Label(window, text="Enter the end date (YYYY-MM-DD):")
label_end_date.pack()
entry_end_date = tk.Entry(window)
entry_end_date.pack()

button_stock = tk.Button(window, text="Get Stock Price", command=store_stock_value)
button_stock.pack()

label_current_price = tk.Label(window, text="Current Price for " + str(alarm_threshold) + " Minutes Comparison:")
label_current_price.pack()
label_price = tk.Label(window, text="N/A")
label_price.pack()

label_realtime_price = tk.Label(window, text="Google - Real-Time Pricing Test:")
label_realtime_price.pack()
label_price_test = tk.Label(window, text="N/A")
label_price_test.pack()

button_flow = tk.Button(window, text="Start Flow of Information", command=start_flow_of_information)
button_flow.pack()

window.mainloop()
