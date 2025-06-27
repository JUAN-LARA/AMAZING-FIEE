class Vidas:
    def __init__(self, cantidad=4):
        self.cantidad = cantidad

    def perder_vida(self):
        self.cantidad -= 1

    def reiniciar(self, cantidad=4):
        self.cantidad = cantidad

    def esta_vivo(self):
        return self.cantidad > 0