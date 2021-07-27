import matplotlib.pyplot as plt
import base64
from io import BytesIO
from datetime import date
def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png =buffer.getvalue()
    #print(image_png)
    graph =base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(x,y,test,train):
    #..
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,5))

    # Textual month, day and year	
    today = date.today()
    d2 = today.strftime("%B %d, %Y")
   # print("d2 =", d2)

    plt.title('Forecasting Bitcoin USD (BTC-USD) for today '+ str(d2))
    #plt.plot(x,y)
    plt.xticks(rotation=45)
    plt.xlabel('days')
    plt.ylabel('value')

   


    y.plot(legend=True,color='blue', linestyle='dashed',label='Predicted Price')
    test.plot(legend=True,color='red', label='Actual Price')
    train.plot(legend=True,color='green', label='Train data(Historical)')
    

    plt.tight_layout()
    graph=get_graph()
    return graph