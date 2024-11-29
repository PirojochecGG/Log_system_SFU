import qrcode

def generate_qr_code():
    qr_data = """123;2024-11-26;2024-11-21;inflow;43534;22222;1111;Контрагент 3;Основной склад;
000001;Товар 1;10;шт;30.99;
000002;Товар 10;103;шт;32.99;"""

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save("operation_qr.png")
    print("код создан")

if __name__ == "__main__":
    generate_qr_code()