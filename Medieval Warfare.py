# Callan Murphy
# 31/05/2018
'''
Medieval Warfare is an RPG fantasy game where the user controls a character
onscreen in their adventure into a new town. Gameplay consists of the ability
to battle other towns to earn gold, which can be used to purchase stronger
items in the shop such as armour or a shield. Watermelon allows the player
to heal health, and each armour item allows them to increase their armour bar
by a third. The hospital functions as a cooldown for townies who have been
injured in battle. The game is intentionally open-ended to allow for a free
playstyle and open-world experience. The game is never "won", however it can
be lost when the player has less than 100 gold and is completely out of health.

Most of the pygame code throughout the file was done with help from
https://www.pygame.org/docs/, any code from other locations has been sourced.
'''

# NOTE - archer arrows are referred to as "bullets" for convenience of imported code from last project
# NOTE - disappearing enemies in battle is a known issue
# NOTE - crashing battle screen is a known issue
# NOTE - enemies getting stuck above trees when attempting to travel downwards is a known issue

import pygame, random  # imports pygame and random modules

pygame.init()  # initializes pygame with all its included components
global clock
# noinspection PyRedeclaration
clock = pygame.time.Clock()


def menu():
    '''
    Main menu function to display the menu upon beginnning the game. Allows
    the player to navigate and choose either 'controls' or 'play game',
    running the corresponding function to display the menu item.
    '''
    menuSelectImage = pygame.image.load("MenuSelect.gif")
    select = menuSelectImage.get_rect()
    menuScreen = pygame.display.set_mode((1280, 705))
    font1 = pygame.font.SysFont('Calibri', 30)
    font4 = pygame.font.SysFont('Calibri', 70)
    font5 = pygame.font.SysFont('Calibri', 45)
    menuText = font4.render('MEDIEVAL WARFARE', False, (255, 255, 255))
    menuOption1Text = font5.render('Play Game', False, (0, 0, 0))
    menuOption2Text = font5.render('Controls', False, (0, 0, 0))
    instructionText = font1.render("Use the 'w' and 's' keys to scroll through the menu and 'enter' to select", False,
                                   (255, 255, 255))
    closeText = font1.render("Press 'ESC' to exit", False, (255, 255, 255))
    select.centerx = 485
    select.centery = 325
    option1 = True  # which menu option is selected
    close = 0  # used to exit main loop
    while True:  # main menu loop
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()  # closes window
                    close = 1
                    break
                if event.key == pygame.K_w:  # moves selector up
                    option1 = True
                    select.centerx = 485
                    select.centery = 325
                if event.key == pygame.K_s:  # moves selector down
                    option1 = False
                    select.centery = 425
                if event.key == pygame.K_RETURN:
                    if option1:
                        close = 1
                        pygame.display.quit()  # closes window
                        main()
                        break
                    elif option1 == False:
                        close = 1
                        pygame.display.quit()  # closes window
                        controls()
                        break
        if close == 1:
            break
        else:
            menuScreen.fill((30, 120, 0))
            menuScreen.blit(menuText, (335, 130))
            menuScreen.blit(menuOption1Text, (550, 300))
            menuScreen.blit(menuOption2Text, (550, 400))
            menuScreen.blit(instructionText, (15, 610))
            menuScreen.blit(closeText, (15, 650))
            menuScreen.blit(menuSelectImage, select)
            pygame.display.flip()  # allows colour/other graphics to be displayed


def controls():
    '''
    Displays a screen to show the controls for the game to the user. The user
    can return to the main menu at any time at which the menu function is
    called.
    '''
    controlsScreen = pygame.display.set_mode((1280, 705))
    wasdImage = pygame.image.load("WASD.gif")
    wasd = wasdImage.get_rect()
    wasd.centerx = 655
    wasd.centery = 300
    close = 0  # used to exit main loop
    font6 = pygame.font.SysFont('Calibri', 35)
    font7 = pygame.font.SysFont('Calibri', 60)
    controlsText = font7.render('CONTROLS', False, (255, 255, 255))
    upText = font6.render('Move Up', False, (255, 255, 255))
    downText = font6.render('Move Down', False, (255, 255, 255))
    rightText = font6.render('Move Right', False, (255, 255, 255))
    leftText = font6.render('Move Left', False, (255, 255, 255))
    exitScreenText = font6.render("Press 'enter' to return to the menu", False, (255, 255, 255))
    controlsScreen.fill((30, 120, 0))
    controlsScreen.blit(upText, (725, 60))
    controlsScreen.blit(downText, (555, 500))
    controlsScreen.blit(rightText, (835, 470))
    controlsScreen.blit(leftText, (325, 487))
    controlsScreen.blit(exitScreenText, (400, 610))
    controlsScreen.blit(controlsText, (20, 10))
    controlsScreen.blit(wasdImage, wasd)
    pygame.display.flip()  # allows colour/other graphics to be displayed
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    close = 1
                    pygame.display.quit()  # closes window
                    menu()
                    break
        if close == 1:
            break


