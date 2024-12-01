import qrcode

def generate_qr_code():
    qr_data = """5;2024-01-01;2024-01-01;приход;Контрагент;Склад;
01824360;Лавровый лист;10;шт;10000;
02353241;Смесь итальянских трав;10;шт;10;
"""

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save("operation_qr.png")
    print("код создан")

if __name__ == "__main__":
    generate_qr_code()