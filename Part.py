class Part:
    def __init__(self, name, price, image_url, url, manufacturer,
                 upper, charging_handle, bcg, lower, attachment):
        self.name = name
        self.price = price
        self.image_url = image_url
        self.url = url
        self.manufacturer = manufacturer
        self.upper = upper
        self.charging_handle = charging_handle
        self.bcg = bcg
        self.lower = lower
        self.attachment = attachment
        self.id = None

    def __str__(self):
        return (self.id + ", " + self.name + ", " + self.price + (", Charging "
                                                                  "Handle: ")
                + str(self.charging_handle) + ", bcg: " + str(self.bcg)
                + ", Manufacturer: " + str(self.manufacturer) + ", Image URL: "
                + str(self.image_url))
