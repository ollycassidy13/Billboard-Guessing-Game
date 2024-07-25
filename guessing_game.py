import billboard

def get_top_tracks(chart_name="hot-100", limit=100):
    chart = billboard.ChartData(chart_name)
    title = [entry.title for entry in chart.entries[:limit]]
    artist = [entry.artist for entry in chart.entries[:limit]]
    return title, artist

title, artist = get_top_tracks()
n = 0
attempts = 2

while n < len(title) and attempts >= 0:
    i = 0
    correct = False
    print("Song " + str(n + 1) + ":")  
    print(title[n])
    print("Who is the artist?")
    guess = input().replace(',', ' ').replace('&', ' ').lower().replace('featuring', ' ').replace(' ', '')
    correct_artist = artist[n].replace(',', ' ').replace('&', ' ').lower().replace('featuring', ' ').replace(' ', '')
    if guess == correct_artist:
        correct = True
        i += 1
        
    if correct:
        print("Correct! The artist was: " + artist[n])
        n += 1
    else:
        if attempts > 0:
            print("Incorrect, try again")
            print (str(attempts) + " attempts remaining")
            attempts -= 1
        else:
            print("Game Over :(")
            print("You scored " + str(n))
            attempts -= 1     

if n == 99 and attempts >= 0:
    print("You won! You scored 100")        