def main():
    '''
    Main function for the game. Consists of all processes which allow the
    town to operate such as trees, building, townies, and ability to access
    the shop and hospital.
    '''
    global talkingTownie, phrase, chosenTownie
    screen = pygame.display.set_mode((1280, 705))

    playerImage = pygame.image.load("WarriorLeft.gif")
    player = playerImage.get_rect()
    player.centerx = 640
    player.centery = 690

    lakeImage = pygame.image.load("Lake.gif").convert()
    lake = lakeImage.get_rect()
    lake.centerx = 975
    lake.centery = 565

    backgroundImage = pygame.image.load(
        "Background.gif").convert()  # .convert() reduces a lot of lag by converting pixel format
    # code above done with help from http://www.pygame.org/docs/tut/newbieguide.html
    background = backgroundImage.get_rect()

    treeImage = pygame.image.load("Tree.gif").convert()
    tree = []
    for i in range(0, 27):  # randomly places 27 trees across two different sections in the town
        tree.append(treeImage.get_rect())
        while True:
            newPlace = 0
            if i < 8:
                tree[i].centerx = random.randint(50, 540)
                tree[i].centery = random.randint(500, 630)
            else:
                tree[i].centerx = random.randint(200, 1200)
                tree[i].centery = random.randint(50, 200)
            for x in range(0, len(tree) - 1):
                if tree[i].colliderect(tree[x]):
                    newPlace = 1
            if newPlace == 0:
                break

    friendlyImages = []

    captainImage = pygame.image.load("CliffRight.gif")
    friendlyImages.append(captainImage)
    captain = captainImage.get_rect()
    captain.centerx = 565
    captain.centery = 590

    townie1Image = pygame.image.load("Townie1Right.gif")
    friendlyImages.append(townie1Image)
    townie1 = townie1Image.get_rect()
    townie1.centerx = 700
    townie1.centery = 300

    townie2Image = pygame.image.load("Townie2Right.gif")
    friendlyImages.append(townie2Image)
    townie2 = townie2Image.get_rect()
    townie2.centerx = 400
    townie2.centery = 300

    townie3Image = pygame.image.load("Townie3Right.gif")
    friendlyImages.append(townie3Image)
    townie3 = townie3Image.get_rect()
    townie3.centerx = 900
    townie3.centery = 200

    townie4Image = pygame.image.load("Townie4Right.gif")
    friendlyImages.append(townie4Image)
    townie4 = townie4Image.get_rect()
    townie4.centerx = 600
    townie4.centery = 400

    characters = [player, captain, townie1, townie2, townie3, townie4]
    townies = [captain, townie1, townie2, townie3, townie4]

    shopImage = pygame.image.load("Shop.gif")
    shop = shopImage.get_rect()
    shop.centery = 329
    shop.centerx = 200

    hospitalImage = pygame.image.load("Hospital.gif")
    hospital = hospitalImage.get_rect()
    hospital.centery = 320
    hospital.centerx = 900

    goldImage = pygame.image.load("Gold.gif")
    goldIcon = goldImage.get_rect()
    goldIcon.centerx = 35
    goldIcon.centery = 200  # 133

    healthImage = [pygame.image.load("Health0.gif"), pygame.image.load("Health1.gif"), pygame.image.load("Health2.gif"),
                   pygame.image.load("Health3.gif"), pygame.image.load("Health4.gif"), pygame.image.load("Health5.gif")]
    health = healthImage[5].get_rect()
    health.centerx = 85
    health.centery = 80
    playerHealth = 5

    armourImage = [pygame.image.load("Armour0.gif"), pygame.image.load("Armour1.gif"), pygame.image.load("Armour2.gif"),
                   pygame.image.load("Armour3.gif")]
    armour = healthImage[5].get_rect()
    armour.centerx = 85
    armour.centery = 155
    playerArmour = 0

    hospitalVisit = 0
    firstBattle = True

    townieSpeech = False
    towniePhrase = False
    townieSpeechCounter = 0

    gold = 200
    counter = 0
    exitLoop = False
    # 4 variables below are used in townie movement
    towniesCounter = []
    for i in range(0, len(townies)):
        towniesCounter.append(0)
    randomMovement = []
    for i in range(0, len(townies)):
        randomMovement.append(0)
    towniesRandomCounterEnd = []
    for i in range(0, len(townies)):
        towniesRandomCounterEnd.append(0)
    randomCounterEnd = 0  # used later to randomly select a number for the counter to end at

    font1 = pygame.font.SysFont('Calibri', 50)
    healthText = font1.render('Health', False, (0, 0, 0))
    armourText = font1.render('Armour', False, (0, 0, 0))
    goldText = font1.render(str(gold), False, (0, 0, 0))

    speechCounter = 0
    speechFont = pygame.font.SysFont('Calibri', 25)
    cliffSpeaking = False
    dead = []
    deadImages = []
    deadCharge = []
    deadCounters = []
    chargeBars = []
    chargeBarsRect = []
    chargeX = 200
    chargeY = 550
    for i in range(0, 5):
        chargeBars.append(pygame.image.load("Health0.gif"))
    for i in range(0, 5):  # charge bars are used to show the townies' health recharging
        chargeBarsRect.append(healthImage[0].get_rect())
        chargeBarsRect[i].centerx = chargeX
        chargeBarsRect[i].centery = chargeY
        if i == 0 or i == 1:
            chargeY -= 200
        if i == 2:
            chargeX += 650
            chargeY = 550
        if i == 3 or i == 4:
            chargeY -= 200

    playerLeft = pygame.image.load("WarriorLeft.gif")
    playerRight = pygame.image.load("WarriorRight.gif")

    slot = [0, 0, 0, 0]  # shop slots to track if player has an item

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()  # closes window
                    exitLoop = True
                    menu()
                    break
                if event.key == pygame.K_SPACE and cliffSpeaking == True:
                    speechCounter = 800
                if event.key == pygame.K_b and playerHealth > 0 and cliffSpeaking == False:
                    pygame.display.quit()
                    gold, townies, playerHealth, dead, deadImages, firstBattle, playerArmour = battle(characters,
                                                                                                      townies,
                                                                                                      goldImage,
                                                                                                      goldIcon,
                                                                                                      goldText,
                                                                                                      healthImage,
                                                                                                      playerHealth,
                                                                                                      health,
                                                                                                      healthText,
                                                                                                      armourImage,
                                                                                                      playerArmour,
                                                                                                      armour,
                                                                                                      armourText,
                                                                                                      player,
                                                                                                      playerImage,
                                                                                                      friendlyImages,
                                                                                                      treeImage, gold,
                                                                                                      dead, deadImages,
                                                                                                      playerLeft,
                                                                                                      playerRight,
                                                                                                      firstBattle)
                    screen = pygame.display.set_mode((1280, 705))
                    playerArmour = 0
                    for i in range(0, len(slot) - 1):
                        if slot[i] != 0:
                            playerArmour += 1
                    goldText = font1.render(str(gold), False, (0, 0, 0))
                    characters = []
                    characters.append(player)
                    for i in townies:
                        characters.append(i)
                    player.centerx = 640
                    player.centery = 600
                    # code below allows for townie movement
                    towniesCounter = []
                    for i in range(0, len(townies)):
                        towniesCounter.append(0)
                    randomMovement = []
                    for i in range(0, len(townies)):
                        randomMovement.append(0)
                    towniesRandomCounterEnd = []
                    for i in range(0, len(townies)):
                        towniesRandomCounterEnd.append(0)
                    for i in characters:
                        i.centerx = 640
                        i.centery = 665
                    goldIcon.centerx = 35
                    goldIcon.centery = 200

        # code below checks if the game has been lost, displaying a game over screen

        if playerHealth == 0 and gold < 100:
            pygame.display.quit()
            screen = pygame.display.set_mode((1280, 705))
            gameOverText = font1.render('GAME OVER', False, (255, 255, 255))
            returnText = font1.render("Press 'enter' to return to the menu", False, (255, 255, 255))
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            pygame.display.quit()
                            exitLoop = True
                            menu()
                            break
                if exitLoop == True:
                    break
                screen.fill((20, 130, 0))
                screen.blit(gameOverText, (515, 200))
                screen.blit(returnText, (290, 380))
                pygame.display.flip()

        if exitLoop == True:
            break

        # code below allows player to move

        if cliffSpeaking == False:
            pressed = pygame.key.get_pressed()  # checks if a key has been pressed. Different way of checking than above since this method will recognize key holds (not just presses) which is better for player movement
            if pressed[pygame.K_w]: player.centery -= 3  # moves the player up by 4 units when 'w' key is pressed
            if pressed[pygame.K_s]: player.centery += 3  # moves the player down by 4 units when 's' key is pressed
            if pressed[pygame.K_a]:
                player.centerx -= 3  # moves the player left by 4 units when 'a' key is pressed
                playerImage = playerLeft  # changes the player image to be facing left
            if pressed[pygame.K_d]:
                player.centerx += 3  # moves the player right by 4 units when 'd' key is pressed
                playerImage = playerRight  # changes the player image to be facing right

        # code below prevents characters from going off-screen and from walking on obstacles (trees, lake, etc)

        for i in characters:
            if i.centerx <= 20:
                i.centerx = 20
            if i.centerx >= 1230:
                i.centerx = 1230
            if i.centery <= 50:
                i.centery = 50
            if i.centery >= 665:
                i.centery = 665
            # code below prevents characters from walking over trees
            for x in tree:
                if i != player:
                    if x.centerx + 37 > i.centerx > x.centerx - 39 and x.centery + 60 > i.centery > x.centery - 83:
                        if i.centerx > x.centerx + 32:
                            i.centerx = x.centerx + 36
                # this seperate code above is required since the townie graphics have a larger background than the player
                if x.centerx + 23 > i.centerx > x.centerx - 39 and i.centery < x.centery + 60 and i.centery > x.centery - 83:
                    if i.centerx > x.centerx + 18:
                        i.centerx = x.centerx + 22
                    if i.centerx < x.centerx - 34:
                        i.centerx = x.centerx - 38
                    if i.centery > x.centery + 55:
                        i.centery = x.centery + 59
                    if i.centery < x.centery - 78:
                        i.centery = x.centery - 82
            # code below prevents character from walking over lake
            if lake.centerx + 245 > i.centerx > lake.centerx - 260 and i.centery < lake.centery + 155 and i.centery > lake.centery - 155:
                if i.centerx > lake.centerx + 240:
                    i.centerx = lake.centerx + 244
                if i.centerx < lake.centerx - 255:
                    i.centerx = lake.centerx - 259
                if i.centery > lake.centery + 150:
                    i.centery = lake.centery + 154
                if i.centery < lake.centery - 150:
                    i.centery = lake.centery - 154

        for i in townies:
            if i.centery <= 370:
                i.centery = 370
            if player.colliderect(i):
                townieSpeech = True
                talkingTownie = i
                pickPhrase = True

        # code below is to allow for random townie movement

        for i in range(0, len(towniesCounter)):
            if towniesCounter[i] == 0:
                towniesRandomCounterEnd[i] = random.randint(25, 75)
            towniesCounter[i] += 1
            if towniesCounter[i] == towniesRandomCounterEnd[i]:
                randomMovement[i] = random.randint(1, 7)
                towniesCounter[i] = 0
            if randomMovement[i] == 1:
                rand = random.randint(1, 3)
                if i == 0 and cliffSpeaking == False:
                    captainImage = pygame.image.load("CliffRight.gif")
                    captain.centerx += 3
                elif i == 1:
                    townie1Image = pygame.image.load("Townie1Right.gif")
                    townie1.centerx += 3
                elif i == 2:
                    townie2Image = pygame.image.load("Townie2Right.gif")
                    townie2.centerx += 3
                elif i == 3:
                    townie3Image = pygame.image.load("Townie3Right.gif")
                    townie3.centerx += 3
                elif i == 4:
                    townie4Image = pygame.image.load("Townie4Right.gif")
                    townie4.centerx += 3
            elif randomMovement[i] == 2:
                rand = random.randint(1, 3)
                if i == 0 and cliffSpeaking == False:
                    captainImage = pygame.image.load("CliffLeft.gif")
                    captain.centerx -= 3
                elif i == 1:
                    townie1Image = pygame.image.load("Townie1Left.gif")
                    townie1.centerx -= 3
                elif i == 2:
                    townie2Image = pygame.image.load("Townie2Left.gif")
                    townie2.centerx -= 3
                elif i == 3:
                    townie3Image = pygame.image.load("Townie3Left.gif")
                    townie3.centerx -= 3
                elif i == 4:
                    townie4Image = pygame.image.load("Townie4Left.gif")
                    townie4.centery -= 3
            elif randomMovement[i] == 3:
                rand = random.randint(1, 3)
                if i == 0 and cliffSpeaking == False:
                    captain.centery -= 3
                elif i == 1:
                    townie1.centery -= 3
                elif i == 2:
                    townie2.centery -= 3
                elif i == 3:
                    townie3.centery -= 3
                elif i == 4:
                    townie4.centery -= 3
            elif randomMovement[i] == 4:
                rand = random.randint(1, 3)
                if i == 0 and cliffSpeaking == False:
                    captain.centery += 3
                elif i == 1 and cliffSpeaking == False:
                    townie1.centery += 3
                elif i == 2 and cliffSpeaking == False:
                    townie2.centery += 3
                elif i == 3 and cliffSpeaking == False:
                    townie3.centery += 3
                elif i == 4 and cliffSpeaking == False:
                    townie4.centery += 3

        # code below is used for keeping track of injured enemies

        for i in range(0, len(dead) - len(deadCharge)):
            deadCharge.append(0)
            deadCounters.append(0)

        for i in range(0, len(deadCounters)):
            deadCounters[i] += 1
            for x in range(300, 1501, 300):
                if deadCounters[i] == x:
                    deadCharge[i] += 1

        for i in range(0, len(deadCharge)):
            if deadCharge[i] == 1:
                chargeBars[i] = pygame.image.load("Health1.gif")
            elif deadCharge[i] == 2:
                chargeBars[i] = pygame.image.load("Health2.gif")
            elif deadCharge[i] == 3:
                chargeBars[i] = pygame.image.load("Health3.gif")
            elif deadCharge[i] == 4:
                chargeBars[i] = pygame.image.load("Health4.gif")
            elif deadCharge[i] == 5:
                chargeBars[i] = pygame.image.load("Health0.gif")
                townies.append(dead[i])
                characters.append(dead[i])
                dead.pop(i)
                deadCharge.pop(i)
                deadCounters.pop(i)
                friendlyImages.append(deadImages[i])
                deadImages.pop(i)
                break

        # code below activates the buildings

        if player.colliderect(shop):
            pygame.display.quit()
            gold, goldText, playerLeft, playerRight, playerHealth, playerArmour = shopping(gold, goldImage, goldIcon,
                                                                                           font1, goldText, slot,
                                                                                           playerLeft, playerRight,
                                                                                           playerHealth, playerArmour)
            playerImage = playerRight
            playerArmour = 0
            for i in range(0, len(slot) - 1):
                if slot[i] != 0:
                    playerArmour += 1
            screen = pygame.display.set_mode((1280, 705))
            player.centerx = 300
            player.centery = 360
            goldIcon.centerx = 35
            goldIcon.centery = 200

        if player.colliderect(hospital):
            pygame.display.quit()
            hospitalVisit = medical(player, playerImage, exitLoop, speechFont, dead, deadImages, chargeBars, health,
                                    chargeBarsRect, townies, deadCharge, deadCounters, friendlyImages, playerLeft,
                                    playerRight, characters, hospitalVisit)
            screen = pygame.display.set_mode((1280, 705))
            player.centerx = 770
            player.centery = 360

        # code below is to draw the graphics to the screen

        screen.blit(backgroundImage, background)
        for i in tree:
            screen.blit(treeImage, i)
        screen.blit(lakeImage, lake)
        screen.blit(shopImage, shop)
        screen.blit(hospitalImage, hospital)
        for i in range(0, len(townies)):
            screen.blit(friendlyImages[i], townies[i])
        screen.blit(playerImage, player)  # draws player on screen
        screen.blit(goldImage, goldIcon)
        screen.blit(goldText, (70, 167))
        screen.blit(healthImage[playerHealth], health)
        screen.blit(healthText, (8, 6))
        screen.blit(armourImage[playerArmour], armour)
        screen.blit(armourText, (8, 85))

        # intro speech (must be below most drawing to draw the speech bubble on top)

        if speechCounter != 800:
            cliffSpeaking = True
            speechCounter += 1
            skipSpeech = speechFont.render("Press 'spacebar' to skip", False, (255, 255, 255))
            screen.blit(skipSpeech, (5, 670))
            if speechCounter < 100:
                introSpeech1 = speechFont.render('Hello wanderer, welcome to our town!', False, (255, 255, 255))
                screen.blit(introSpeech1, (captain.centerx, captain.centery - 70))
            elif speechCounter < 200:
                introSpeech1 = speechFont.render("I'm Cliff, the captain of our army.", False, (255, 255, 255))
                screen.blit(introSpeech1, (captain.centerx, captain.centery - 70))
            elif speechCounter < 300:
                introSpeech1 = speechFont.render("You're welcome to wander about...", False, (255, 255, 255))
                screen.blit(introSpeech1, (captain.centerx, captain.centery - 70))
            elif speechCounter < 400:
                introSpeech1 = speechFont.render("and make yourself at home!", False, (255, 255, 255))
                screen.blit(introSpeech1, (captain.centerx, captain.centery - 70))
            elif speechCounter < 500:
                introSpeech1 = speechFont.render("We often fight other villages...", False, (255, 255, 255))
                screen.blit(introSpeech1, (captain.centerx, captain.centery - 70))
            elif speechCounter < 600:
                introSpeech1 = speechFont.render("for power and for gold!", False, (255, 255, 255))
                screen.blit(introSpeech1, (captain.centerx, captain.centery - 70))
            elif speechCounter < 700:
                introSpeech1 = speechFont.render("Press the 'b' key at any time to join us in a battle!", False,
                                                 (255, 255, 255))
                screen.blit(introSpeech1, (captain.centerx, captain.centery - 70))
            elif speechCounter < 800:
                introSpeech1 = speechFont.render("Farewell!", False, (255, 255, 255))
                screen.blit(introSpeech1, (captain.centerx, captain.centery - 70))
        else:
            cliffSpeaking = False

        if townieSpeech == True:
            if townieSpeechCounter != 70:
                townieSpeechCounter += 1
                if townieSpeechCounter == 1:
                    chosenTownie = talkingTownie
                    choice = random.randint(1, 10)
                    if choice == 1:
                        phrase = speechFont.render("Hello!", False, (255, 255, 255))
                    elif choice == 2:
                        phrase = speechFont.render("Outta my way!", False, (255, 255, 255))
                    elif choice == 3:
                        phrase = speechFont.render("Gold! Gold! Gold!", False, (255, 255, 255))
                    elif choice == 4:
                        phrase = speechFont.render("I could go for a change of scenery around here...", False,
                                                   (255, 255, 255))
                    elif choice == 5:
                        phrase = speechFont.render("I wanna battle an enemy town!!", False, (255, 255, 255))
                    elif choice == 6:
                        phrase = speechFont.render("I wish I had a bow and arrows...", False, (255, 255, 255))
                    elif choice == 7:
                        phrase = speechFont.render("You must be new around here!", False, (255, 255, 255))
                    elif choice == 8:
                        phrase = speechFont.render("I could go for a vacation", False, (255, 255, 255))
                    elif choice == 9:
                        phrase = speechFont.render("What is there to do around here?", False, (255, 255, 255))
                    elif choice == 10:
                        phrase = speechFont.render("Walking walking walking", False, (255, 255, 255))
                try:
                    screen.blit(phrase, (chosenTownie.centerx, chosenTownie.centery - 70))
                except:
                    pass
            else:
                townieSpeech = False
                townieSpeechCounter = 0

        # allows drawing and timing

        pygame.display.flip()  # allows colour/other graphics to be displayed
        clock.tick(80)


