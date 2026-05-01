import csv
import datetime
import locale
import os
from sources.database import retrieve_info, reduce_quantity
from PySide6.QtCore import QSize, QUrl, Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import QMessageBox


def add_to_cart(self, id: int):
    info = retrieve_info(id)
    if info is None:
        play_sfx(self, "warning")
        _ = QMessageBox(QMessageBox.Icon.Warning,
        "Erro", "Não foi possível obter informações do produto.",
        QMessageBox.StandardButton.Ok, self).exec_()
        return

    name = info["name"]
    price = info["price"]
    quantity = info["quantity"]

    if quantity == 0:
        play_sfx(self, "warning")
        _ = QMessageBox(QMessageBox.Icon.Warning,
        "Quantidade esgotada",
        ("A quantidade disponível do carrinho esgotou."
        " Por favor, selecione outro carrinho ou volte mais tarde."),
        QMessageBox.StandardButton.Ok, self).exec_()
        return

    existing = find_in_cart(self, name)
    if existing:
        if existing["quantity"] + 1 > quantity:
            play_sfx(self, "warning")
            _ = QMessageBox(QMessageBox.Icon.Warning,
            "Máximo antigido",
            ("Atingiu a quantidade máxima disponível do carrinho."
            "Por favor, selecione outro carrinho ou volte mais tarde."),
            QMessageBox.StandardButton.Ok, self).exec_()
            return
        existing["quantity"] += 1
        play_sfx(self, "information")
        _ = QMessageBox(QMessageBox.Icon.Information,
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
        _ = QMessageBox(QMessageBox.Icon.Information,
        "Carrinho adicionado", "O carrinho foi adicionado com sucesso.",
        QMessageBox.StandardButton.Ok, self).exec_()
    if hasattr(self, "cart_window") and self.cart_window is not None:
        self.cart_window.update_cart_display()
        self.cart_window.update_total_label()


def create_csv(self, cart_list):
    path = "reports/sales.csv"
    path_exists = os.path.isfile(path)
    date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    os.makedirs("reports", exist_ok=True)


    try:
        _ = locale.setlocale(locale.LC_ALL, '')
    except Exception:
        try:
            _ = locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        except Exception:
            pass


    try:
        with open(path, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['Nome',
            "Preço","Quantidade","Total","Data"])
            if not path_exists or os.path.getsize(path) == 0:
                writer.writeheader()
            for item in cart_list:
                total = item['quantity']* item['price']
                try:
                    price_str = locale.currency(item['price'], symbol=True, grouping=True)
                    total_str = locale.currency(total, symbol=True, grouping=True)
                except Exception:
                    price_str = f"{item['price']:.2f}€"
                    total_str = f"{total:.2f}€"
                writer.writerow({
                    "Nome": item['name'],
                    "Preço": price_str,
                    "Quantidade": item['quantity'],
                    "Total": total_str,
                    "Data": date})
        play_sfx(self, "information")
        _ = QMessageBox(QMessageBox.Icon.Information, "Relatório criado/guardado",
        "O relatório foi criado/guardado com sucesso.",
        QMessageBox.StandardButton.Ok,self).exec_()
    except Exception as e:
        play_sfx(self, "warning")
        _ = QMessageBox(QMessageBox.Icon.Warning, "Erro escrita",
        f"Erro ao criar/guardar o relatório das vendas.\n{e}",
        QMessageBox.StandardButton.Ok, self).exec_()


def finalize_purchase(self, cart_list):
    reduce_quantity(cart_list)
    create_csv(self, cart_list)
    self.cart_list.clear()
    if hasattr(self, "cart_window") and self.cart_window is not None:
        self.cart_window.update_cart_display()
        self.cart_window.update_total_label()
    parent = self.parent()
    if parent is not None:
        parent.update_car_labels()
    play_sfx(self, "purchase")
    _ = QMessageBox(QMessageBox.Icon.Information,
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


def set_image(self, img_name: str, w: int, h: int):
    path = f"images/{img_name}.png"
    pix = QPixmap(path)
    if pix.isNull():
        return
    scaled = pix.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
    self.setIcon(QIcon(scaled))
    self.setIconSize(QSize(w, h))
    self.setFixedSize(w, h)
    self.setStyleSheet("border: none; padding: 0;")