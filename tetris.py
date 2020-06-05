from random import randint
import pyxel
#import pdb

TILE_SIZE = 8
MAP_WIDTH = 14
MAP_HEIGHT = 25
WAIT = 30
NOIR = 7

class Tetris:
    def __init__(self):
      self.mGameOver = False
      self.mNext = randint(0, 6)
      self.mX = 0
      self.mY = 0
      self.mA = 0
      self.mT = 0
      self.score = 0
      self.mWait = 0
      self.state = 'res'  # ポーズのために　使います
      self.musique = 0
     

      pyxel.init(MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE, caption="Tetris", scale=3,
      fps=10)   
      pyxel.load("tetris.pyxres")
      pyxel.playm(0, loop=True)
      self.musique = 1

      self.next()
      pyxel.run(self.update, self.draw)
      #pyxel.run_with_profiler(self.update, self.draw)



    def update(self):
      if self.mGameOver:
        return
      
      if self.mWait <= WAIT / 2:
        self.wait()
        return
      
      if self.musique == 0:
        pyxel.playm(0, loop=True)
        self.musique = 1
      

      # false すると消える感じです
      self.put(self.mX, self.mY, self.mT, self.mA, False, False)
      a = self.mA
      
      # peut être il faut faire des threads 
      if pyxel.btnp(pyxel.KEY_D):
        a -= 1
      if pyxel.btnp(pyxel.KEY_F):
        a += 1
      # ça c'est une betise ne c'est pas?
      if pyxel.btnp(pyxel.KEY_1):
        a = 0
      a &= 3  # il y a que des cinq position possibles
      if self.put(self.mX, self.mY, self.mT, a, True, True):
        self.mA = a
      
      if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

      if pyxel.btnp(pyxel.KEY_P):
        if self.state == 'res':
          self.state = 'pause'
        else :
          self.state = 'res'

      if pyxel.btnp(pyxel.KEY_M):  # à faire
        if self.musique:
          pyxel.stop(0)
          self.musique = 0
        else: 
          pyxel.playm(0, loop=True)
          self.musique = 1
      
      # cette petit parte pour le space est faux; il faut le réparer
      if pyxel.btnp(pyxel.KEY_SPACE):
        if pyxel.tilemap(0).get( self.mX , self.mY + 5) == NOIR:
          #if pyxel.tilemap(0).get(self.mX + 1, self.mY + 3) == NOIR :
          #pyxel.tilemap(0).set(self.mX, self.mY + 3, pyxel.tilemap(0).get(self.mX, self.mY))
          self.mY += 3 
          self.score += 1

      if self.state == 'pause':
        return


      
      x = self.mX   
      if pyxel.btnp(pyxel.KEY_LEFT, 20, 1):
        x -= 1
      if pyxel.btnp(pyxel.KEY_RIGHT, 20, 1):
        x += 1
      if self.put(x, self.mY, self.mT, self.mA, True, True):
        self.mX = x
      
      if self.put(self.mX, self.mY + 1, self.mT, self.mA, True, True):
        self.mY += 1
        self.mWait = WAIT
      else: 
        self.mWait -= 1
      
      self.put(self.mX, self.mY, self.mT, self.mA, True, False)
    
    def draw(self):
      pyxel.bltm(0, 0, 0, 0, 0, MAP_WIDTH, MAP_HEIGHT)
      pyxel.text(4, 4, "POINTS " + str(self.score), 7)
      if self.mGameOver:
        # à faire écrire les meilleures resultats
        pyxel.text(20, 80, "C'est fini!", 7)
        pyxel.text(10, 90, "Votre resultat est: {0}".format(self.score), 7)
        #pyxel.text(20, 100, "Le utf8 fonctionne? éçà", 7)
        # quand on finit le jeux on faire quoi?

    # s == false ならタイル消えます
    def put(self, x, y, t, a, s, test):
      for j in range(4):
        for i in range(4):
          p = [ i, 3 - j, 3 - i, j]
          q = [ j, i, 3  - j, 3 - i]

          # on sept tiles differents
          # mais ici 7 c'est la noir
          if pyxel.tilemap(0).get(17 + t * 4 + p[a], q[a]) == NOIR:
            continue
          #pdb.set_trace() 
          v = t
          # もし s == false 消えます
          if s == False:
            v = NOIR 

          # si c'est pas pixel noir; dans notre pyxres pixel noir est definé comme
          # si c'est pas la noir on a touche une autre piece ou le zid
          # 7
          elif pyxel.tilemap(0).get( x + i, y + j) != NOIR:
            return False
          # si on ne deboug pas
          '''
            set(x, y, data)
            (x, y) に値または文字列のリストでイメージのデータを設定する
            例：pyxel.image(0).set(10, 10, ["1234", "5678", "9abc", "defg"])
          '''
          if test == False:
            pyxel.tilemap(0).set( x + i, y + j, v)
      return True
   

    def next(self):
      self.mX = 5
      self.mY = 2 
      self.mT = self.mNext
      self.mWait = WAIT
      self.mA = 0
      
      if pyxel.btn(pyxel.KEY_F):
        self.mA = 3
      if pyxel.btn(pyxel.KEY_D):
        self.mA = 1
      if pyxel.btn(pyxel.KEY_E):  # pourquoi c'est change pas? 
        self.mA = 2
      
      if self.put(self.mX, self.mY, self.mT, self.mA, True, False) == False:
        self.mGameOver = True
      self.put(5, -1, self.mNext, 0, False, False)
      
      # choisir le prochiane type et le montrer
      self.mNext = randint(0, 6)
      self.put(5, -1, self.mNext, 0, True, False)


    def wait(self):
      self.mWait -= 1
      if self.mWait == 0:
        self.next()

      if self.mWait == WAIT / 2 - 1:
        for y in range(22, 2, -1):
          n = 0
          for x in range(2, 12):
            if pyxel.tilemap(0).get(x, y) < NOIR:
              n += 1

          if n != 10:
            continue
          
          # n == 10 それでラインを消えます
          self.score += 10
          #pyxel.playm(1, loop=False)
          #self.musique = 0

          for x in range(2, 12):
            pyxel.tilemap(0).set(x, y, 10)

      if self.mWait == 1:
        for y in range(22, 2, -1):
          while pyxel.tilemap(0).get(2, y) == 10:
            self.mWait = WAIT / 2 - 2
            for i in range(y, 3, -1):
              for x in range(2, 12):
                pyxel.tilemap(0).set(x, i, pyxel.tilemap(0).get(x, i - 1))
            for x in range(2, 12):
              pyxel.tilemap(0).set(x, 3, 7)

    def meilleur(): # enregistre ou lit les meilleurs résultats
        # éntrez votre nom
        # à faire
        fd = open("res.db", "r", encoding="utf-8")
        while True:
            ligne = fd.readline()
            if not ligne:
                break
            print(ligne)
        fd.close()

Tetris()