def medical(player, playerImage, exitLoop, speechFont, dead, deadImages, chargeBars, health, chargeBarsRect, townies,
            deadCharge, deadCounters, friendlyImages, playerLeft, playerRight, characters, hospitalVisit):
    '''
    This function allows the hospital to operate. It includes the nurse's
    speech to the player and the healing of townies who have been hospitalized.
    '''
    hospitalScreen = pygame.display.set_mode((1280, 705))
    bedImage = pygame.image.load("Bed.gif")
    nurseImage = pygame.image.load("Nurse.gif")
    nurse = nurseImage.get_rect()
    nurse.centerx = 400
    nurse.centery = 530
    exitText = speechFont.render("Press 'ESC' to leave", False, (255, 255, 255))
    beds = []
    bedx = 300
    bedy = 500
    for i in range(0, 6):  # beds for the injured townies
        beds.append(bedImage.get_rect())
    for i in range(0, len(beds)):
        beds[i].centerx = bedx
        beds[i].centery = bedy
        if i == 2:
            bedy = 500
            bedx = 950
        else:
            bedy -= 200
    player.centerx = 640
    player.centery = 650
    speechCounter = 0
    nurseSpeaking = False
    nurseCounter = 0
    nurseCounterEnd = 0
    randomMovement = 0

    characters = [player, nurse]

    # code below is for hospitalizing townies

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()  # closes window
                    exitLoop = True
                    break
                if event.key == pygame.K_SPACE and nurseSpeaking == True:
                    speechCounter = 900
        if exitLoop == True:
            break

        for i in range(0, len(dead)):
            dead[i].centerx = beds[i].centerx
            dead[i].centery = beds[i].centery

        if nurseSpeaking == False:
            pressed = pygame.key.get_pressed()  # checks if a key has been pressed. Different way of checking than above since this method will recognize key holds (not just presses) which is better for player movement
            if pressed[pygame.K_w]: player.centery -= 3  # moves the player up by 4 units when 'w' key is pressed
            if pressed[pygame.K_s]: player.centery += 3  # moves the player down by 4 units when 's' key is pressed
            if pressed[pygame.K_a]:
                player.centerx -= 3  # moves the player left by 4 units when 'a' key is pressed
                playerImage = playerLeft  # changes the player image to be facing left
            if pressed[pygame.K_d]:
                player.centerx += 3  # moves the player right by 4 units when 'd' key is pressed
                playerImage = playerRight  # changes the player image to be facing right

        for i in characters:
            if i.centerx <= 20:
                i.centerx = 20
            if i.centerx >= 1230:
                i.centerx = 1230
            if i.centery <= 50:
                i.centery = 50
            if i.centery >= 665:
                i.centery = 665

        for i in range(0, len(deadCounters)):
            deadCounters[i] += 1
            for x in range(300, 1501, 300):
                if deadCounters[i] == x:
                    deadCharge[i] += 1

        for i in range(0, len(deadCharge)):
            if deadCharge[i] == 1:
                chargeBars[i] = pygame.image.load("Health1.gif")
            elif deadCharge[i] == 2:
                chargeBars[i] = pygame.image.load("Health2.gif")
            elif deadCharge[i] == 3:
                chargeBars[i] = pygame.image.load("Health3.gif")
            elif deadCharge[i] == 4:
                chargeBars[i] = pygame.image.load("Health4.gif")
            elif deadCharge[i] == 5:
                chargeBars[i] = pygame.image.load("Health0.gif")
                townies.append(dead[i])
                characters.append(dead[i])
                dead.pop(i)
                deadCharge.pop(i)
                deadCounters.pop(i)
                friendlyImages.append(deadImages[i])
                deadImages.pop(i)
                break

        if nurseCounter == 0:
            nurseCounterEnd = random.randint(25, 75)
        nurseCounter += 1
        if nurseCounter == nurseCounterEnd:
            randomMovement = random.randint(1, 7)
            nurseCounter = 0
        if randomMovement == 1 and nurseSpeaking == False:
            nurse.centerx += 3
        elif randomMovement == 2 and nurseSpeaking == False:
            nurse.centerx -= 3
        elif randomMovement == 3 and nurseSpeaking == False:
            nurse.centery -= 3
        elif randomMovement == 4 and nurseSpeaking == False:
            nurse.centery += 3

        hospitalScreen.fill((205, 133, 63))
        for i in beds:
            hospitalScreen.blit(bedImage, i)
        for i in range(0, len(dead)):
            hospitalScreen.blit(deadImages[i], dead[i])
        for i in range(0, len(dead)):
            hospitalScreen.blit(chargeBars[i], chargeBarsRect[i])
        hospitalScreen.blit(playerImage, player)
        hospitalScreen.blit(nurseImage, nurse)
        hospitalScreen.blit(exitText, (8, 670))

        for i in beds:
            melonSpeech = speechFont.render(
                "You cannot join the hospital! You must purchase watermelon from the shop to heal yourself", False,
                (255, 255, 255))
            if player.colliderect(i):
                hospitalScreen.blit(melonSpeech, (8, 630))

        if hospitalVisit == 0:
            if speechCounter != 900:
                nurseSpeaking = True
                speechCounter += 1
                skipSpeech = speechFont.render("Press 'spacebar' to skip", False, (255, 255, 255))
                hospitalScreen.blit(skipSpeech, (8, 630))
                if speechCounter < 100:
                    introSpeech1 = speechFont.render('Hello! Welcome to the hospital.', False, (255, 255, 255))
                    hospitalScreen.blit(introSpeech1, (nurse.centerx, nurse.centery - 75))
                elif speechCounter < 200:
                    introSpeech1 = speechFont.render("My name is Doctor Mallory.", False, (255, 255, 255))
                    hospitalScreen.blit(introSpeech1, (nurse.centerx, nurse.centery - 75))
                elif speechCounter < 300:
                    introSpeech1 = speechFont.render("We have 6 beds here for any injured townies.", False,
                                                     (255, 255, 255))
                    hospitalScreen.blit(introSpeech1, (nurse.centerx, nurse.centery - 75))
                elif speechCounter < 400:
                    introSpeech1 = speechFont.render("When a townie becomes injured in a battle...", False,
                                                     (255, 255, 255))
                    hospitalScreen.blit(introSpeech1, (nurse.centerx, nurse.centery - 75))
                elif speechCounter < 500:
                    introSpeech1 = speechFont.render("they will arrive here and recover over time.", False,
                                                     (255, 255, 255))
                    hospitalScreen.blit(introSpeech1, (nurse.centerx, nurse.centery - 75))
                elif speechCounter < 600:
                    introSpeech1 = speechFont.render("Each patient will have a health bar...", False, (255, 255, 255))
                    hospitalScreen.blit(introSpeech1, (nurse.centerx, nurse.centery - 75))
                elif speechCounter < 700:
                    introSpeech1 = speechFont.render("beside their bed so that...", False, (255, 255, 255))
                    hospitalScreen.blit(introSpeech1, (nurse.centerx, nurse.centery - 75))
                elif speechCounter < 800:
                    introSpeech1 = speechFont.render("...their progress can be observed.", False, (255, 255, 255))
                    hospitalScreen.blit(introSpeech1, (nurse.centerx, nurse.centery - 75))
                elif speechCounter < 900:
                    introSpeech1 = speechFont.render("If you have any questions, I'll be around!", False,
                                                     (255, 255, 255))
                    hospitalScreen.blit(introSpeech1, (nurse.centerx, nurse.centery - 75))
            else:
                nurseSpeaking = False
                hospitalVisit = 1

        pygame.display.flip()
        clock.tick(80)

    return hospitalVisit


