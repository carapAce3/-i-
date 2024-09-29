#da

from panda3d.core import Point3, Vec3
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import CollisionTraverser, CollisionHandlerQueue, CollisionNode, CollisionSphere
from panda3d.core import CollisionRay, BitMask32


class CoinCollectionGame(ShowBase): # добавити наслідування класу "ShowBase"
    def __init__(self): # виправити помилку створення конструктора
        ShowBase.__init__(self)# виправити помилку виклику конструктора

        self.disableMouse()
        self.camera.setPos(0, -20, 10)
        self.camera.lookAt(0, 0, 0)

        self.player = self.loader.loadModel("models/box")
        self.player.setScale(1, 1, 1)
        self.player.setPos(0, 0, 0)
        self.player.reparentTo(self.render)

        self.coins = [] # створити пустий список
        self.num_coins = 5
        for i in range(self.num_coins):
            coin = self.loader.loadModel("models/smiley")
            coin.setScale(0.5, 0.5, 0.5)
            coin.setPos(i * 2 - 4, i * 2, 0)
            coin.reparentTo(self.render)
            self.coins.append(coin)
            # до списку self.coins додати coin

        # виправити помилку під час створення змінної в класі
        score = 0
        self.score_display = OnscreenText(text="Coins: 0", pos=(-1.3, 0.9), scale=0.07)

        self.cTrav = CoinCollectionGame() # створити об'єкт класу CollisionTraverser
        self.cHandler = CollisionHandlerQueue()

        self.player_coll_sphere = CollisionSphere(0, 0, 0, 1)
        self.player_coll_node = CollisionNode("player")
        self.player_coll_node.addSolid(self.player_coll_sphere)
        self.player_coll_node.setFromCollideMask(BitMask32.bit(1))
        self.player_coll_node.setIntoCollideMask(BitMask32.allOff())
        self.player_coll_np = self.player.attachNewNode(self.player_coll_node)

        self.coin_handler = CoinCollectionGame() # створити об'єкт класу CollisionHandlerQueue

        for coin in self.coins:  # виправити помилку створення циклу
            coin_sphere = CollisionSphere(0, 0, 0, 1)
            coin_node = CollisionNode("coin")
            coin_node.addSolid(coin_sphere)
            coin_node.setIntoCollideMask(BitMask32.bit(1))
            coin_node_path = coin.attachNewNode(coin_node)
            self.cTrav.addCollider(self.player_coll_np, self.coin_handler)

        # замість "?" викликати функцію, яка відповідає за рух у даній програмі
        self.accept("arrow_up", "self.move_player", [Vec3(0, 1, 0)])   
        self.accept("arrow_down", "self.move_player", [Vec3(0, -1, 0)]) 
        self.accept("arrow_left", "self.move_player", [Vec3(-1, 0, 0)])
        self.accept("arrow_right", "self.move_player", [Vec3(1, 0, 0)]) 

        self.accept("w", "r", [Vec3(0, 0, 1)]) 
        self.accept("s", "r", [Vec3(0, 0, -1)]) 

        # Додаємо завдання для оновлення стану гри
        self.taskMgr.add(self.update, "update")

    # виправити помилки при створення функції
    def move_player(self, direction):  # виправити помилки при створенні функції
        new_pos = self.player.getPos() + direction
        self.player.setPos(new_pos)

    # виправити помилки при створення функції
    def update(self, task):
        self.cTrav.traverse(self.render)


        for entry in self.coin_handler.getEntries():
            collided_coin = entry.getIntoNodePath().getParent()
            if collided_coin in self.coins:
                self.coins.remove(collided_coin)
                collided_coin.removeNode()
                self.score += 1
                self.update_score()
                # викликати функію update_score
        # повернути Task.cont

    # виправити помилки під час створення функції
    def update_score(self):
        self.score_display.setText(f"Coins: {self.score}")


game = CoinCollectionGame # створити об'єкт класу CoinCollectionGame
game.run()
# викликати функцію run() до об'єкта вище
