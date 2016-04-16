# -*- coding: utf-8 -*-

import requests
import string
import json
import difflib


def call_text_enricher(text):
    printable = string.printable
    text = filter(lambda x: x in printable, text)
    url = "http://text-enricher.myntra.com/AttrTags"
    payload = {
        "id": "123",
        "payload":
            {
                "text_to_enrich": text,
                "entity_id": "234"
            }
    }
    res = requests.post(url=url, data=json.dumps(payload), headers={'Content-type': 'application/json'})
    print res.text
    return res


def create_set_string_care_about():
    tags = set()
    # file_name = "Article_type.txt"
    file_name = "Strings_I_Care_About.txt"
    f = open(file_name, 'r')
    for line in f:
        values = line.split(',')
        if values[0].lower()[:-1] in tags:
            continue
        tags.add(values[0].lower()[:-1])
    return tags


def filter_data(res):
    tags = create_set_string_care_about()
    json_response = res.json()
    return_tags = set()
    for item in tags:
        new_list = [s for s in json_response["response"]["data"]["tags"] if item in s]
        if len(new_list):
            [return_tags.add(s) for s in new_list]
    print return_tags

    '''
    for item in json_response["response"]["data"]["tags"]:
        if " " in item and item.split(" ")[-1] in tags:
            print item
        #values = difflib.get_close_matches(item, tags)
        #if len(values):
        #    #print item, values
    '''


