class Part:
    def __init__(self, name, price, image_url, url, manufacturer,
                 upper, charging_handle, bcg, lower):
        self.name = name
        self.price = price
        self.image_url = image_url
        self.url = url
        self.manufacturer = manufacturer
        self.upper = upper
        self.charging_handle = charging_handle
        self.bcg = bcg
        self.lower = lower
        self.nano_id = None

    def __str__(self):
        return self.nano_id + ", " + self.name + ", " + self.price + ", Charging Handle: " + str(self.charging_handle) + ", bcg: " + str(self.bcg)