def shopping(gold, goldImage, goldIcon, font1, goldText, slot, playerLeft, playerRight, playerHealth, playerArmour):
    '''
    The shopping function is responsible for allowing the shop to operate.
    It allows the player to purchase items which they have the required
    funds for, if they have not previously purchased that item.
    '''
    shopBackgroundImage = pygame.image.load("ShopLayout4.png")
    shopBackground = shopBackgroundImage.get_rect()
    shopBackground.centerx = 640
    shopBackground.centery = 352
    goldIcon.centerx = 35
    goldIcon.centery = 35
    exitLoop = False
    shopScreen = pygame.display.set_mode((1280, 705))
    shopFont = pygame.font.SysFont('Calibri', 36)
    escFont = pygame.font.SysFont('Calibri', 30)
    successText = shopFont.render("Item purchased successfully!", False, (0, 150, 0))
    failText = shopFont.render("Insufficient funds!", False, (150, 0, 0))
    purchasedText = shopFont.render("You've already purchased this item!", False, (150, 0, 0))
    melonText = shopFont.render("You cannot buy watermelon at full health!", False, (150, 0, 0))
    shopPrice1 = font1.render("500", False, (0, 0, 0))
    shopPrice2 = font1.render("600", False, (0, 0, 0))
    shopPrice3 = font1.render("400", False, (0, 0, 0))
    shopPrice4 = font1.render("100", False, (0, 0, 0))
    num1 = font1.render("1", False, (0, 0, 0))
    num2 = font1.render("2", False, (0, 0, 0))
    num3 = font1.render("3", False, (0, 0, 0))
    num4 = font1.render("4", False, (0, 0, 0))
    nums = [num1, num2, num3, num4]
    shopPrices = [shopPrice1, shopPrice2, shopPrice3, shopPrice4]
    shopText = shopFont.render("Press the corresponding # to the item you wish to buy!", False, (255, 255, 255))
    '''shopx = [82,402,724,1043,82,402,724,1043]
    shopy = [317,317,317,319,631,631,631,632]'''
    escText = escFont.render("Press 'ESC' to exit", False, (255, 255, 255))
    shopx = [82, 404, 727, 1046]
    shopy = [130, 130, 127, 127]
    success = False
    fail = False
    purchased = False
    melon = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()  # closes window
                    exitLoop = True
                    break
                if event.key == pygame.K_1:
                    if slot[0] != 0:
                        melon = False
                        fail = False
                        success = False
                        purchased = True
                    elif gold >= 500:
                        melon = False
                        fail = False
                        purchased = False
                        success = True
                        gold -= 500
                        playerLeft = pygame.image.load("PantsLeft.gif")
                        playerRight = pygame.image.load("PantsRight.gif")
                        slot[0] = 1
                        if slot[1] == 1:
                            playerLeft = pygame.image.load("ChestPantsLeft.gif")
                            playerRight = pygame.image.load("ChestPantsRight.gif")
                        if slot[2] == 1:
                            playerLeft = pygame.image.load("PantsShieldLeft.gif")
                            playerRight = pygame.image.load("PantsShieldRight.gif")
                        if slot[2] == 1 and slot[0] == 1:
                            playerLeft = pygame.image.load("ChestPantsShieldLeft.gif")
                            playerRight = pygame.image.load("ChestPantsShieldRight.gif")
                    else:
                        melon = False
                        success = False
                        purchased = False
                        fail = True

                elif event.key == pygame.K_2:
                    if slot[1] != 0:
                        melon = False
                        success = False
                        fail = False
                        purchased = True
                    elif gold >= 600:
                        melon = False
                        fail = False
                        purchased = False
                        success = True
                        gold -= 600
                        playerLeft = pygame.image.load("ChestplateLeft.gif")
                        playerRight = pygame.image.load("ChestPlateRight.gif")
                        slot[1] = 1
                        if slot[0] == 1:
                            playerLeft = pygame.image.load("ChestPantsLeft.gif")
                            playerRight = pygame.image.load("ChestPantsRight.gif")
                        if slot[2] == 1:
                            playerLeft = pygame.image.load("ChestShieldLeft.gif")
                            playerRight = pygame.image.load("ChestShieldRight.gif")
                        if slot[2] == 1 and slot[0] == 1:
                            playerLeft = pygame.image.load("ChestPantsShieldLeft.gif")
                            playerRight = pygame.image.load("ChestPantsShieldRight.gif")
                    else:
                        melon = False
                        success = False
                        purchased = False
                        fail = True

                elif event.key == pygame.K_3:
                    if slot[2] != 0:
                        melon = False
                        fail = False
                        success = False
                        purchased = True
                    elif gold >= 400:
                        melon = False
                        fail = False
                        purchaed = False
                        success = True
                        gold -= 400
                        playerLeft = pygame.image.load("ShieldLeft.gif")
                        playerRight = pygame.image.load("ShieldRight.gif")
                        slot[2] = 1
                        if slot[0] == 1:
                            playerLeft = pygame.image.load("PantsShieldLeft.gif")
                            playerRight = pygame.image.load("PantsShieldRight.gif")
                        if slot[1] == 1:
                            playerLeft = pygame.image.load("ChestShieldLeft.gif")
                            playerRight = pygame.image.load("ChestShieldRight.gif")
                        if slot[2] == 1 and slot[0] == 1:
                            playerLeft = pygame.image.load("ChestPantsShieldLeft.gif")
                            playerRight = pygame.image.load("ChestPantsShieldRight.gif")
                    else:
                        melon = False
                        success = False
                        purchased = False
                        fail = True

                elif event.key == pygame.K_4:
                    if playerHealth >= 5:
                        fail = False
                        success = False
                        purchased = False
                        melon = True
                    elif gold >= 100:
                        melon = False
                        fail = False
                        purchased = False
                        success = True
                        gold -= 100
                        playerHealth += 1
                    else:
                        melon = False
                        success = False
                        purchased = False
                        fail = True

                goldText = font1.render(str(gold), False, (0, 0, 0))
        if exitLoop == True:
            break

        shopScreen.blit(shopBackgroundImage, shopBackground)
        shopScreen.blit(goldImage, goldIcon)
        shopScreen.blit(goldText, (70, 1))
        shopScreen.blit(escText, (1050, 8))
        shopScreen.blit(shopText, (400, 500))  # (183,9))
        for i in range(0, len(shopPrices)):
            shopScreen.blit(shopPrices[i], (shopx[i], shopy[i]))
        numx = 25
        for i in nums:
            shopScreen.blit(i, (numx, 392))
            numx += 325

        if success == True:
            shopScreen.blit(successText, (500, 600))
        if fail == True:
            shopScreen.blit(failText, (470, 600))
        if purchased == True:
            shopScreen.blit(purchasedText, (450, 600))
        if melon == True:
            shopScreen.blit(melonText, (450, 600))

        pygame.display.flip()
        clock.tick(80)
    pygame.display.quit()

    return gold, goldText, playerLeft, playerRight, playerHealth, playerArmour


