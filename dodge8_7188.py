import random
import tkinter as tk

W, H, P = 20, 24, 16  # マス数(横・縦)と1ドットのピクセル数
BG, FG, HI = "#0f380f", "#8bac0f", "#9bbc0f"  # ゲームボーイ風4階調のうち3色


class Game:
    def __init__(self, root):
        root.title("DODGE-8")
        root.resizable(False, False)
        self.c = tk.Canvas(root, width=W * P, height=H * P, bg=BG, highlightthickness=0)
        self.c.pack()
        root.bind("<Left>", lambda e: self.move(-1))
        root.bind("<Right>", lambda e: self.move(1))
        root.bind("<space>", lambda e: self.dead and self.reset())
        self.root = root
        self.reset()
        self.tick()

    def reset(self):
        self.x, self.rocks, self.score, self.t, self.dead = W // 2, [], 0, 0, False

    def move(self, d):
        if not self.dead:
            self.x = max(0, min(W - 1, self.x + d))

    def tick(self):
        if not self.dead:
            self.t += 1
            if self.t % 3 == 0:
                self.rocks.append([random.randrange(W), 0])
            for r in self.rocks:
                r[1] += 1
            self.rocks = [r for r in self.rocks if r[1] < H]
            self.score += 1
            self.dead = [self.x, H - 1] in self.rocks
        self.draw()
        self.root.after(max(40, 110 - self.score // 25), self.tick)

    def box(self, x, y, color):
        self.c.create_rectangle(x * P, y * P, x * P + P - 2, y * P + P - 2, fill=color, outline="")

    def draw(self):
        self.c.delete("all")
        for x, y in self.rocks:
            self.box(x, y, FG)
        self.box(self.x, H - 1, HI)
        self.c.create_text(6, 6, anchor="nw", fill=HI, font=("Courier", 12, "bold"),
                           text=f"SCORE {self.score}")
        if self.dead:
            self.c.create_text(W * P // 2, H * P // 2, fill=HI, font=("Courier", 16, "bold"),
                               text="GAME OVER\nSPACE: RETRY", justify="center")


if __name__ == "__main__":
    root = tk.Tk()
    Game(root)
    root.mainloop()
