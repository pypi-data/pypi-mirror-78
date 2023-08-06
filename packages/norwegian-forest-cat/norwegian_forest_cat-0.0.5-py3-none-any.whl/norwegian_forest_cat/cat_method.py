import requests


class Cat:
    def __init__(self, name, age=0):
        self.name = name
        self.age = age

    def get_name(self):
        return self.name

    def get_age(self):
        return self.age

    def get_requests(self):
        r = requests.get("https://api.github.com/events")
        return r.text


if __name__ == "__main__":
    cat = Cat("inside poyo")
    print(cat.get_name())
    print(cat.get_age())
    print(cat.get_requests())