from flask import Flask, render_template, request

app = Flask(__name__)

pivoted_items = {
    'mining': {
        'coal': {'points': 1},
        'salt': {'points': 1},
        'stone': {'points': 1},
        'iron': {'points': 2},
        'quartz': {'points': 2},
        'copper': {'points': 2},
        'marble': {'points': 2},
        'mercury': {'points': 3},
        'sulfur': {'points': 3},
        'silver': {'points': 3},
        'manganese': {'points': 3},
        'obsidian': {'points': 4},
        'gold': {'points': 4},
        'soul gem': {'points': 4},
        'spell crystal': {'points': 4}
    },
    'hunting': {
        'bone': {'points': 1},
        'feathers': {'points': 1},
        'honey': {'points': 1, 'expiration': '1 month'},
        'food': {'points': 1, 'expiration': '1 month'},
        'soft pelt': {'points': 2},
        'demon blood': {'points': 2},
        'large hide': {'points': 3},
        'celestial blood': {'points': 3},
        'fae blood': {'points': 4}
    },
    'mercantile': {
        'cloth': {'points': 1},
        '5 postage (domestic)': {'points': 1},
        'paper': {'points': 1},
        'glass': {'points': 2},
        'blood ink': {'points': 2},
        '5 postage (overseas)': {'points': 2},
        'sanctified water': {'points': 3},
        'ritual component': {'points': 4}
    },
    'black_market': {
        'zye scarab': {'points': 3},
        'zye blood parasites': {'points': 4}
    }
}

item_lookup = {
    'coal': {'points': 1, 'cat': 'mining'},
    'salt': {'points': 1, 'cat': 'mining'},
    'stone': {'points': 1, 'cat': 'mining'},
    'iron': {'points': 2, 'cat': 'mining'},
    'quartz': {'points': 2, 'cat': 'mining'},
    'copper': {'points': 2, 'cat': 'mining'},
    'marble': {'points': 2, 'cat': 'mining'},
    'mercury': {'points': 3, 'cat': 'mining'},
    'sulfur': {'points': 3, 'cat': 'mining'},
    'silver': {'points': 3, 'cat': 'mining'},
    'manganese': {'points': 3, 'cat': 'mining'},
    'obsidian': {'points': 4, 'cat': 'mining'},
    'gold': {'points': 4, 'cat': 'mining'},
    'soul gem': {'points': 4, 'cat': 'mining'},
    'spell crystal': {'points': 4, 'cat': 'mining'},
    'bone': {'points': 1, 'cat': 'hunting'},
    'feathers': {'points': 1, 'cat': 'hunting'},
    'honey': {'points': 1, 'cat': 'hunting', 'expiration': '1 month'},
    'food': {'points': 1, 'cat': 'hunting', 'expiration': '1 month'},
    'soft pelt': {'points': 2, 'cat': 'hunting'},
    'demon blood': {'points': 2, 'cat': 'hunting'},
    'large hide': {'points': 3, 'cat': 'hunting'},
    'celestial blood': {'points': 3, 'cat': 'hunting'},
    'fae blood': {'points': 4, 'cat': 'hunting'},
    'cloth': {'points': 1, 'cat': 'mercantile'},
    '5 postage (domestic)': {'points': 1, 'cat': 'mercantile'},
    'paper': {'points': 1, 'cat': 'mercantile'},
    'glass': {'points': 2, 'cat': 'mercantile'},
    'blood ink': {'points': 2, 'cat': 'mercantile'},
    '5 postage (overseas)': {'points': 2, 'cat': 'mercantile'},
    'sanctified water': {'points': 3, 'cat': 'mercantile'},
    'ritual component': {'points': 4, 'cat': 'mercantile'},
    'zye scarab': {'points': 3, 'cat': 'black_market'},
    'zye blood parasites': {'points': 4, 'cat': 'black_market'}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/order', methods=["GET", "POST"])
def order():
    if request.method == "POST":
        # Collect checked items and their quantities
        submitted = {}
        for cat, items_in_cat in pivoted_items.items():
            for item in items_in_cat:
                checkbox_name = f"chk_{item}"
                qty_name = f"qty_{item}"
                if checkbox_name in request.form:
                    submitted[item] = int(request.form.get(qty_name, 1))
        
        # Print selections to terminal
       
        order_details=construct_order(submitted)
        
        return render_template('confirmation.html', order_details=order_details)
    
    return render_template('order.html', items=pivoted_items)

def construct_order(order):
    order_details=[]
    order_printout=''
    total_cost=0

    for item,quantity in order.items():
        item_cost=item_lookup[item]['points']
        if item_cost>1:
            item_cost*=1.5
        order_cost=item_cost*quantity
        total_cost+=order_cost
        item_detail=f'{quantity} {item} ({order_cost} silver)'
        order_details.append(item_detail)
    for item in order_details:
        printout=f'{item}<br><br>'
        order_printout+=printout

    total_cost_readout=f'<strong>Total cost: {total_cost} silver</strong>'

    order_printout+=total_cost_readout

    return order_printout

if __name__=="__main__":
    app.run(debug=True)
