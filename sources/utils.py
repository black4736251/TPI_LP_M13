import csv
import datetime
import locale
import os
import platform
import subprocess

from PySide6.QtCore import QSize, Qt, QUrl 
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import QApplication, QMessageBox

from sources.database import reduce_quantity, retrieve_info
from sources.config import IMAGES_PATH, REPORTS_PATH, SOUNDS_PATH 


def add_to_cart(self, id: int):
    mods = QApplication.keyboardModifiers()


    def show_message(icon, title, text):
        _ = QMessageBox(icon, title, text, QMessageBox.StandardButton.Ok, self).exec_()


    info = retrieve_info(id)
    if info is None:
        play_sfx(self, "warning")
        show_message(QMessageBox.Icon.Warning, "Erro", "Não foi possível obter informações do carrinho.")
        return

    name = info["name"]
    price = info["price"]
    stock = info["quantity"]  # Available stock

    if stock == 0:
        play_sfx(self, "warning")
        show_message(QMessageBox.Icon.Warning, "Quantidade esgotada",
        "A quantidade disponível do carrinho esgotou. Por favor, selecione outro carrinho ou volte mais tarde.")
        return

    # Determine how many to add depending on modifiers
    if mods & Qt.KeyboardModifier.ShiftModifier:
        add_amount = 10
    elif mods & Qt.KeyboardModifier.ControlModifier:
        add_amount = 5
    else:
        add_amount = 1

    existing = find_in_cart(self, name)
    if existing:
        new_qty = existing["quantity"] + add_amount
        if new_qty > stock:
            play_sfx(self, "warning")
            show_message(QMessageBox.Icon.Warning, "Máximo atingido",
            f"Não é possível adicionar {add_amount} carrinho(s). Stock disponível: {stock - existing['quantity']}.")
            return
        existing["quantity"] = new_qty
        play_sfx(self, "information")
        show_message(QMessageBox.Icon.Information, "Carrinho atualizado",
        f"+{add_amount} carrinho(s) adicionado(s) com sucesso.")
    else:
        # If adding for the first time, cap to stock
        to_add = min(add_amount, stock)
        self.cart_list.append({
            "id": id,
            "name": name,
            "price": price,
            "quantity": to_add
        })
        play_sfx(self, "information")
        show_message(QMessageBox.Icon.Information, "Carrinho adicionado",
        f"{to_add} carrinho(s) adicionado(s) ao carrinho com sucesso.")

    if hasattr(self, "cart_window") and self.cart_window is not None:
        self.cart_window.update_cart_display()
        self.cart_window.update_total_label()


def create_csv(self, cart_list):
    path = REPORTS_PATH
    path_exists = os.path.isfile(path)
    date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    os.makedirs(os.path.dirname(path), exist_ok=True)


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


def is_empty_file(PATH: str):
    return os.path.isfile(PATH) and os.path.getsize(PATH) == 0


def open_purchase_history(self):
        system = platform.system()

        if is_empty_file(REPORTS_PATH):
            self._show_message(QMessageBox.Icon.Warning, "Relatório vazio", ("O relatório encontra-se vazio."
            " Espere que alguma compra seja efetuada."))
            return

        if system == "Windows":
            os.startfile(REPORTS_PATH)
        elif system == "Darwin":
            _ = subprocess.run(['open', REPORTS_PATH])
        else:
            _ = subprocess.run(['xdg-open', REPORTS_PATH])


def play_sfx(self, sfx_name: str):
    sfx_name = f"{SOUNDS_PATH}/{sfx_name}.mp3"
    self.player = QMediaPlayer()
    self.audio_out = QAudioOutput()
    self.player.setAudioOutput(self.audio_out)
    self.player.setSource(QUrl.fromLocalFile(f"{sfx_name}"))
    self.audio_out.setVolume(1)
    self.player.play()


def set_image(self, img_name: str, w: int, h: int):
    path = f"{IMAGES_PATH}/{img_name}.png"
    pix = QPixmap(path)
    if pix.isNull():
        return
    scaled = pix.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
    self.setIcon(QIcon(scaled))
    self.setIconSize(QSize(w, h))
    self.setFixedSize(w, h)
    self.setStyleSheet("border: none; padding: 0;")