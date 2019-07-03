from bokeh.plotting import figure
from bokeh.embed import components

def per_payee(collection):

    payee = [ doc['_id'] for doc in collection.aggregate([ { '$group': {'_id': "$contas.payee", 'total': {'$sum': "$contas.amount"} } }])]
    expediture = [ doc['total'] for doc in collection.aggregate([ { '$group': {'_id': "$contas.payee", 'total': {'$sum': "$contas.amount"} } }])]

    p = figure(x_range=payee, plot_height=250, title="Spendings",
            toolbar_location=None, tools="")

    p.vbar(x=payee, top=expediture, width=0.9)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.sizing_mode = "scale_width"

    return components(p)

def per_month(collection):

        month = [ doc['_id'] for doc in collection.aggregate(
                [
                        { '$match': {'contas.amount': {'$gt':0} } },
                        { '$group': {'_id': "$contas.month_ref", 'total': {'$sum': "$contas.amount"} } },
                        { '$sort': {'_id': 1}}
                ],
        )]

        expediture = [ doc['total'] for doc in collection.aggregate(
                [
                        { '$match': {'contas.amount': {'$gt':0} } },
                        { '$group': {'_id': "$contas.month_ref", 'total': {'$sum': "$contas.amount"} } },
                        { '$sort': {'_id': 1}}
                ],
        )]

        p = figure(x_range=month, plot_height=250, title="Spendings",
                toolbar_location=None, tools="")

        p.line(x=month, y=expediture, line_width=4)
        p.circle(x=month, y=expediture, size=10)

        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        p.y_range.end = max(expediture)+200
        p.sizing_mode = "scale_width"

        return components(p)