# noinspection PyUnreachableCode
def battle(characters, friendlies, goldImage, goldIcon, goldText, healthImage, playerHealth, health, healthText,
           armourImage, playerArmour, armour, armourText, player, playerImage, friendlyImages, treeImage, gold, dead,
           deadImages, playerLeft, playerRight, firstBattle):
    '''
    The battle function controls all of the aspects to the battle screen.
    This includes the movement of friendlies and enemies, the ability for
    the player to attack and be damaged, and the ability for a given team
    to win if the opponent has been wiped out.
    '''
    global soldierNum
    if firstBattle == True:
        font1 = pygame.font.SysFont('Calibri', 30)
        tutorialText1 = font1.render("In a battle, your team must survive and defeat the other team!", False,
                                     (255, 255, 255))
        tutorialText2 = font1.render(
            "Kill enemies by running into them, however be careful that they are not in attack mode.", False,
            (255, 255, 255))
        tutorialText3 = font1.render(
            "Enemies will damage you when in attack mode (left) and will not when in passive mode (right)", False,
            (255, 255, 255))
        tutorialText4 = font1.render("The winning team will obtain gold from the losing team!", False, (255, 255, 255))
        tutorialText5 = font1.render("Press 'enter' to continue to the battle", False, (255, 255, 255))
        tutorialScreen = pygame.display.set_mode((1280, 705))
        soldier11Image = pygame.image.load("Soldier11.gif")
        soldier112Image = pygame.image.load("Soldier112.gif")
        soldier11 = soldier11Image.get_rect()
        soldier112 = soldier112Image.get_rect()
        soldier11.centerx = 840
        soldier112.centerx = 420
        soldier11.centery = 450
        soldier112.centery = 450
        exitLoop2 = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.quit()  # closes window
                        exitLoop2 = True
                        break
                    elif event.key == pygame.K_RETURN:
                        pygame.display.quit()  # closes window
                        exitLoop2 = True
                        break
            if exitLoop2 == True:
                break
            tutorialScreen.fill((20, 130, 0))
            tutorialScreen.blit(soldier11Image, soldier11)
            tutorialScreen.blit(soldier112Image, soldier112)
            tutorialScreen.blit(tutorialText1, (60, 30))
            tutorialScreen.blit(tutorialText2, (60, 100))
            tutorialScreen.blit(tutorialText3, (60, 170))
            tutorialScreen.blit(tutorialText4, (60, 240))
            tutorialScreen.blit(tutorialText5, (420, 600))
            pygame.display.flip()  # allows graphics to be drawn on screen
            clock.tick(80)

    # archer varibles below

    archerTimerStop = 50
    archerTimer = 0
    archer1, archer2, archer3, archer4, archer5, archer6 = [], [], [], [], [], []
    archer1m, archer2m, archer3m, archer4m, archer5m, archer6m = [], [], [], [], [], []
    bullets = [archer1, archer2, archer3, archer4, archer5, archer6]
    bulletSpeed = [archer1m, archer2m, archer3m, archer4m, archer5m, archer6m]
    battleTree = []
    friendlyImages2 = [pygame.image.load("Cliff2.gif"), pygame.image.load("Townie1-2.gif"),
                       pygame.image.load("Townie2-2.gif"), pygame.image.load("Townie3-2.gif"),
                       pygame.image.load("Townie4-2.gif")]

    # enemy variables below

    soldier11Image = pygame.image.load("Soldier11.gif")
    soldier112Image = pygame.image.load("Soldier112.gif")
    soldier12Image = pygame.image.load("Soldier12.gif")
    soldier122Image = pygame.image.load("Soldier122.gif")
    soldier21Image = pygame.image.load("Soldier21.gif")
    soldier212Image = pygame.image.load("Soldier212.gif")
    soldier22Image = pygame.image.load("Soldier22.gif")
    soldier31Image = pygame.image.load("Soldier31.gif")
    soldier312Image = pygame.image.load("Soldier312.gif")
    soldier32Image = pygame.image.load("Soldier32.gif")
    soldier222Image = 0
    soldier322Image = 0
    team1Images = [soldier11Image, soldier12Image]
    team2Images = [soldier21Image, soldier22Image]
    team3Images = [soldier31Image, soldier32Image]
    team1ChangeImages = [soldier112Image, soldier122Image]
    team2ChangeImages = [soldier212Image, soldier222Image]
    team3ChangeImages = [soldier312Image, soldier322Image]
    soldierChangeImages = ["placeholder", team1ChangeImages, team2ChangeImages, team3ChangeImages]
    soldierImages = ["placeholder", team1Images, team2Images, team3Images]
    bulletImage = pygame.image.load("Bullet.gif")

    # miscellaneous varibles below

    battleScreen = pygame.display.set_mode((1280, 705))
    exitLoop = False  # used later to exit loop
    archers = False
    willEnemiesMove = 0
    archerCounter = 0
    counter = 0  # used later for random enemy movements
    randomCounterEnd = 0  # used later for random enemy movements
    randomMovement = 0  # used later for random enemy movements
    movingEnemies = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # placeholder values until the list is appended
    hit = 1
    win = 3
    attacker = 0
    willEnemiesMove2 = 0
    counter2 = 0
    randomCounterEnd2 = 0
    randomMovement2 = 0
    treex = 0
    treey = 280
    movingFriendlies = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    player.centerx = 200
    player.centery = 500
    green = random.randint(50, 120)

    while True:
        team = random.randint(1, 3)  # which team of enemies the player will be against
        if firstBattle == True and team == 3:  # ensures that the hardest team is not selected first
            pass
        else:
            break

    firstBattle = False

    for i in friendlies:  # random positions for friendlies
        i.centerx = random.randint(350, 450)
        i.centery = random.randint(50, 650)

    if team == 1:
        soldier11 = []  # two types of soldiers
        soldier12 = []
        for i in range(0, random.randint(3, 5)):  # random number of soldiers
            soldier11.append(soldier11Image.get_rect())
        for i in range(0, random.randint(3, 5)):
            soldier12.append(soldier12Image.get_rect())
        soldierNum = [soldier11, soldier12]

    elif team == 2:
        archers = True
        soldier21 = []  # two types of soldiers
        soldier22 = []
        for i in range(0, random.randint(4, 5)):  # random number of soldiers
            soldier21.append(soldier21Image.get_rect())
        for i in range(0, random.randint(2, 3)):
            soldier22.append(soldier22Image.get_rect())
        soldierNum = [soldier21, soldier22]

    elif team == 3:
        archers = True
        soldier31 = []  # two types of soldiers
        soldier32 = []
        for i in range(0, random.randint(5, 8)):  # random number of soldiers
            soldier31.append(soldier31Image.get_rect())
        for i in range(0, random.randint(3, 6)):
            soldier32.append(soldier32Image.get_rect())
        soldierNum = [soldier31, soldier32]

    enemies = []
    for soldierValue in soldierNum:
        for i in soldierValue:
            enemies.append(i)  # total of enemy sprites

    for i in reversed(soldierNum):  # reversed since archers are at the end, allowing them to be drawn first
        if archers == True:  # special spawning properties for archers
            if archerCounter == 0:
                for x in range(0, len(i)):  # sets enemy spawn locations
                    characters.append(i[x])  # appends the soldiers to a list which keeps track of existing characters
                    i[x].centerx = 1200
                    i[x].centery = random.randint(50, 650)
                    '''Code below is used to prevent enemies from
                    spawning on top of one another. For an unknown
                    reason, it does not work with 100% effectiveness
                    but does prevent more overlapping spawn locations
                    than ordinary coordinate selection'''
                    for z in range(0, len(characters) - 1):
                        while True:
                            if i[x].colliderect(characters[z]):
                                i[x].centerx = 1200
                                i[x].centery = random.randint(50, 650)
                            else:
                                break
                archers = False
                archerCounter = 1
        else:
            for x in range(0, len(i)):  # sets enemy spawn locations
                characters.append(i[x])  # appends the soldiers to a list which keeps track of existing characters
                i[x].centerx = random.randint(800, 1200)
                i[x].centery = random.randint(50, 650)
                '''Code below is used to prevent enemies from
                spawning on top of one another. For an unknown
                reason, it does not work with 100% effectiveness
                but does prevent more overlapping spawn locations
                than ordinary coordinate selection'''
                for z in range(0, len(characters) - 1):
                    while True:
                        if i[x].colliderect(characters[z]):
                            i[x].centerx = random.randint(800, 1200)
                            i[x].centery = random.randint(50, 650)
                        else:
                            break

    for i in range(0, random.randint(15, 20)):  # amount of trees
        battleTree.append(treeImage.get_rect())
        while True:
            newPlace = 0
            if i < 4:
                battleTree[i].centerx = treex
                battleTree[i].centery = treey
                treex += 50
            elif i < 8:
                battleTree[i].centerx = treex
                battleTree[i].centery = treey
                treey -= 100
            else:
                battleTree[i].centerx = random.randint(270, 1100)
                battleTree[i].centery = random.randint(150, 650)
            for x in range(0, len(battleTree) - 1):  # makes sure tree is not spawned on top of sprite
                if battleTree[i].colliderect(battleTree[x]):
                    newPlace = 1
                for z in friendlies:
                    if battleTree[i].colliderect(z):
                        newPlace = 1
                for z in enemies:
                    if battleTree[i].colliderect(z):
                        newPlace = 1
            if newPlace == 0:
                break

    if archerCounter == 1:  # resets archers to the proper value
        pass
        archers = True

    while True:  # main battle loop

        # code below allows the battle to be exited

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()  # closes window
                    exitLoop = True
                    break
        if exitLoop == True:
            break

        # code below allows player to move

        pressed = pygame.key.get_pressed()  # checks if a key has been pressed. Different way of checking than above since this method will recognize key holds (not just presses) which is better for player movement
        if pressed[pygame.K_w]: player.centery -= 3  # moves the player up by 4 units when 'w' key is pressed
        if pressed[pygame.K_s]: player.centery += 3  # moves the player down by 4 units when 's' key is pressed
        if pressed[pygame.K_a]:
            player.centerx -= 3  # moves the player left by 4 units when 'a' key is pressed
            playerImage = playerLeft  # changes the player image to be facing left
        if pressed[pygame.K_d]:
            player.centerx += 3  # moves the player right by 4 units when 'd' key is pressed
            playerImage = playerRight  # changes the player image to be facing right

        # code below prevents characters from travelling off screen

        for i in characters:
            if i.centerx <= 20:
                i.centerx = 20
            if i.centerx >= 1230:
                i.centerx = 1230
            if i.centery <= 50:
                i.centery = 50
            if i.centery >= 655:
                i.centery = 655

        # code below detects player collisions with trees

        for x in battleTree:
            if x.centerx + 23 > player.centerx > x.centerx - 39 and player.centery < x.centery + 60 and player.centery > x.centery - 83:
                if player.centerx > x.centerx + 18:
                    player.centerx = x.centerx + 22
                if player.centerx < x.centerx - 34:
                    player.centerx = x.centerx - 38
                if player.centery > x.centery + 55:
                    player.centery = x.centery + 59
                if player.centery < x.centery - 78:
                    player.centery = x.centery - 82

        # code below allows for archer firing

        if archers == True:
            archerTimer += 1
            if archerTimer == archerTimerStop:
                try:
                    for i in range(0, random.randint(1, (len(soldierNum[1])))):
                        bullets[i].append(bulletImage.get_rect())
                        bulletSpeed[i].append([-10, 0])
                        bullets[i][-1].centerx = soldierNum[1][i].centerx
                        bullets[i][-1].centery = soldierNum[1][i].centery
                except:
                    pass
                archerTimer = 0
                archerTimerStop = random.randint(30, 80)

        # code below allows for random enemy movement from right to left

        if len(enemies) > 0 and team == 1 or len(enemies) - len(soldierNum[1]) > 0 and team == 2 or len(enemies) - len(
                soldierNum[1]) > 0 and team == 3:
            if counter == 0:
                randomCounterEnd = random.randint(25, 75)
            counter += 1
            if counter == randomCounterEnd:
                willEnemiesMove = 1
                while True:
                    movingEnemy1 = 0  # placeholder
                    graphic12 = False  # attacking graphic
                    movingEnemy2 = 1
                    graphic22 = False
                    movingEnemy3 = 2
                    graphic32 = False
                    movingEnemy4 = 3
                    graphic42 = False
                    if len(enemies) > 1 and team == 1 or len(enemies) - len(soldierNum[1]) > 1 and team == 2 or len(
                            enemies) - len(soldierNum[1]) > 1 and team == 3:
                        movingEnemy1, graphic12 = randomEnemySelector(soldierNum, team)
                    if len(enemies) > 2 and team == 1 or len(enemies) - len(soldierNum[1]) > 2 and team == 2 or len(
                            enemies) - len(soldierNum[1]) > 2 and team == 3:
                        movingEnemy2, graphic22 = randomEnemySelector(soldierNum, team)
                    if len(enemies) > 3 and team == 1 or len(enemies) - len(soldierNum[1]) > 3 and team == 2 or len(
                            enemies) - len(soldierNum[1]) > 3 and team == 3:
                        movingEnemy3, graphic42 = randomEnemySelector(soldierNum, team)
                    if len(enemies) > 5 and team == 1 or len(enemies) - len(soldierNum[1]) > 5 and team == 2 or len(
                            enemies) - len(soldierNum[1]) > 5 and team == 2:
                        movingEnemy4, graphic42 = randomEnemySelector(soldierNum, team)
                    if movingEnemy1 != movingEnemy2 and movingEnemy1 != movingEnemy3 and movingEnemy1 != movingEnemy4 and movingEnemy2 != movingEnemy3 and movingEnemy2 != movingEnemy4 and movingEnemy3 != movingEnemy4:
                        break
                if len(enemies) > 5 and team == 1 or len(enemies) - len(soldierNum[1]) > 5 and team == 2 or len(
                        enemies) - len(soldierNum[1]) > 5 and team == 3:
                    movingEnemies = [movingEnemy1, movingEnemy2, movingEnemy3, movingEnemy4]
                if len(enemies) > 3 and team == 1 or len(enemies) - len(soldierNum[1]) > 3 and team == 2 or len(
                        enemies) - len(soldierNum[1]) > 3 and team == 3:
                    movingEnemies = [movingEnemy1, movingEnemy2, movingEnemy3]
                elif len(enemies) > 2 and team == 1 or len(enemies) - len(soldierNum[1]) > 2 and team == 2 or len(
                        enemies) - len(soldierNum[1]) > 2 and team == 3:
                    movingEnemies = [movingEnemy1, movingEnemy2]
                elif len(enemies) > 1 and team == 1 or len(enemies) - len(soldierNum[1]) > 1 and team == 2 or len(
                        enemies) - len(soldierNum[1]) > 1 and team == 3:
                    movingEnemies = [movingEnemy1]
                counter = 0
            if willEnemiesMove == 1:  # if enemies are moving
                stopMoveEnemies = 0
                for i in movingEnemies:
                    for tree in battleTree:  # prevents tree collisions
                        try:
                            if i.colliderect(tree):
                                if i.centery > tree.centery + 50 and tree.centerx - 25 < i.centerx < tree.centerx + 25:
                                    i.centerx += 3
                                    stopMoveEnemies = 1
                                else:
                                    i.centery -= 3
                                    stopMoveEnemies = 1
                        except:
                            pass
                    if stopMoveEnemies == 0:  # enemy movement to track player
                        if i.centerx < player.centerx - 40:
                            i.centerx += 3
                        elif player.centerx - 40 < i.centerx < player.centerx + 40:
                            if i.centery > player.centery:
                                i.centery -= 3
                            elif i.centery < player.centery:
                                i.centery += 3
                        else:
                            i.centerx -= 3

                for bad in movingEnemies:  # kills friendlies and players if collision occurs
                    for good in friendlies:
                        if bad.colliderect(good):
                            dead.append(good)
                            removeIndex = friendlies.index(good)
                            friendlies.pop(removeIndex)
                            deadImages.append(friendlyImages[removeIndex])
                            friendlyImages.pop(removeIndex)
                    if bad.colliderect(player):
                        for i in movingEnemies:
                            if i == attacker:
                                hit = 0
                                break
                            else:
                                hit = 1
                        if hit == 1:
                            if playerArmour > 0:
                                playerArmour -= 1
                            else:
                                playerHealth -= 1
                            hit = 0
                            attacker = bad

        # friendlies drawing

        if len(friendlies) > 0:
            if counter2 == 0:
                randomCounterEnd2 = random.randint(25, 75)
            counter2 += 1
            if counter2 == randomCounterEnd2:
                willEnemiesMove2 = random.randint(1, 1)
                while True:
                    movingFriendly1 = friendlies[random.randint(0, len(friendlies) - 1)]
                    movingFriendly2 = 0  # placeholder
                    movingFriendly3 = 1
                    movingFriendly4 = 2
                    if len(friendlies) > 1:
                        movingFriendly2 = friendlies[random.randint(0, len(friendlies) - 1)]
                    if len(friendlies) > 2:
                        movingFriendly3 = friendlies[random.randint(0, len(friendlies) - 1)]
                    if len(friendlies) > 3:
                        movingFriendly4 = friendlies[random.randint(0, len(friendlies) - 1)]
                    if movingFriendly1 != movingFriendly2 and movingFriendly1 != movingFriendly3 and movingFriendly1 != movingFriendly4 and movingFriendly2 != movingFriendly3 and movingFriendly2 != movingFriendly4 and movingFriendly3 != movingFriendly4:
                        break
                if len(friendlies) > 3:
                    movingFriendlies = [movingFriendly1, movingFriendly2, movingFriendly3, movingFriendly4]
                if len(friendlies) > 2:
                    movingFriendlies = [movingFriendly1, movingFriendly2, movingFriendly3]
                if len(friendlies) > 1:
                    movingFriendlies = [movingFriendly1, movingFriendly2]
                if len(friendlies) > 0:
                    movingFriendlies = [movingFriendly1]

                counter2 = 0
            if willEnemiesMove2 == 1:
                stopMoveFriendlies = 0
                for i in movingFriendlies:
                    for tree in battleTree:
                        if i.colliderect(tree):
                            i.centery -= 3
                            stopMoveFriendlies = 1
                if stopMoveFriendlies == 0 and movingFriendly1.centerx <= 1229:
                    movingFriendly1.centerx += 3
                    if len(friendlies) > 1 and movingFriendly2.centerx <= 1229:
                        movingFriendly2.centerx += 3
                    if len(friendlies) > 2 and movingFriendly3.centerx <= 1229:
                        movingFriendly3.centerx += 3
                    if len(friendlies) > 3 and movingFriendly4.centerx <= 1229:
                        movingFriendly4.centerx += 3
                for good in movingFriendlies:  # kills enemies if collision occurs
                    for bad in enemies:
                        if good.colliderect(bad):
                            removeIndex = enemies.index(bad)
                            enemies.pop(removeIndex)
                            for soldr in soldierNum:
                                for num in soldr:
                                    if num == bad:
                                        removeIndex = soldr.index(bad)
                                        soldr.pop(removeIndex)
                            for enemy in movingEnemies:
                                if enemy == bad:
                                    removeIndex = movingEnemies.index(bad)
                                    movingEnemies.pop(removeIndex)

        for i in friendlies:  # prevents tree collisions
            for tree in battleTree:
                if i.colliderect(tree):
                    i.centery -= 3
                    i.centerx -= 3

        for bad in enemies:  # kills enemies if player collides with them
            if player.colliderect(bad):
                removeIndex = enemies.index(bad)
                enemies.pop(removeIndex)
                for soldr in soldierNum:
                    for num in soldr:
                        if num == bad:
                            removeIndex = soldr.index(bad)
                            soldr.pop(removeIndex)
                for enemy in movingEnemies:
                    if enemy == bad:
                        removeIndex = movingEnemies.index(bad)
                        movingEnemies.pop(removeIndex)

        # code below checks if the battle has been won or lost

        if len(enemies) == 0:
            exitLoop = True
            win = 1

        if playerHealth == 0:
            exitLoop = True
            win = 0

        # all drawing to the screen is done below this point

        battleScreen.fill((20, green, 0))
        soldierIndex = -1
        for soldrNum in soldierNum:  # big block of code is the draw enemies with the proper graphics (attack mode vs passive mode)
            soldierIndex += 1
            for i in range(0, len(soldrNum)):
                if willEnemiesMove == 1:
                    if len(movingEnemies) == 4:
                        if soldrNum[i] == movingEnemies[0] or soldrNum[i] == movingEnemies[1] or soldrNum[i] == \
                                movingEnemies[2] or soldrNum[i] == movingEnemies[3]:
                            if graphic12 != False:
                                battleScreen.blit(soldierChangeImages[team][soldierIndex], soldrNum[i])
                            if graphic22 != False:
                                battleScreen.blit(soldierChangeImages[team][soldierIndex], soldrNum[i])
                            if graphic32 != False:
                                battleScreen.blit(soldierChangeImages[team][soldierIndex], soldrNum[i])
                            if graphic42 != False:
                                battleScreen.blit(soldierChangeImages[team][soldierIndex], soldrNum[i])
                        else:
                            battleScreen.blit(soldierImages[team][soldierIndex], soldrNum[i])
                    elif len(movingEnemies) == 3:
                        if soldrNum[i] == movingEnemies[0] or soldrNum[i] == movingEnemies[1] or soldrNum[i] == \
                                movingEnemies[2]:
                            if graphic12 != False:
                                battleScreen.blit(soldierChangeImages[team][soldierIndex], soldrNum[i])
                            if graphic22 != False:
                                battleScreen.blit(soldierChangeImages[team][soldierIndex], soldrNum[i])
                            if graphic32 != False:
                                battleScreen.blit(soldierChangeImages[team][soldierIndex], soldrNum[i])
                            if graphic42 != False:
                                battleScreen.blit(soldierChangeImages[team][soldierIndex], soldrNum[i])
                        else:
                            battleScreen.blit(soldierImages[team][soldierIndex], soldrNum[i])
                    elif len(movingEnemies) == 2:
                        if soldrNum[i] == movingEnemies[0] or soldrNum[i] == movingEnemies[1]:
                            if graphic12 != False:
                                battleScreen.blit(soldierChangeImages[team][soldierIndex], soldrNum[i])
                            if graphic22 != False:
                                battleScreen.blit(soldierChangeImages[team][soldierIndex], soldrNum[i])
                            if graphic32 != False:
                                battleScreen.blit(soldierChangeImages[team][soldierIndex], soldrNum[i])
                            if graphic42 != False:
                                battleScreen.blit(soldierChangeImages[team][soldierIndex], soldrNum[i])
                        else:
                            battleScreen.blit(soldierImages[team][soldierIndex], soldrNum[i])
                    elif len(movingEnemies) == 1:
                        if soldrNum[i] == movingEnemies[0]:
                            if graphic12 != False:
                                battleScreen.blit(soldierChangeImages[team][soldierIndex], soldrNum[i])
                            if graphic22 != False:
                                battleScreen.blit(soldierChangeImages[team][soldierIndex], soldrNum[i])
                            if graphic32 != False:
                                battleScreen.blit(soldierChangeImages[team][soldierIndex], soldrNum[i])
                            if graphic42 != False:
                                battleScreen.blit(soldierChangeImages[team][soldierIndex], soldrNum[i])
                        else:
                            battleScreen.blit(soldierImages[team][soldierIndex], soldrNum[i])
                    elif len(movingEnemies) == 0:
                        battleScreen.blit(soldierImages[team][soldierIndex], soldrNum[i])
                else:
                    battleScreen.blit(soldierImages[team][soldierIndex], soldrNum[i])
        for i in range(0, len(battleTree)):
            battleScreen.blit(treeImage, battleTree[i])
        for i in range(0, len(friendlies)):
            battleScreen.blit(friendlyImages[i], friendlies[i])

        # big block of code below is for drawing the archer bullets and detecting if they hit a tree or friendly

        for archer in range(0, len(bullets)):
            for bullet in range(0, len(bullets[archer]) - 1):
                bullets[archer][bullet] = bullets[archer][bullet].move(bulletSpeed[archer][bullet])
                breakLoop = False
                for i in battleTree:
                    # noinspection PyUnreachableCode
                    if bullets[archer][bullet].colliderect(i):
                        bullets[archer].pop(bullet)  # removes the bullet
                        bulletSpeed[archer].pop(bullet)  # removes the corresponding bullet speed
                        breakLoop = True
                        break
                if breakLoop == True:
                    break
                for i in friendlies:
                    if bullets[archer][bullet].colliderect(i):
                        bullets[archer].pop(bullet)  # removes the bullet
                        bulletSpeed[archer].pop(bullet)  # removes the corresponding bullet speed
                        dead.append(i)
                        removeIndex = friendlies.index(i)
                        friendlies.pop(removeIndex)
                        deadImages.append(friendlyImages[removeIndex])
                        friendlyImages.pop(removeIndex)
                        break
                        breakLoop = True
                if breakLoop == True:
                    break
                if bullets[archer][bullet].colliderect(player):
                    bullets[archer].pop(bullet)  # removes the bullet
                    bulletSpeed[archer].pop(bullet)  # removes the corresponding bullet speed
                    breakLoop = True
                    if playerArmour > 0:
                        playerArmour -= 1
                    else:
                        playerHealth -= 1
                if breakLoop == False:
                    battleScreen.blit(bulletImage, bullets[archer][bullet])

        battleScreen.blit(playerImage, player)
        battleScreen.blit(goldImage, goldIcon)
        battleScreen.blit(goldText, (70, 167))
        battleScreen.blit(healthImage[playerHealth], health)
        battleScreen.blit(healthText, (8, 6))
        battleScreen.blit(armourImage[playerArmour], armour)
        battleScreen.blit(armourText, (8, 85))
        pygame.display.flip()  # allows graphics to be drawn on screen
        clock.tick(80)

    pygame.display.quit()  # quits window once loop is exited
    if win == 1 or win == 0:
        gold, friendlies = battleEnd(goldImage, goldIcon, gold, win, friendlies)

    return gold, friendlies, playerHealth, dead, deadImages, firstBattle, playerArmour


