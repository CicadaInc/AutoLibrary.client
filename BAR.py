try:
    import barcode
    from barcode.writer import ImageWriter
except Exception as error:
    print(str(error))


class BarcodeGenerator:
    def __init__(self, barcode_type, condition=False):
        try:
            if condition:
                print(barcode.PROVIDED_BARCODES)

            self.TYPE = barcode.get_barcode_class(barcode_type)
        except Exception as error:
            print(str(error))

    def generate_barcode(self, code, filename):
        try:
            barcode_to_print = self.TYPE(code, writer=ImageWriter())
            barcode_to_print.save(filename)
            return True

        except Exception as error:
            print(str(error))

# Example
# ean = EAN('5901234123457', writer=ImageWriter())
# fullname = ean.save('ean_1')
