from database import retrieve_info, reduce_quantity
from PySide6.QtCore import QSize, QUrl
from PySide6.QtGui import QIcon
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import QMessageBox

def add_to_cart(self, id: int):
    info = retrieve_info(id)
    if info is None:
        play_sfx(self, "warning")
        QMessageBox(QMessageBox.Icon.Warning,
        "Erro", "Não foi possível obter informações do produto.",
        QMessageBox.StandardButton.Ok, self).exec_()
        return
    
    name, price, quantity = info

    if quantity == 0:
        play_sfx(self, "warning")
        QMessageBox(QMessageBox.Icon.Warning,
        "Quantidade esgotada",
        """A quantidade disponível do carrinho esgotou.
Por favor, selecione outro carrinho ou volte mais tarde.""",
        QMessageBox.StandardButton.Ok, self).exec_()
        return

    existing = find_in_cart(self, name)
    if existing:
        if existing["quantity"] + 1 > quantity:
            play_sfx(self, "warning")
            QMessageBox(QMessageBox.Icon.Warning,
            "Máximo antigido",
            """Atingiu a quantidade máxima disponível do carrinho.
Por favor, selecione outro carrinho ou volte mais tarde.""",
            QMessageBox.StandardButton.Ok, self).exec_()
            return
        existing["quantity"] += 1
        play_sfx(self, "information")
        QMessageBox(QMessageBox.Icon.Information,
        "Carrinho adicionado", "+1 carrinho adicionado com sucesso.",
        QMessageBox.StandardButton.Ok, self).exec_()
    else:
        self.cart_list.append({
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1
        })
        play_sfx(self, "information")
        QMessageBox(QMessageBox.Icon.Information,
        "Carrinho adicionado", "O carrinho foi adicionado com sucesso.",
        QMessageBox.StandardButton.Ok, self).exec_()
    if hasattr(self, "cart_window") and self.cart_window is not None:
        self.cart_window.update_cart_display()
        self.cart_window.update_total_label()

def finalize_purchase(self):
    reduce_quantity(self)
    self.cart_list.clear()
    if hasattr(self, "cart_window") and self.cart_window is not None:
        self.cart_window.update_cart_display()
        self.cart_window.update_total_label()
    parent = self.parent()
    if parent is not None:
        parent.update_car_labels()
    QMessageBox(QMessageBox.Icon.Information,
    "Compra efetuada", "Compra efetuada com sucesso.",
    QMessageBox.StandardButton.Ok, self).exec_()

def find_in_cart(self, name):
    for item in self.cart_list:
        if item["name"] == name:
            return item
    return None

def play_sfx(self, sfx_name: str):
    sfx_name = "sounds/" + f"{sfx_name}" + ".mp3"
    self.player = QMediaPlayer()
    self.audio_out = QAudioOutput()
    self.player.setAudioOutput(self.audio_out)
    self.player.setSource(QUrl.fromLocalFile(f"{sfx_name}"))
    self.audio_out.setVolume(1)
    self.player.play()

def set_image(self, img_name: str, w: int, h:int):
    img_name = "images/" + f"{img_name}" + ".png"
    self.setIcon(QIcon(img_name))
    self.setIconSize(QSize(w,h))