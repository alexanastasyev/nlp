import spacy
import requests

nlp = spacy.load("ru_core_news_md")
weather_full = nlp("Погода в городе")
weather_temp = nlp("Сколько градусов в городе")

api_key = "019947b686adde825c5c6104b3e13d7e"


def get_weather(city_name):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&lang=ru".format(city_name, api_key)
    http_response = requests.get(api_url)
    response_dict = http_response.json()
    return response_dict


def get_full_weather(city_name):
    weather_response = get_weather(city_name)
    weather_desc = weather_response["weather"][0]["description"]
    temp = int(weather_response["main"]["temp"]) - 274
    return weather_desc + ", " + str(temp) + " градусов"


def chatbot(statement):
    statement = nlp(statement)
    min_similarity = 0.35

    if (weather_full.similarity(statement) >= min_similarity) or (weather_temp.similarity(statement) >= min_similarity):
        for ent in statement.ents:
            if ent.label_ == "LOC":
                city = str(ent.lemma_)
                return get_full_weather(city)
    else:
        return "Извините, я не понимаю"


while True:
    user_input = input("\nЧем я могу вам помочь?\n")
    response = chatbot(user_input)
    print(response)

