# Original string of words
text = 'amenorrhea; centimeter; commensurate; diameter; dimension; gematria; geometry; immense; isometric; meal (n.1) "food, time for eating;" measure; menarche; meniscus; menopause; menses; menstrual; menstruate; mensural; meter (n.1) "poetic measure;" meter (n.2) unit of length; meter (n.3) "device for measuring;" -meter; Metis; metric; metrical; metronome; -metry; Monday; month; moon; parameter; pentameter; perimeter; piecemeal; semester; symmetry; thermometer; trigonometry; trimester.'
# Split the string by semicolons
word_list = text.split(";")

# Strip any leading or trailing whitespace from each word and print each word
for word in word_list:
    print(word.strip())