def u_encode(input):
    if isinstance(input, dict):
        return {u_encode(key): u_encode(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [u_encode(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('ascii')
    else:
        return input

if __name__ == "__main__":
    str = '''Sonam Kapoor claims she is your average millennial. She cusses online, fights her trolls, occasionally states she’s “looking like a mess” and is unabashed about Instagramming OOTD pictures of herself. And yes, like the rest of us, she’s addicted to her phone too; as we talk, it beeps constantly with Twitter notifications (no doubt triggered by her gargantuan fanbase). She is quick to Google every time she gets stuck, like the number of times she’s been on the cover of Vogue—counting this issue, that’s seven in total. So Kapoor might seem like she’s like the rest of us, but how many millennials can stake claim to her credentials?
We are sitting in the three-storeyed home she shares with her parents, sister Rhea, brother Harshvardhan and two fluffy Pomeranians, nestled in a quiet but decidedly star-studded lane in suburban Mumbai. The living room is brimming with coffee-table books, paintings, oversized sculptures and globes of marigold blooms propped up on sticks—objects that lend it the dramatic flair of a Bollywood home. “I spend so much time with my family that they want me out of the house. I speak to my mom five times a day, I speak to my dad every day,” she says. And yet, Kapoor is fiercely independent, has managed her own finances since she was a teenager and is determined to better herself this year “by being healthier, fitter and happier.” Despite this self-improvement mission, she doesn’t shy away from embracing her frothier side: she dreams about filling her wardrobe space (it was actually a dream) with a certain pair of Stella McCartney loafers that she is certain she would look ridiculous in…“like Donald Duck.”
For someone who dreams about fashion, it’s hardly surprising that she tops every style survey—including Vogue’s very own. “The best shoots that Vogue has done have been of me,” says Kapoor. She sure knows a thing or two about loving herself, though she insists “it’s not in a narcissistic way.” Turning 30 last June has made her shift gear. Damn the critics who chide her for her fashion craze and her motor mouth, Kapoor’s philosophy is simple: what she does, she does for herself. And she’s made peace with it.
This is Sonam Kapoor 2.0, embracing herself. She speaks to Vogue about her goals for 2016.
1. “I will think before I react”
Kapoor admits she lets her motor mouth get the better of her. “Sarcasm gets lost a lot of times…especially with me. People tend to take me very literally,” she says. This year, the actor will attempt to practise brevity in speech and “think things through and react with a little more patience.”
2. “I want to do more meaningful cinema”
Kapoor strongly believes that young girls need to have a voice in India. It’s the reason why, since the early days of her career, she has tackled female-centric roles head-on, she says. “I want to be remembered for good work or not remembered at all,” she declares. Films like Aisha (2010) and Khoobsurat (2014) had strong female leads, even if they were a bit silly. With her upcoming release, Neerja, Kapoor hopes to better herself (it’s the most emotionally challenging role she has done so far). Produced by photographer Atul Kasbekar and Fox Star Studios, Neerja tells the story of the 22-year-old Pan Am flight attendant, Neerja Bhanot, who was killed while trying to help three children escape the Mumbai-New York flight hijacked in 1986. Playing the lead character has humbled Kapoor, who says that on most days of filming she felt like a fraud. “[It’s] one of those films that inspire you to have courage in the face of things that are not going your way.”

3.“I will shop less”
“There are so many ways to cheat [on this resolution], so I’ll give up half my credit cards and add a credit card limit. If there is something that I want, I won’t buy it. Save more, shop less—that’s the only way.”
4. “I won’t stand bullying”
Last year, Kapoor’s tweet about misogyny and the beef and porn bans went viral. “It was a general mindset that I was critiquing,” she explains. Being in the film industry doesn’t make her a politician or even a social worker, she points out, but that didn’t stop people from wondering if the actor owned a dictionary. Kapoor isn’t one to sit back and let others tell her what to do. “Initially, I tried to respond to each one and after that I was just like, “&*^% it. I will say what I want to say,” she declares. Expect more badass retorts from her this year!
5. “I will make healthy the new sexy”
“I’m a food-obsessed human being. I get excited ordering pav bhaji, which is so embarrassing for my team,” she says with a laugh. “I eat absolute rubbish, [and this year] I need to stop doing that and start taking care of my health.” A healthy lifestyle starts with the right diet and for Kapoor that’s where the struggle lies. “I don’t mind being bigger or having bad skin, but I do mind being unhealthy.”
Read the rest of her resolutions and more about Sonam Kapoor in Vogue India’s January 2016 issue. On stands on December 31. Subscribe to the print edition or get the single digital copy of the January 2016 issue of Vogue India now.'''
    str = '''Ladies, it’s time to bare your clavicles. With this season’s love of all things off-shoulder—from clingy knit dresses to peasant blouses—Vogue revisits the sexy silhouette popularised by Brigitte Bardot in the late ’50s. The French actor paired her off­-shoulder blouses with everything from midi skirts to cropped trousers for an unapologetically seductive look. A bare décolletage may seem like the perfect canvas for your favourite statement necklace, but suppress the urge. Keep jewellery to a minimum (try some stud earrings or a delicate gold chain) and let your toned collarbone steal the spotlight. Take cues from these women’s styling choices to master the shoulder parade.
    '''
    str = '''
    Flared jeans are one of those love-or-hate trends that you either never really gave up on or have an acute aversion to. Though bell-bottoms were the pants of choice for American sailors in the early 19th century, they became a mainstream rage only in the ’60s and ’70s, followed by brief comebacks in 1996 and 2006.
But let’s be honest. With the retro revival in full swing these days, this is not a style you want to resign to the back of your closet. While they may have been a staple in the erstwhile flower child’s wardrobe (one with a strictly bohemian sartorial sensibility), millennial fashionistas have discovered more than just that one way to style it.
Vogue brings you inspiration from our go-to celebrities who have a flair for flare.
'''
    str = '''The lesson you should be picking up from Kareena Kapoor Khan’s look is to play with varied tones of the same hue—blue, in her case—accentuated by a tan belt. Choose a hemline that skims the floor for a look even Ali MacGraw would approve of.
    '''
    str = '''Malaika Arora Khan’s look oozes yesteryear movie star glamour (did you expect any less from her?). Take a cue from her and pair your flared jeans with a fuss-free top and oversized sunnies for a lunch date.'''
    str = '''Olivia Palermo gives us a masterclass in combining two reigning trends—flared denims and military jackets. You can tweak her look a bit to keep it summer-appropriate by layering a white tank with an army-print cape.'''
    response = call_text_enricher(str.lower())
    filter_data(response)
