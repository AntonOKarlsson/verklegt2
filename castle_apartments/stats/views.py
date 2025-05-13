from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def stats_home(request):
    return render(request, 'stats_home.html')  # Just renders the page

def index_plot(request):
    url = 'https://frs3o1zldvgn.objectstorage.eu-frankfurt-1.oci.customer-oci.com/n/frs3o1zldvgn/b/public_data_for_download/o/kaupvisitala.csv'
    data = pd.read_csv(url, encoding='utf-8')

    data['Date'] = pd.to_datetime(data['AR'].astype(str) + '-' + data['MANUDUR'].astype(str), format='%Y-%m')
    data = data.set_index('Date')
    data = data.drop(columns=['AR', 'MANUDUR'])
    data = data.replace(',', '.', regex=True).apply(pd.to_numeric, errors='coerce')

    data = data.drop(columns=['UTGAFUDAGUR'], errors='ignore')

    fig, ax = plt.subplots(figsize=(10, 6))
    data.plot(ax=ax)
    ax.set_title("Property Sales Index Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Index Value")
    ax.legend(title="Indicators", bbox_to_anchor=(1.05, 1))
    plt.tight_layout()

    # Save plot to base64 image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close(fig)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    image_base64 = base64.b64encode(image_png).decode('utf-8')

    return render(request, 'stats/stats_home.html', {'plot_base64': image_base64})
