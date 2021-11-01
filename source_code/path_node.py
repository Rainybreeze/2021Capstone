class Node:
    def __init__(self, mother_node, recent_node):
        self.mother_node = mother_node
        self.self_node = recent_node + 1
        self.isLeft = [None, 0]
        self.isRight = [None, 0]
        self.isFront = [None, 0]
        self.isPassed = False

    def pass_node(self):
        self.isPassed = True

    def get_left_node(self):
        if self.isLeft[0]:
            return self.isLeft[1]
        else:
            return None

    def get_front_node(self):
        if self.isFront[0]:
            return self.isFront[1]
        else:
            return None

    def get_right_node(self):
        if self.isRight[0]:
            return self.isRight[1]
        else:
            return None
