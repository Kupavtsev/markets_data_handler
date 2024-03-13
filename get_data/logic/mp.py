from get_data.models import DailyPrices, AssetSymbol


def prepair():
    assets : list = AssetSymbol.objects.all()
    for asset in assets:
        print(asset)

def main():
    prepair()