def randomEnemySelector(soldierNum, team):
    '''
    This function is called upon by the battle function to select a random
    enemy that will attack in the battle. It also changes their graphic
    to the attack mode graphic.
    '''
    while True:  # loop to select soldiers to move prevents archers from being selected
        while True:
            randomGraphic = random.choice(soldierNum)
            if len(randomGraphic) != 0:
                break

        if team == 2 or team == 3:
            if randomGraphic != soldierNum[1]:  # which is solider22
                break
        elif len(randomGraphic) == 0:
            pass
        else:
            break
    randomSoldier = random.randint(0, len(randomGraphic) - 1)
    if randomGraphic == soldierNum[0] and team == 1:
        graphic2 = pygame.image.load("Soldier112.gif")
    elif randomGraphic == soldierNum[1] and team == 1:
        graphic2 = pygame.image.load("Soldier122.gif")
    elif randomGraphic == soldierNum[0] and team == 2:
        graphic2 = pygame.image.load("Soldier212.gif")
    elif randomGraphic == soldierNum[0] and team == 3:
        graphic2 = pygame.image.load("Soldier312.gif")
    else:
        graphic2 = False

    return randomGraphic[randomSoldier], graphic2


def battleEnd(goldImage, goldIcon, gold, win, friendlies):
    '''
    This function is called at the end of the battle to signify to the player
    whether they won or lost, as well as how much gold was won or lost.
    '''
    font1 = pygame.font.SysFont('Calibri', 50)
    goldWon = random.randint(100, 400)
    if win == 1:
        gold += goldWon
    elif win == 0:
        gold -= goldWon
        if gold < 0:
            gold = 0
    winScreen = pygame.display.set_mode((1280, 705))
    goldIcon.centerx = 735
    goldIcon.centery = 400
    goldText = font1.render(str(goldWon), False, (0, 0, 0))
    exitLoop = False
    winFont = pygame.font.SysFont('Ariel', 100)
    exitFont = pygame.font.SysFont('Calibri', 40)
    if win == 1:
        winText = winFont.render("BATTLE WON", False, (0, 0, 0))
        earnedText = font1.render("Gold earned:", False, (0, 0, 0))
    else:
        winText = winFont.render("BATTLE LOST", False, (0, 0, 0))
        earnedText = font1.render("Gold lost:", False, (0, 0, 0))
    exitText = exitFont.render("Press 'enter' to exit", False, (255, 255, 255))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.display.quit()  # closes window
                    exitLoop = True
                    break
                if event.key == pygame.K_1:
                    pygame.display.quit()
        if exitLoop == True:
            break
        winScreen.fill((20, 130, 0))
        winScreen.blit(winText, (420, 150))
        if win == 1:
            winScreen.blit(goldText, (775, 367))
            winScreen.blit(earnedText, (440, 367))
        elif win == 0:
            winScreen.blit(goldText, (745, 367))
            winScreen.blit(earnedText, (480, 367))
            goldIcon.centerx = 710
        winScreen.blit(goldImage, goldIcon)
        winScreen.blit(exitText, (485, 560))
        pygame.display.flip()
        clock.tick(80)
    pygame.display.quit()

    return gold, friendlies


menu()
